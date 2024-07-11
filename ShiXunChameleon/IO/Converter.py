__all__ = [
    'bytes_to_binary',
    'binary_to_bytes',
    'binary_to_bytes',
    'bytes_to_binary',
]

"""
這裡的程式碼都是改寫自ChatGPT-4o
"""



# bytes <-> str: 0x...
def bytes_to_hex(byte_data: bytes) -> str:
    if not isinstance(byte_data, (bytes, bytearray)):
        error_message = "Input must be bytes or bytearray."
        raise ValueError(error_message)
    
    hex_str = byte_data.hex()
    
    return '0x' + hex_str


def hex_to_bytes(hex_str: str) -> bytes:
    if not isinstance(hex_str, str):
        error_message = "Input must be a string."
        raise ValueError(error_message)
    
    if hex_str.startswith('0x'):
        hex_str = hex_str[2:]
    
    if len(hex_str) % 2 != 0:
        error_message = "Hex to bytes needs even length of hex string."
        raise ValueError(error_message)
    
    try:
        byte_data = bytes.fromhex(hex_str)
    except ValueError as e:
        error_message = "Invalid hex string: {hex_str}".format(hex_str)
        raise ValueError(error_message)
    
    return byte_data



# bytes <-> str: 0b...
def bytes_to_binary(byte_data: bytes) -> str:
    integer_value = int.from_bytes(byte_data, byteorder='big')
    
    binary_str = bin(integer_value)[2:]
    original_length = len(byte_data) * 8
    
    binary_str = binary_str.zfill(original_length)
    return '0b' + binary_str


def binary_to_bytes(data: str) -> bytes:
    binary_str = data[2:]

    integer_value = int(binary_str, 2)
    byte_length = (integer_value.bit_length() + 7) // 8

    byte_data = integer_value.to_bytes(byte_length, byteorder='big')
    return byte_data