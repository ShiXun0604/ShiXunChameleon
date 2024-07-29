from ShiXunChameleon.Config import config

from ShiXunChameleon.Math.Matrix import IntMatrix
from ShiXunChameleon.Cipher.CA import SXchameleonCA
from ShiXunChameleon.Cipher.Crypto import SXchameleonUser
from ShiXunChameleon.Cipher import BasicSIS
from ShiXunChameleon.IO import Evaluate



def SIS_collision_demo():
    para = config.cryptParameter
    
    # 生成帶有trapdoor的A
    A, R = BasicSIS.gen_A_with_trapdoor()
    
    # 舉出SIS實例
    x = BasicSIS.gen_x()
    u = (A * x) % para.q
    
    # 計算雜湊
    x2 = BasicSIS.inverse_SIS(A, u, R)
    u2 = (A * x2) % para.q
    
    print('是否產生碰撞：', u == u2)
    print('x是否相同：', x == x2)
    
    if False:
        Evaluate.normal_analyze(A, 3)
        Evaluate.gauss_analyze(R, 7)
        
    
def ShiXunChameleon_setup_phase() -> None:
    CA_obj = SXchameleonCA()
    
    # 生成MPK、MSK
    CA_obj.generate_MPK_MSK()
    
    # 保存MPK、MSK
    MPK_pem = CA_obj.extract_master_key()
    with open('MPK.pem', 'wb') as f:
        f.write(MPK_pem)
    
    MSK_pem = CA_obj.extract_master_private_key()
    with open('MSK.pem', 'wb') as f:
        f.write(MSK_pem)
    

def ShiXunChameleon_generate_user_SK(ID: str) -> None:
    # 讀取MPK
    CA_obj = SXchameleonCA()
    with open('MSK.pem', 'rb') as f:
        MSK_pem = f.read()
    CA_obj.import_key(MSK_pem)
    
    # 生成並保存R_ID
    R_ID_pem= CA_obj.extract_user_private_key(ID)
    with open('SK_{}.pem'.format(ID), 'wb') as f:
        f.write(R_ID_pem)
    

def ShiXunChameleon_hash(ID: str) -> IntMatrix:
    usr_obj = SXchameleonUser(ID)
    with open('MPK.pem', 'rb') as f:
        MPK_pem = f.read()
    usr_obj.import_MPK(MPK_pem)
    
    # ----- 雜湊 -----
    # 舉出SIS實例
    x = BasicSIS.gen_x()
    u = usr_obj.hashing(x)
    
    # ----- 碰撞 -----
    # 讀取並載入R_ID
    with open('SK_{}.pem'.format(ID), 'rb') as f:
        R_ID_pem = f.read()
    usr_obj.import_key(R_ID_pem)
    
    # 計算雜湊碰撞
    x2 = usr_obj.forge(u)
    u2 = usr_obj.hashing(x2)
    
    print('是否產生碰撞：', u == u2)
    print('x是否相同：', x == x2)
    
    

if __name__ == '__main__':
    ID = '101'
    #config.set_parameter(n=30, q=104729, l=len(ID), sigma=0.35)
    config.set_parameter(n=3, q=13, l=len(ID), sigma=0.35)
    
    # SIS collision demo
    if True:
        SIS_collision_demo()
    
    # ShiXunChameleon demo 
    if True:
        ShiXunChameleon_setup_phase()
        ShiXunChameleon_generate_user_SK(ID)
        ShiXunChameleon_hash(ID)
    
    