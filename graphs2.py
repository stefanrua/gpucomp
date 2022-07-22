import matplotlib.pyplot as plt

names = ['ans', 'bitcomp', 'cascaded', 'deflate', 'gdeflate', 'lz4', 'snappy', 'zstd_cpu']
ratios = [2.2211, 1.1954, 1.0656, 3.8680, 3.8215, 2.9964, 3.6101, 100/16.16]
through_c = [0.5734, 14.8923, 1.5420, 0.0525, 0.0528, 0.0602, 0.0717, 0.097]
through_c = [x * 1000 for x in through_c]
through_d = [0.6817, 0.8594, 2.6342, 0.1865, 0.4175, 0.1688, 0.2831, 0.225]

def plot():
    plt.yscale('log')
    for i in range(len(names)):
        plt.scatter(ratios[i], through_c[i], label=names[i])
    plt.legend()
    plt.show()

plot()
