# PanChIP

[![PyPI version](https://badge.fury.io/py/PanChIP.svg)](https://badge.fury.io/py/PanChIP)

**Pan-ChIP-seq Analysis of Protein Colocalization Using Peak Sets**

## Installation
```shell
pip3 install panchip
```

## Usage

### panchip <command> [options]

```shell
Commands:
    init            Initialization of the PanChIP library
    analysis        Analysis of a list peak sets
    filter          Filtering library for quality control
Run panchip <command> -h for help on a specific command.

PanChIP: Pan-ChIP-seq Analysis of Peak Sets

positional arguments:
  command     Subcommand to run

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

### panchip init [-h] library_directory

```shell

Initialization of the PanChIP library

positional arguments:
  library_directory  Directory wherein PanChIP library will be stored. > 13.6
                     GB of storage required.

optional arguments:
  -h, --help         show this help message and exit
```

### panchip analysis [-h] [-t THREADS] [-r REPEATS] library_directory input_directory output_directory

```shell

Analysis of a list peak sets

positional arguments:
  library_directory  Directory wherein PanChIP library was stored.
  input_directory    Input directory wherein peak sets in the format of .bed
                     files are located.
                     (.bed6 format with numeric scores in 5th column required)
  output_directory   Output directory wherein output files will be stored.

optional arguments:
  -h, --help         show this help message and exit
  -t THREADS         Number of threads to use. (default: 1)
  -r REPEATS         Number of repeats to perform. (default: 1)
```

### panchip filter [-h] [-t THREADS] library_directory input_file output_directory

```shell

Filtering library for quality control

positional arguments:
  library_directory  Directory wherein PanChIP library was stored.
  input_file         Path to the input .bed file.
                     (.bed6 format with numeric scores in 5th column required)
  output_directory   Output directory wherein output files will be stored.

optional arguments:
  -h, --help         show this help message and exit
  -t THREADS         Number of threads to use. (default: 1)
```
