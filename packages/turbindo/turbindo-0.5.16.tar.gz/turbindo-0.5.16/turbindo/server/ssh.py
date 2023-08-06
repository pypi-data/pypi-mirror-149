import crypt
import inspect
import json
import sys
import time
import uuid
from traceback import print_exc
from turbindo.database import default as db

import asyncssh

from turbindo.auth.user import User
from turbindo.util import timestamp, json_pretty


class InvalidScopeException(Exception):
    pass


class InvalidCommandException(Exception):
    pass


class CustomSSHServerImpl(asyncssh.SSHServer):
    passwords = {
        'admin': ('abc123', '12345'),
        'user123': ('abcd1234', "12345"),
        'test_user': ('abc123', '12345'),

    }
    authorized_keys = {
        "g": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIK2Ak/d8NyBod2MMGQ6lPiWYgF8le+gH1GdVR0Wum83y g@8a6358246b81"
    }

    def connection_made(self, conn):
        print('SSH connection received from %s.' %
              conn.get_extra_info('peername')[0])

    def connection_lost(self, exc):
        if exc:
            print('SSH connection error: ' + str(exc), file=sys.stderr)
        else:
            print('SSH connection closed.')

    def begin_auth(self, username):
        # If the user's password is the empty string, no auth is required
        return CustomSSHServerImpl.passwords.get(username) != ''

    # def validate_public_key(self, username, key:AIOSSHKey):
    #     authorized_keys = asyncssh.read_authorized_keys(['authorized_keys_g'])
    #     resp = authorized_keys.validate(key, client_addr=None, client_host=None)
    #     lookup_key:AIOSSHKey = asyncssh.import_public_key(lookup_raw)
    #
    #     lookup = lookup_key.get_fingerprint()
    #     provided = key.public_data
    #     try:
    #         assert lookup == provided
    #     except:
    #         return False
    #     return True

    def password_auth_supported(self):
        return True

    def validate_password(self, username, password):
        if username not in CustomSSHServerImpl.passwords:
            return False
        pw = CustomSSHServerImpl.passwords[username]
        lookup = crypt.crypt(password, pw[1])
        crypt_entry = crypt.crypt(pw[0], pw[1])
        return lookup == crypt_entry


class Session:
    def __init__(self, process, user_scopes, context={}):
        self.remote_peername = process.get_extra_info("remote_peername")
        self.username = process.get_extra_info('username')
        self.socket = process.get_extra_info('socket')
        self.sockname = process.get_extra_info('sockname')
        self.scopes = user_scopes
        self.scope = self.get_scope(self.username)
        self.path = [self.scope]
        self.context = context
        self.scope_class = None
        self.scope_class_instance = None

    def get_scope(self, username):
        return self.scopes[username]

    async def ainit(self):
        if self.username != "admin":
            self.user: User = User.from_dbuser(await db.readUser(self.username))
        else:
            self.user = User(name="admin", organizaion="admin", admin=True, tags=["admin"])

        if inspect.isclass(self.scope):
            self.scope_class = self.scope
            sig = inspect.signature(self.scope.__init__)
            if "user" in sig.parameters and len(sig.parameters) == 2:
                self.scope_class_instance = self.scope(self.user)
            else:
                self.scope_class_instance = self.scope()

        return self

    def get_subscopes(self) -> list:
        dscope = dir(self.scope)
        resp = [x for x in dscope if not x.startswith('_')]
        return resp

    def get_scope_fns(self) -> list:
        if self.scope_class_instance is None:
            return [f for f in dir(self.scope) if
                    (inspect.iscoroutinefunction(getattr(self.scope, f)) or inspect.isfunction(getattr(self.scope, f)))]
        scidir = dir(self.scope_class_instance)
        filter = [x for x in scidir if
                  (not x.startswith('_'))
                  and
                  (
                          inspect.iscoroutinefunction(getattr(self.scope_class_instance, x))
                          or
                          inspect.isfunction(getattr(self.scope_class_instance, x))
                  )
                  ]
        return filter

    def get_scope_fn_sig(self, name):
        fn = None
        if self.scope_class_instance is None:
            fn = getattr(self.scope, name)
        else:
            fn = getattr(self.scope_class_instance, name)
        assert fn is not None
        sig = inspect.getfullargspec(fn)
        return sig

    def enter_subscope(self, subscope):
        if subscope not in self.get_subscopes():
            raise InvalidScopeException(f"{subscope} is not a valid subscope")
        target = getattr(self.scope, subscope)
        if inspect.isclass(target):
            self.scope_class = target
            sig = inspect.signature(target.__init__)
            if "user" in sig.parameters and len(sig.parameters) == 2:
                self.scope_class_instance = target(self.user)
            else:
                self.scope_class_instance = target()
        else:
            self.scope_class_instance = None
            self.scope_class = None
        self.path.append(getattr(self.scope, subscope))
        self.scope = getattr(self.scope, subscope)

    def move_up(self):
        if len(self.path) == 1:
            raise InvalidScopeException("You are already at the top level scope")
        self.path.pop()
        self.scope = self.path[-1]

    async def invoke_scope_method(self, process, name, args: list, kwargs: dict = {}):
        avail_fns = self.get_scope_fns()
        if name not in avail_fns:
            raise InvalidCommandException(f"{name} is not a valid command in this scope")
        if self.scope_class_instance is None:
            fn = getattr(self.scope, name)
        else:
            fn = getattr(self.scope_class_instance, name)
        return await fn(process, *args, **kwargs)


def args_from_tokens(t: list) -> list:
    args = []
    t = t[1:]
    for x in t:
        if '=' in x:
            break
        args.append(x)
    return args


def kwargs_from_tokens(t: list) -> dict:
    kwargs = {}
    for x in t:
        if '=' in x:
            k, v = x.split('=')
            kwargs[k] = v
    return kwargs


async def process_cmd(process, cmd, session: Session):
    builtins = [
        "help",
        "scope",
        "ls",
        "..",
        "describe",
        "whoami",
        "quit",
        "exit"
    ]

    cmd = cmd.rstrip('\n')
    tokens = cmd.split(' ')
    cmd = tokens[0]
    if cmd:
        cmdid = str(uuid.uuid4())
        try:
            scope_fns = session.get_scope_fns()
            if cmd not in builtins and cmd not in scope_fns:
                process.stdout.write(f"Error: {cmd} not a valid command in this scope")

            await db.writeConsoleHistory(id=cmdid,
                                         cmd=tokens[0], args=tokens[1:], started=timestamp())
            if cmd == "help":
                process.stdout.write("HELP:\n"
                                     "ls: show subscopes \n"
                                     "cmd: show scope commands\n"
                                     "describe: show cmd arguments\n"
                                     "scope: select subscope or .. to go back")
            elif cmd == "whoami":
                process.stdout.write(session.username)
            elif cmd == "scope":
                if tokens[1] in session.get_subscopes():
                    session.enter_subscope(tokens[1])
                else:
                    process.stdout.write("Error: not a valid scope")
            elif cmd == "ls":
                process.stdout.write("\n".join([str(s) for s in session.get_subscopes()]))
            elif cmd == "describe":
                if len(tokens) != 2:
                    process.stdout.write("Error: args: cmd")
                else:
                    sig = session.get_scope_fn_sig(tokens[1])
                    process.stdout.write(str(sig))
            elif cmd == "cmd":
                process.stdout.write("\n".join(session.get_scope_fns()))
            elif cmd == "..":
                if len(session.path) == 1:
                    process.stdout.write("Error: you are at the top level scope")
                else:
                    session.move_up()
            elif cmd == "quit" or cmd == "exit":
                process.exit(0)
            elif cmd in session.get_scope_fns():
                try:
                    res = await session.invoke_scope_method(process, cmd,
                                                            args_from_tokens(tokens),
                                                            kwargs_from_tokens(tokens))
                except Exception as e:
                    process.stdout.write(f"Error: {str(e)}\n")
                    res = ""
                    print_exc()
                if isinstance(res, dict):
                    res = json_pretty(res)
                elif isinstance(res, list):
                    res = [json_pretty(r) for r in res]
                    res = "\n".join(res)
                process.stdout.write(str(res))




        except AssertionError:
            process.stderr.write('Invalid command: %s\n' % cmd)
        await db.writeConsoleHistory(cmdid, finished=timestamp())


async def handle_ssh_conn(user_scopes, process):
    cl = "Turbindo SSH console"
    process.stdout.write(cl)
    process.stdout.write('Welcome %s! \n\n' %
                         process.get_extra_info("username"))

    session = await Session(process, user_scopes).ainit()
    exit_flag = False
    while not process.stdin.at_eof() and not exit_flag:
        try:
            process.stdout.write(f'{session.path[-1].__name__}> ')

            async for cmd in process.stdin:
                await process_cmd(process, cmd, session)
                process.stdout.write('\n')
                process.stdout.write(f'{session.path[-1].__name__}> ')
        except asyncssh.BreakReceived:
            exit_flag = True
        except asyncssh.TerminalSizeChanged as exc:
            pass

    process.exit(0)
