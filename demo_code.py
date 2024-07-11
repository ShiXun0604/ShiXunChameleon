from ShiXunChameleon.Math.Matrix import IntMatrix
from ShiXunChameleon.Cipher import BasicSIS
from ShiXunChameleon.Config import config
from ShiXunChameleon.Cipher.CA import SXchameleonCA
import matplotlib.pyplot as plt


def count_number_distribution(matrix, interval_size, q):
    array = []
    for ele in matrix:
        array += ele
        
    distribution = {}
    for start in range(0, q + 1, interval_size):
        end = start + interval_size - 1
        range_label = f"{start}-{end}"
        distribution[range_label] = 0
    
    for number in array:
        range_start = (number // interval_size) * interval_size
        range_end = range_start + interval_size - 1
        range_label = f"{range_start}-{range_end}"
        if range_label in distribution:
            distribution[range_label] += 1
    
    return distribution



def plot_distribution(distribution):
    ranges = list(distribution.keys())
    counts = list(distribution.values())

    plt.bar(ranges, counts, align='center', alpha=0.7, edgecolor='black')
    plt.xlabel('Range')
    plt.ylabel('Count')
    plt.title('Number Distribution in Intervals')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()



def analyze(M: IntMatrix, interval: int) -> None:
    para = config.cryptParameter
    distribution = count_number_distribution(M.IntMatrix, interval, para.q)
    plot_distribution(distribution)

def test():
    q = 1024
    mu = int(q/2)
    size = (50, 50)
    sigma = 10
    interval = 20

    M1 = IntMatrix.gauss_distribute_matrix(size=size, mu=mu, sigma=sigma)
    M1_list = [element for row in M1.IntMatrix for element in row]
    
    for i in range(100):
        M1 += IntMatrix.gauss_distribute_matrix(size=size, mu=mu, sigma=sigma)
        
    M1 = M1 % q
    M1_list = [element for row in M1.IntMatrix for element in row]
    plot_distribution(count_number_distribution(M1_list, interval, q))



def SIS_collision_demo():
    para = config.cryptParameter
    
    # 生成帶有trapdoor的A
    A, R = BasicSIS.gen_A_with_trapdoor()
    
    # 舉出SIS實例
    x = BasicSIS.gen_x()
    u = (A * x) % para.q
    
    x2 = BasicSIS.inverse_SIS(A, u, R)
    u2 = (A * x2) % para.q
    
    print(u == u2)
    print(x == x2)
    


def ShiXunChameleon_setup_phase():
    para = config.cryptParameter
    
    CA_obj = SXchameleonCA()
    MPK, MSK, A_bar = CA_obj.generate_MPK_MSK() 
    
    


    
    

if __name__ == '__main__':
    ShiXunChameleon_setup_phase()
   
   