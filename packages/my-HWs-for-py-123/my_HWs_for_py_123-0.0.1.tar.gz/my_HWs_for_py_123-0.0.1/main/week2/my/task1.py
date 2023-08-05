
def filter_list(item_list):
    # res = item_list[:]
    # for item in item_list:
    #     if not isinstance(item, int):
    #         res.remove(item)
    # return res

    # return [item for item in item_list if type(item) == int]

    return list(filter(lambda x: isinstance(x, int), item_list))


if __name__ == '__main__':
    assert filter_list([1, 2, 'a', 'b']) == [1, 2]
    assert filter_list([1, 'a', 'b', 0, 15]) == [1, 0, 15]
    assert filter_list([1, 2, 'aasf', '1', '123', 123]) == [1, 2, 123]
