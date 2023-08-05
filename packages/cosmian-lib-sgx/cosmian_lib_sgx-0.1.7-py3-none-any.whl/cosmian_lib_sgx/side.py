"""cosmian_lib_sgx.side module."""

from enum import Enum


class Side(Enum):
    """Side enum."""

    Enclave = 1
    CodeProvider = 2
    DataProvider = 3
    ResultConsumer = 4
