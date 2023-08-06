# GammaLearn

<p align="left">
<img src="https://gammalearn.pages.in2p3.fr/pages/images/glearn.png" width="60px" >
<b><i>Deep Learning for Imaging Cherenkov Telescopes Data Analysis.</b></i>
</p>

GammaLearn is a collaborative project to apply deep learning to the analysis of low-level Imaging Atmospheric Cherenkov Telescopes such as CTA.
It provides a framework to easily train and apply models from a configuration file.


[![](https://img.shields.io/badge/GammaLearn-Pages-yellow)](https://purl.org/gammalearn)
[![](https://img.shields.io/badge/GammaLearn-Code-blue)](https://gitlab.in2p3.fr/gammalearn/gammalearn)
[![](https://img.shields.io/badge/GammaLearn-Documentation-orange)](https://gammalearn.pages.in2p3.fr/gammalearn)
[![](https://img.shields.io/badge/GammaLearn-Slack-green)](https://gammalearn.slack.com/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5879803.svg)](https://doi.org/10.5281/zenodo.5879803)

[![pipeline status](https://gitlab.in2p3.fr//gammalearn/gammalearn/badges/master/pipeline.svg)](https://gitlab.in2p3.fr//gammalearn/gammalearn/-/commits/master)

## Table of Contents

1. [Implementation](#implementation)
1. [Usage](#usage)
1. [Contributing](#contributing)
1. [Cite Us](#cite us)
1. [License](#license)


## Implementation


### Dependencies

- PyTorch (>= 1.7)
- Numpy
- PyTables
- Matplotlib
- scikit-image
- PyTorch Lightning (>=1.4.6)
- TensorBoard
- IndexedConv (>=1.3)
- ctapipe
- dl1-data-handler
- lstchain (~0.7)
- torch-tb-profiler

### Installation procedure

We recommend the use of [Anaconda](https://www.anaconda.com/products/individual) with Python 3.8. 

Create the environment:
```
VERSION=0.8
wget https://gitlab.in2p3.fr/gammalearn/gammalearn/-/raw/v${VERSION}/environment.yml -O glearn_${VERSION}_env.yml
conda install mamba -n base -c conda-forge
mamba env create -f glearn_${VERSION}_env.yml
conda activate glearn
```

**Note for OSX and/or no-gpu users:** please edit the environment file to remove `cudatoolkit` from the dependencies.


Install GammaLearn

- with pip (recommended for users)
```
pip install gammalearn==$VERSION
```

- or from source (for developpers):
```
git clone --depth 1 https://gitlab.in2p3.fr/gammalearn/gammalearn
cd gammalearn
pip install .
```


## Usage
First activate your conda environment

To run an experiment
```
gammalearn path_to_your_experiment_settings_file.py
```
you can find an example of setting file in https://gitlab.lapp.in2p3.fr/GammaLearn/GammaLearn/-/tree/master/examples and some sample data in https://lapp-gitlab.in2p3.fr/GammaLearn/GammaLearn/share/data

To visualise the results from your experiment, GammaLearn integrates with
[GammaBoard](https://github.com/vuillaut/ctaplot) that provides high-level metrics and plots to assess IACTs reconstruction performances

To visualise the convolution kernels of your trained network (experimental feature)
```
gexplore-net path_to_your_experiments experiment_name checkpoint_version
```


## Contributing
Contributions are very much welcome.   
Open an issue to first discuss potential changes/additions.



## Cite Us

Please cite

_Jacquemont M, Vuillaume T, Benoit A, Maurin G, Lambert P, Lamanna G, Brill A. 
GammaLearn: A Deep Learning Framework for IACT Data. In36th International Cosmic Ray Conference (ICRC2019) 2019 Jul (Vol. 36, p. 705).
[DOI: https://doi.org/10.22323/1.358.0705](https://doi.org/10.22323/1.358.0705)_

For reproducibility purposes, please also cite the exact version of GammaLearn you used by citing the corresponding DOI on Zenodo:
- Version 0.7.4: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5879804.svg)](https://doi.org/10.5281/zenodo.5879804)



## License

#### MIT License

Copyright (c), 2018, GammaLearn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


**[Back to top](#table-of-contents)**
