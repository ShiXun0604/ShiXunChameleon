from ShiXunChameleon.Math.Matrix import IntMatrix
from ShiXunChameleon.Cipher.CA import SXchameleonCA
from ShiXunChameleon.Cipher import BasicSIS
from ShiXunChameleon.IO import Evaluate
from ShiXunChameleon.Config import config



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
    
    print(u == u2)
    print(x == x2)
    


def ShiXunChameleon_setup_phase():
    config.set_parameter(n=50, q=509, l=100, sigma=0.17)
    para = config.cryptParameter
    print(para.m)
    CA_obj = SXchameleonCA()
    MPK, MSK = CA_obj.generate_MPK_MSK()
    
    
    # 假設身分訊息每個bit都是1
    Fid = IntMatrix.gen_zero(size=(para.n, para.m))
    Rid = IntMatrix.gen_zero(size=(para.mp, para.n * para.log_q))
    for i in range(para.l):
        Fid += MPK[i][1]
        Rid += MSK[i][1]
    Fid %= para.q
    
    # 舉出SIS實例
    x = BasicSIS.gen_x()
    u = (Fid * x) % para.q
    
    # 計算雜湊
    x2 = BasicSIS.inverse_SIS(Fid, u, Rid)
    u2 = (Fid * x2) % para.q
    
    print(u == u2)
    print(x == x2)
    print(Evaluate.calcu_x_len(x2))
    
    Evaluate.normal_analyze(Fid, 50)
    Evaluate.gauss_analyze(Rid, 7)
    
    

if __name__ == '__main__':
    ShiXunChameleon_setup_phase()
   
   