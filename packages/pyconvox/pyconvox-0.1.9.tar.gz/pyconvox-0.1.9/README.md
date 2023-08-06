# PyConvox
------------------
## Description

A Wrapper application built around convox cli application. This can be modified more to restrict/limit convox access.

------------------

## Requirements

- Python version 3 and above
- Convox cli installed and configured with the key

------------------

## Installation

```sh
#Install Pyconvox using pip package (Only supported python3 and above)
pip install pyconvox
```
------------------

## Usage
```sh
usage: pyconvox [-h] [--version] {envset,env,railsc,scale,instances,logs,releases,ps} ...

pyconvox - a wrapper for the convox application

positional arguments:
  {envset,env,railsc,scale,instances,logs,releases,ps}
                        Commands
    envset              set env var
    env                 list env vars
    railsc              run rails c
    scale               scale of a application
    instances           instances details of the rack
    logs                logs of a service
    releases            releases of a application
    ps                  processes running for application

optional arguments:
  -h, --help            show this help message and exit
  --version, -V         show program's version number and exit
```

