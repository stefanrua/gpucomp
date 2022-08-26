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

The Lempel-Ziv[^lz_wiki]^,^[^lz_paper] (LZ) family of compression algorithms replace patterns with references to previous occurrences.

[^lz_wiki]: <https://en.wikipedia.org/wiki/Lempel-Ziv-Welch>
[^lz_paper]: <https://courses.cs.duke.edu/spring03/cps296.5/papers/ziv_lempel_1978_variable-rate.pdf>

## Asymmetric numeral systems

Asymmetric numeral systems[^ans_wiki]^,^[^ans_paper] (ANS) encodes the data into a natural number based on the frequency of different symbols.

[^ans_wiki]: <https://en.wikipedia.org/wiki/Asymmetric_numeral_systems>
[^ans_paper]: <https://arxiv.org/pdf/1311.2540.pdf>
