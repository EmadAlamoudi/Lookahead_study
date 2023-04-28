#!/bin/sh

source /p/project/fitmulticell/emad/anaconda3/etc/profile.d/conda.sh
conda activate lookagead_fix
module load R
export PYTHONPATH=/p/software/juwels/stages/2020/software/GEOS/3.8.1-GCCcore-10.3.0-Python-3.8.5/lib/python3.8/site-packages:/p/software/juwels/stages/2020/software/Python/3.8.5-GCCcore-10.3.0/easybuild/python
module load Stages/2022
module load GCC/11.2.0
module load Stages/2020
module load gnuplot
module --show-hidden load SWIG/.4.0.2-Python-3.8.5

