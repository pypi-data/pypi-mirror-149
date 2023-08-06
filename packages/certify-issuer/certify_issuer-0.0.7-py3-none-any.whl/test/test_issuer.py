from certify_issuer.issuer import issue, revoke, issue_by_hash, revoke_by_hash


def test_issue():
    tx, error = issue(src_path='./test.pdf',
                      dest_path='./result.pdf',
                      cert_num='',
                      address='0x89995e30DAB8E3F9113e216EEB2f44f6B8eb5730',
                      issuer_name='test_user',
                      expire_date=0,
                      description='test',
                      is_testnet=True,
                      node_url='https://node-testnet.corexchain.io',
                      private_key='a737d20b2e2a001bbf54c7edfcbffb015b0e67924e20f561c238ddaad6c4ed0e',
                      certify_address='0xcc546a88db1af7d250a2f20dee42ec436f99e075')
    assert error is None


def test_issue_by_hash():
    random_str = '89995e30DAB8E3F9113e216EEB2f44f6B8eb5738'
    (tx, proof), error = issue_by_hash(hash_str=random_str,
                                       cert_num='',
                                       address='0x89995e30DAB8E3F9113e216EEB2f44f6B8eb5730',
                                       expire_date=0,
                                       description='test',
                                       is_testnet=True,
                                       node_url='https://node-testnet.corexchain.io',
                                       private_key='a737d20b2e2a001bbf54c7edfcbffb015b0e67924e20f561c238ddaad6c4ed0e',
                                       certify_address='0xcc546a88db1af7d250a2f20dee42ec436f99e075')
    assert error is None
    assert random_str.upper() in proof.upper()


def test_revoke():
    tx, error = revoke(src_path='./result.pdf',
                       address='0x89995e30DAB8E3F9113e216EEB2f44f6B8eb5730',
                       revoker_name='test_user',
                       node_url='https://node-testnet.corexchain.io',
                       private_key='a737d20b2e2a001bbf54c7edfcbffb015b0e67924e20f561c238ddaad6c4ed0e',
                       certify_address='0xcc546a88db1af7d250a2f20dee42ec436f99e075')
    assert error is None


def test_revoke_by_hash():
    tx, error = revoke_by_hash('89995e30DAB8E3F9113e216EEB2f44f6B8eb5738',
                               address='0x89995e30DAB8E3F9113e216EEB2f44f6B8eb5730',
                               revoker_name='test_user',
                               node_url='https://node-testnet.corexchain.io',
                               private_key='a737d20b2e2a001bbf54c7edfcbffb015b0e67924e20f561c238ddaad6c4ed0e',
                               certify_address='0xcc546a88db1af7d250a2f20dee42ec436f99e075')
    assert error is None
