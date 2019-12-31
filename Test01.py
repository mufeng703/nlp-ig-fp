import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

a = 0
b = 1
mu = 0
variance = 1
c = (b - a) / 10

ary1 = np.arange(10000)
ary = ary1.astype(float)

for i in range(10000):
    U = random.uniform(a, b)
    U2 = random.uniform(a, b)
    x = math.cos(2 * math.pi * U) * math.pow(-2 * np.log(U2), 0.5)
    result = mu + x * variance

    ary[i] = result

print(ary)
df = pd.DataFrame(ary)
df.columns = ['RV']

plt.hist(df.values, bins=10, edgecolor="k")
plt.show()
