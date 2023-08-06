"""cosmian_lib_sgx.args module."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Dict, List

from cosmian_lib_sgx.crypto_lib import enclave_x25519_keypair, enclave_get_quote
from cosmian_lib_sgx.key_info import KeyInfo
from cosmian_lib_sgx.side import Side


def parse_args() -> Dict[Side, List[KeyInfo]]:
    """Argument parser for the entrypoint."""
    if int(os.environ.get("RUN", 1)) == 0:  # env RUN=0
        enclave_pubkey, _ = enclave_x25519_keypair()  # type: bytes, bytes
        # print enclave's public key
        print(enclave_pubkey.hex())
        # dump enclave's quote
        print(json.dumps({
            "isvEnclaveQuote": enclave_get_quote(
                hashlib.sha256(enclave_pubkey).digest()
            )
        }))
        # exit
        sys.exit(0)

    # env RUN=1
    parser = argparse.ArgumentParser(
        description="CP, DPs and RCs keys for code execution"
    )
    parser.add_argument("--code_provider",
                        help="Code Provider symmetric key sealed")
    parser.add_argument("--result_consumers",
                        help="Result Consumers symmetric keys sealed",
                        nargs="+")
    parser.add_argument("--data_providers",
                        help="Data Providers symmetric keys sealed",
                        nargs="+")

    args: argparse.Namespace = parser.parse_args()

    return {
        Side.CodeProvider: ([KeyInfo.from_path(Path(args.code_provider))]
                            if args.code_provider else []),
        Side.DataProvider: [
            KeyInfo.from_path(Path(shared_key_path))
            for shared_key_path in args.data_providers
        ],
        Side.ResultConsumer: [
            KeyInfo.from_path(Path(shared_key_path))
            for shared_key_path in args.result_consumers
        ]
    }
