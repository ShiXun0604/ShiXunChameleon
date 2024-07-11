def is_prime(n: int) -> bool:
    if not isinstance(n, int):
        error_message = 'Invalid data type input.'
        raise TypeError(error_message)
    
    if n < 2:
        return False
    
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
