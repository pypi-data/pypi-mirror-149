import json
import os

from web3.auto import w3
import certify_issuer.utils as Utils
from certify_issuer.certify_sc_utils import add_certification, get_credit, revoke_certification, get_certificate
from certify_issuer.pdf import add_metadata

DEFAULT_CERTIFY_ADDRESS = ""
DEFAULT_NODE_URL = ""
VERSION = "v1.0"


def issue(src_path: str,
          dest_path: str,
          cert_num: str,
          address: str,
          issuer_name: str,
          expire_date: int = 0,
          description: str = "",
          private_key: str = "",
          key_store="",
          passphrase: str = "",
          certify_address=DEFAULT_CERTIFY_ADDRESS,
          node_url=DEFAULT_NODE_URL,
          is_testnet=False):
    # validation
    if not os.path.exists(src_path) or not os.path.isfile(src_path):
        raise ValueError('Source path should be valid')

    if os.path.isdir(dest_path):
        raise ValueError('Destination path already exists')

    # insert meta data
    Utils.insert_metadata_to_certificate(src_path, dest_path, cert_num, issuer_address=w3.toChecksumAddress(address),
                                         issuer_name=issuer_name)
    # calc hash
    hash_str = Utils.calc_hash(dest_path)

    (tx, proof), error = issue_by_hash(hash_str, cert_num, address, expire_date, description, private_key, key_store,
                                       passphrase, certify_address, node_url, is_testnet)
    add_metadata(dest_path, dest_path, chainpoint_proof='/CHAINPOINTSTART' + proof + '/CHAINPOINTEND')

    return tx, error


def issue_by_hash(hash_str, cert_num, address: str,
                  expire_date: int = 0,
                  description: str = "",
                  private_key: str = "",
                  key_store="",
                  passphrase: str = "",
                  certify_address=DEFAULT_CERTIFY_ADDRESS,
                  node_url=DEFAULT_NODE_URL,
                  is_testnet=False):
    if not w3.isAddress(address):
        raise ValueError("Address is invalid")

    if not w3.isAddress(certify_address):
        raise ValueError("Certify address is invalid")

    # issuer address
    address = w3.toChecksumAddress(address)
    # address of smart contract
    certify_address = w3.toChecksumAddress(certify_address)

    pk = private_key
    if private_key == "":
        if os.path.isdir(key_store):
            path = os.path.join(key_store, address + '.json')
            pk = Utils.decrypt_account(passphrase, path)
        elif os.path.isfile(key_store):
            pk = Utils.decrypt_account(passphrase, key_store)
        else:
            raise ValueError("Private key or key store file is required")

    # check credit
    if check_credit(address, certify_address, node_url) == 0:
        raise ValueError("Not enough credit")

    cp = Utils.prepare_chainpoint_tree([hash_str])

    if check_revoked_hash(cp.get_merkle_root(), certify_address, node_url):
        raise ValueError("Certificate revoked")

    if check_hash_exists(cp.get_merkle_root(), certify_address, node_url):
        raise ValueError("Certificate already registered")

    tx, error = add_certification(cp.get_merkle_root(), cert_num, expire_date, version=VERSION, desc=description,
                                  node_url=node_url, address=address, contract_address=certify_address, pk=pk)
    if error is not None:
        raise RuntimeError(error)

    # insert proof
    proof = json.dumps(cp.get_receipt(0, tx, is_testnet))

    return (tx, proof), None


def revoke(src_path: str,
           address: str,
           revoker_name: str,
           private_key: str = "",
           key_store="",
           passphrase: str = "",
           certify_address=DEFAULT_CERTIFY_ADDRESS,
           node_url=DEFAULT_NODE_URL):
    # validation
    if not os.path.exists(src_path) or not os.path.isfile(src_path):
        raise ValueError('Source path should be valid')

    # calc hash
    temp_path = Utils.create_temporary_copy(src_path)
    add_metadata(temp_path, temp_path, chainpoint_proof='')
    hash_str = Utils.calc_hash(temp_path)
    return revoke_by_hash(hash_str, address, revoker_name, private_key, key_store, passphrase, certify_address,
                          node_url)


def revoke_by_hash(hash_str: str,
                   address: str,
                   revoker_name: str,
                   private_key: str = "",
                   key_store="",
                   passphrase: str = "",
                   certify_address=DEFAULT_CERTIFY_ADDRESS,
                   node_url=DEFAULT_NODE_URL):
    address = w3.toChecksumAddress(address)
    certify_address = w3.toChecksumAddress(certify_address)

    pk = private_key
    if private_key == "":
        if os.path.isdir(key_store):
            path = os.path.join(key_store, address + '.json')
            pk = Utils.decrypt_account(passphrase, path)
        elif os.path.isfile(key_store):
            pk = Utils.decrypt_account(passphrase, key_store)
        else:
            raise ValueError("Private key or key store file is required")

    # check credit
    if check_credit(address, certify_address, node_url) == 0:
        raise ValueError("Not enough credit")

    cp = Utils.prepare_chainpoint_tree([hash_str])
    if check_revoked_hash(cp.get_merkle_root(), certify_address, node_url):
        raise ValueError("Certificate already revoked")

    if check_hash_exists(cp.get_merkle_root(), certify_address, node_url) is False:
        raise ValueError("Certificate not found")

    tx, error = revoke_certification(cp.get_merkle_root(), revoker_name, node_url=node_url,
                                     address=address, contract_address=certify_address, pk=pk)

    if error is not None:
        print(error)
        raise RuntimeError(error)

    return tx, None


def check_credit(address: str,
                 certify_address=DEFAULT_CERTIFY_ADDRESS,
                 node_url=DEFAULT_NODE_URL):
    address = w3.toChecksumAddress(address)
    certify_address = w3.toChecksumAddress(certify_address)
    return get_credit(address, certify_address, node_url)


def check_revoked_hash(hash_str,
                       certify_address=DEFAULT_CERTIFY_ADDRESS,
                       node_url=DEFAULT_NODE_URL):
    certify_address = w3.toChecksumAddress(certify_address)
    t = get_certificate(hash_str, certify_address, node_url)
    return t[6]


def check_hash_exists(hash_str,
                      certify_address=DEFAULT_CERTIFY_ADDRESS,
                      node_url=DEFAULT_NODE_URL):
    certify_address = w3.toChecksumAddress(certify_address)
    t = get_certificate(hash_str, certify_address, node_url)
    if t[0] > 0:
        return True
    return False


def generate_account(key_store_dir_path: str, verbose=False):
    acc = w3.eth.account.create()
    passphrase = Utils.random_passphrase(20)
    keystore = acc.encrypt(passphrase)
    with open(os.path.join(key_store_dir_path, acc.address + '.json'), 'w') as outfile:
        json.dump(keystore, outfile)

    if verbose:
        print("New address generated: ", acc.address)

    return acc.address, passphrase
