import random

l = list('AAAAAAAABBBBCCD')
random.shuffle(l)
print(''.join(l))
print('')

codes = {
    'A': '0',
    'B': '10',
    'C': '11',
    'D': '111',
}

for c in codes:
    print(c, '0'+format(ord(c), 'b'))
print('')
for c in codes:
    print(c, codes[c])
print('')

lb = ['0'+format(ord(x), 'b') for x in l]
print(''.join(lb))
print('')

lc = [codes[x] for x in l]
print(''.join(lc))
