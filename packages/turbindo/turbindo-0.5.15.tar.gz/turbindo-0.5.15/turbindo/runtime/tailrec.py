import inspect

# https://towardsdatascience.com/tagged/tail-call-optimization?p=4d0ea55b0542

def tail_rec(func):
    rec_flag = False
    targs = []
    tkwargs = []

    def helper(*args, **kwargs):
        nonlocal rec_flag
        nonlocal targs
        nonlocal tkwargs
        f = inspect.currentframe()

        if f.f_code == f.f_back.f_back.f_code:
            rec_flag = True
            targs = args
            tkwargs = kwargs
            return
        else:
            while True:
                try:
                    result = func(*args, **kwargs)
                except TypeError as e:
                    raise Exception("It is possible that the decorated function is not tail recursive")
                if rec_flag:
                    rec_flag = False
                    args = targs
                    kwargs = tkwargs
                else:
                    return result

    return helper
