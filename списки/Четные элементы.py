c = input() .split()
for k in range(len(c)):
    c[k] = int(c[k])
    if c[k] %2 == 0:
        print(c[k], end =' ')