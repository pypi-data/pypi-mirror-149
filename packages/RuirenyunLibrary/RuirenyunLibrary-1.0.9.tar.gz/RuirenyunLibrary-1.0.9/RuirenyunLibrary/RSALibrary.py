import os.path
import base64
import rsa


def generate_keypair(key_path="", long=1024):
    # 生成密钥
    pubkey, privkey = rsa.newkeys(long)
    # 保存密钥公钥
    with open(os.path.join(key_path, 'public.pem'), 'w+') as f:
        f.write(pubkey.save_pkcs1().decode())
    # 保存私钥
    with open(os.path.join(key_path, 'private.pem'), 'w+') as f:
        f.write(privkey.save_pkcs1().decode())


# 用公钥加密
def encrypt(information, public_key):
    with open(public_key, 'r') as publickfile:
        p = publickfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(p)
    original_text = information.encode('utf8')
    crypt_text = rsa.encrypt(original_text, pubkey)
    print(f"crypt_text:{crypt_text}")
    # 加密后的密文
    return crypt_text


# 用私钥解密
def decrypt(crypt_text, private_key):
    with open(private_key, 'rb') as privatefile:
        p = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(p)
    # bytes类型decode()转化为str
    lase_text = rsa.decrypt(crypt_text, privkey).decode()
    print(lase_text)


def str2key(s):
    # 对字符串解码
    b_str = base64.b64decode(s)

    if len(b_str) < 162:
        return False

    hex_str = b_str.hex()

    # 找到模数和指数的开头结束位置
    m_start = 29 * 2
    e_start = 159 * 2
    m_len = 128 * 2
    e_len = 3 * 2

    modulus = hex_str[m_start:m_start + m_len]
    exponent = hex_str[e_start:e_start + e_len]
    return modulus, exponent


def encrypt_by_keystr(keystr, message):
    """
        通过后台接口返回的公钥字符串加密信息
    :param keystr:          str|后台接口返回的公钥字符串
    :param message:         str|需要加密的字符串
    :return:                str|加密后的字符串
    """
    key = str2key(str(keystr))
    modulus = int(key[0], 16)
    exponent = int(key[1], 16)
    rsa_pubkey = rsa.PublicKey(modulus, exponent)
    crypto = rsa.encrypt(str(message).encode('utf8'), rsa_pubkey)
    b64str = base64.b64encode(crypto)
    return b64str.decode()


if __name__ == '__main__':
    pubkey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDO85c6WFtsbMsRnvKiHD/tP/f+/0RgcgO1FKMsa/uXLiihp75pGm4aAxALTgwTBj6tkICCdlow+sBXDwuFXbPBl/iDCEuyrWabQvgaL57uvl7KoCXv8+Mailzs33Q5W63LHXr0Pbv/ZL8Qibd7J/s1iEN2Wrhn7j13M2HTdJl5fwIDAQAB"
    b64_str = encrypt_by_keystr(pubkey, "123123")
