from __future__ import print_function
from math import sin, cos, radians
import timeit
def bench():
    product = 1.0
    for counter in range(1, 1000, 1):
        for dex in list(range(1, 360, 1)):
            angle = radians(dex)
            product *= sin(angle)**2 + cos(angle)**2
    return product

if __name__ == '__main__':
    result = timeit.repeat('bench.bench()', setup='import bench', number=10, repeat=10)
    result = list(sorted(result))
    print(*result[:3])
