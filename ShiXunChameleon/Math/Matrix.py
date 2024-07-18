# External
from __future__ import annotations
from time import time
import multiprocessing as mp
import random

# Internal


__all__ = ['IntMatrix']



class IntMatrix():
    """整數矩陣物件
    此class定義了整數矩陣以及其相應的各種運算。
    如果有效能上的需求，請自行更改此class中的資料結構，
    使用numpy可以有效的提高運算速度，
    此版本為了追求通過源碼掃描，
    因此只使用py內建的雙層list資料結構。    
    """
    def __init__(self, data: list[list[int]] = []) -> None:
        self.IntMatrix = data
        
    @property
    def rows(self) -> int:
        return len(self.IntMatrix)
    
    @property
    def cols(self) -> int:
        return len(self.IntMatrix[0]) if self.rows > 0 else 0
    
    @property
    def maxlen(self) -> int:
        """_summary_
        為了讓印出的矩陣對齊，
        必須找出矩陣中字串長度最長的元素，
        此property只在self.print_str()中使用，
        效率極差，沒事請不要呼叫它。

        Returns:
            int: 矩陣中字串長度最長的元素
        """
        max_length = 0
        for row in self.IntMatrix:
            for element in row:
                max_length = max(max_length, len(str(element)))
                
        return int(max_length)
        

    @property
    def trans(self) -> IntMatrix:
        """_summary_
        回傳轉置矩陣。
        
        Returns:
            IntMatrix: 轉置矩陣的物件
        """
        result = [[self.IntMatrix[i][j] for i in range(self.rows)] for j in range(self.cols)]
        
        return IntMatrix(result)
    

    # 定義加法運算
    def __add__(self, other: IntMatrix) -> IntMatrix:
        # 偵錯
        if not isinstance(other, IntMatrix):
            error_message = 'Invalid type input.'
            raise TypeError(error_message)
        elif self.rows != other.rows or self.cols != other.cols:
            error_message = 'The dimensions of the two matrices are different and cannot be added.'
            raise ValueError(error_message)
        
        # 加法運算
        result = [[self.IntMatrix[j][i] + other.IntMatrix[j][i] for i in range(self.cols)] for j in range(self.rows)]
        
        return IntMatrix(result)
    
    # 定義減法運算
    def __sub__(self, other: IntMatrix) -> IntMatrix:
        # 偵錯
        if not isinstance(other, IntMatrix):
            error_message = 'Invalid type input.'
            raise TypeError(error_message)
        elif self.rows != other.rows or self.cols != other.cols:
            error_message = 'The dimensions of the two matrices are different and cannot be added.'
            raise ValueError(error_message)
        
        # 減法運算
        result = [[self.IntMatrix[j][i] - other.IntMatrix[j][i] for i in range(self.cols)] for j in range(self.rows)]
        
        return IntMatrix(result)


    # 定義乘法運算
    def __rmul__(self, other: int) -> IntMatrix:
        return self.__mul__(other)
    
    
    # 也是定義乘法運算
    def __mul__(self, other: IntMatrix | int) -> IntMatrix:
        # 偵錯
        if not isinstance(other, IntMatrix) and not isinstance(other, int):
            error_message = "unsupported operand type(s) for *: '{}' and 'IntMatrix'.".format(str(type(other)).split("'")[1])
            raise TypeError(error_message)
        elif isinstance(other, IntMatrix) and self.cols != other.rows:
            error_message = "IntMatrix A row len not equal to IntMatrix B column len."
            raise ValueError(error_message)
        
        result = []
        # 矩陣*矩陣 的情況
        if isinstance(other, IntMatrix):
            result = [[0 for _ in range(other.cols)] for __ in range(self.rows)]
            for i in range(self.rows):
                for j in range(other.cols):
                    for k in range(self.cols):
                        result[i][j] += self.IntMatrix[i][k] * other.IntMatrix[k][j]
        # 整數*矩陣 or 矩陣*整數 的情況
        else:  
            result = [[0 for _ in range(self.cols)] for __ in range(self.rows)]
            for i in range(self.rows):
                for j in range(self.cols):
                    result[i][j] = self.IntMatrix[i][j] * other

        return IntMatrix(result)
    
    
    # 定義模除運算
    def __mod__(self, other: int) -> IntMatrix:
        # 偵錯
        if not isinstance(other, int):
            error_message = "unsupported operand type(s) for %: '{}' and 'IntMatrix'.".format(str(type(other)).split("'")[1])
            raise TypeError(error_message)

        # 模除運算
        result = [[0 for _ in range(self.cols)] for __ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                result[i][j] = self.IntMatrix[i][j] % other  # 需要進行multiprocessing

        return IntMatrix(result)
    

    # 定義 ==
    def __eq__(self,  other: object) -> bool:
        if not isinstance(other, IntMatrix):
            return False
        
        return self.IntMatrix == other.IntMatrix


    # 定義str()該如何回傳
    def __str__(self) -> str:
        return '\n'.join(' '.join(str(element) for element in row) for row in self.IntMatrix)
    

    # 回傳維度大小
    def dsize(self) -> str:
        return '{}x{}'.format(self.rows, self.cols)
    

    @staticmethod
    def str_to_matrix(str_data) -> IntMatrix:
        """_summary_
        此方法可以將str(IntMatrix)後的字串值重新轉換回IntMatrix物件。
        沒有寫偵錯程式請別亂用。
        
        Args:
            str(IntMatrix)後的字串

        Returns:
            IntMatrix: 原始的IntMatrix物件
        """
        data = str_data.split('\n')
        
        for i in range(len(data)):
            data[i] = data[i].split(' ') 
            for j in range(len(data[i])):
               data[i][j] = int(data[i][j])
        
        return IntMatrix(data)


    def print_str(self) -> None:
        """
        工整的印出矩陣。
        print()效率極差，大矩陣請小心使用。
        """
        s = '\n'.join('  '.join(f'{element:{self.maxlen}}' for element in row) for row in self.IntMatrix)
        print(s)
        
    
    def write_str(self) -> str:
        """_summary_
        回傳工整的矩陣字串，
        不可使用於str_to_matrix()的輸入，
        儘可用於寫入檔案方便閱讀用。
        
        Returns:    
            str: 工整的矩陣字串
        """
        s = '\n'.join('  '.join(f'{element:{self.maxlen}}' for element in row) for row in self.IntMatrix)
        
        return s
    
    
    def combine_row(self, M2: IntMatrix) -> IntMatrix:
        """_summary_
        橫向合併兩個IntMatrix矩陣。
        不會更改class值，需另外定義變數儲存回傳值。

        Args:
            M2 (IntMatrix): IntMatrix物件

        Raises:
            ValueError: 若兩矩陣row數不同則觸發ValueError

        Returns:
            IntMatrix: 橫向合併後的IntMatrix物件
        """
        if self.rows != M2.rows:
            error_message = 'Can\'t combine matrixes with diffrent row count.'
            raise ValueError(error_message)
        
        return IntMatrix([self.IntMatrix[i] + M2.IntMatrix[i] for i in range(self.rows)])
    
    
    def combine_col(self, M2: IntMatrix) -> IntMatrix:
        """_summary_
        縱向合併兩個IntMatrix矩陣。
        不會更改class值，需另外定義變數儲存回傳值。

        Args:
            M2 (IntMatrix): IntMatrix物件

        Raises:
            ValueError: 若兩矩陣cols數不同則觸發ValueError

        Returns:
            IntMatrix: 縱向合併後的IntMatrix物件
        """
        if self.cols != M2.cols:
            error_message = 'Can\'t combine matrixes with diffrent column count.'
            raise ValueError(error_message)
        
        return IntMatrix(self.IntMatrix + M2.IntMatrix)


    @staticmethod
    def normal_distribute_matrix(size: tuple[int, int], rng: tuple[int, int]) -> IntMatrix:
        """_summary_
        回傳隨機分布矩陣。
        
        Args:
            size (tuple[int, int]): 定義矩陣維度
            rng (tuple[int, int]): 定義矩陣元素數值範圍

        Returns:
            IntMatrix: 隨機分布的IntMatrix物件
        """
        result = [[random.randint(*rng) for _ in range(size[1])] for __ in range(size[0])]
        
        return IntMatrix(result)


    @staticmethod
    def gauss_distribute_matrix(size: tuple[int, int], mu: int = 0, sigma: float | int = 1) -> IntMatrix:
        """_summary_
        回傳高斯分布矩陣。

        Args:
            size (tuple[int, int]): 定義矩陣維度
            mu (int, optional): 定義高斯分布中心點 Defaults to 0.
            sigma (float | int, optional): 定義高斯分布標準差 Defaults to 1.

        Returns:
            IntMatrix: 高斯分布的IntMatrix物件
        """
        result = [[round(random.gauss(mu, sigma)) for _ in range(size[1])] for __ in range(size[0])]
        
        return IntMatrix(result)
    
    
    @staticmethod
    def gen_zero(size: tuple[int, int]) -> IntMatrix:
        """_summary_
        回傳加法單位矩陣。

        Args:
            size (tuple[int, int]): 定義矩陣維度

        Returns:
            IntMatrix: 加法單位矩陣的IntMatrix物件
        """
        result = [[0 for _ in range(size[1])] for __ in range(size[0])]
        
        return IntMatrix(result)
    
    
    @staticmethod
    def gen_I(n) -> IntMatrix: 
        """_summary_
        回傳乘法單位矩陣。
        
        Args:
            n (_type_): 定義矩陣維度(n*n)

        Returns:
            IntMatrix: 成法單位矩陣的IntMatrix物件
        """
        I = [[0 for _ in range(n)] for __ in range(n)]
        for i in range(n):
            I[i][i] = 1
        
        return IntMatrix(I)
    
    