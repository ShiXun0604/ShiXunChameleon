from ShiXunChameleon.Math.Matrix import IntMatrix


def extract(MPK: list[list[IntMatrix]], MSK: list[list[IntMatrix]]) -> None:
    with open('MPK.txt', 'w') as f:
        for i, ele in enumerate(MPK):
            f.write('l = {}\n'.format(i))
            f.write('bit 0:\n')
            f.write(str(ele[0]) + '\n\n')
            
            f.write('bit 1:\n')
            f.write(str(ele[1]) + '\n\n')
            
    
    with open('MSK.txt', 'w') as f:
        for i, ele in enumerate(MSK):
            f.write('l = {}\n'.format(i))
            f.write('bit 0:\n')
            f.write(str(ele[0]) + '\n\n')
            
            f.write('bit 1:\n')
            f.write(str(ele[1]) + '\n\n')
            