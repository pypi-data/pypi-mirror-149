import tooltable


rows = [
    [1, 2, 3],
    [1e6, 2e7, 3e8],
    [1.12345, 2.12345, 3.12345],
    ['cat', 'dog', 'panda'],
]
headers = ['a', 'b', 'c']


def test_print_table_basic():
    # test that prints without error
    tooltable.print_table(rows=rows, headers=headers)

