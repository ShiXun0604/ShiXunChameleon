from ShiXunChameleon.Cipher.UserKeyPair import SXchameleonKeyPair
from ShiXunChameleon.Cipher import BasicSIS
from ShiXunChameleon.IO import Error
from ShiXunChameleon.Config import config
from ShiXunChameleon.Math.Matrix import IntMatrix

import base64



class SXchameleonUser(SXchameleonKeyPair):
    def __init__(self , ID: str) -> None:
        super().__init__()
        self.MPK = None
        self.ID = ID
                
    def __calcu_F_ID(self) -> IntMatrix:
        # 偵錯
        if self.MPK == None:
            error_message = 'Without MPK importing'
            raise Error.NoPublicKeyError(error_message)
        
        # 計算F_ID
        para = config.cryptParameter
        F_ID = IntMatrix.gen_zero(size=(para.n, para.m))
        for i in range(para.l):
            F_ID += self.MPK[i][int(self.ID[i])]
        F_ID %= para.q
        
        self.F_ID = F_ID
    
    
    def import_MPK(self, data: bytes) -> None:
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
            
        if base64_data_list[0] == '-----BEGIN SHIXUN CHAMELEON MASTER PUBLIC KEY-----':
            self.MPK = KEY
            self.__calcu_F_ID()
        else:
            error_message = 'Error occure while key importing.'
            raise Error.KeyImportError(error_message)
    
    
    def hashing(self, x: IntMatrix) -> IntMatrix:
        para = config.cryptParameter
        return (self.F_ID * x) % para.q
    
    
    def forge(self, u: IntMatrix) -> IntMatrix:
        if self.R_ID == None:
            error_message = 'Without trapdoor imported.'
            raise Error.NoPrivateKeyError(error_message)
        
        return BasicSIS.inverse_SIS(self.F_ID, u, self.R_ID)
        
        