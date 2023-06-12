import asyncio
import datetime

from aiohttp import ClientSession
from arq import create_pool
from arq.connections import RedisSettings
from arq.worker import Worker
from arq_prometheus import ArqPrometheusMetrics


async def download_content(ctx, url):
    session: ClientSession = ctx["session"]
    async with session.get(url) as response:
        content = await response.text()
        print(f"{url}: {content[:80]}...")
    return len(content)


async def startup(ctx):
    ctx["session"] = ClientSession()
    arq_prometheus = ArqPrometheusMetrics(ctx, delay=delay, enable_webserver=True)
    ctx["arq_prometheus"] = await arq_prometheus.start()


async def shutdown(ctx):
    await ctx["session"].close()
    await ctx["arq_prometheus"].stop()


async def main():
    redis = await create_pool(RedisSettings())
    for url in ("https://facebook.com", "https://microsoft.com", "https://github.com"):
        await redis.enqueue_job("download_content", url)


# WorkerSettings defines the settings to use when creating the worker,
# it's used by the arq cli.
# For a list of available settings,
# see https://arq-docs.helpmanual.io/#arq.worker.Worker
class CustomWorker(Worker):
    def __init__(self):
        super().__init__(functions=[download_content], on_startup=startup, on_shutdown=shutdown, health_check_interval=delay.total_seconds())


if __name__ == "__main__":
    delay = datetime.timedelta(seconds=5)
    asyncio.run(main())
