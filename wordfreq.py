import time
from datetime import timedelta

from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag

from tornado import gen, httpclient, ioloop, queues

base_url = ''
concurrency = 10

async def main():
    q = queues.Queue()
    start = time.time()
    fetching, fetched = set(), set()

    async def fetch_url(current_url):
        if current_url in fetching:
            return

    print('fetching %s' % current_url)
    fetching.add(current_url)
    urls = await get_links_from_url(current_url)
    fetched.add(current_url)

    for new_url in urls:
        # only follow links beneath the base url
        if new_url.startswith(base_url):
            await q.put(new_url)

    async def worker():
        async for url in q:
            if url is None:
                return
            try:
                await fetch_url(url)
            except Exception as e:
                print('Exception: %s, %s' % (e, url))
            finally:
                q.task_done()

    await q.put(base_url)

    # Start workers, then wait for the worker queue to be empty
    workers = gewn.multi([worker() for _ in range(concurrency)])
    await q.join(timeout=timedelta(seconds=300))
    assert fetching == fetched
    print ('Done in %d seconds, fethed %s urls' % (
        time.time() - start, len(fetched)))

    # signal all the workers to exit
    for _ in range(concurrency):
        await q.put(None)
    await workers


if '__name__' == '__main__':
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)
