import asyncio
import types

# def transpose_list(list_of_lists):
#     return [
#         list(row)
#         for row in zip(*list_of_lists)
#     ]
#
# l = [[1,2],[3,4]]
# for row in zip(*l):
#     print(row)
#     print(list(row))

# def gen():
#     yield
#
# class A:
#     def __init__(self):
#         self.index=0
#
#     def __iter__(self):
#
#         return self
#
#     def __next__(self):
#         self.index +=1
#         if self.index > 10:
#             raise StopIteration
#         return self.index
#
#
# a = A()
# for v in a:
#     print(v)

# a=A()
# print(next(a))

class Waiting:
    def __await__(self): # __await__ method must return an iterator, but await must 'await' on #1 object implemented __await__ or #2 coroutine
        # return A()
        # return gen()
        # return asyncio.sleep(2).__await__()
        return asyncio.sleep(0.1)

@types.coroutine
def gen2():
    yield
    return 2


async def main():
    await Waiting()
    # v=await gen2()
    # print(v)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())