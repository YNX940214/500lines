# https://stackoverflow.com/questions/65369022/exception-in-python-asyncio-task-not-raised-until-main-task-complete
import asyncio

@asyncio.coroutine
def coro1():
    try:
        print("coro1 primed")
        yield
        raise Exception("abc")
    except Exception as e:
        print(e)
        return 1
        # raise


@asyncio.coroutine
def coro2(loop):
    try:
        print("coro2 primed")
        ts = [asyncio.Task(coro1(),loop=loop) for _ in range(2)]
        res = yield from asyncio.sleep(10)
        print(res)
    except Exception as e:
        print("aaa:",e)
        raise


async def coro3():
    try:
        print("coro3 primed")
        res, *ignored = await asyncio.gather(
            coro1(),
            coro1(),
            *[coro1() for _ in range(2)],
            asyncio.sleep(3)
        )
        print(res)
    except Exception as e:
        print(e)
        raise


loop= asyncio.get_event_loop()
# loop.run_until_complete(coro2(loop))
loop.run_until_complete(coro3())