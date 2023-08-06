# Certify Issuer
Certify Issuer нь сертификат, диплом, дансны хуулга зэрэг бичиг баримтыг блокчэйн дээр
баталгаажуулж өгөх https://github.com/corex-mn/certify-sc ухаалаг гэрээтэй харьцдаг python хэлний сан юм.

Ингэхдээ https://chainpoint.org/ ийн v2.0 стандартыг ашигласан.

## Суулгах заавар
`pip install certify-issuer`

## Функцүүд
### `issue`
PDF файлын хаш утгыг тооцож ухаалаг гэрээнд бичээд, 
гүйлгээний мэдээлэл болон нэмэлт мэдээллүүдийг файлын мэтадата дээр нэмэн шинэ файлд хадгална. 

| Параметр       | Тайлбар                               |   Заавал эсэх |  
| -------------  | -------------                         | ------------- | 
| `src_path`       | PDF эх файлын зам                     | тийм          |
| `dest_path`      | Мэтадата бичсэн PDF-ийг хадгалах зам  | тийм          |
| `cert_num`       | Сертификатын дахин давхцахгүй дугаар  | үгүй          | 
| `address`        | Баталгаажуулагчийн блокчэйн хаяг      | тийм          |
| `issuer_name`    | Баталгаажуулагчийн нэр                | үгүй          | 
| `expire_date`    | Дуусах хугацаа                        | үгүй          | 
| `description`    | Тайлбар, нэмэлт мэдээлэл              | үгүй          |
| `private_key`    | Баталгаажуулагчийн хувийн түлхүүр     | үгүй /keystore, passphrase өгөөгүй бол заавал/         |
| `keystore`       | Хувийн түлхүүрийн keystore файл       | үгүй /private_key өгөөгүй бол заавал/           |
| `passphrase`     | Хувийн түлхүүрийн passphrase файл     | үгүй /private_key өгөөгүй бол заавал/           |
| `certify_address`| Ухаалаг гэрээний хаяг                 | тийм          | 
| `node_url`       | Гүйлгээ хийх блокчэйний нөүдний хаяг  | тийм          |
| `is_testnet`     | Тест орчинд ажиллаж буй бол True утга өгнө|үгүй /default=False/

#### Жишээ
```
from certify_issuer import issuer
try:
    txid, error = issuer.issue(src_path='test.pdf',
                               dest_path='test_result.pdf',
                               cert_num='D00123123',
                               address=MY_ADDRESS,
                               issuer_name='Монгол Улсын Их Сургууль',
                               expire_date=0,
                               description='2022 оны хаврын улирлын төгсөлт',
                               private_key=MY_PRIVATE_KEY,
                               certify_address=CERTIFY_CONTRACT_ADDRESS,
                               node_url='https://node.corexchain.io',
                               is_testnet=False)
    if error is not None:
        print("Error: {}", error)
    else
        print("Success: {}", txid)
except Exception as e:
    print("Error: {}", e)
```
### `issue_by_hash`
Хаш стрингийг шууд ухаалаг гэрээнд баталгаажуулаад  

| Параметр       | Тайлбар                               |   Заавал эсэх |  
| -------------  | -------------                         | ------------- | 
| `hash_str`       | хаш утга                              | тийм          |
| `cert_num`       | Сертификатын дахин давхцахгүй дугаар  | үгүй          | 
| `address`        | Баталгаажуулагчийн блокчэйн хаяг      | тийм          |
| `expire_date`    | Дуусах хугацаа                        | үгүй          | 
| `description`    | Тайлбар, нэмэлт мэдээлэл              | үгүй          |
| `private_key`    | Баталгаажуулагчийн хувийн түлхүүр     | үгүй /keystore, passphrase өгөөгүй бол заавал/         |
| `keystore`       | Хувийн түлхүүрийн keystore файл       | үгүй /private_key өгөөгүй бол заавал/           |
| `passphrase`     | Хувийн түлхүүрийн passphrase файл     | үгүй /private_key өгөөгүй бол заавал/           |
| `certify_address`| Ухаалаг гэрээний хаяг                 | тийм          | 
| `node_url`       | Гүйлгээ хийх блокчэйний нөүдний хаяг  | тийм          |
| `is_testnet`     | Тест орчинд ажиллаж буй бол True утга өгнө|үгүй /default=False/

#### Жишээ
```
from certify_issuer import issuer
hash_str = some_hash_function(file_or_something)
try:
    (tx, proof), error = issuer.issue(
                               hash_str='89995e30DAB8E3F9113e216EEB2f44f6B8eb5738',
                               cert_num='D00123123',
                               address=MY_ADDRESS,
                               expire_date=0,
                               description='2022 оны хаврын улирлын төгсөлт',
                               private_key=MY_PRIVATE_KEY,
                               certify_address=CERTIFY_CONTRACT_ADDRESS,
                               node_url='https://node.corexchain.io',
                               is_testnet=False)
    if error is not None:
        print("Error: {}", error)
    else
        print("Success: {} {}", tx, proof)
except Exception as e:
    print("Error: {}", e)
```

### `revoke`
Нэгэнт ухаалаг гэрээнд баталгаажсан PDF файлыг буцаан хүчингүй болгох функц

| Параметр       | Тайлбар                               |   Заавал эсэх |  
| -------------  | -------------| ------------- |
| `src_path`       | Мэтадата бичигдсэн PDF файлын зам     | тийм          |
| `address`        | Баталгаажуулагчийн блокчэйн хаяг      | тийм          |
| `revoker_name`   | Хүчингүй болгож буй хүний нэр         | тийм          | 
| `private_key`    | Баталгаажуулагчийн хувийн түлхүүр     | үгүй /keystore, passphrase өгөөгүй бол заавал/         |
| `keystore`       | Хувийн түлхүүрийн keystore файл       | үгүй /private_key өгөөгүй бол заавал/           |
| `passphrase`     | Хувийн түлхүүрийн passphrase файл     | үгүй /private_key өгөөгүй бол заавал/           |
| `certify_address`| Ухаалаг гэрээний хаяг                 | тийм          | 
| `node_url`       | Гүйлгээ хийх блокчэйний нөүдний хаяг  | тийм          |
| `is_testnet`     | Тест орчинд ажиллаж буй бол True утга өгнө|үгүй /default=False/

#### Жишээ
```
from certify_issuer import issuer
try:
    tx, error = issuer.revoke(
                           src_path='test_result.pdf',
                           address=MY_ADDRESS,
                           revoker_name='Mr. Revoker'
                           private_key=MY_PRIVATE_KEY,
                           certify_address=CERTIFY_CONTRACT_ADDRESS,
                           node_url='https://node.corexchain.io',
                           is_testnet=False)
    if error is not None:
        print("Error: {}", error)
    else
        print("Success: {}", tx)

except Exception as e:
    print("Error: {}", e)
```
### `revoke_by_hash`
Нэгэнт ухаалаг гэрээнд баталгаажсан хаш утгыг буцаан хүчингүй болгох функц

| Параметр       | Тайлбар                               |   Заавал эсэх |  
| -------------  | -------------                         | ------------- | 
| `hash_str`       | хаш                                   | тийм          |
| `address`        | Баталгаажуулагчийн блокчэйн хаяг      | тийм          |
| `revoker_name`   | Хүчингүй болгож буй хүний нэр         | тийм          | 
| `private_key`    | Баталгаажуулагчийн хувийн түлхүүр     | үгүй /keystore, passphrase өгөөгүй бол заавал/         |
| `keystore`       | Хувийн түлхүүрийн keystore файл       | үгүй /private_key өгөөгүй бол заавал/           |
| `passphrase`     | Хувийн түлхүүрийн passphrase файл     | үгүй /private_key өгөөгүй бол заавал/           |
| `certify_address`| Ухаалаг гэрээний хаяг                 | тийм          | 
| `node_url`       | Гүйлгээ хийх блокчэйний нөүдний хаяг  | тийм          |
| `is_testnet`     | Тест орчинд ажиллаж буй бол True утга өгнө|үгүй /default=False/

#### Жишээ
```
from certify_issuer import issuer
hash_str = some_hash_function(file_or_something)
try:
    tx, error = issuer.revoke_by_hash(
                           hash_str=hash_str,
                           address=MY_ADDRESS,
                           revoker_name='Mr. Revoker'
                           private_key=MY_PRIVATE_KEY,
                           certify_address=CERTIFY_CONTRACT_ADDRESS,
                           node_url='https://node.corexchain.io',
                           is_testnet=False)
    if error is not None:
        print("Error: {}", error)
    else
        print("Success: {}", tx)
except Exception as e:
    print("Error: {}", e)
```
