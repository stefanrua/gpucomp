---
title: Exploration of GPU-enabled lossless compressors
author: Stefan Rua
---

`stefan.elias.rua@cern.ch` \
<!--`stefan.rua@aalto.fi` \-->
`stefan.rua@iki.fi`


We present the results of a study on the use of GPUs for data compression, using collision data collected by the CMS experiment as a case study.

<!--
![](results/combined-pp-nolegend.png){ width=80% } \

* = GPU \
** = NX \
-->

# Background

The Compact Muon Solenoid (CMS) is a detector and an experiment at CERN. It gathers data on collisions taking place in the Large Hadron Collider (LHC). Not all of the data contains interesting events, and it goes through multiple levels of triggers where most of it is discarded. The last trigger is the High Level Trigger (HLT), from which the data is sent to datacenters away from the detector. In order to speed up the network transfers between the HLT and datacenters, the data is compressed.


# Motivation

Currently the data is compressed using CPUs which are used for other workloads as well. The machines at the HLT are equipped with GPUs, so it would be good to reduce CPU time taken by the compression workload by transferring it onto the GPUs. <!--GPUs can also be very fast.-->


<!--
# What I did

- Looked for GPU compressor implementations
- Added them to a benchmarking program
- Compared them to CPU compressors
-->


# Benchmarking

We implemented the compressors into a benchmarking program called `lzbench`. When possible, compressors are compiled with the same compiler options to achieve the fairest possible comparison. `lzbench` runs the compression in memory, meaning that disk reads and writes are excluded.

The benchmarks were run on two machines, one that resembles the machines in the HLT and a POWER9 machine. The HLT doesn't have POWER9 machines, but we wanted to investigate `libnxz`, a zlib-compatible library that makes use of the NX GZIP hardware accelerator present on the POWER9 chip.


## Compressors

<!--
| Name | Description |
|:---|:---|
| `bsc`[^bsc] | **B**lock-**s**orting **c**ompressor by Ilya Grebnov. |
| `dietgpu`[^dietgpu] | Asymmetric numeral systems (ANS)[^ans] implementation by Facebook. |
| `libxz`[^libnxz]^,^[^libnxz_git] | IBM's POWER9 processors have a hardware accelerator, NX, for `gzip`. `libnxz` is the library for compressing on it. |
| `nvcomp`[^nvcomp]^,^[^nvcomp_git] | Compression library by Nvidia, unfortunately made proprietary in version 2.3. |
-->

Following is a list of the compressors we benchmarked. Links to their source code be found in the "Links" section.

- `bsc` \
Block-sorting compressor by Ilya Grebnov. \
- `dietgpu` \
Asymmetric numeral systems (ANS) implementation by Facebook. \
- `libxz` \
IBM's POWER9 processors have a hardware accelerator for `gzip` called NX. `libnxz` is the library for compressing on it. \
- `nvcomp` \
Compression library by Nvidia, unfortunately made proprietary in version 2.3. We tested the earlier open source version which was already in `lzbench`.

<!--
- `bsc`[^bsc] \
**B**lock-**s**orting **c**ompressor by Ilya Grebnov. \
- `dietgpu`[^dietgpu] \
Asymmetric numeral systems (ANS)[^ans] implementation by Facebook. \
- `libxz`[^libnxz]^,^[^libnxz_git] \
IBM's POWER9 processors have a hardware accelerator, NX, for `gzip`. `libnxz` is the library for compressing on it. \
- `nvcomp`[^nvcomp]^,^[^nvcomp_git] \
Compression library by Nvidia, unfortunately made proprietary in version 2.3.


[^bsc]: <https://github.com/IlyaGrebnov/libbsc>
[^ans]: <https://arxiv.org/pdf/1311.2540.pdf>
[^dietgpu]: <https://github.com/facebookresearch/dietgpu>
[^libnxz]: <https://dl.acm.org/doi/pdf/10.1109/ISCA45697.2020.00012>
[^libnxz_git]: <https://github.com/libnxz/power-gzip>
[^nvcomp]: <https://developer.nvidia.com/nvcomp>
[^nvcomp_git]: <https://github.com/NVIDIA/nvcomp>
-->


## Data

Two types of collisions take place at the LHC: proton-proton and heavy ion collisions. We ran the benchmarks on both types of data.

### Proton-proton events

<!--
- HadronsTaus stream from 2022
- pileup $\approx$ 50
-->
- 100 files
- 170 MB
- 1 event per file
- 1.4 MB to 2.1 MB each

### Heavy ion events

<!--
- from 2018
-->
- 100 files
- 131 MB
- 1 event per file
- 644 KB to 5.5 MB each

<!--
## Timing

- Wall time
- Disk $\rightarrow$ RAM **excluded**
- RAM $\rightarrow$ GPU memory **included**
- Fastest from 5 repeats
-->

## Hardware

### HLT-like machine

- AMD EPYC 75F3
    - 32 cores
    - max. 4 GHz
    - 256 MB L3 cache
- Nvidia Tesla T4
    - 2560 CUDA cores
    - 16 GB GDDR6
    - 8.1 TFLOPS

### POWER9 machine

- 8335-GTH / IBM Power System AC922
- IBM POWER9
    - 32 cores
    - max. 4 GHz
    - 320 MB L3 cache
- 4 x Nvidia Tesla V100
    - 5120 CUDA cores
    - 32 GB HBM2
    - 15.7 TFLOPS


# Results

## Proton-proton events

![](results/combined-pp.png){ width=80% } \

\* = GPU \
** = NX \
no star = CPU


## Heavy ion events

![](results/combined-hi.png){ width=80% } \

\* = GPU \
** = NX \
no star = CPU

<!--
## First simple tests

Note: these were simply run from the command line and timed using the `time` command, so copying from disk to RAM and back is included.

![](results/first.png){ width=80% }
-->


# Conclusion

Using the CPU compressor `zstd` is a reasonable choice with our current hardware and the current state of GPU compressors. `dietgpu` is promising, and may see significant improvements in the future, as it is in a very early stage in development. `dietgpu` uses a compression algorithm called Asymmetric Numeral Systems (ANS)[^ans_paper], which is an important part of `zstd` as well. This looks promising for a future GPU implementation of `zstd`.

[^ans_paper]: <https://arxiv.org/pdf/1311.2540.pdf>

# Links

## Compressors

| Name | Device | Code |
|:-----|:-------|:-------|
| `bsc` | GPU | <https://github.com/IlyaGrebnov/libbsc> |
| `dietgpu` | GPU | <https://github.com/facebookresearch/dietgpu> |
| `libnxz` | IBM NX | <https://github.com/libnxz/power-gzip> |
| `lz4` | CPU | <https://github.com/lz4/lz4> |
| `lzma` | CPU | <https://www.7-zip.org/> |
| `nvcomp_lz4` | GPU | <https://github.com/NVIDIA/nvcomp> |
| `zlib` | CPU | <http://zlib.net/> |
| `zstd` | CPU | <https://github.com/facebook/zstd> |

<!--
| Name | Device | Code |
|:-----|:-------|:-------|
| `bsc` | GPU | <https://github.com/IlyaGrebnov/libbsc> |
| `culzss` | GPU | <https://github.com/adnanozsoy/CUDA_Compression> |
| `dietgpu` | GPU | <https://github.com/facebookresearch/dietgpu> |
| `hcmc` | GPU | <https://github.com/smadhiv/HuffmanCoding_MPI_CUDA> |
| `libnxz` | IBM NX | <https://github.com/libnxz/power-gzip> |
| `lz4` | CPU | <https://github.com/lz4/lz4> |
| `lzma` | CPU | <https://www.7-zip.org/> |
| `nvcomp_lz4` | GPU | <https://github.com/NVIDIA/nvcomp> |
| `xz` | CPU | <https://tukaani.org/xz/> |
| `zlib` | CPU | <http://zlib.net/> |
| `zstd` | CPU | <https://github.com/facebook/zstd> |
-->

## Benchmarking and plotting

- `lzbench`, the benchmarking program: <https://github.com/inikep/lzbench> \
- our fork of `lzbench`: <https://github.com/stefanrua/lzbench> \
- `gpucomp`, the code for the plots and a report: <https://github.com/stefanrua/gpucomp>
