"""cosmian_lib_sgx.import_hook module."""

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location
from importlib.machinery import ModuleSpec
import os.path
import sys
from types import ModuleType
from typing import Dict, List, Sequence, Optional, Union, cast

from cosmian_lib_sgx.crypto_lib import enclave_decrypt
from cosmian_lib_sgx.error import SecurityError, CryptoError
from cosmian_lib_sgx.key_info import KeyInfo
from cosmian_lib_sgx.side import Side


class CipheredMetaFinder(MetaPathFinder):
    """CipheredMetaFinder class."""

    def __init__(self, key: bytes) -> None:
        """Init constructor of CipheredMetaFinder."""
        self.key: bytes = key

    # pylint: disable=unused-argument
    def find_spec(self,
                  fullname: str,
                  path: Optional[Sequence[Union[bytes, str]]],
                  target:  Optional[ModuleType] = None) -> Optional[ModuleSpec]:
        """Find the spec for a module."""
        path = cast(Optional[Sequence[str]], path)

        if not path:
            cwd = os.getcwd()
            if cwd not in sys.path:
                sys.path.append(os.getcwd())
            path = sys.path

        if "." in fullname:
            *_, name = fullname.split(".")
        else:
            name = fullname

        for entry in path:
            if os.path.isdir(os.path.join(entry, name)):
                # this module has child modules
                _filename = os.path.join(entry, name, "__init__.py.enc")
                filename = os.path.join(entry, name, "__init__.py")
                submodule_locations = [os.path.join(entry, name)]
            else:
                _filename = os.path.join(entry, name + ".py.enc")
                filename = os.path.join(entry, name + ".py")
                submodule_locations = None

            if os.path.exists(_filename):
                # print("found encrypted module: ", _filename)

                # handle this encrypted file with the Cosmian loader
                return spec_from_file_location(
                    fullname,
                    filename,
                    loader=CipheredLoader(
                        _filename,
                        self.key
                    ),
                    submodule_search_locations=submodule_locations
                )

            if os.path.exists(filename):
                # not us, use the standard loader
                return None

        return None  # we don't know how to import this


class CipheredLoader(Loader):
    """CipheredLoader class."""

    def __init__(self,
                 filename: str,
                 key: bytes) -> None:
        """Init constructor of CipheredLoader."""
        self.filename: str = filename
        self.key: bytes = key

    def create_module(self, spec):
        """Create the module object from the given specification."""
        return None  # use default module creation semantics

    def exec_module(self, module):
        """Initialize the given module object."""
        with open(self.filename, 'rb') as f:
            ciphered_module = f.read()
            try:
                plain_module = enclave_decrypt(
                    encrypted_data=ciphered_module,
                    sealed_key=self.key
                ).decode("utf-8")
            except CryptoError as exc:
                raise CryptoError(
                    f"Failed to decrypt python file: {self.filename}"
                ) from exc
            # pylint: disable=exec-used
            exec(plain_module, vars(module))

    def module_repr(self, module):
        """Return a module's repr.

        Used by the module type when the method does not raise
        NotImplementedError.

        This method is deprecated.

        """
        # The exception will cause ModuleType.__repr__ to ignore this method.
        raise NotImplementedError


def import_set_key(keys: Dict[Side, List[KeyInfo]]) -> None:
    """Configure import hook with CodeProvider symmetric key."""
    if Side.CodeProvider not in keys:
        raise SecurityError("Key not found for Code Provider!")

    if len(keys[Side.CodeProvider]) != 1:
        raise SecurityError("Multiple Code Provider key found!")

    key_info, *_ = keys[Side.CodeProvider]

    # insert the finder into the import machinery
    sys.meta_path.insert(0, CipheredMetaFinder(key_info.enc_symkey))
