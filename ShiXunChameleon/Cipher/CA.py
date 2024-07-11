from ShiXunChameleon.Config import config
from ShiXunChameleon.Math.Matrix import IntMatrix
from ShiXunChameleon.Cipher import BasicSIS



class SXchameleonCA():
    def __init__(self) -> None:
        self.MPK = []
        self.__MSK = []
        
    def generate_MPK_MSK(self):
        para = config.cryptParameter
        G = BasicSIS.gen_G()
        
        # 生成A_bar、A_list
        A_list = []
        Ai_size, Ai_rng = (para.n, para.mp), para.rng
        
        for i in range(para.l):
            A_i = IntMatrix.rand_normal_distribute_matrix(size=Ai_size, rng=Ai_rng)
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
        A_01 = A_list[0].combine_row(G - A_bar*MSK[0][1])
        MPK.append([A_00, A_01])

        for i in range(1, para.l):
            A_i0 = A_list[i].combine_row(zero - A_bar*MSK[i][0])
            A_i1 = A_list[i].combine_row(zero - A_bar*MSK[i][1])
            MPK.append([A_i0, A_i1])
        
        # 測試
        Fid = IntMatrix.gen_zero(size=(para.n, para.m))
        Rid = IntMatrix.gen_zero(size=(para.mp, para.n * para.log_q))
        for i in range(para.l):
            Fid += MPK[i][0]
            Rid += MSK[i][0]
        Fid %= para.q
        
           
        RidI = BasicSIS.RI(Rid)
        
        r = (Fid*RidI) % para.q
        r.print_str()
        
        
        '''
        G = BasicSIS.gen_G()
        left = (G - (A_bar * Rid)) % para.q
        print('left')
        left.print_str()
        '''
        return MPK, MSK, A_bar
        
        
        
        
        
        
            
    
    
    
