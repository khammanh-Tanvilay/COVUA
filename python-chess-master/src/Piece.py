#
# Các lớp quân cờ trong trò chơi cờ vua
#
# TODO: Thêm kiểm tra chiếu sau khi di chuyển quân cờ được đề xuất

# Lớp quân cờ tổng quát
from enums import Player


class Piece:
    """
    Lớp cơ sở cho tất cả các quân cờ trong trò chơi cờ vua
    Chứa các thuộc tính và phương thức chung cho mọi quân cờ
    """
    
    def __init__(self, name, row_number, col_number, player):
        """
        Khởi tạo quân cờ với các thông tin cơ bản
        
        Args:
            name: Tên quân cờ (r, n, b, q, k, p)
            row_number: Số hàng hiện tại của quân cờ (0-7)
            col_number: Số cột hiện tại của quân cờ (0-7) 
            player: Người chơi sở hữu quân cờ (white/black)
        """
        self._name = name
        self.row_number = row_number
        self.col_number = col_number
        self._player = player

    def get_row_number(self):
        """Lấy số hàng hiện tại của quân cờ"""
        return self.row_number

    def get_col_number(self):
        """Lấy số cột hiện tại của quân cờ"""
        return self.col_number

    def get_name(self):
        """Lấy tên quân cờ"""
        return self._name

    def get_player(self):
        """Lấy người chơi sở hữu quân cờ"""
        return self._player

    def is_player(self, player_checked):
        """Kiểm tra xem quân cờ có thuộc về người chơi được chỉ định không"""
        return self.get_player() == player_checked

    def can_move(self, board, starting_square):
        """Phương thức trừu tượng - kiểm tra khả năng di chuyển"""
        pass

    def can_take(self, is_check):
        """Phương thức trừu tượng - kiểm tra khả năng ăn quân"""
        pass

    def change_row_number(self, new_row_number):
        """Thay đổi số hàng của quân cờ"""
        self.row_number = new_row_number

    def change_col_number(self, new_col_number):
        """Thay đổi số cột của quân cờ"""
        self.col_number = new_col_number

    def get_valid_piece_takes(self, game_state):
        """Phương thức trừu tượng - lấy danh sách các ô có thể ăn quân"""
        pass

    def get_valid_peaceful_moves(self, game_state):
        """Phương thức trừu tượng - lấy danh sách các ô có thể di chuyển (không ăn quân)"""
        pass

    def get_valid_piece_moves(self, board):
        """Phương thức trừu tượng - lấy tất cả các nước đi hợp lệ"""
        pass


# Lớp Xe (Rook)
class Rook(Piece):
    """
    Lớp Xe - có thể di chuyển theo hàng ngang và dọc
    """
    
    def __init__(self, name, row_number, col_number, player):
        """Khởi tạo Xe với thuộc tính đã di chuyển hay chưa"""
        super().__init__(name, row_number, col_number, player)
        self.has_moved = False  # Để kiểm tra khả năng nhập thành

    def get_valid_peaceful_moves(self, game_state):
        """Lấy danh sách các ô có thể di chuyển mà không ăn quân"""
        return self.traverse(game_state)[0]

    def get_valid_piece_takes(self, game_state):
        """Lấy danh sách các ô có thể ăn quân"""
        return self.traverse(game_state)[1]

    def get_valid_piece_moves(self, game_state):
        """Lấy tất cả các nước đi hợp lệ của Xe"""
        return self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)

    def traverse(self, game_state):
        """
        Duyệt qua tất cả các hướng có thể di chuyển của Xe
        Trả về tuple (các ô di chuyển được, các ô có thể ăn quân)
        """
        _peaceful_moves = []  # Danh sách các ô di chuyển được
        _piece_takes = []     # Danh sách các ô có thể ăn quân

        # Khởi tạo các bước di chuyển
        self._up = 1
        self._down = 1
        self._left = 1
        self._right = 1

        # Kiểm tra hướng trái của Xe
        self._breaking_point = False
        while self.get_col_number() - self._left >= 0 and not self._breaking_point:
            # Khi ô bên trái trống
            if game_state.get_piece(self.get_row_number(), self.get_col_number() - self._left) is Player.EMPTY:
                _peaceful_moves.append((self.get_row_number(), self.get_col_number() - self._left))
                self._left += 1
            # Khi ô bên trái có quân đối phương
            elif game_state.is_valid_piece(self.get_row_number(), self.get_col_number() - self._left) and \
                    not game_state.get_piece(self.get_row_number(), self.get_col_number() - self._left).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number(), self.get_col_number() - self._left))
                self._breaking_point = True
            else:
                self._breaking_point = True

        # Kiểm tra hướng phải của Xe
        self._breaking_point = False
        while self.get_col_number() + self._right < 8 and not self._breaking_point:
            # Khi ô bên phải trống
            if game_state.get_piece(self.get_row_number(), self.get_col_number() + self._right) is Player.EMPTY:
                _peaceful_moves.append((self.get_row_number(), self.get_col_number() + self._right))
                self._right += 1
            # Khi ô bên phải có quân đối phương
            elif game_state.is_valid_piece(self.get_row_number(), self.get_col_number() + self._right) and \
                    not game_state.get_piece(self.get_row_number(), self.get_col_number() + self._right).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number(), self.get_col_number() + self._right))
                self._breaking_point = True
            else:
                self._breaking_point = True

        # Kiểm tra hướng dưới của Xe
        self._breaking_point = False
        while self.get_row_number() + self._down < 8 and not self._breaking_point:
            # Khi ô bên dưới trống
            if game_state.get_piece(self.get_row_number() + self._down, self.get_col_number()) is Player.EMPTY:
                _peaceful_moves.append((self.get_row_number() + self._down, self.get_col_number()))
                self._down += 1
            # Khi ô bên dưới có quân đối phương
            elif game_state.is_valid_piece(self.get_row_number() + self._down, self.get_col_number()) and \
                    not game_state.get_piece(self.get_row_number() + self._down, self.get_col_number()).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number() + self._down, self.get_col_number()))
                self._breaking_point = True
            else:
                self._breaking_point = True

        # Kiểm tra hướng trên của Xe
        self._breaking_point = False
        while self.get_row_number() - self._up >= 0 and not self._breaking_point:
            # Khi ô bên trên trống
            if game_state.get_piece(self.get_row_number() - self._up, self.get_col_number()) is Player.EMPTY:
                _peaceful_moves.append((self.get_row_number() - self._up, self.get_col_number()))
                self._up += 1
            # Khi ô bên trên có quân đối phương
            elif game_state.is_valid_piece(self.get_row_number() - self._up, self.get_col_number()) and \
                    not game_state.get_piece(self.get_row_number() - self._up, self.get_col_number()).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number() - self._up, self.get_col_number()))
                self._breaking_point = True
            else:
                self._breaking_point = True
        return (_peaceful_moves, _piece_takes)


# Lớp Mã (Knight)
class Knight(Piece):
    """
    Lớp Mã - di chuyển theo hình chữ L (2 ô theo một hướng, 1 ô theo hướng vuông góc)
    """
    
    def get_valid_peaceful_moves(self, game_state):
        """Lấy danh sách các ô có thể di chuyển mà không ăn quân"""
        _moves = []
        # Các thay đổi tọa độ để tạo hình chữ L
        row_change = [-2, -2, -1, -1, +1, +1, +2, +2]
        col_change = [-1, +1, -2, +2, -2, +2, +1, -1]

        for i in range(0, 8):
            new_row = self.get_row_number() + row_change[i]
            new_col = self.get_col_number() + col_change[i]
            evaluating_square = game_state.get_piece(new_row, new_col)
            # Khi ô đích trống
            if evaluating_square == Player.EMPTY:
                _moves.append((new_row, new_col))
        return _moves

    def get_valid_piece_takes(self, game_state):
        """Lấy danh sách các ô có thể ăn quân"""
        _moves = []
        # Các thay đổi tọa độ để tạo hình chữ L
        row_change = [-2, -2, -1, -1, +1, +1, +2, +2]
        col_change = [-1, +1, -2, +2, -2, +2, +1, -1]

        for i in range(0, 8):
            new_row = self.get_row_number() + row_change[i]
            new_col = self.get_col_number() + col_change[i]
            evaluating_square = game_state.get_piece(new_row, new_col)
            # Khi ô đích có quân đối phương
            if game_state.is_valid_piece(new_row, new_col) and self.get_player() is not evaluating_square.get_player():
                _moves.append((new_row, new_col))
        return _moves

    def get_valid_piece_moves(self, game_state):
        """Lấy tất cả các nước đi hợp lệ của Mã"""
        # Code cũ đã được comment - sử dụng phương pháp mới hiệu quả hơn
        return self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)

# Lớp Tượng (Bishop)
class Bishop(Piece):
    """
    Lớp Tượng - di chuyển theo đường chéo
    """
    
    def __init__(self, name, row_number, col_number, player):
        super().__init__(name, row_number, col_number, player)

    def get_valid_piece_takes(self, game_state):
        """Lấy danh sách các ô có thể ăn quân"""
        return self.traverse(game_state)[1]

    def get_valid_peaceful_moves(self, game_state):
        """Lấy danh sách các ô có thể di chuyển mà không ăn quân"""
        return self.traverse(game_state)[0]

    def get_valid_piece_moves(self, game_state):
        """Lấy tất cả các nước đi hợp lệ của Tượng"""
        return self.get_valid_piece_takes(game_state) + self.get_valid_peaceful_moves(game_state)

    def traverse(self, game_state):
        _peaceful_moves = []
        _piece_takes = []

        # Hướng chéo trên-trái
        up, left = 1, 1
        while self.get_col_number() - left >= 0 and self.get_row_number() - up >= 0:
            if game_state.get_piece(self.get_row_number() - up, self.get_col_number() - left) == Player.EMPTY:
                _peaceful_moves.append((self.get_row_number() - up, self.get_col_number() - left))
            elif game_state.is_valid_piece(self.get_row_number() - up, self.get_col_number() - left) and \
                    not game_state.get_piece(self.get_row_number() - up, self.get_col_number() - left).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number() - up, self.get_col_number() - left))
                break
            else:
                break
            up += 1
            left += 1

        # Hướng chéo trên-phải
        up, right = 1, 1
        while self.get_col_number() + right < 8 and self.get_row_number() - up >= 0:
            if game_state.get_piece(self.get_row_number() - up, self.get_col_number() + right) == Player.EMPTY:
                _peaceful_moves.append((self.get_row_number() - up, self.get_col_number() + right))
            elif game_state.is_valid_piece(self.get_row_number() - up, self.get_col_number() + right) and \
                    not game_state.get_piece(self.get_row_number() - up, self.get_col_number() + right).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number() - up, self.get_col_number() + right))
                break
            else:
                break
            up += 1
            right += 1

        # Hướng chéo dưới-trái
        down, left = 1, 1
        while self.get_col_number() - left >= 0 and self.get_row_number() + down < 8:
            if game_state.get_piece(self.get_row_number() + down, self.get_col_number() - left) == Player.EMPTY:
                _peaceful_moves.append((self.get_row_number() + down, self.get_col_number() - left))
            elif game_state.is_valid_piece(self.get_row_number() + down, self.get_col_number() - left) and \
                    not game_state.get_piece(self.get_row_number() + down, self.get_col_number() - left).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number() + down, self.get_col_number() - left))
                break
            else:
                break
            down += 1
            left += 1

        # Hướng chéo dưới-phải
        down, right = 1, 1
        while self.get_col_number() + right < 8 and self.get_row_number() + down < 8:
            if game_state.get_piece(self.get_row_number() + down, self.get_col_number() + right) == Player.EMPTY:
                _peaceful_moves.append((self.get_row_number() + down, self.get_col_number() + right))
            elif game_state.is_valid_piece(self.get_row_number() + down, self.get_col_number() + right) and \
                    not game_state.get_piece(self.get_row_number() + down, self.get_col_number() + right).is_player(self.get_player()):
                _piece_takes.append((self.get_row_number() + down, self.get_col_number() + right))
                break
            else:
                break
            down += 1
            right += 1

        return (_peaceful_moves, _piece_takes)


# Lớp Tốt (Pawn)
class Pawn(Piece):
    """
    Lớp Tốt - di chuyển tiến về phía trước, ăn quân theo đường chéo
    """
    
    def get_valid_piece_takes(self, game_state):
        """Lấy danh sách các ô có thể ăn quân"""
        _moves = []
        if self.is_player(Player.PLAYER_1):  # Tốt trắng
            # Khi ô chéo dưới-trái có quân đen
            if game_state.is_valid_piece(self.get_row_number() + 1, self.get_col_number() - 1) and \
                    game_state.get_piece(self.get_row_number() + 1, self.get_col_number() - 1).is_player(Player.PLAYER_2):
                _moves.append((self.get_row_number() + 1, self.get_col_number() - 1))
            # Khi ô chéo dưới-phải có quân đen
            if game_state.is_valid_piece(self.get_row_number() + 1, self.get_col_number() + 1) and \
                    game_state.get_piece(self.get_row_number() + 1, self.get_col_number() + 1).is_player(Player.PLAYER_2):
                _moves.append((self.get_row_number() + 1, self.get_col_number() + 1))
            # Kiểm tra khả năng bắt tốt qua đường (en passant)
            if game_state.can_en_passant(self.get_row_number(), self.get_col_number()):
                _moves.append((self.get_row_number() + 1, game_state.previous_piece_en_passant()[1]))
        # Khi tốt là quân đen
        elif self.is_player(Player.PLAYER_2):
            # Khi ô chéo trên-trái có quân trắng
            if game_state.is_valid_piece(self.get_row_number() - 1, self.get_col_number() - 1) and \
                    game_state.get_piece(self.get_row_number() - 1, self.get_col_number() - 1).is_player(Player.PLAYER_1):
                _moves.append((self.get_row_number() - 1, self.get_col_number() - 1))
            # Khi ô chéo trên-phải có quân trắng
            if game_state.is_valid_piece(self.get_row_number() - 1, self.get_col_number() + 1) and \
                    game_state.get_piece(self.get_row_number() - 1, self.get_col_number() + 1).is_player(Player.PLAYER_1):
                _moves.append((self.get_row_number() - 1, self.get_col_number() + 1))
            # Kiểm tra khả năng bắt tốt qua đường (en passant)
            if game_state.can_en_passant(self.get_row_number(), self.get_col_number()):
                _moves.append((self.get_row_number() - 1, game_state.previous_piece_en_passant()[1]))
        return _moves

    def get_valid_peaceful_moves(self, game_state):
        """Lấy danh sách các ô có thể di chuyển mà không ăn quân"""
        _moves = []
        # Khi tốt là quân trắng
        if self.is_player(Player.PLAYER_1):
            # Khi ô phía dưới trống
            if game_state.get_piece(self.get_row_number() + 1, self.get_col_number()) == Player.EMPTY:
                # Khi tốt chưa được di chuyển lần nào (ở hàng 1)
                if self.get_row_number() == 1 and game_state.get_piece(self.get_row_number() + 2,
                                                                       self.get_col_number()) == Player.EMPTY:
                    _moves.append((self.get_row_number() + 1, self.get_col_number()))
                    _moves.append((self.get_row_number() + 2, self.get_col_number()))
                # Khi tốt đã được di chuyển trước đó
                else:
                    _moves.append((self.get_row_number() + 1, self.get_col_number()))
        # Khi tốt là quân đen
        elif self.is_player(Player.PLAYER_2):
            # Khi ô phía trên trống
            if game_state.get_piece(self.get_row_number() - 1, self.get_col_number()) == Player.EMPTY:
                # Khi tốt chưa được di chuyển lần nào (ở hàng 6)
                if self.get_row_number() == 6 and game_state.get_piece(self.get_row_number() - 2,
                                                                       self.get_col_number()) == Player.EMPTY:
                    _moves.append((self.get_row_number() - 1, self.get_col_number()))
                    _moves.append((self.get_row_number() - 2, self.get_col_number()))
                # Khi tốt đã được di chuyển trước đó
                else:
                    _moves.append((self.get_row_number() - 1, self.get_col_number()))
        return _moves

    def get_valid_piece_moves(self, game_state):
        """Lấy tất cả các nước đi hợp lệ của Tốt"""
        # Code cũ đã được comment - sử dụng phương pháp mới hiệu quả hơn
        return self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)


# Lớp Hậu (Queen) - đi ngang, dọc, chéo không giới hạn số ô (miễn không bị cản)
class Queen(Piece):
    """
    Lớp Hậu - implement trực tiếp logic di chuyển 8 hướng
    """
    
    def __init__(self, name, row_number, col_number, player):
        super().__init__(name, row_number, col_number, player)
        self.has_moved = False
    
    def get_valid_peaceful_moves(self, game_state):
        """Lấy danh sách các ô có thể di chuyển mà không ăn quân"""
        return self.traverse(game_state)[0]

    def get_valid_piece_takes(self, game_state):
        """Lấy danh sách các ô có thể ăn quân"""
        return self.traverse(game_state)[1]

    def get_valid_piece_moves(self, game_state):
        """Lấy tất cả các nước đi hợp lệ của Hậu"""
        return self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)
    
    def traverse(self, game_state):
        """
        Duyệt qua tất cả 8 hướng có thể di chuyển của Hậu
        Trả về tuple (các ô di chuyển được, các ô có thể ăn quân)
        """
        _peaceful_moves = []
        _piece_takes = []
        
        # 8 hướng di chuyển: 4 hướng thẳng + 4 hướng chéo
        directions = [
            (-1, 0),   # lên
            (1, 0),    # xuống  
            (0, -1),   # trái
            (0, 1),    # phải
            (-1, -1),  # chéo trên-trái
            (-1, 1),   # chéo trên-phải
            (1, -1),   # chéo dưới-trái
            (1, 1)     # chéo dưới-phải
        ]
        
        for row_dir, col_dir in directions:
            step = 1
            while True:
                new_row = self.get_row_number() + (row_dir * step)
                new_col = self.get_col_number() + (col_dir * step)
                
                # Kiểm tra xem có ra ngoài bàn cờ không
                if new_row < 0 or new_row >= 8 or new_col < 0 or new_col >= 8:
                    break
                
                piece_at_square = game_state.get_piece(new_row, new_col)
                
                # Nếu ô trống
                if piece_at_square is Player.EMPTY:
                    _peaceful_moves.append((new_row, new_col))
                    step += 1
                # Nếu có quân đối phương
                elif (game_state.is_valid_piece(new_row, new_col) and 
                      not piece_at_square.is_player(self.get_player())):
                    _piece_takes.append((new_row, new_col))
                    break  # Dừng lại sau khi gặp quân
                # Nếu có quân cùng phe
                else:
                    break  # Dừng lại
        
        return (_peaceful_moves, _piece_takes)

# Lớp Vua (King)
class King(Piece):
    """
    Lớp Vua - di chuyển 1 ô theo mọi hướng, có thể nhập thành
    """
    
    def get_valid_piece_takes(self, game_state):
        """Lấy danh sách các ô có thể ăn quân"""
        _moves = []
        # Các thay đổi tọa độ để di chuyển 1 ô theo mọi hướng
        row_change = [-1, +0, +1, -1, +1, -1, +0, +1]
        col_change = [-1, -1, -1, +0, +0, +1, +1, +1]
        
        for i in range(0, 8):
            new_row = self.get_row_number() + row_change[i]
            new_col = self.get_col_number() + col_change[i]
            evaluating_square = game_state.get_piece(new_row, new_col)
            # Khi ô đích có quân đối phương
            if game_state.is_valid_piece(new_row, new_col) and self.get_player() is not evaluating_square.get_player():
                _moves.append((new_row, new_col))
        return _moves

    def get_valid_peaceful_moves(self, game_state):
        """Lấy danh sách các ô có thể di chuyển mà không ăn quân"""
        _moves = []
        # Các thay đổi tọa độ để di chuyển 1 ô theo mọi hướng
        row_change = [-1, +0, +1, -1, +1, -1, +0, +1]
        col_change = [-1, -1, -1, +0, +0, +1, +1, +1]
        
        for i in range(0, 8):
            new_row = self.get_row_number() + row_change[i]
            new_col = self.get_col_number() + col_change[i]
            evaluating_square = game_state.get_piece(new_row, new_col)
            # Khi ô đích trống
            if evaluating_square == Player.EMPTY:
                _moves.append((new_row, new_col))
        return _moves

    def get_valid_piece_moves(self, game_state):
        """Lấy tất cả các nước đi hợp lệ của Vua"""
        # Code cũ đã được comment - sử dụng phương pháp mới hiệu quả hơn
        return self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)
