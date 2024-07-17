from ShiXunChameleon.Config import config
from ShiXunChameleon.Math.Matrix import IntMatrix
from ShiXunChameleon.Cipher import BasicSIS
from ShiXunChameleon.IO import Error
import base64

 


class SXchameleonCA():
    """_summary_
    定義phase1、phase2的過程。
    """
    def __init__(self) -> None:
        self.MPK = None
        self.__MSK = None
    
    @property
    def MSK(self):
        return self.__MSK
    
    
    def __insert_line_breaks(self, s):
        WIDTH = 64
        return b'\n'.join([s[i:i+WIDTH] for i in range(0, len(s), WIDTH)])
    
    
    def generate_MPK_MSK(self) -> None:
        para = config.cryptParameter
        G = BasicSIS.gen_G()
        
        # 生成A_bar、A_list
        A_list = []
        Ai_size, Ai_rng = (para.n, para.mp), para.rng
        
        for i in range(para.l):
            A_i = IntMatrix.normal_distribute_matrix(size=Ai_size, rng=Ai_rng)
            A_list.append(A_i)

        A_bar = A_list[0]
        for i in range(1, len(A_list)):
            A_bar += A_list[i]
        A_bar %= para.q
        
        # 生成MSK
        MSK = []  # MSK[bit index][0 or 1]
        Ri_size, Ri_sigma = (para.mp, para.n * para.log_q), para.sigma
        for i in range(para.l):
            R_i0 = IntMatrix.gauss_distribute_matrix(size=Ri_size, mu=0, sigma=Ri_sigma)
            R_i1 = IntMatrix.gauss_distribute_matrix(size=Ri_size, mu=0, sigma=Ri_sigma)
            MSK.append([R_i0, R_i1])
            
        
        # 計算MPK
        MPK = []
        zero = IntMatrix.gen_zero(size=(para.n, para.n * para.log_q))
        
        A_00 = A_list[0].combine_row(G - A_bar*MSK[0][0])
        A_00 %= para.q
        
        A_01 = A_list[0].combine_row(G - A_bar*MSK[0][1])
        A_01 %= para.q
        MPK.append([A_00, A_01])

        for i in range(1, para.l):
            A_i0 = A_list[i].combine_row(zero - A_bar*MSK[i][0])
            A_i0 %= para.q
            A_i1 = A_list[i].combine_row(zero - A_bar*MSK[i][1])
            A_i1 %= para.q
            MPK.append([A_i0, A_i1])
        
        self.MPK = MPK
        self.__MSK = MSK
        return MPK, MSK
    
    
    def extract_master_key(self) -> tuple[bytes, bytes]:
        if self.MPK == None:
            error_message = 'No PMK in object.'
            raise Error.KeyExtractionError(error_message)

        ext_data = ''
        for ele in self.MPK:
            for i in range(2):
                ext_data += str(ele[i]).replace('\n', '\\')
                ext_data += '$'
        ext_data = ext_data.strip('$')
                
        ext_data = ext_data.encode()
        ext_data = base64.b64encode(ext_data)
        ext_data = self.__insert_line_breaks(ext_data)
        
        ext_str = b'-----BEGIN SHIXUN CHAMELEON MASTER PUBLIC KEY-----\n'
        ext_str += ext_data + b'\n-----END SHIXUN CHAMELEON MASTER PUBLIC KEY-----'

        return ext_str
    
    
    def extract_master_private_key(self) -> tuple[bytes, bytes]:
        if self.__MSK == None:
            error_message = 'No PSK in object.'
            raise Error.KeyExtractionError(error_message)

        ext_data = ''
        for ele in self.__MSK:
            for i in range(2):
                ext_data += str(ele[i]).replace('\n', '\\')
                ext_data += '$'
        ext_data = ext_data.strip('$')
                
        ext_data = ext_data.encode()
        ext_data = base64.b64encode(ext_data)
        ext_data = self.__insert_line_breaks(ext_data)
        
        ext_str = b'-----BEGIN SHIXUN CHAMELEON MASTER PRIVATE KEY-----\n'
        ext_str += ext_data + b'\n-----END SHIXUN CHAMELEON MASTER PRIVATE KEY-----'

        return ext_str


    def extract_user_private_key(self, ID: str) -> IntMatrix:
        para = config.cryptParameter
        
        if self.__MSK == None:
            error_message = 'No PSK in object.'
            raise Error.KeyExtractionError(error_message)
        
        # 組成RID
        R_ID = IntMatrix.gen_zero(size=(para.mp, para.n * para.log_q))
        for i in range(para.l):
            R_ID += self.__MSK[i][int(ID[i])]
                
        ext_data = str(R_ID).replace('\n', '\\').encode()
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
        ext_data = ext_data.split('$')
        
        # 構成KEY
        KEY = []
        for i in range(0, len(ext_data), 2):
            R_i0 = ext_data[i].replace('\\', '\n')
            R_i1 = ext_data[i+1].replace('\\', '\n')
            
            R_i0 = IntMatrix.str_to_matrix(R_i0)
            R_i1 = IntMatrix.str_to_matrix(R_i1)
            KEY.append([R_i0, R_i1])
            
        if base64_data_list[0] == '-----BEGIN SHIXUN CHAMELEON MASTER PRIVATE KEY-----':
            self.__MSK = KEY
        elif base64_data_list[0] == '-----BEGIN SHIXUN CHAMELEON MASTER PUBLIC KEY-----':
            self.MPK = KEY
        else:
            error_message = 'Error occure while key importing.'
            raise Error.KeyImportError(error_message)
        
        

            
            