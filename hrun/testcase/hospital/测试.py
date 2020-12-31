arr = [64, 34, 25, 12, 22, 11, 90]
def bubbleSort(collection):
    compare_count = 0
    length = len(collection)
    last_change_index = 0  # 最后一个交换的位置
    border = length - 1  # 有序和无序的分界线
    for i in range(length - 1):
        swapped = False
        for j in range(0, border):
            compare_count += 1
            if collection[j] > collection[j + 1]:
                swapped = True
                collection[j], collection[j + 1] = collection[j + 1], collection[j]
                last_change_index = j
        if not swapped:
            break  # Stop iteration if the collection is sorted.
        border = last_change_index  # 最后一个交换的位置就是边界
    return collection


arr = bubbleSort(arr)
print("排序后的数组:", arr)