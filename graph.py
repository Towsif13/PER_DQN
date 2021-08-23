import numpy as np
import matplotlib.pyplot as plt


def moving_average(a, n=100):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


scores_per = np.loadtxt("scores_per.txt")
print(len(scores_per))
scores_ma_per = moving_average(scores_per, n=100)
print(len(scores_ma_per))
scores_ma_per_1000 = moving_average(scores_per, n=1000)
print(len(scores_ma_per_1000))

plt.plot(np.arange(len(scores_ma_per)), scores_ma_per,
         alpha=0.2, color='b')
plt.plot(np.arange(len(scores_ma_per_1000)),
         scores_ma_per_1000, label="PER", color='b')

plt.ylabel('Score')
plt.xlabel('Episode ')
plt.legend()
plt.savefig('graph_per.png')
plt.show()
