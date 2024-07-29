from ShiXunChameleon.IO import Error
from ShiXunChameleon.Math.Matrix import IntMatrix
from ShiXunChameleon.Config import config
import base64



class SXchameleonKeyPair():
    """
    定義有關使用者公鑰、私鑰的相關操作。
    """
    def __init__(self) -> None:
        self.F_ID = None
        self.__R_ID = None
    
    @property
    def R_ID(self) -> IntMatrix:
        return self.__R_ID
    

    def __insert_line_breaks(self, s):
        WIDTH = 64
        return b'\n'.join([s[i:i+WIDTH] for i in range(0, len(s), WIDTH)])
    

    def extract_key(self) -> bytes:
        """
        輸出物件中的使用者公鑰的pem格式文檔，
        可使用open寫入文件中存檔用。

        Return:
            bytes: .pem格式的公鑰字串
        """
        # 若未輸入MPK則無法輸出公鑰
        if self.F_ID == None:
            error_message = 'No PMK in object.'
            raise Error.KeyExtractionError(error_message)

        # 將F_ID轉換為字串
        ext_data = ''
        ext_data += str(self.F_ID).replace('\n', '\\')

        # 進行base64編碼
        ext_data = ext_data.encode()
        ext_data = base64.b64encode(ext_data)

        # 轉換為pem格式
        ext_data = self.__insert_line_breaks(ext_data)
        ext_str = b'-----BEGIN SHIXUN CHAMELEON PUBLIC KEY-----\n'
        ext_str += ext_data + b'\n-----END SHIXUN CHAMELEON PUBLIC KEY-----'

        return ext_str
    
    
    def extract_private_key(self) -> bytes:
        """
        輸出物件中的使用者私鑰的pem格式文檔，
        可使用open寫入文件中存檔用。

        Return:
            bytes: .pem格式的私鑰字串
        """
        if self.R_ID == None:
            error_message = 'No PMK in object.'
            raise Error.KeyExtractionError(error_message)

        ext_data = ''
        ext_data += str(self.R_ID).replace('\n', '\\')

        ext_data = ext_data.encode()
        ext_data = base64.b64encode(ext_data)
        ext_data = self.__insert_line_breaks(ext_data)
        
        ext_str = b'-----BEGIN SHIXUN CHAMELEON PRIVATE KEY-----\n'
        ext_str += ext_data + b'\n-----END SHIXUN CHAMELEON PRIVATE KEY-----'

        return ext_str


    def import_key(self, data: bytes) -> None:
        """
        載入格式為.pem的金鑰。
        使用open將.pem檔讀取後，
        放入此方法的參數即可。

        Args:
            data(bytes): .pem檔的完整金鑰字串
        """
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
    