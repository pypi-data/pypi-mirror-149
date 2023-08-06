import asyncio
from typing import List

import aiohttp.web
from aiohttp import web
from aiohttp.web_routedef import RouteDef


async def start_http(port: int, routes: List[RouteDef]):
    server = web.Application(loop=asyncio.get_running_loop())
    server.add_routes(routes)
    app_runner = aiohttp.web.AppRunner(server)
    await app_runner.setup()
    tcp_site = aiohttp.web.TCPSite(app_runner,port=port)
    await tcp_site.start()
