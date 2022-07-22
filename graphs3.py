import matplotlib.pyplot as plt
import pandas as pd

# first line is memcpy
results_lzbench = pd.read_csv(open('results-lzbench.csv', 'rb'))[1:]
results_nvcomp = pd.read_csv(open('results-nvcomp.csv', 'rb'))

def to_dict(names, ratios, throughputs):
    res = {}
    for i, n in enumerate(names):
        if not n in res: res[n] = ([], [])
        res[n][0].append(ratios[i])
        res[n][1].append(throughputs[i])
    return res

def extract_lzbench(results):
    names = [x.split()[0] for x in results['Compressor name']]
    ratios = list(results['Ratio']/100)
    throughputs = list(results['Compression speed'])
    return to_dict(names, ratios, throughputs)

def extract_nvcomp(results):
    names = list(results['Compressor name'])
    ratios = list(1/results['Compression ratio'])
    throughputs = (1000*results['Compression throughput (uncompressed) in GB/s'])
    return to_dict(names, ratios, throughputs)

results = {}
results.update(extract_lzbench(results_lzbench))
results.update(extract_nvcomp(results_nvcomp))

plt.style.use('ggplot')
plt.yscale('log')
plt.xlabel('Compression ratio (outsize/insize)')
plt.ylabel('Throughput (MB/s)')

for name in results:
    res = results[name]
    plt.plot(res[0], res[1], marker='o')
    tooclose = name in ['nvcomp_deflate', 'bsc']
    valign = 'top' if tooclose else 'bottom'
    plt.annotate(name, (res[0][0], res[1][0]), verticalalignment=valign, fontsize=9)

plt.subplots_adjust(left=0.2, right=0.8)
plt.savefig('results3.png', dpi=300)
#plt.show()
