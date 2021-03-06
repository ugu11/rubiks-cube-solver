from populations_ops import repair
# a = ["l'", "u'", 'r', 'l', "r'"]
a = ['u', 'n', 'n', 'n']
b = {'fit': 0, 'val': a}

p = [b]

p2 = repair(p)

print(p)
print(p2)