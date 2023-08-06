"""cosmian_lib_sgx.enclave module."""

from contextlib import ContextDecorator
from io import BytesIO
from pathlib import Path
from typing import Iterator, Optional, Dict, List, Union

from cosmian_lib_sgx.args import parse_args
from cosmian_lib_sgx.crypto_lib import is_running_in_enclave
from cosmian_lib_sgx.import_hook import import_set_key
from cosmian_lib_sgx.key_info import KeyInfo
from cosmian_lib_sgx.reader import InputData
from cosmian_lib_sgx.side import Side
from cosmian_lib_sgx.writer import OutputData


class Enclave(ContextDecorator):
    """Enclave class to be used as context manager.

    Parameters
    ---------
    debug : bool
        Whether you want to use debug mode or not.

    Attributes
    ----------
    debug : bool
        Whether you want to debug or not.
    keys : Dict[Side, List[KeyInfo]]
        Sealed symmetric keys of all participants (CodeProvider,
        DataProvider and ResultConsumer).
    root_path : Path
        Current working directory path.
    input_data : InputData
        Reader from Data Providers.
    output_data : OutputData
        Writer for Result Consumers.

    """

    def __init__(self, debug: bool = False):
        """Init constructor of Enclave."""
        self.debug: bool = debug
        self.keys: Dict[Side, List[KeyInfo]] = {} if self.debug else parse_args()
        self.root_path: Path = Path.cwd().absolute()
        self.input_data: InputData = InputData(
            root_path=self.root_path,
            keys=self.keys,
            debug=self.debug
        )
        self.output_data: OutputData = OutputData(
            root_path=self.root_path,
            keys=self.keys,
            debug=self.debug
        )

    def __enter__(self):
        """Enter the context manager.

        Check if it's running inside Intel SGX enclave and
        decrypt ciphered modules.

        """
        if not self.debug and is_running_in_enclave():
            import_set_key(self.keys)

        return self

    def __exit__(self, *exc):
        """Exit the context manager."""
        return False

    def read(self, n: Optional[int] = None) -> Iterator[BytesIO]:
        """Read a piece of data from Data Providers.

        Parameters
        ----------
        n : Optional[int]
            Read only n-th DP's data if it's an integer.
            WARNING: it starts from 0 so DP₁ -> DP₀, DP₂ -> DP₁ and so on...

        """
        return self.input_data.read(n)

    def write(self, data: Union[bytes, BytesIO], n: Optional[int] = None):
        """Write an encrypted piece of data for Result Consumers.

        Parameters
        ----------
        data : Union[bytes, BytesIO]
            Data to write for Result Consumer (unencrypted).
        n : Optional[int]
            Write for the n-th RC if it's an integer.
            WARNING: it starts from 0 so RC₁ -> RC₀, RC₂ -> RC₁ and so on...

        """
        return self.output_data.write(data, n)
