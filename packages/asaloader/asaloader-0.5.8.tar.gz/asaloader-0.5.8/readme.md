# asaloader

A program to load your code to asa-series board.

## Quick Start

Install the package using pip

```
pip install asaloader
```

Use CLI to call asaloader and load your program.

```
asaloader prog -p COM5 -f main.hex
```

## Options

```
> asaloader --help
usage: __main__.py [-h] [--lc LC] {prog,print-devices,pd,print-ports,pp} ...

Program to ASA-series board.

positional arguments:
  {prog,print-devices,pd,print-ports,pp}
    prog                Program code to board.
    print-devices (pd)  List all available devices.
    print-ports (pp)    List all available serial ports.

optional arguments:
  -h, --help            show this help message and exit
  --lc LC               Set the language code. e.g. `zh_TW`, `en_US`
```

## Used by

This project is used by:

  - [ASA_HMI_data_agent](https://gitlab.com/MVMC-lab/hmi/ASA_HMI_Data_Agent)

## Note

This project's old name is py-asa-loader.
And the name is no longer used.
