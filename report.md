---
geometry: margin=3cm
toc: true
title: Exploration of GPU-enabled lossless compressors
author: Stefan Rua, `stefan.elias.rua@cern.ch`
---


# Introduction

The data produced by CMS's High Level Trigger (HLT) is compressed to speed up network transfers, and currently this is done using CPUs. However, as we have new computers with powerful GPUs, it would be nice to transfer some of the load onto the GPUs. This is the motivation for finding a good GPU-enabled compressor. GPU-enabled compressors aren't widely adopted yet, but in the last ten years some researchers and companies have showed interest in the topic.


# Algorithms

Most compressors use a combination of multiple more fundamental compression algorithms. The most common ones are explained briefly in this section.

## Burrows-Wheeler transform

The Burrows-Wheeler transform[^bwt_wiki]^,^[^bwt_paper], also called block-sorting compression, sorts the data so that repeating patterns are near each other, making it easier to compress.

\begin{gather*}
\texttt{SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES} \\
\downarrow \\
\texttt{TEXYDST.E.IXIXIXXSSMPPS.B..E.S.EUSFXDIIOIIIT}
\end{gather*}

[^bwt_wiki]: <https://en.wikipedia.org/wiki/Burrows-Wheeler_transform>
[^bwt_paper]: <https://www.hpl.hp.com/techreports/Compaq-DEC/SRC-RR-124.pdf>

## Huffman coding

Huffman coding[^huffman_wiki]^,^[^huffman_paper] gives characters prefix codes that vary in length based on their frequency, so that the most common ones take the least space.

$$
\texttt{CAAACBDABAAABAB}
$$

$$
\text{ASCII codes}
$$

|     |            |
|-----|------------|
| `A` | `01000001` |
| `B` | `01000010` |
| `C` | `01000011` |
| `D` | `01000100` |

$$
\text{Huffman codes}
$$

|     |       |
|-----|-------|
| `A` | `0`   |
| `B` | `10`  |
| `C` | `110` |
| `D` | `111` |

\begin{gather*}
\texttt{010000110100000101000001010000010100001101000010010001000100} \\
\texttt{000101000010010000010100000101000001010000100100000101000010} \\
\downarrow \\
\texttt{1100001101011101000010010}
\end{gather*}

[^huffman_wiki]: <https://en.wikipedia.org/wiki/Huffman_coding>
[^huffman_paper]: <http://compression.ru/download/articles/huff/huffman_1952_minimum-redundancy-codes.pdf>

## The Lempel-Ziv family

The Lempel-Ziv[^lz_wiki]^,^[^lz_paper] (LZ) family of compression algorithms replace patterns with references to previous occurences.

[^lz_wiki]: <https://en.wikipedia.org/wiki/Lempel-Ziv-Welch>
[^lz_paper]: <https://courses.cs.duke.edu/spring03/cps296.5/papers/ziv_lempel_1978_variable-rate.pdf>

## Asymmetric numeral systems

Asymmetric numeral systems[^ans_wiki]^,^[^ans_paper] (ANS) encodes the data into a natural number based on the frequency of different symbols.

[^ans_wiki]: <https://en.wikipedia.org/wiki/Asymmetric_numeral_systems>
[^ans_paper]: <https://arxiv.org/pdf/1311.2540.pdf>


# Compressors

## CPU

### zlib

zlib[^zlib] is a compression library that implements the DEFLATE algorithm, which is a combination of Huffman coding and LZ77, a Lempel-Ziv variant.

[^zlib]: <https://en.wikipedia.org/wiki/Zlib>

### LZ4

LZ4[^lz4] is an algorithm based on LZ77 that prioritizes speed.

[^lz4]: <https://en.wikipedia.org/wiki/LZ4_(compression_algorithm)>

### LZMA

LZMA[^lzma], the Lempel–Ziv–Markov chain algorithm, is an algorithm that prioritizes compression ratio.

[^lzma]: <https://en.wikipedia.org/wiki/Lempel-Ziv-Markov_chain_algorithm>

### Zstandard

Zstandard[^zstd] is the compressor that is currently used for HLT data. It is used as a reference point for all comparisons in this report. Zstandard combines ANS and LZ77.

[^zstd]: <https://en.wikipedia.org/wiki/Zstd>

### XZ

Another point of comparison running on the CPU is xz[^xz], which achieves great compression ratios at the cost of throughput. xz combines LZMA with some preprocessing.

[^xz]: <https://en.wikipedia.org/wiki/XZ_Utils>

## GPU

### BSC

BSC[^bsc] is a GPU accelerated block-sorting compressor. The default makefile doesn't compile the necessary files for CUDA support, so a few changes were needed. Multiple block sorting algorithms are available: the Burrows-Wheeler transform and sort transforms of order 3 to 8. The sort transform is a generalization of the Burrows-Wheeler transform that takes into account a different size context when sorting. Only sort transforms of order 5 to 8 can use the GPU, of which 7 and 8 use it by default and 5 and 6 require and additional flag for it.

[^bsc]: <https://github.com/IlyaGrebnov/libbsc>

### CULZSS

CULZSS[^culzss]^,^[^culzss_paper] is a CUDA implementation of LZSS. CULZSS-bit[^culzss-bit], a more recent and reportedly better performing version exists, but no source code or binary is available for it. I emailed the author, but he couldn't find the code either. He also mentioned that the code for the original CULZSS on github might not work.

[^culzss]: <https://github.com/adnanozsoy/CUDA_Compression>
[^culzss_paper]: <https://web.cs.hacettepe.edu.tr/~aozsoy/papers/2011-ppac.pdf>
[^culzss-bit]: <https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7079027>

### nvCOMP

nvCOMP[^nvcomp] is a library for GPU compression by Nvidia, and it implements Deflate, LZ4, Cascaded, Snappy, BitComp, and ANS. I expect nvCOMP's compressors to perform well, as it is in Nvidia's interest to make their GPUs look good. Unfortunately nvCOMP was made proprietary in version 2.3.

[^nvcomp]: <https://developer.nvidia.com/nvcomp>

### DietGPU

DietGPU[^dietgpu] is a work-in-progress ("very early alpha preview") compression library by Facebook which implements ANS. As its purpose they state speeding up network transfers in a datacenter environment, which matches our use case. DietGPU provides two codecs: a general byte-oriented entropy encoder and decoder, and another one specifically for floating point data. At the time of writing only a Python API for PyTorch tensors is ready, but the underlying encoders and decoders are implemented in C++ and CUDA, making it possible to utilize library for other data as well.

[^dietgpu]: <https://github.com/facebookresearch/dietgpu>

### HuffmanCoding_MPI_CUDA

HuffmanCoding_MPI_CUDA[^hcmc] performs Huffman compression with the option of using CUDA, MPI, CUDA and MPI, or no parallelization at all. I used it on the CUDA setting.

[^hcmc]: <https://github.com/smadhiv/HuffmanCoding_MPI_CUDA>

### cuda_bzip2

cuda_bzip2[^cuda_bzip2] is a modified version of bzip2 with CUDA support. bzip2 is a compressor based on the Burrows-Wheeler transform.

[^cuda_bzip2]: <https://github.com/aditya12agd5/cuda_bzip2>

## NX

### libnxz

IBM's POWER9 processor has a dedicated hardware accelerator for compression called NX. The library that provides an interface for compressing on this accelerator is called libnxz, and is a drop-in replacement for zlib.

# Benchmarking

## Crude first tests

As a first step I ran the compressors from the command line, measuring the time taken by them using the `time` command. This gave me a rough idea of their performance, based on which I selected the ones to examine in more detail. libnxz and DietGPU are excluded from these because I found out about them later, and they seemed promising enough right away. The only CPU compressors included in this part are Zstandard and XZ because they give a good enough idea of the compression ratios and throughputs achievable with CPUs.

## Finer evaluation

lzbench[^lzbench] is an in-memory benchmarking tool for compressors. Excluding the time taken to read and write files to and from the disk gives a more accurate idea of the compressor's throughput. I added the most promising compressors to lzbench. The throughputs shown are the highest ones from 5 runs. For the GPU compressors, copying from RAM to GPU memory and back is included.

Adding the more recent proprietary version of nvCOMP to lzbench was taking more time than what I was willing to spend on it, so it is excluded from the tests. The LZ4 implementation from nvCOMP's older open-source version is included since it was already available in lzbench.
<!--so its results are the ones reported by Nvidia's own proprietary benchmarking binaries. I expect these to exclude all possible overhead, such as copying the files to GPU memory from RAM.-->

The lzbench benchmarks were run on two machines:

- one that resembles the actual HLT ones, with an AMD EPYC 75F3 CPU and Nvidia Teslta T4 GPU, and
- another with a POWER9 CPU (8335-GTH) and four Nvidia Tesla V100 GPUs.

The libnxz benchmark are only in the POWER9 results, as that is the chip with the NX accelerator.
<!--did any of the compressors utilize multiple gpus?-->

[^lzbench]: <https://github.com/inikep/lzbench>

## Data

The data that was compressed in these benchmarks consists of raw event files as they come from the HLT. All lzbench benchmarks were run on 100 proton-proton collision files and 100 heavy ion collision files, both sets taking approximately 100 MB.

The crude tests were run on a single file containing a few heavy ion events.

# Results

The labels in the plots are the command or library names, some of which differ from the more verbose names used earlier.

<!--| bsc | BSC | CPU |
| bsc_cuda | BSC | GPU |-->

| Abbreviation | Compressor | Device |
|--------------|------------|--------|
| bsc | BSC | GPU |
| culzss | CULZSS | GPU |
| dietgpu | DietGPU | GPU |
| hcmc | HuffmanCoding_MPI_CUDA | GPU |
| libnxz | libnxz | IBM NX |
| lz4 | LZ4 | CPU |
| lzma | LZMA | CPU |
| nvcomp_lz4 | nvCOMP's LZ4 | GPU |
| xz | XZ | CPU |
| zlib | zlib | CPU |
| zstd | Zstandard | CPU |

![First crude tests. GPU compressors are marked with `*`](results/first.png){ width=80% }

![Compressor performance on proton-proton events. GPU compressors are marked with `*`, NX with `**`.](results/combined-pp.png){ width=80% }

![Compressor performance on heavy ion events. GPU compressors are marked with `*`, NX with `**`.](results/combined-hi.png){ width=80% }

\newpage


# Discussion

The best candidate from the GPU compressors included in the crude tests seems to be BSC, which on its lowest setting performs similarly to zstd on its highest setting. HuffmanCoding_MPI_CUDA is faster than BSC but doesn't compresses nearly as well. CULZSS manages to increase the file size, indicating that the author was correct: the code on github might not work.
<!--explain lzss earlier and mention that lzss shouldn't increase the size due to the break-even point?-->

Out of the results produced by lzbench, libnxz stands out with its combination of extreme throughput and reasonable compression ratio. BSC is outperformed by XZ and LZMA in both ratio and throughput, and DietGPU is very fast, but suffers from relatively poor compression.

It would be nice to use libnxz, but POWER9 machines are prohibitively expensive and as stated in the introduction, the whole point is to make use of the GPUs that we already have. DietGPU would make use of them, but even ignoring the suboptimal compression ratio, throughput would most likely be worse than for Zstandard which can be run on a massive number of threads at once for separate event files.
<!--explain that the GPU is pretty much used by one process at a time-->
<!--dietgpu can compress multiple files in parallel from one call, investigate?-->


# Conclusion

Continuing to use Zstandard seems to be the reasonable choice with our current hardware and the state of GPU compressors. An eye should be kept on DietGPU, as it is still under rapid development.
