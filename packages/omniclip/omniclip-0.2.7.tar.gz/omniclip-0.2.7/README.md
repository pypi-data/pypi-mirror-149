# omniCLIP

[![Pypi Releases](https://img.shields.io/pypi/v/omniclip.svg)](https://pypi.python.org/pypi/omniclip)
[![Downloads](https://pepy.tech/badge/omniclip)](https://pepy.tech/project/omniclip)

omniCLIP is a Bayesian peak caller that can be applied to data from CLIP-Seq experiments to detect regulatory elements in RNAs.

_This is a fork version by Chang Y._
_Please cite the original paper: Drewe-Boss, P., Wessels, HH. & Ohler, U. omniCLIP: probabilistic identification of protein-RNA interactions from CLIP-seq data. Genome Biol 19, 183 (2018). https://doi.org/10.1186/s13059-018-1521-2_

## Overview

[Introduction](#introduction)

[Installation](#installation)

[Usage](#usage)

[Contributors](#contributors)

[License](#license)

## Introduction

omniCLIP can call peaks for CLIP-Seq data data while accounting for confounding factors such as the gene expression and it automatically learns relevant diagnostic events from the data. Furtermore, it can leverage replicate information and model technical and biological variance.

## Installation

This package is not release on pypi, you can install it by:

```bash
pip install omniclip
```

## Usage

An omniCLIP analysis is run into four different steps :

- Generating the annotation database
- Parsing the background RNA-seq files
- Parsing the CLIP files
- Running the omniCLIP algorithm

The following is an example of the commands. The commands in this example only show the **required** arguments for the analysis. The following files are necessary to run an analysis.

| File name           | Description                                                                           |
| ------------------- | ------------------------------------------------------------------------------------- |
| $GFF_file           | Genome annotation file                                                                |
| $GENOME_dir         | Directory containing FASTA files with each of the chromosomes sequence                |
| $BG_file[1,2,...]   | BAM files for the background library. The alignments need to have the MD and NM tags. |
| $CLIP_file[1,2,...] | BAM files for the CLIP library. The alignments need to have the MD and NM tags.       |

The following files will be created.

| File name | Description                                 |
| --------- | ------------------------------------------- |
| $DB_file  | SQL database of the genome annotation.      |
| $BG_dat   | H5PY file of the parsed background library. |
| $CLIP_dat | H5PY file of the parsed CLIP library.       |
| $OUT_dir  | Directory containing the final results      |

### 1. Generating the annotation database

```bash
omniCLIP generateDB \
  --gff-file $GFF_file --db-file $DB_file
```

### 2. Parsing the background RNA-seq files

```bash
omniCLIP parsingBG \
  --db-file $DB_file --genome-dir $GENOME_dir --bg-files $BG_file1 --bg-files $BG_file2 --out-file $BG_dat
```

### 3. Parsing the CLIP files

```bash
omniCLIP parsingCLIP \
  --db-file $DB_file --genome-dir $GENOME_dir --clip-files $CLIP_file1 --clip-files $CLIP_file2 --out-file $CLIP_dat
```

### 4. Running the omniCLIP algorithm

```bash
omniCLIP run_omniCLIP \
  --db-file $DB_file --bg-dat $BG_dat --clip-dat $CLIP_dat --out-dir $OUT_dir
```

### Optional arguments

For the full list of optional arguments of the different step, consult the help of the commands using :

```bash
omniCLIP parsingBG --help
```

## Contributors

## License

GNU GPL license (v3)
