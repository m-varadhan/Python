def return4():
    yield 4


def yield_from():
    yield from range(4)
    yield from return4()


def test_yield_from():
    for x in yield_from():
        print(x)


test_yield_from()
