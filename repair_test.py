from populations_ops import repair
# a = ["l'", "u'", 'r', 'l', "r'"]
a = ['u', 'u', 'f', 'n', 'f2', 'l', "l'", 'r', "l"]
# u2 f' r l2
b = {'fit': 0, 'val': a}

p = [b]

p2 = repair(p)

print(p)
print(p2)