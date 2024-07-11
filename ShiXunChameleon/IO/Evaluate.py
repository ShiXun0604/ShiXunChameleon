from ShiXunChameleon.Math.Matrix import IntMatrix
from ShiXunChameleon.Config import config
import matplotlib.pyplot as plt


# 統計隨機分布矩陣
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



def normal_analyze(M: IntMatrix, interval: int) -> None:
    para = config.cryptParameter
    distribution = count_number_distribution(M.IntMatrix, interval, para.q)
    plot_distribution(distribution)
    
# 統計高斯分布矩陣
def count_numbers_in_range(arr, x):
    count_dict = {i: 0 for i in range(-x, x+1)}
    for num in arr:
        if -x <= num <= x:
            count_dict[num] += 1
    return count_dict


def plot_counts(count_dict):
    keys = list(count_dict.keys())
    values = list(count_dict.values())

    plt.bar(keys, values, color='blue')
    plt.xlabel('Numbers')
    plt.ylabel('Counts')
    plt.title('Counts of Numbers in Range')
    plt.show()
    
    
def gauss_analyze(M: IntMatrix, interval: int):
    array = []
    for ele in M.IntMatrix:
        array += ele
    count_dict = count_numbers_in_range(array, interval)
    plot_counts(count_dict)


# 計算x長度
def calcu_x_len(x: IntMatrix) -> float:
    num = 0
    for ele in x.IntMatrix:
        num += ele[0]*ele[0]
    return num**(0.5)