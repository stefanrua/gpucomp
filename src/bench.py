#!/usr/bin/env python3

# Usage: cd to dir with .dat files, run

import sys
import os
import resource
import time as pytime
import pickle

n_repeats = 5
parallel = False
cputime = False

# To add a new compressor:
#  - create a list of options
#  - add an entry to the `comps` dict
#  - specify how it should be called in the `compcommand` function

def levels(mi, ma):
    return [f"-{x}" for x in range(mi, ma+1)]

options_zstd = levels(1, 19)
options_xz = levels(1, 9)
options_lz4 = levels(1, 9)
# libbsc
options_bsc = ['-G -b1 -m6 -cf -e0 -H15 -M4']
options_bsc_cpu = [x[3:] for x in options_bsc]
# CUDA_Compression
options_culzss = ['']
# HuffmanCoding_MPI_CUDA
options_hcmc = ['']
# cuda_bzip2
options_cuda_bzip2 = ['']

# List: 0=options, 1=throughputs, 2=relative compressed sizes
comps = {
    'zstd': [options_zstd, [], []],
    'xz': [options_xz, [], []],
    'lz4': [options_lz4, [], []],
    'bsc': [options_bsc, [], []],
    #'bsc_cpu': [options_bsc_cpu, [], []],
    'culzss': [options_culzss, [], []],
    'hcmc': [options_hcmc, [], []],
    'cuda_bzip2': [options_cuda_bzip2, [], []],
    }

outpath = 'out/'
resfile = 'results.pkl'

def compcommand(compressor, opt):
    if compressor == 'zstd':
        command = f"zstd {opt} $f -o {outpath}$f.zst"
    if compressor in ['bsc', 'bsc_cpu']:
        command = f"bsc e $f {outpath}$f.bsc {opt}"
    if compressor == 'xz':
        command = f"xz {opt} -k $f; mv $f.xz {outpath}"
    if compressor == 'lz4':
        command = f"lz4 {opt} $f; mv $f.lz4 {outpath}"
    if compressor == 'culzss':
        command = f"culzss -i $f -o {outpath}$f.culzss"
    if compressor == 'hcmc':
        command = f"hcmc $f {outpath}$f.hcmc"
    if compressor == 'cuda_bzip2':
        command = f"cuda_bzip2 9 0 $f; mv $f.bz2 {outpath}"
    return command

def walltime():
    return pytime.time()

def cputime():
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    return sum(usage[0:2])

def time():
    if cputime: return cputime()
    return walltime()

def size(path):
    s = 0
    for f in os.listdir(path):
        if '.dat' in f:
            s += os.path.getsize(f"{path}{f}")
    return s

# MB/s
def time_to_throughput(t):                                                        
    return [size_orig/x/1000000 for x in t]

def size_to_percentage(sizes):
    return [x / size_orig for x in sizes]

def compress(command):
    bg = '&' if parallel else ''
    script = f"""
for f in *.dat*
do
    {command} {bg}
done
wait
"""
    t = time()
    os.system(script)
    t = time()-t
    s = size(outpath)
    os.system(f"rm {outpath}*")
    return t, s

def benchmark(compressor, options):
    times = []
    sizes = []
    for opt in options:
        command = compcommand(compressor, opt)
        t_rep = []
        s_rep = []
        for r in range(n_repeats):
            t, s = compress(command)
            t_rep.append(t)
            s_rep.append(s)
        times.append(min(t_rep))
        sizes.append(min(s_rep))
    return times, sizes

size_orig = size('./')
os.system(f"mkdir {outpath}")
for c in comps:
    options = comps[c][0]
    times, sizes = benchmark(c, options)
    comps[c][1] = time_to_throughput(times)
    comps[c][2] = size_to_percentage(sizes)
os.system(f"rmdir {outpath}")

pickle.dump(comps, open(resfile, 'wb'))
