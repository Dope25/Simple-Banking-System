card = '400000635752838'
summary = 0
count = 0
array = [int(x) for x in card]
print(array)
for x in array:
    if count % 2 == 0:
        array[count] = x * 2
    if array[count] > 9:
        array[count] -= 9
    summary += array[count]
    count += 1
print(array)
print(summary)
print(sum(array))
print(10 - summary % 10)

