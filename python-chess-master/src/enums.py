# Lớp định nghĩa các hằng số cho người chơi và quân cờ
class Player:
    # Định nghĩa người chơi 1 (quân trắng)
    PLAYER_1 = 'white'
    # Định nghĩa người chơi 2 (quân đen) 
    PLAYER_2 = 'black'
    # Định nghĩa ô trống trên bàn cờ
    EMPTY = -9
    # Danh sách tất cả các loại quân cờ (trắng và đen)
    # r: xe, n: mã, b: tượng, q: hậu, k: vua, p: tốt
    PIECES = ['white_r', 'white_n', 'white_b', 'white_q', 'white_k', 'white_p',
              'black_r', 'black_n', 'black_b', 'black_q', 'black_k', 'black_p']
