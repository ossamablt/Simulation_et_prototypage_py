import copy

a = [1, 2, 3]
b = copy.copy(a)
b[0] = 99

b[1] = 99
print(a)  # ستتأثر القائمة الأصلية
a[1] = 99
print(b)  # ستتأثر القائمة الأصلية
