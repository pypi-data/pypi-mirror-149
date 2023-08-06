# Cosmian lib SGX

## Overview

Python library for code providers using [Cosmian Secure Computation](https://cosmian.com/secure-computation/).

## Example

A simple structure of the code should look like:

```console
$ tree .
.
├── secret_mod.py
└── run.py
```

where `run.py` is called the entrypoint and is the only file which can't be encrypted.

The goal of the entrypoint is to manage the I/O of you program whereas other module can hide the Python code you want to keep secret.

Here is an example of a statistical mean code where:

- Code Provider hides the whole module `secret_mod` which is decrypted in the SGX enclave
- Data Providers send bytes of an arbitrary long integer in big-endian as data input for the Code Provider
- Result Consumers receive bytes of the statistical mean of all input datas represented as IEEE 754 binary64

```python
"""run module."""

from io import BytesIO
import struct
from typing import Iterator

from cosmian_lib_sgx import Enclave


def convert_input(datas: Iterator[BytesIO]) -> Iterator[int]:
    """Transform input data bytes to integer."""
    for data in datas:  # type: BytesIO
        yield int.from_bytes(data.read(), byteorder="big")


def main() -> int:
    """Entrypoint of your code."""
    with Enclave() as enclave:
        # import your ciphered module normally
        import secret_mod

        # convert input data bytes sent by Data Providers
        datas: Iterator[int] = convert_input(enclave.read())

        # apply function of your module on datas
        output: float = secret_mod.custom_mean(datas)

        # convert output result
        result: bytes = struct.pack("d", output)

        # write result for Result Consumers
        enclave.write(result)

    return 0


if __name__ == "__main__":
    main()
```

```python
"""secret_mod module."""

from typing import Iterator


def custom_mean(input_datas: Iterator[int]) -> float:
    """Statistical mean of input datas."""
    n: int = 0
    mean: float = 0.0

    for x in input_datas:  # type: int
        n += 1
        mean += (x - mean) / (i + 1)
    
    return mean if n > 0 else float("nan")
```
