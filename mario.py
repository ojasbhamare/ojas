while True:
    n = int(input('Height: '))
    if 0 < n < 9:
        break

for i in range(n):
    for j in range(n):
        if j >= n - i - 1:
            print('#', end='')
        else:
            print(' ', end='')
    print()

