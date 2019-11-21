#!/bin/bash
ENV=project
echo "Installing/updating conda environment and dependencies"
conda env create -f environment.yml || conda env update -f environment.yml --prune
echo "creating .env for autoenv, follow README.md for its installation"
rm .env
echo "conda activate $ENV > /dev/null 2>&1" >> .env

conda init bash
conda activate $ENV
conda clean --all -y
echo "Installation completed !!!"
