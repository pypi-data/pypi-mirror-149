# sailfish
 ![ubuntu-latest](https://github.com/justinhchae/sailfish/actions/workflows/ubuntu-latest.yml/badge.svg)
 ![ubuntu-1804](https://github.com/justinhchae/sailfish/actions/workflows/ubuntu-1804.yml/badge.svg)
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
 [![Generic badge](https://img.shields.io/badge/Python-3.7|3.8|3.9-<COLOR>.svg)](https://shields.io/)
 [![Generic badge](https://img.shields.io/badge/OS-Mac|Linux|Windows-blue.svg)](https://shields.io/)
 [![Generic badge](https://img.shields.io/badge/Build-Beta-red.svg)](https://shields.io/)

 Sailfish provides data engineering and management utilities to apply common optimizations to Pandas Dataframes.

 Sailfish primarily works by identifying the optimal data type for each column. For example, for integer-only columns, 
 it may be possible to have a datatype of int32 versus int64 which can save roughly have the memory. On big datasets, these 
 types of optmizations can provide tremendous savings.
 
 This project replaces the [pd-helper project](https://github.com/justinhchae/pd-helper) as of [pd-helper 1.0.1](https://pypi.org/project/pd-helper/); sailfish is basically pd-helper 2.0.0.

## Install
 ```bash
 pip install sailfish
 ```

