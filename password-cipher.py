from functools import reduce


def recall_password(cipher_grille, ciphered_password):
    array = list(cipher_grille)
    password = list(ciphered_password)
    result = ''
    for _ in range(4):
        result += reduce(lambda x, y: x+y, 
                         [
                             password[i][j] for i in range(len(array)) 
                             for j in range(len(array[i])) if array[i][j] == 'X'
                         ])
        array = reverce_array(array)
    return result


def reverce_array(array):
    new_list = []
    for i in range(len(array)):
        new_list.append(list(reversed([array[j][i] for j in range(len(array[i]))])))
    return new_list

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert recall_password(
        ('X...',
         '..X.',
         'X..X',
         '....'),
        ('itdf',
         'gdce',
         'aton',
         'qrdi')) == 'icantforgetiddqd', 'First example'

    assert recall_password(
        ('....',
         'X..X',
         '.X..',
         '...X'),
        ('xhwc',
         'rsqx',
         'xqzz',
         'fyzr')) == 'rxqrwsfzxqxzhczy', 'Second example'
