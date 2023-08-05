"""cosmian_lib_sgx.writer module."""

from io import BytesIO
from pathlib import Path
from typing import List, Dict, Optional, Union

from cosmian_lib_sgx.error import UserError
from cosmian_lib_sgx.side import Side
from cosmian_lib_sgx.key_info import KeyInfo
from cosmian_lib_sgx.crypto_lib import enclave_encrypt


class OutputData:
    """OutputData class for Result Consumers output.

    Parameters
    ----------
    root_path : Path
        The root path for output data.
    keys : Dict[Side, List[KeyInfo]]
        Participants keys.
    debug : bool
        Whether you want to use debug mode or not.

    Attributes
    ----------
    debug : bool
        Whether you want to use debug mode or not.
    root_path : Path
        The root path of the program.
    output_path : Path
        The output path for RCs data.
    keys : Dict[Side, List[KeyInfo]]
        Participants keys.

    """

    def __init__(self,
                 root_path: Path,
                 keys: Dict[Side, List[KeyInfo]],
                 debug: bool = False) -> None:
        """Init constructor of OutputData."""
        self.debug: bool = debug
        self.root_path: Path = root_path
        self.output_path: Path = self.root_path / "result"
        if not self.debug:
            assert Side.ResultConsumer in keys, "Need at least 1 RC key"
        self.keys: List[KeyInfo] = [] if self.debug else keys[Side.ResultConsumer]

    def write(self, data: Union[bytes, BytesIO], n: Optional[int] = None):
        """Write data for all Result Consumers or optionally a specific one `n`."""
        if n is not None and not 0 < n < len(self.keys):
            raise UserError(f"bad Result Consumer index '{n}'")

        b: bytes = data.read() if isinstance(data, BytesIO) else data

        if self.debug:
            self.output_path.mkdir(parents=True, exist_ok=True)
            (self.output_path / "result.bin").write_bytes(b)
        else:
            for i, key_info in enumerate(self.keys):
                temp_path: Path = self.output_path / key_info.fingerprint
                temp_path.mkdir(parents=True, exist_ok=True)
                if n is None or n == i:
                    (temp_path / "result.bin.enc").write_bytes(
                        enclave_encrypt(data=b,
                                        sealed_key=key_info.enc_symkey)
                    )
