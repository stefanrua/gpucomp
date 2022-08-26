---
documentclass: scrartcl
geometry: 
- margin=2cm
- bottom=0.2cm
classoption: twocolumn
papersize: a3
fontsize: 12
title: Exploration of GPU-enabled lossless compressors
author: Stefan Rua, `stefan.elias.rua@cern.ch` / `stefan.rua@iki.fi`
---
\thispagestyle{empty}

\ 

![First simple tests.](results/first.png){ width=45% }

![Compressor performance on proton-proton events.](results/combined-pp.png){ width=45% }

![Compressor performance on heavy ion events.](results/combined-hi.png){ width=45% }


\newpage

\ 

# Why?

- Data from the HLT is compressed
- This is done on CPUs
- GPUs can be very fast


# What I did

- Looked for GPU compressor implementations
- Added them to a benchmarking program
- Compared them to CPU compressors


# Benchmarking

First I ran some simple tests using the `time` command and  the standalone executables of the compressors. After determining the most promising ones, I implemented them into a benchmarking program called `lzbench` to get proper measuremets that exclude disk reads and writes. The benchmarks were run on two machines, one that resembles the machines in the HLT and a POWER9 machine. The HLT doesn't have POWER9 machines, but I wanted to try out `libnxz`, a zlib-compatible library that makes use of the NX GZIP hardware accelerator present on that chip.

Data:

- 100 Proton-proton events
- 100 Heavy ion events

Timing:

- Wall time
- Disk $\rightarrow$ RAM **excluded**
- RAM $\rightarrow$ GPU memory **included**
- Fastest from 5 repeats

POWER9 machine:

- IBM POWER9
- Nvidia Tesla V100

HLT-like machine:

- AMD EPYC 75F3
- Nvidia Tesla T4


# Conclusion

Continuing to use Zstandard seems to be the reasonable choice with our current hardware and the state of GPU compressors. An eye should be kept on DietGPU, as it is still in its infancy and under rapid development.

# Results

In all figures GPU compressors are marked with `*` and the NX compressor with `**`.


# Links

## Compressors

\scriptsize{\textbf{bsc}: \url{https://github.com/IlyaGrebnov/libbsc}} \ 
\scriptsize{\textbf{culzss}: \url{https://github.com/adnanozsoy/CUDA_Compression}} \ 
\scriptsize{\textbf{dietgpu}: \url{https://github.com/facebookresearch/dietgpu}} \ 
\scriptsize{\textbf{hcmc}: \url{https://github.com/smadhiv/HuffmanCoding_MPI_CUDA}} \ 
\scriptsize{\textbf{libnxz}: \url{https://github.com/libnxz/power-gzip}} \ 
\scriptsize{\textbf{lz4}: \url{https://github.com/lz4/lz4}} \ 
\scriptsize{\textbf{nvcomp_lz4}: \url{https://github.com/NVIDIA/nvcomp}} \ 
\scriptsize{\textbf{xz}: \url{https://tukaani.org/xz/}} \ 
\scriptsize{\textbf{zlib}: \url{http://zlib.net/}} \ 
\scriptsize{\textbf{zstd}: \url{https://github.com/facebook/zstd}} \ 

<!--
**bsc**: <https://github.com/IlyaGrebnov/libbsc> \
**culzss**: <https://github.com/adnanozsoy/CUDA_Compression> \
**dietgpu**: <https://github.com/facebookresearch/dietgpu> \
**hcmc**: <https://github.com/smadhiv/HuffmanCoding_MPI_CUDA> \
**libnxz**: <https://github.com/libnxz/power-gzip> \
**lz4**: <https://github.com/lz4/lz4> \
**nvcomp_lz4**: <https://github.com/NVIDIA/nvcomp> \
**xz**: <https://tukaani.org/xz/> \
**zlib**: <http://zlib.net/> \
**zstd**: <https://github.com/facebook/zstd> \
-->

<!--
| Name | Device | Code |
|------|--------|--------|
| bsc | GPU | <https://github.com/IlyaGrebnov/libbsc> |
| culzss | GPU | <https://github.com/adnanozsoy/CUDA_Compression> |
| dietgpu | GPU | <https://github.com/facebookresearch/dietgpu> |
| hcmc | GPU | <https://github.com/smadhiv/HuffmanCoding_MPI_CUDA> |
| libnxz | IBM NX | <https://github.com/libnxz/power-gzip> |
| lz4 | CPU | <https://github.com/lz4/lz4> |
| nvcomp_lz4 | GPU | <https://github.com/NVIDIA/nvcomp> |
| xz | CPU | <https://tukaani.org/xz/> |
| zlib | CPU | <http://zlib.net/> |
| zstd | CPU | <https://github.com/facebook/zstd> |
-->

<!--
| lzma | LZMA | CPU |
-->
