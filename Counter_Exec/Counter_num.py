from collections import Counter

number = [1, 2, 3, 2, 1,
          2, 3, 4, 5, 6,
          5, 4, 3, 3, 3,
          4, 5, 6, 7, 8,
          9, 9, 7, 6, 6,
          5, 5, 4, 4, 5]

number_counter = Counter(number)

print(number_counter)

print(number_counter.keys())
print(number_counter.values())
print(number_counter.items())

sorted_C_union = sorted(number_counter.items(), key=lambda x: [x[0], x[1]])

print(sorted_C_union)



