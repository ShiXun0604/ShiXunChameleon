from ShiXunChameleon.IO import Error
from ShiXunChameleon.Math.Matrix import IntMatrix
import base64



class SXchameleonKeyPair():
    def __init__(self) -> None:
        self.F_ID = None
        self.__R_ID = None
    
    @property
    def R_ID(self) -> IntMatrix|None:
        return self.__R_ID
    
    def __insert_line_breaks(self, s):
        WIDTH = 64
        return b'\n'.join([s[i:i+WIDTH] for i in range(0, len(s), WIDTH)])
    
    
    def extract_key(self) -> bytes:
        if self.F_ID == None:
            error_message = 'No PMK in object.'
            raise Error.KeyExtractionError(error_message)

        ext_data = ''
        
        ext_data += str(self.F_ID).replace('\n', '\\')

        ext_data = ext_data.encode()
        ext_data = base64.b64encode(ext_data)
        ext_data = self.__insert_line_breaks(ext_data)
        
        ext_str = b'-----BEGIN SHIXUN CHAMELEON PUBLIC KEY-----\n'
        ext_str += ext_data + b'\n-----END SHIXUN CHAMELEON PUBLIC KEY-----'

        return ext_str
    
    
    def extract_private_key(self) -> bytes:
        if self.R_ID == None:
            error_message = 'No PMK in object.'
            raise Error.KeyExtractionError(error_message)

        ext_data += str(self.R_ID).replace('\n', '\\')

        ext_data = ext_data.encode()
        ext_data = base64.b64encode(ext_data)
        ext_data = self.__insert_line_breaks(ext_data)
        
        ext_str = b'-----BEGIN SHIXUN CHAMELEON PRIVATE KEY-----\n'
        ext_str += ext_data + b'\n-----END SHIXUN CHAMELEON PRIVATE KEY-----'

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
            
        if base64_data_list[0] == '-----BEGIN SHIXUN CHAMELEON PRIVATE KEY-----':
            self.__R_ID = KEY
        elif base64_data_list[0] == '-----BEGIN SHIXUN CHAMELEON PUBLIC KEY-----':
            self.F_ID = KEY
        else:
            error_message = 'Error occure while key importing.'
            raise Error.KeyImportError(error_message)
    