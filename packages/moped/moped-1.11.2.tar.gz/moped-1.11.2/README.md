[![pipeline status](https://gitlab.com/marvin.vanaalst/moped/badges/main/pipeline.svg)](https://gitlab.com/marvin.vanaalst/moped/-/commits/main)
[![coverage report](https://gitlab.com/marvin.vanaalst/moped/badges/main/coverage.svg)](https://gitlab.com/marvin.vanaalst/moped/-/commits/main)
[![Documentation Status](https://readthedocs.org/projects/moped/badge/?version=latest)](https://moped.readthedocs.io/en/latest/?badge=latest)
[![PyPi](https://img.shields.io/pypi/v/moped)](https://pypi.org/project/moped/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Downloads](https://pepy.tech/badge/moped)](https://pepy.tech/project/moped)

# moped

A metabolic object-oriented Python modelling environment.

## Installation

You can install moped using pip

`pip install moped`  

However, you will still need to install NCBI Blast if you want to use the genome / proteome reconstruction methods

If you are using conda or mamba, you can install blast from bioconda: 

`conda install -c bioconda blast==2.12.0`  
`mamba install -c bioconda blast==2.12.0`  

If you want to install BLAST yourself:
- download the latest blast version from [NCBI](ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)
- Extract the downloaded folder to a path of your liking
- Add blast to your path e.g. by adding the following line to your .bashrc
  - `export PATH="your_blast_directory/bin:$PATH"`


## Documentation

Check out our tutorial on [readthedocs](https://moped.readthedocs.io/en/latest/) 


## Contributing

All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.
If you want to contribute code to the project, please consider our [contribution guide](https://gitlab.com/marvin.vanaalst/moped/-/blob/main/CONTRIBUTING.md)

## License

moped is licensed under [GPL 3](https://gitlab.com/marvin.vanaalst/moped/-/blob/main/LICENSE)

## Issues and support

If you experience issues using the software please contact us through our [issues](https://gitlab.com/marvin.vanaalst/moped/issues) page.
