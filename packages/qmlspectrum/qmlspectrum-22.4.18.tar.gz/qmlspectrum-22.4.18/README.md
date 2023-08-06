# qmlspectrum ![:EXPERIMENTAL](https://img.shields.io/badge/EXPERIMENTAL-yellow.svg)![:VERSON](https://img.shields.io/badge/VERSION-black.svg)![:UNDER](https://img.shields.io/badge/UNDER-yellow.svg)![:DEVELOPMENT](https://img.shields.io/badge/DEVELOPMENT-black.svg)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python3](https://img.shields.io/badge/Language-Python3-blue.svg)](https://www.python.org/download/releases/3.0/)
![Domain: Chemistry](https://img.shields.io/badge/Domain-Chemistry-green.svg)

`qmlspectrum` is a small test-suite that uses [qml](https://www.qmlcode.org/) package for modeling spectra as continuous functions. In this repository, we also distribute suitable datasets suitable for spectral modeling. Example input scripts collected in `example_scripts` show how to use the `qmlspectrum` test-suite.

## Status

We are developing new content through collaborative efforts which will soon be collected here. 

## Installation

`qmlspectrum` can be installed using the Python package manager `pip3`

```
pip3 install qmlspectrum --user
```

## Re-installation

You can check the recent subversion number at [https://pypi.org/project/qmlspectrum/#description](https://pypi.org/project/qmlspectrum/#description) and compare your version using

```
pip3 show qmlspectrum 
```

To update your version, you can uninstall and re-install 

```
pip3 uninstall qmlspectrum 
pip3 install qmlspectrum --user
```

## Dependencies

* `matplotlib`, `pandas`, `scipy`, `numpy`, and `qml` 
* All of these can be installed using the Python package manager `pip/pip3`

## References

If you are using the program and the bigQM7ω dataset distributed here, please consider citing the following references.

#### 1. bigQM7ω dataset and full-spectrum modeling
[_Resolution-vs.-Accuracy Dilemma in Machine Learning Modeling of Electronic Excitation Spectra_](https://arxiv.org/abs/2110.11798)                
Prakriti Kayastha, Sabyasachi Chakraborty, Raghunathan Ramakrishnan (2022)     
```
@article{kayastha2022resolution,
  title={Resolution-vs.-Accuracy Dilemma in Machine Learning Modeling of Electronic Excitation Spectra},
  author={Kayastha, Prakriti and Chakraborty, Sabyasachi and Ramakrishnan, Raghunathan},
  journal={arXiv preprint arXiv:2110.11798},
  url={https://doi.org/10.48550/arXiv.2110.11798},
  year={2022}
}
```

#### 2. QML, A Python Toolkit for Quantum Machine Learning
[_AS Christensen, FA Faber, B Huang, LA Bratholm, A Tkatchenko, KR Muller, OA von Lilienfeld (2017) "QML: A Python Toolkit for Quantum Machine Learning, https://github.com/qmlcode/qml"_](https://github.com/qmlcode/qml)  
```
@misc{christensenqml,
  title={QML: A Python Toolkit for Quantum Machine Learning, 2019},
  author={Christensen, Anders S and Bratholm, Lars A and Amabilino, Silvia and Kromann, Jimmy C 
  and Faber, Felix A and Huang, Bing and Tkatchenko, A and von Lilienfeld, OA}
  url={https://www.qmlcode.org/}
}
```

## Development

This test-suite is developed by Raghunathan Ramakrishnan and maintained at [https://github.com/raghurama123/qmlspectrum/](https://github.com/raghurama123/qmlspectrum/) and [https://pypi.org/project/qmlspectrum/](https://pypi.org/project/qmlspectrum/)   

## Contributions from

* Arpan Choudhury 
* Prakriti Kayastha    
* Sabyasachi Chakraborty         
* Debashree Ghosh   


