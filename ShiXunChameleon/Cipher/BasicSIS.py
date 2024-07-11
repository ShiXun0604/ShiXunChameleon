from ShiXunChameleon.Config import config
from ShiXunChameleon.Math.Matrix import IntMatrix
from random import randint



def gen_G():
    para = config.cryptParameter
    
    ZERO = [0 for _ in range(para.log_q)]
    g = [2**i for i in range(para.log_q)] 
    
    G = []
    for i in range(para.n):
        G_ele = []
        
        for _ in range(i):
            G_ele += ZERO
        G_ele += g
        for _ in range(para.n-i-1):
            G_ele += ZERO
            
        G.append(G_ele)
        
    return IntMatrix(G)



def gen_I(n) -> IntMatrix: 
    I = [[0 for _ in range(n)] for __ in range(n)]
    for i in range(n):
        I[i][i] = 1
    
    return IntMatrix(I)



def gen_x() -> IntMatrix:
    para = config.cryptParameter
    return IntMatrix.rand_normal_distribute_matrix(size=(para.m, 1), rng=(-1,1))



def gen_A_with_trapdoor():
    para = config.cryptParameter
    B = IntMatrix.rand_normal_distribute_matrix(size=(para.n, para.mp), rng=para.rng)
    R = IntMatrix.gauss_distribute_matrix(
        size = (para.mp, para.n * para.log_q), 
        mu = 0,
        sigma = para.sigma,
        )
    
    G = gen_G()
    
    m2 = G - (B * R)
    A = B.combine_row(m2) % para.q
    
    return A, R



def RI(R: IntMatrix) -> IntMatrix:
    I = gen_I(R.cols)
    return R.combine_col(I)


    
def inverse_sis(U: int, log_q: int) -> list[int]:
    # log_q = k
    ans_list = []
    
    def is_int(num: float) -> bool:
        if num % 1 == 0:
            return True
        else:
            return False
    
    def recur_tool(u: int, curr_result: list[int], num: int):
        if len(curr_result) == log_q:
            ans = 0
            for i in range(len(curr_result)):
                ans += 2**i * curr_result[i]

            if ans == num:
                ans_list.append(curr_result)
            return

        # 嘗試三種情況
        for x_i in [-1, 0, 1]:
            U = (u - x_i) / 2
            if is_int(U):
                next = curr_result + [x_i]
                recur_tool(U, next, num)
    
    recur_tool(u=U, curr_result=[], num=U)
    return ans_list



def inverse_SIS(A: IntMatrix, u: IntMatrix, R: IntMatrix) -> IntMatrix:
    para = config.cryptParameter
    
    # step1 算z = f_G^-1(u)
    z = [] 
    for u_ele in u.IntMatrix:
        ans_list = inverse_sis(u_ele[0], para.log_q)
        for ele in ans_list[randint(0, len(ans_list)-1)]:
            z.append([ele])
    z = IntMatrix(z)
    
    # step2 算x'
    R_I = RI(R)
    xp = R_I * z
    
    return xp