---
documentclass: scrartcl
geometry: margin=2cm
classoption: twocolumn
papersize: a3
fontsize: 12
title: Exploration of GPU-enabled lossless compressors
author: Stefan Rua, `stefan.elias.rua@cern.ch`
---
\thispagestyle{empty}


# Why?

- Data from the HLT is compressed
- This is done on CPUs
- GPUs can be very fast


# What I did

- Looked for GPU compressor implementations
- Added them to a benchmarking program
- Compared them to CPU compressors


# Benchmarking

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

\newpage

![Crude first tests.](results/first.png){ width=50% }

![Compressor performance on proton-proton events.](results/combined-pp.png){ width=50% }

![Compressor performance on heavy ion events.](results/combined-hi.png){ width=50% }
