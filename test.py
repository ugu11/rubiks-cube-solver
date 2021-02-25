from ga import repair_chromossome, fix_empty_moves
from populations_ops import *
from selections import *

# # a = "b2 f' d2 b2 u u2 f".split(" ") # b d' l2 l' r2 r' b u' f u l2 d u2 d2 f' b' u2 n".split(" ")
# a = "b2 f' d2 b2 u u2 f b d' l2 l' r2 r' b u' f u l2 d n n n n n n".split(" ")
# c = {'fit': 0, 'val': a}
# print(c['val'])

# chrom = repair_chromossome(c)
# chroms = fix_empty_moves(chrom)
# # chrom = repair_chromossome(chrom)

# print(chrom['val'])
# print(" ")
# for c in chroms:
#     print(c['val'])

pop = generate_pop()
evaluate_pop(Cube(), pop)
roullete_selection(Cube(), pop)


print([c['fit'] for c in pop])
