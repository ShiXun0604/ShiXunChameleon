from ShiXunChameleon.Config import config
from ShiXunChameleon.Math.Matrix import IntMatrix
from ShiXunChameleon.Math import Tools
from random import randint



def gen_G():
    """_summary_
    生成工具矩陣G
    
    Returns:
        IntMatrix: 工具矩陣G的IntMatrix物件
    """
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



def gen_x() -> IntMatrix:
    """_summary_
    生成隨機向量x，其中x元素屬於{-1, 0, 1}。
    
    Returns:
        IntMatrix: 隨機x向量的IntMatrix物件
    """
    para = config.cryptParameter
    
    return IntMatrix.normal_distribute_matrix(size=(para.m, 1), rng=(-1,1))



def gen_A_with_trapdoor() -> tuple[IntMatrix, IntMatrix]:
    """_summary_
    生成帶有trapdoor R的矩陣A。

    Returns:
        tuple[IntMatrix, IntMatrix]: (隨機矩陣A物件, trapdoor R物件)
    """
    para = config.cryptParameter
    
    B = IntMatrix.normal_distribute_matrix(size=(para.n, para.mp), rng=para.rng)
    R = IntMatrix.gauss_distribute_matrix(
        size = (para.mp, para.n * para.log_q), 
        mu = 0,
        sigma = para.sigma,
        )
    G = gen_G()
    
    A = B.combine_row(G - (B * R)) % para.q
    
    return A, R



def RI(R: IntMatrix) -> IntMatrix:
    """_summary_
    將trapdoor R下面並一個矩陣I
    
    Args:
        R (IntMatrix): trapdoor R

    Returns:
        IntMatrix: RI物件
    """
    I = IntMatrix.gen_I(R.cols)
    
    return R.combine_col(I)


    
def inverse_sis(x: int) -> list[int]:
    """_summary_
    運算f_g^-1(u)。
    
    Args:
        x (int): 整數

    Returns:
        list[int]: 所有可能的結果
    """
    def recur_tool(u: int, curr_result: list[int]):
        # 傳說中高效的演算法
        # 應該有更高效的寫法
        # 請參考影片 https://www.youtube.com/watch?v=fVen9vkFWlk&list=LL&index=59&ab_channel=SimonsInstitute
        if len(curr_result) == para.log_q:
            ans = 0
            for i in range(len(curr_result)):
                ans += 2**i * curr_result[i]

            if ans == x:
                ans_list.append(curr_result)
            return

        # 每一個bit嘗試三種情況
        for x_i in [-1, 0, 1]:
            U = (u - x_i) / 2
            if Tools.is_int(U):
                next = curr_result + [x_i]
                recur_tool(U, next)
                
    para = config.cryptParameter
    
    # 計算f_g^-1(u) = [x1, ... ,x?]
    ans_list = []
    recur_tool(u=x, curr_result=[])
    
    return ans_list



def inverse_SIS(A: IntMatrix, u: IntMatrix, R: IntMatrix) -> IntMatrix:
    """_summary_
    運算f_A^-1(u)。
    
    Args:
        A (IntMatrix): 矩陣A
        u (IntMatrix): 向量u
        R (IntMatrix): trapdoor R

    Returns:
        IntMatrix: 雜湊碰撞x'物件
    """
    # step1 算z = f_G^-1(u)
    z = [] 
    for u_ele in u.IntMatrix:
        ans_list = inverse_sis(u_ele[0])
        for ele in ans_list[randint(0, len(ans_list)-1)]:  # 隨機取一項
            z.append([ele])
    z = IntMatrix(z)
    
    # step2 算x'
    xp = RI(R) * z
    
    return xp