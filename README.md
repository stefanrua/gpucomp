# gpucomp

An exploration of GPU-enabled lossless compressors, a report and related scripts.

![](results/combined-pp.png)

`lzbench` was run with these options:

```bash
src/lzbench/lzbench -i5,5 -j -o4 -ezlib/zstd/lzma/lz4/xz/bsc/bsc_cuda/dietgpu/nvcomp_lz4/libnxz benchdata/pp/*.dat
```
