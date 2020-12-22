from asyncio import Queue
import asyncio


# from crawler.code import crawling

# loop = asyncio.get_event_loop()
# q= Queue(maxsize=2,loop=loop)
# for i in range(3):
#     q.put(3)
#
# print("done")

# c = crawling.Crawler("abc")
# print(type(c.crawl()))

# def gen():
#     print("begin")
#     try:
#         v = yield 11
#         print("receive {0}".format(v))
#         return True
#     finally:
#         print(2)
#
# g = gen()
# v = g.send(None)
# v = g.send('b')

# from random import randint
# def c():
#     return randint(1,10)
# a= iter(c,1)
# for v in a:
#     print(v)


def gen_throws():
    print("next called")
    yield
    print("yielded")
    raise Exception("abc")
    return 2


loop = asyncio.get_event_loop()
loop.run_until_complete(gen_throws())

# g = gen_throws()
#
# def warp():
#     # g = gen_throws()
#     v = yield from gen_throws()
#     print(v)
#
# w= warp()

# w.send(None)
# w.send(1)
# w.send(1)
# w.send(1)
# w.send(1)

# asyncio.run(g)
# loop = asyncio.get_event_loop()
#
# async def run_by_workers():
#     asyncio.Task(gen_throws(),loop=loop)
#     # workers = [asyncio.Task(gen_throws(), loop=loop) for _ in range(2)]
#     await asyncio.sleep(3)
#     # for w in workers:
#     #     w.cancel()
#
# loop.run_until_complete(run_by_workers())


