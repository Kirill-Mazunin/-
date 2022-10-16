count = 0

a = [int(i) for i in input().split()]
for k in range(1, len(a)-1):
    if a[k - 1] < a[k] and a [k] > a[k + 1]:
        count+=1

print(count)