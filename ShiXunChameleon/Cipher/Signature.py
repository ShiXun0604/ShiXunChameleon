from ShiXunChameleon.Cipher import BasicSIS
from ShiXunChameleon.IO import Error, Converter, Evaluate
from ShiXunChameleon.Math.Matrix import IntMatrix
from ShiXunChameleon.Config import config

from hashlib import sha256
import base64



# 忽然想到可以用SIS做Signature,參考著看吧
class SISkeyPair():
    def __init__(self) -> None:
        self.A = None
        self.R = None

    def __insert_line_breaks(self, s):
        WIDTH = 64
        return b'\n'.join([s[i:i+WIDTH] for i in range(0, len(s), WIDTH)])


    def extract_key(self) -> bytes:
        if self.A == None:
            error_message = 'No PMK in object.'
            raise Error.KeyExtractionError(error_message)

        ext_data = ''
        
        ext_data += str(self.A).replace('\n', '\\')

        ext_data = ext_data.encode()
        ext_data = base64.b64encode(ext_data)
        ext_data = self.__insert_line_breaks(ext_data)
        
        ext_str = b'-----BEGIN EXPERTOS PUBLIC KEY-----\n'
        ext_str += ext_data + b'\n-----END EXPERTOS PUBLIC KEY-----'

        return ext_str
    
    
    def extract_private_key(self) -> bytes:
        if self.R == None:
            error_message = 'No PMK in object.'
            raise Error.KeyExtractionError(error_message)

        ext_data = str(self.R).replace('\n', '\\')

        ext_data = ext_data.encode()
        ext_data = base64.b64encode(ext_data)
        ext_data = self.__insert_line_breaks(ext_data)
        
        ext_str = b'-----BEGIN EXPERTOS PRIVATE KEY-----\n'
        ext_str += ext_data + b'\n-----END EXPERTOS PRIVATE KEY-----'

        return ext_str


    def import_key(self, data: bytes) -> None:
        base64_data_list = data.decode().split('\n')

        # 取出中間字段，去掉---BEGIN---和---END---
        ext_data = ''
        for i in range(1, len(base64_data_list)-1):
            ext_data += base64_data_list[i]
        ext_data = base64.b64decode(ext_data.encode()).decode()
        
        # 構成KEY
        KEY = ext_data.replace('\\', '\n')
        KEY = IntMatrix.str_to_matrix(KEY)
            
        if base64_data_list[0] == '-----BEGIN EXPERTOS PRIVATE KEY-----':
            self.R = KEY
        elif base64_data_list[0] == '-----BEGIN EXPERTOS PUBLIC KEY-----':
            self.A = KEY
        else:
            error_message = 'Error occure while key importing.'
            raise Error.KeyImportError(error_message)
    
    
    def generate_key(self) -> None:
        A, R = BasicSIS.gen_A_with_trapdoor()
        self.A = A
        self.R = R


class SISsignature(SISkeyPair):
    def __init__(self) -> None:
        super().__init__()
    
    def hashing(self, m: str) -> IntMatrix:
        para = config.cryptParameter
        
        sha_256 = sha256()
        sha_256.update(m.encode('utf-8'))
        hash_result = sha_256.hexdigest()
        
        hash_result = Converter.hex_to_bytes(hash_result)
        hash_result = Converter.bytes_to_binary(hash_result)[2:]
        
        x = []
        for i in range(para.m):
            x.append([int(hash_result[i % 256])])
        x = IntMatrix(x)
        
        u = (self.A * x) % para.q
        
        return u
           
       
    def signing(self, m: str) -> bytes:
        u = self.hashing(m)
        
        x2 = BasicSIS.inverse_SIS(self.A, u, self.R)
        
        # 將IntMatrix訊息化為base64
        ext_data = str(x2).replace('\n', '\\')
        ext_data = ext_data.encode()
        ext_data = base64.b64encode(ext_data)
        
        return ext_data
    
    def verify(self, m: str, sign:bytes) -> bool:
        # 將base64訊息化為IntMatrix
        ext_data = base64.b64decode(sign)
        ext_data = ext_data.decode().replace('\\', '\n')
        x2 = IntMatrix.str_to_matrix(ext_data)
        
        para = config.cryptParameter
        
        u2 = (self.A * x2) % para.q
        u = self.hashing(m)
        
        len_x2 = Evaluate.calcu_x_len(x2)
        if len_x2 > (para.q/(para.n**0.5)):
            return False
        
        return u == u2