
def f():
    try:
        raise Exception
    except Exception as e:
        raise
        return 1
    finally:
        return 2


print(f())