import matplotlib.pyplot as plt

results = {'zstd': [['-1', '-3', '-9', '-19'], [258.4140463296379, 163.88852924781074, 43.72637526427399, 9.687707828359505], [0.7933601455488924, 0.7782279396745265, 0.7702009160626969, 0.756965973429537]], 'xz': [['-0', '-3', '-6', '-9'], [11.606166096022688, 9.458649823623368, 5.100490349702948, 4.885381564136004], [0.6994451579373356, 0.6877364378594628, 0.646091372563434, 0.646091372563434]], 'bsc_cuda': [['-G -m5 -e0', '-G -m5 -e1', '-G -m5 -e2'], [10.621215693845622, 9.186427734113185, 6.122815660623057], [0.7569990726725884, 0.7499531398838015, 0.743792291826334]], 'culzss': [[''], [17.34874110339761], [1.1181232253731117]], 'hcmc': [[''], [16.585734771547497], [0.9126902314990318]], 'cuda_bzip2': [[''], [6.499193246661601], [0.766410046955208]]}

def scatter(results, colors=None):
    i = 0
    for c in results:
        throughputs = results[c][1]
        ratios = results[c][2]
        col = None if not colors else colors[i]
        plt.scatter(ratios, throughputs, label=c, c=col)
        i += 1

#colors = ['cornflowerblue', 'red', 'goldenrod']
#colors_single = ['lightsteelblue', 'pink', 'gold']
#scatter(results, colors)
#scatter(results_single, colors_single)
#scatter(results)

#plt.yscale('log')
#plt.axvline(x=1, color='gray', linewidth='0.5')
#plt.xlabel('Compression ratio (in/out)')
#plt.ylabel('Throughput (MB/s, CPU time)')
#plt.legend()
#plt.show()



plt.style.use('ggplot')
plt.yscale('log')
plt.xlabel('Compression ratio (outsize/insize)')
plt.ylabel('Throughput (MB/s)')

for name in results:
    res = results[name]
    plt.plot(res[2], res[1], marker='o', markersize=3)
    tooclose = name in ['nvcomp_deflate', 'bsc']
    valign = 'top' if tooclose else 'bottom'
    plt.annotate(name, (res[2][0], res[1][0]), verticalalignment=valign, fontsize=9)

plt.subplots_adjust(left=0.2, right=0.8)
plt.savefig('results1.png', dpi=300)
