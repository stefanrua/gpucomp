---
title: GPU compressor exploration
author: Stefan Rua
colortheme: dove
---


# Why?

- Data from the HLT is compressed
- This is done on CPUs
- GPUs can be very fast


# What I've been doing

- Looking for GPU compressor implementations
- Adding them to a benchmarking program
- Comparing them to CPU compressors


# Results - PP events

![](../results/combined-pp.png) \

\scriptsize{* = GPU} \
\scriptsize{** = NX}


# Results - HI events

![](../results/combined-hi.png) \

\scriptsize{* = GPU} \
\scriptsize{** = NX}


# Results - details

Data:

- 100 PP events
- 100 HI events

Timing:

- Wall time
- Disk $\rightarrow$ RAM **excluded**
- RAM $\rightarrow$ GPU memory **included**
- Fastest from 5 repeats


# Results - details

POWER9 machine:

- IBM POWER9
- Nvidia Tesla V100

HLT-like machine:

- AMD EPYC 75F3
- Nvidia Tesla T4


# That's it

**Contact info**

Stefan Rua

`stefan.elias.rua@cern.ch` \
`stefan.rua@iki.fi`


# Extra - less promising ones

![](../results/first.png) \


# Extra - problems

Nvidia

![](nvcomp-proprietary.png) \
\

Researchers

![](culzss-bit-mail.png) \

