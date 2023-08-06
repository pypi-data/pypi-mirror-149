import hashlib
import json
import os
import random
import shutil
import string
import tempfile

import certify_issuer.pdf as pdf_utils
from certify_issuer.chainpoint import ChainPointV2


def random_passphrase(length=8):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation
    all = lower + upper + num + symbols
    temp = random.sample(all, length)
    return "".join(temp)


def decrypt_account(passphrase: str, path: str):
    from web3.auto import w3
    with open(path) as keyfile:
        encrypted_key = keyfile.read()
        private_key = w3.eth.account.decrypt(encrypted_key, passphrase)
        return w3.toHex(private_key)


def insert_metadata_to_certificate(src_path, dest_path, cert_num, issuer_name, issuer_address):
    issuer = {
        "name": issuer_name,
        "identity": {
            "address": issuer_address
        }
    }
    version = 1
    metadata = {'name': issuer_name, 'certNum': cert_num}
    pdf_utils.add_metadata(src_path, dest_path, version=version,
                           issuer=json.dumps(issuer), metadata=json.dumps(metadata),
                           chainpoint_proof='')


def calc_hash(file):
    with open(file, 'rb') as cert:
        hash_str = hashlib.sha256(cert.read()).hexdigest()
    return hash_str


def create_temporary_copy(path):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, 'temp_file_name')
    shutil.copy2(path, temp_path)
    return temp_path


def prepare_chainpoint_tree(hashes):
    cp = ChainPointV2()
    cp.add_leaf(hashes)
    cp.make_tree()
    return cp


if __name__ == "__main__":
    print(prepare_chainpoint_tree(['1', '2', '3', '4', '5']).get_merkle_root())
