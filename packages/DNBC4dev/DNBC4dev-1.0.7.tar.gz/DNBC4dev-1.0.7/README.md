# DNBC4dev
An open source and flexible pipeline to analysis high-throughput DNBelab C Series single-cell RNA datasets
## Introduction
- **Propose**
  - An open source and flexible pipeline to analyze DNBelab C Series<sup>TM</sup> single-cell RNA datasets. 
- **Language**
  - Python3 and R scripts.
- **Hardware/Software requirements** 
  - x86-64 compatible processors.
  - require at least 50GB of RAM and 4 CPU. 
  - centos 7.x 64-bit operating system (Linux kernel 3.10.0, compatible with higher software and hardware configuration). 

## Installation
installation manual

### Install miniconda and creat DNBC4dev environment
- Creat DNBC4dev environment
```
cd DNBC4dev
source /miniconda3/bin/activate
conda env create -f DNBC4dev.yaml -n DNBC4dev
```
- Install R package that cannot be installed using conda
```
conda activate DNBC4dev
Rscript -e "devtools::install_github(c('chris-mcginnis-ucsf/DoubletFinder','ggjlab/scHCL','ggjlab/scMCA'),force = TRUE);"
```
