import multiprocessing, math
from ShiXunChameleon.IO import Error



__all__ = ['MultiprocEnv', 'CryptParameter', 'config']



class MultiprocEnv():
    def __init__(self) -> None:
        self.is_multiproc = True
        self.ENV_CPU_COUNT = multiprocessing.cpu_count()
        self.__used_cpu_count = int(multiprocessing.cpu_count()/2)
    

    def set_used_cpu(self, num: int) -> None:
        self.__used_cpu_count = num
    

    @property
    def used_cpu_count(self) -> int:
        if self.is_multiproc:
            return self.__used_cpu_count
        else:
            return 1



class CryptParameter():
    def __init__(self, n: int, q: int, l: int, sigma: int|float) -> None:
        self.__n = int(n)
        self.__q = int(q)
        self.__l = int(l)
        self.__sigma = sigma

    @property
    def n(self) -> int:
        return self.__n
    
    @property
    def m(self) -> int:
        return self.mp + (self.n * self.log_q)
    
    @property
    def q(self) -> int:
        return self.__q
    
    @property
    def l(self) -> int:
        return self.__l
    
    @property
    def sigma(self) -> int|float:
        return self.__sigma
    
    @property
    def log_q(self) -> int:
        return int(math.log(self.q, 2) + 1)  # log向上取整
    
    @property
    def mp(self) -> int:
        return int(self.n + math.log(self.q, 2) + 1)
    
    @property
    def rng(self) -> tuple:
        return (0, self.q-1)
    
    @property
    def beta(self) -> int:
        return int(self.q / self.n)
        
    def ext_size(self) -> tuple[int, int]:
        return (self.n, self.m)
    

    def __str__(self) -> str:
        data = [self.n, self.m, self.q, self.rng[0], self.rng[1]]
        return ' '.join(str(i) for i in data)



# 設定的class物件
class config:
    multiprocEnv = MultiprocEnv()
    #cryptParameter = CryptParameter(n=128, q=15991, l=100, sigma=1)
    cryptParameter = CryptParameter(n=2, q=7, l=2, sigma=0.5)

    def set_parameter(n: int, q: int, l: int, sigma: int|float) -> None:
        if not isinstance(n, int) or not isinstance(q, int):
            error_message = 'Invalid data type input.'
            raise TypeError(error_message)

        config.cryptParameter = CryptParameter(n, q, l, sigma)