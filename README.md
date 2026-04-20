# NCCS Software Provisioning (NSP)

## About

The National Center for Computational Sciences (NCCS) at Oak Ridge National Laboratory has developed NCCS Software
Provisioning (NSP), a unified framework for deploying software stacks and monitoring their usage on HPC systems.
NSP leverages Ansible to automate the deployment of Spack environments using templates and to manage installation
procedures for non-Spack software through custom roles. Additionally, NSP enhances vendor-managed LMOD installations
using hooks, enabling dynamic and responsive software layouts that adapt seamlessly to changes in the programming
environment.

## Cite

### DOI
`https://doi.org/10.1145/3757348.3757362`

### ACM
``` text
Asa Rentschler, Nicholas Hagerty, Elijah Maccarthy, and Edwin Fernando Posada Correa. 2025. Deploying and Tracking Software with NCCS Software Provisioning. In Proceedings of the Cray User Group (CUG '25). Association for Computing Machinery, New York, NY, USA, 127–134. https://doi.org/10.1145/3757348.3757362
```

### BibTex
``` latex
@inproceedings{10.1145/3757348.3757362,
author = {Rentschler, Asa and Hagerty, Nicholas and Maccarthy, Elijah and Posada Correa, Edwin Fernando},
title = {Deploying and Tracking Software with NCCS Software Provisioning},
year = {2025},
isbn = {9798400713279},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3757348.3757362},
doi = {10.1145/3757348.3757362},
abstract = {The National Center for Computational Sciences (NCCS) at Oak Ridge National Laboratory has a long history of deploying ground-breaking leadership-class supercomputers for the U.S. Department of Energy. The latest in this line of supercomputers is Frontier, the first supercomputer to break the exascale barrier (1018 floating-point operations per second) on the TOP500 list. Frontier serves a wide array of scientific domains, from traditional simulation-based workloads to newer AI and Machine Learning workloads. To best serve the NCCS user community, NCCS uses Spack to deploy a comprehensive software stack of scientific software packages, providing straightforward access to these packages through Lmod Environment Modules. Maintaining a large software stack while also including multiple new compiler releases each year is a very time-consuming task. Additionally, it is not straightforward to provide a software stack alongside existing vendor-provided software such as the HPE/Cray Programming Environment (CPE), and existing CPE, Spack, and Lmod integration does not allow for multiple versions of GPU libraries such as AMD’s ROCm to be used. To address these challenges and shortcomings, NCCS has developed the NCCS Software Provisioning tool (NSP)1, a tool for deploying and monitoring software stacks on HPC systems. NSP allows NCCS to quickly and effectively provision software stacks from the ground up using template-driven recipes and configuration files. NSP is successfully deployed on Frontier and several other NCCS clusters, enabling the NCCS software team to quickly deploy software stacks for newly-released compilers, expand current software offerings, better support GPU-based software, and monitor Lmod module usage to identify unused software packages that can be removed from the software stack. In this work, we discuss the shortcomings of the previous CPE, Spack, and Lmod usage at NCCS, provide further details on the implementation and structure of NSP, then discuss the benefits that NSP provides.},
booktitle = {Proceedings of the Cray User Group},
pages = {127–134},
numpages = {8},
keywords = {Software deployments, High-Performance Computing, Spack, Configuration as code},
location = {
},
series = {CUG '25}
}
```
