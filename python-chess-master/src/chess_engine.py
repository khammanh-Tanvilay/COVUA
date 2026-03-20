#
# Lớp Bàn cờ vua
# Lưu trữ trạng thái trò chơi cờ vua, in bàn cờ, tìm các nước đi hợp lệ, lưu trữ lịch sử nước đi
#
# Lưu ý: Lớp move log được lấy cảm hứng từ Eddie Sharick
#
from Piece import Rook, Knight, Bishop, Queen, King, Pawn
from enums import Player

'''
Cấu trúc bàn cờ 8x8:
r \ c     0           1           2           3           4           5           6           7 
0   [(r=0, c=0), (r=0, c=1), (r=0, c=2), (r=0, c=3), (r=0, c=4), (r=0, c=5), (r=0, c=6), (r=0, c=7)]
1   [(r=1, c=0), (r=1, c=1), (r=1, c=2), (r=1, c=3), (r=1, c=4), (r=1, c=5), (r=1, c=6), (r=1, c=7)]
2   [(r=2, c=0), (r=2, c=1), (r=2, c=2), (r=2, c=3), (r=2, c=4), (r=2, c=5), (r=2, c=6), (r=2, c=7)]
3   [(r=3, c=0), (r=3, c=1), (r=3, c=2), (r=3, c=3), (r=3, c=4), (r=3, c=5), (r=3, c=6), (r=3, c=7)]
4   [(r=4, c=0), (r=4, c=1), (r=4, c=2), (r=4, c=3), (r=4, c=4), (r=4, c=5), (r=4, c=6), (r=4, c=7)]
5   [(r=5, c=0), (r=5, c=1), (r=5, c=2), (r=5, c=3), (r=5, c=4), (r=5, c=5), (r=5, c=6), (r=5, c=7)]
6   [(r=6, c=0), (r=6, c=1), (r=6, c=2), (r=6, c=3), (r=6, c=4), (r=6, c=5), (r=6, c=6), (r=6, c=7)]
7   [(r=7, c=0), (r=7, c=1), (r=7, c=2), (r=7, c=3), (r=7, c=4), (r=7, c=5), (r=7, c=6), (r=7, c=7)]
'''


# TODO: Lật bàn cờ theo người chơi
# TOD
# O: Tốt thường được biểu thị bằng không có chữ cái
# TODO: Xử lý stalemate (hòa)
# TODO: Lịch sử nước đi - sửa lỗi cập nhật boolean nhập thành của vua
# TODO: Thay đổi tham số is_ai trong phương thức move thành cách thanh lịch hơn
class game_state:
    """
    Lớp quản lý trạng thái trò chơi cờ vua
    Chứa bàn cờ, các quân cờ, lịch sử nước đi và logic game
    """
    
    def __init__(self, player_at_bottom='white'):
        """
        Khởi tạo trạng thái ban đầu của trò chơi cờ vua
        """
        # Bàn cờ là một mảng 2D
        # TODO: Chuyển sang định dạng numpy sau này
        
        # Các quân cờ đã bị bắt
        self.white_captives = []  # Quân trắng bị bắt
        self.black_captives = []  # Quân đen bị bắt
        
        # Lịch sử các nước đi
        self.move_log = []
        
        # Trạng thái lượt chơi
        self.white_turn = True  # True = lượt quân trắng, False = lượt quân đen
        
        # Trạng thái bắt tốt qua đường (en passant)
        self.can_en_passant_bool = False
        self._en_passant_previous = (-1, -1)
        
        # Trạng thái kết thúc game
        self.checkmate = False   # Chiếu hết
        self.stalemate = False   # Hòa (stalemate)
        
        # Trạng thái chiếu
        self._is_check = False
        
        # Vị trí của các vua
        self._white_king_location = [0, 3]  # Vua trắng ở ô e1
        self._black_king_location = [7, 3]  # Vua đen ở ô e8
        
        # Khả năng nhập thành của vua trắng
        # [Vua chưa di chuyển, Xe trái chưa di chuyển, Xe phải chưa di chuyển]
        self.white_king_can_castle = [True, True, True]
        
        # Khả năng nhập thành của vua đen
        self.black_king_can_castle = [True, True, True]

        # Khởi tạo các quân cờ trắng
        white_rook_1 = Rook('r', 0, 0, Player.PLAYER_1)      # Xe trái
        white_rook_2 = Rook('r', 0, 7, Player.PLAYER_1)      # Xe phải
        white_knight_1 = Knight('n', 0, 1, Player.PLAYER_1)  # Mã trái
        white_knight_2 = Knight('n', 0, 6, Player.PLAYER_1)  # Mã phải
        white_bishop_1 = Bishop('b', 0, 2, Player.PLAYER_1)  # Tượng trái
        white_bishop_2 = Bishop('b', 0, 5, Player.PLAYER_1)  # Tượng phải
        white_queen = Queen('q', 0, 4, Player.PLAYER_1)      # Hậu
        white_king = King('k', 0, 3, Player.PLAYER_1)        # Vua
        white_pawn_1 = Pawn('p', 1, 0, Player.PLAYER_1)      # Tốt a2
        white_pawn_2 = Pawn('p', 1, 1, Player.PLAYER_1)      # Tốt b2
        white_pawn_3 = Pawn('p', 1, 2, Player.PLAYER_1)      # Tốt c2
        white_pawn_4 = Pawn('p', 1, 3, Player.PLAYER_1)      # Tốt d2
        white_pawn_5 = Pawn('p', 1, 4, Player.PLAYER_1)      # Tốt e2
        white_pawn_6 = Pawn('p', 1, 5, Player.PLAYER_1)      # Tốt f2
        white_pawn_7 = Pawn('p', 1, 6, Player.PLAYER_1)      # Tốt g2
        white_pawn_8 = Pawn('p', 1, 7, Player.PLAYER_1)      # Tốt h2
        
        # Danh sách tất cả quân cờ trắng
        self.white_pieces = [white_rook_1, white_rook_2, white_knight_1, white_knight_2, white_bishop_1, white_bishop_2,
                             white_queen, white_king, white_pawn_1, white_pawn_2, white_pawn_3, white_pawn_4,
                             white_pawn_5, white_pawn_6, white_pawn_7, white_pawn_8]

        # Khởi tạo các quân cờ đen
        black_rook_1 = Rook('r', 7, 0, Player.PLAYER_2)      # Xe trái
        black_rook_2 = Rook('r', 7, 7, Player.PLAYER_2)      # Xe phải
        black_knight_1 = Knight('n', 7, 1, Player.PLAYER_2)  # Mã trái
        black_knight_2 = Knight('n', 7, 6, Player.PLAYER_2)  # Mã phải
        black_bishop_1 = Bishop('b', 7, 2, Player.PLAYER_2)  # Tượng trái
        black_bishop_2 = Bishop('b', 7, 5, Player.PLAYER_2)  # Tượng phải
        black_queen = Queen('q', 7, 4, Player.PLAYER_2)      # Hậu
        black_king = King('k', 7, 3, Player.PLAYER_2)        # Vua
        black_pawn_1 = Pawn('p', 6, 0, Player.PLAYER_2)      # Tốt a7
        black_pawn_2 = Pawn('p', 6, 1, Player.PLAYER_2)      # Tốt b7
        black_pawn_3 = Pawn('p', 6, 2, Player.PLAYER_2)      # Tốt c7
        black_pawn_4 = Pawn('p', 6, 3, Player.PLAYER_2)      # Tốt d7
        black_pawn_5 = Pawn('p', 6, 4, Player.PLAYER_2)      # Tốt e7
        black_pawn_6 = Pawn('p', 6, 5, Player.PLAYER_2)      # Tốt f7
        black_pawn_7 = Pawn('p', 6, 6, Player.PLAYER_2)      # Tốt g7
        black_pawn_8 = Pawn('p', 6, 7, Player.PLAYER_2)      # Tốt h7
        
        # Danh sách tất cả quân cờ đen
        self.black_pieces = [black_rook_1, black_rook_2, black_knight_1, black_knight_2, black_bishop_1, black_bishop_2,
                             black_queen, black_king, black_pawn_1, black_pawn_2, black_pawn_3, black_pawn_4,
                             black_pawn_5, black_pawn_6, black_pawn_7, black_pawn_8]

        # Khởi tạo bàn cờ với vị trí ban đầu, tùy theo player_at_bottom
        if player_at_bottom == 'white':
            self.board = [
                [white_rook_1, white_knight_1, white_bishop_1, white_king, white_queen, white_bishop_2, white_knight_2, white_rook_2],  # Hàng 0 (a1-h1)
                [white_pawn_1, white_pawn_2, white_pawn_3, white_pawn_4, white_pawn_5, white_pawn_6, white_pawn_7, white_pawn_8],  # Hàng 1 (a2-h2)
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY],  # Hàng 2 (a3-h3)
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY],  # Hàng 3 (a4-h4)
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY],  # Hàng 4 (a5-h5)
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY],  # Hàng 5 (a6-h6)
                [black_pawn_1, black_pawn_2, black_pawn_3, black_pawn_4, black_pawn_5, black_pawn_6, black_pawn_7, black_pawn_8],  # Hàng 6 (a7-h7)
                [black_rook_1, black_knight_1, black_bishop_1, black_king, black_queen, black_bishop_2, black_knight_2, black_rook_2]   # Hàng 7 (a8-h8)
            ]
        else:
            self.board = [
                [black_rook_1, black_knight_1, black_bishop_1, black_king, black_queen, black_bishop_2, black_knight_2, black_rook_2],  # Hàng 0 (a1-h1)
                [black_pawn_1, black_pawn_2, black_pawn_3, black_pawn_4, black_pawn_5, black_pawn_6, black_pawn_7, black_pawn_8],  # Hàng 1 (a2-h2)
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY],  # Hàng 2 (a3-h3)
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY],  # Hàng 3 (a4-h4)
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY],  # Hàng 4 (a5-h5)
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY],  # Hàng 5 (a6-h6)
                [white_pawn_1, white_pawn_2, white_pawn_3, white_pawn_4, white_pawn_5, white_pawn_6, white_pawn_7, white_pawn_8],  # Hàng 6 (a7-h7)
                [white_rook_1, white_knight_1, white_bishop_1, white_king, white_queen, white_bishop_2, white_knight_2, white_rook_2]   # Hàng 7 (a8-h8)
            ]

    def get_piece(self, row, col):
        """
        Lấy quân cờ tại vị trí (row, col)
        
        Tham số:
            row: Số hàng (0-7)
            col: Số cột (0-7)
        Trả về:
            Quân cờ tại vị trí đó hoặc Player.EMPTY nếu ô trống
        """
        # Kiểm tra vị trí hợp lệ trên bàn cờ
        if (0 <= row < 8) and (0 <= col < 8):
            return self.board[row][col]

    def is_valid_piece(self, row, col):
        """
        Kiểm tra xem tại vị trí (row, col) có quân cờ hợp lệ không
        """
        evaluated_piece = self.get_piece(row, col)
        return (evaluated_piece is not None) and (evaluated_piece != Player.EMPTY)

    def get_valid_moves(self, starting_square):
        """
        Lấy danh sách các nước đi hợp lệ cho quân cờ tại vị trí starting_square
        
        Giải thích dễ hiểu:
        - Nếu quân cờ bị chiếu, chỉ cho phép các nước đi có thể đỡ chiếu hoặc ăn quân đang chiếu.
        - Nếu quân cờ bị ghim (pin), chỉ cho phép di chuyển trên đường thẳng giữa vua và quân ghim.
        - Nếu là vua, không được đi vào ô bị chiếu.
        - Nếu không bị chiếu hay ghim, trả về tất cả nước đi hợp lệ của quân cờ đó.
        """
        current_row = starting_square[0]
        current_col = starting_square[1]

        if self.is_valid_piece(current_row, current_col):
            valid_moves = []
            moving_piece = self.get_piece(current_row, current_col)
            if self.get_piece(current_row, current_col).is_player(Player.PLAYER_1):
                king_location = self._white_king_location
            else:
                king_location = self._black_king_location
            group = self.check_for_check(king_location, moving_piece.get_player())
            checking_pieces = group[0]
            pinned_pieces = group[1]
            pinned_checks = group[2]
            initial_valid_piece_moves = moving_piece.get_valid_piece_moves(self)

            # immediate check
            if checking_pieces:
                for move in initial_valid_piece_moves:
                    can_move = True
                    for piece in checking_pieces:
                        if moving_piece.get_name() == "k":
                            temp = self.board[current_row][current_col]
                            self.board[current_row][current_col] = Player.EMPTY
                            temp2 = self.board[move[0]][move[1]]
                            self.board[move[0]][move[1]] = temp
                            if not self.check_for_check(move, moving_piece.get_player())[0]:
                                pass
                            else:
                                can_move = False
                            self.board[current_row][current_col] = temp
                            self.board[move[0]][move[1]] = temp2
                        elif move == piece and len(checking_pieces) == 1 and moving_piece.get_name() != "k" and \
                                (current_row, current_col) not in pinned_pieces:
                            pass
                        elif move != piece and len(checking_pieces) == 1 and moving_piece.get_name() != "k" and \
                                (current_row, current_col) not in pinned_pieces:
                            temp = self.board[move[0]][move[1]]
                            self.board[move[0]][move[1]] = moving_piece
                            self.board[current_row][current_col] = Player.EMPTY
                            if self.check_for_check(king_location, moving_piece.get_player())[0]:
                                can_move = False
                            self.board[current_row][current_col] = moving_piece
                            self.board[move[0]][move[1]] = temp
                        else:
                            can_move = False
                    if can_move:
                        valid_moves.append(move)
                self._is_check = True
            # pinned checks
            elif pinned_pieces and moving_piece.get_name() != "k":
                if starting_square not in pinned_pieces:
                    for move in initial_valid_piece_moves:
                        valid_moves.append(move)
                elif starting_square in pinned_pieces:
                    for move in initial_valid_piece_moves:

                        temp = self.board[move[0]][move[1]]
                        self.board[move[0]][move[1]] = moving_piece
                        self.board[current_row][current_col] = Player.EMPTY
                        if not self.check_for_check(king_location, moving_piece.get_player())[0]:
                            valid_moves.append(move)
                        self.board[current_row][current_col] = moving_piece
                        self.board[move[0]][move[1]] = temp
            else:
                if moving_piece.get_name() == "k":
                    for move in initial_valid_piece_moves:
                        temp = self.board[current_row][current_col]
                        temp2 = self.board[move[0]][move[1]]
                        self.board[current_row][current_col] = Player.EMPTY
                        self.board[move[0]][move[1]] = temp
                        if not self.check_for_check(move, moving_piece.get_player())[0]:
                            valid_moves.append(move)
                        self.board[current_row][current_col] = temp
                        self.board[move[0]][move[1]] = temp2
                else:
                    for move in initial_valid_piece_moves:
                        valid_moves.append(move)
            # if not valid_moves:
            #     if self._is_check:
            #         self.checkmate = True
            #     else:
            #         self.stalemate = True
            # else:
            #     self.checkmate = False
            #     self.stalemate = False
            return valid_moves
        else:
            return None

    # 0 if white lost, 1 if black lost, 2 if stalemate, 3 if not game over
    def checkmate_stalemate_checker(self):
        all_white_moves = self.get_all_legal_moves(Player.PLAYER_1)
        all_black_moves = self.get_all_legal_moves(Player.PLAYER_2)
        if self._is_check and self.whose_turn() and not all_white_moves:
            print("white lost")
            return 0
        elif self._is_check and not self.whose_turn() and not all_black_moves:
            print("black lost")
            return 1
        elif not all_white_moves and not all_black_moves:
            return 2
        else:
            return 3

    def get_all_legal_moves(self, player):
        # _all_valid_moves = [[], []]
        # for row in range(0, 8):
        #     for col in range(0, 8):
        #         if self.is_valid_piece(row, col) and self.get_piece(row, col).is_player(player):
        #             valid_moves = self.get_valid_moves((row, col))
        #             if valid_moves:
        #                 _all_valid_moves[0].append((row, col))
        #                 _all_valid_moves[1].append(valid_moves)
        _all_valid_moves = []
        for row in range(0, 8):
            for col in range(0, 8):
                if self.is_valid_piece(row, col) and self.get_piece(row, col).is_player(player):
                    valid_moves = self.get_valid_moves((row, col))
                    for move in valid_moves:
                        _all_valid_moves.append(((row, col), move))
        return _all_valid_moves

    def king_can_castle_left(self, player):
        if player is Player.PLAYER_1:
            return self.white_king_can_castle[0] and self.white_king_can_castle[1] and \
                   self.get_piece(0, 1) is Player.EMPTY and self.get_piece(0, 2) is Player.EMPTY and not self._is_check
        else:
            return self.black_king_can_castle[0] and self.black_king_can_castle[1] and \
                   self.get_piece(7, 1) is Player.EMPTY and self.get_piece(7, 2) is Player.EMPTY and not self._is_check

    def king_can_castle_right(self, player):
        if player is Player.PLAYER_1:
            return self.white_king_can_castle[0] and self.white_king_can_castle[2] and \
                   self.get_piece(0, 6) is Player.EMPTY and self.get_piece(0, 5) is Player.EMPTY and not self._is_check
        else:
            return self.black_king_can_castle[0] and self.black_king_can_castle[2] and \
                   self.get_piece(7, 6) is Player.EMPTY and self.get_piece(7, 5) is Player.EMPTY and not self._is_check

    def promote_pawn(self, starting_square, moved_piece, ending_square):
        while True:
            new_piece_name = input("Thăng cấp tốt thành (r, n, b, q):\n")
            piece_classes = {"r": Rook, "n": Knight, "b": Bishop, "q": Queen}
            if new_piece_name in piece_classes:
                move = chess_move(starting_square, ending_square, self, self._is_check)
                # Tạo quân cờ mới thay thế tốt
                new_piece = piece_classes[new_piece_name](new_piece_name, ending_square[0],
                                                          ending_square[1], moved_piece.get_player())
                self.board[ending_square[0]][ending_square[1]] = new_piece
                self.board[moved_piece.get_row_number()][moved_piece.get_col_number()] = Player.EMPTY
                moved_piece.change_row_number(ending_square[0])
                moved_piece.change_col_number(ending_square[1])
                move.pawn_promotion_move(new_piece)
                self.move_log.append(move)
                break
            else:
                print("Vui lòng chọn 1 trong 4: r, n, b, q.\n")

    def promote_pawn_ai(self, starting_square, moved_piece, ending_square):
        move = chess_move(starting_square, ending_square, self, self._is_check)
        # AI luôn thăng cấp tốt thành hậu (queen)
        new_piece = Queen("q", ending_square[0], ending_square[1], moved_piece.get_player())
        self.board[ending_square[0]][ending_square[1]] = new_piece
        self.board[moved_piece.get_row_number()][moved_piece.get_col_number()] = Player.EMPTY
        moved_piece.change_row_number(ending_square[0])
        moved_piece.change_col_number(ending_square[1])
        move.pawn_promotion_move(new_piece)
        self.move_log.append(move)

    def promote_pawn_gui(self, starting_square, moved_piece, ending_square, new_piece_name):
        """Phong cấp tốt dựa trên lựa chọn từ GUI (new_piece_name: 'q', 'r', 'n', 'b')"""
        piece_classes = {"r": Rook, "n": Knight, "b": Bishop, "q": Queen}
        if new_piece_name in piece_classes:
            move = chess_move(starting_square, ending_square, self, self._is_check)
            new_piece = piece_classes[new_piece_name](new_piece_name, ending_square[0], ending_square[1], moved_piece.get_player())
            self.board[ending_square[0]][ending_square[1]] = new_piece
            self.board[moved_piece.get_row_number()][moved_piece.get_col_number()] = Player.EMPTY
            moved_piece.change_row_number(ending_square[0])
            moved_piece.change_col_number(ending_square[1])
            move.pawn_promotion_move(new_piece)
            self.move_log.append(move)

    # have to fix en passant for ai
    def can_en_passant(self, current_square_row, current_square_col):
        return False
        # if is_ai:
        #     return False
        # else:
        #     return self.can_en_passant_bool and current_square_row == self.previous_piece_en_passant()[0] \
        #            and abs(current_square_col - self.previous_piece_en_passant()[1]) == 1

    def previous_piece_en_passant(self):
        return self._en_passant_previous

    # Move a piece
    def move_piece(self, starting_square, ending_square, is_ai):
        """
        Di chuyển quân cờ từ ô bắt đầu đến ô kết thúc
        Giải thích dễ hiểu:
        - Kiểm tra nước đi hợp lệ
        - Xử lý các trường hợp đặc biệt: nhập thành, phong cấp tốt, bắt tốt qua đường (en passant)
        - Cập nhật trạng thái bàn cờ, lượt chơi, lịch sử nước đi
        """
        current_square_row = starting_square[0]  # The integer row value of the starting square
        current_square_col = starting_square[1]  # The integer col value of the starting square
        next_square_row = ending_square[0]  # The integer row value of the ending square
        next_square_col = ending_square[1]  # The integer col value of the ending square

        if self.is_valid_piece(current_square_row, current_square_col) and \
                (((self.whose_turn() and self.get_piece(current_square_row, current_square_col).is_player(
                    Player.PLAYER_1)) or
                  (not self.whose_turn() and self.get_piece(current_square_row, current_square_col).is_player(
                      Player.PLAYER_2)))):

            # Quân cờ tại ô bắt đầu
            moving_piece = self.get_piece(current_square_row, current_square_col)

            valid_moves = self.get_valid_moves(starting_square)

            temp = True

            if ending_square in valid_moves:
                moved_to_piece = self.get_piece(next_square_row, next_square_col)
                if moving_piece.get_name() == "k":
                    if moving_piece.is_player(Player.PLAYER_1):
                        if moved_to_piece == Player.EMPTY and next_square_col == 1 and self.king_can_castle_left(
                                moving_piece.get_player()):
                            move = chess_move(starting_square, ending_square, self, self._is_check)
                            move.castling_move((0, 0), (0, 2), self)
                            self.move_log.append(move)

                            # Di chuyển xe
                            self.get_piece(0, 0).change_col_number(2)

                            self.board[0][2] = self.board[0][0]
                            self.board[0][0] = Player.EMPTY

                            self.white_king_can_castle[0] = False
                            self.white_king_can_castle[1] = False

                        elif moved_to_piece == Player.EMPTY and next_square_col == 5 and self.king_can_castle_right(
                                moving_piece.get_player()):
                            move = chess_move(starting_square, ending_square, self, self._is_check)
                            move.castling_move((0, 7), (0, 4), self)
                            self.move_log.append(move)
                            # Di chuyển xe
                            self.get_piece(0, 7).change_col_number(4)

                            self.board[0][4] = self.board[0][7]
                            self.board[0][7] = Player.EMPTY

                            self.white_king_can_castle[0] = False
                            self.white_king_can_castle[2] = False
                        else:
                            move = chess_move(starting_square, ending_square, self, self._is_check)
                            self.move_log.append(move)
                            self.white_king_can_castle[0] = False
                        self._white_king_location = (next_square_row, next_square_col)
                    else:
                        if moved_to_piece == Player.EMPTY and next_square_col == 1 and self.king_can_castle_left(
                                moving_piece.get_player()):
                            move = chess_move(starting_square, ending_square, self, self._is_check)
                            move.castling_move((7, 0), (7, 2), self)
                            self.move_log.append(move)

                            self.get_piece(7, 0).change_col_number(2)
                            # Di chuyển xe
                            self.board[7][2] = self.board[7][0]
                            self.board[7][0] = Player.EMPTY

                            self.black_king_can_castle[0] = False
                            self.black_king_can_castle[1] = False
                        elif moved_to_piece == Player.EMPTY and next_square_col == 5 and self.king_can_castle_right(
                                moving_piece.get_player()):
                            move = chess_move(starting_square, ending_square, self, self._is_check)
                            move.castling_move((7, 7), (7, 4), self)
                            self.move_log.append(move)

                            self.get_piece(0, 7).change_col_number(4)

                            # Di chuyển xe
                            self.board[7][4] = self.board[7][7]
                            self.board[7][7] = Player.EMPTY

                            self.black_king_can_castle[0] = False
                            self.black_king_can_castle[2] = False
                        else:
                            move = chess_move(starting_square, ending_square, self, self._is_check)
                            self.move_log.append(move)
                            self.black_king_can_castle[0] = False
                        self._black_king_location = (next_square_row, next_square_col)
                        # self.can_en_passant_bool = False  CÁI NÀY LÀ GÌ
                elif moving_piece.get_name() == "r":
                    if moving_piece.is_player(Player.PLAYER_1) and current_square_col == 0:
                        self.white_king_can_castle[1] = False
                    elif moving_piece.is_player(Player.PLAYER_1) and current_square_col == 7:
                        self.white_king_can_castle[2] = False
                    elif moving_piece.is_player(Player.PLAYER_2) and current_square_col == 0:
                        self.white_king_can_castle[1] = False
                    elif moving_piece.is_player(Player.PLAYER_2) and current_square_col == 7:
                        self.white_king_can_castle[2] = False
                    self.move_log.append(chess_move(starting_square, ending_square, self, self._is_check))
                    self.can_en_passant_bool = False
                # Thêm class nước đi ở đây
                elif moving_piece.get_name() == "p":
                    # Phong cấp tốt trắng
                    if moving_piece.is_player(Player.PLAYER_1) and next_square_row == 7:
                        if is_ai:
                            self.promote_pawn_ai(starting_square, moving_piece, ending_square)
                        else:
                            # Trả về yêu cầu chọn quân phong cấp cho GUI
                            return {
                                'promotion': True,
                                'color': 'white',
                                'from': starting_square,
                                'to': ending_square,
                                'player': Player.PLAYER_1
                            }
                        temp = False
                    # Phong cấp tốt đen
                    elif moving_piece.is_player(Player.PLAYER_2) and next_square_row == 0:
                        if is_ai:
                            self.promote_pawn_ai(starting_square, moving_piece, ending_square)
                        else:
                            # Trả về yêu cầu chọn quân phong cấp cho GUI
                            return {
                                'promotion': True,
                                'color': 'black',
                                'from': starting_square,
                                'to': ending_square,
                                'player': Player.PLAYER_2
                            }
                        temp = False
                    # Di chuyển tốt lên hai ô
                    # Vấn đề với tốt và en passant cho AI
                    elif abs(next_square_row - current_square_row) == 2 and current_square_col == next_square_col:
                        # print("move pawn forward")
                        self.move_log.append(chess_move(starting_square, ending_square, self, self._is_check))
                        # self.can_en_passant_bool = True
                        self._en_passant_previous = (next_square_row, next_square_col)
                    # en passant
                    elif abs(next_square_row - current_square_row) == 1 and abs(
                            current_square_col - next_square_col) == 1 and \
                            self.can_en_passant(current_square_row, current_square_col):
                        # print("en passant")
                        if moving_piece.is_player(Player.PLAYER_1):
                            move = chess_move(starting_square, ending_square, self, self._is_check)
                            move.en_passant_move(self.board[next_square_row - 1][next_square_col],
                                                 (next_square_row - 1, next_square_col))
                            self.move_log.append(move)
                            self.board[next_square_row - 1][next_square_col] = Player.EMPTY
                        else:
                            move = chess_move(starting_square, ending_square, self, self._is_check)
                            move.en_passant_move(self.board[next_square_row + 1][next_square_col],
                                                 (next_square_row + 1, next_square_col))
                            self.move_log.append(move)
                            self.board[next_square_row + 1][next_square_col] = Player.EMPTY
                    # Di chuyển lên một ô hoặc ăn quân
                    else:
                        self.move_log.append(chess_move(starting_square, ending_square, self, self._is_check))
                        self.can_en_passant_bool = False
                else:
                    self.move_log.append(chess_move(starting_square, ending_square, self, self._is_check))
                    self.can_en_passant_bool = False

                if temp:
                    moving_piece.change_row_number(next_square_row)
                    moving_piece.change_col_number(next_square_col)
                    self.board[next_square_row][next_square_col] = self.board[current_square_row][current_square_col]
                    self.board[current_square_row][current_square_col] = Player.EMPTY

                self.white_turn = not self.white_turn

            else:
                pass

    def undo_move(self):
        """
        Hoàn tác nước đi vừa thực hiện
        Giải thích dễ hiểu:
        - Lấy nước đi cuối cùng từ lịch sử
        - Đưa quân cờ về vị trí cũ, khôi phục quân bị ăn (nếu có)
        - Khôi phục trạng thái đặc biệt: nhập thành, phong cấp, en passant
        - Đảo lại lượt chơi
        """
        if self.move_log:
            undoing_move = self.move_log.pop()
            if undoing_move.castled is True:
                self.board[undoing_move.starting_square_row][
                    undoing_move.starting_square_col] = undoing_move.moving_piece
                self.board[undoing_move.ending_square_row][undoing_move.ending_square_col] = undoing_move.removed_piece
                self.get_piece(undoing_move.starting_square_row, undoing_move.starting_square_col).change_row_number(
                    undoing_move.starting_square_row)
                self.get_piece(undoing_move.starting_square_row, undoing_move.starting_square_col).change_col_number(
                    undoing_move.starting_square_col)

                self.board[undoing_move.rook_starting_square[0]][
                    undoing_move.rook_starting_square[1]] = undoing_move.moving_rook
                self.board[undoing_move.rook_ending_square[0]][undoing_move.rook_ending_square[1]] = Player.EMPTY
                undoing_move.moving_rook.change_row_number(undoing_move.rook_starting_square[0])
                undoing_move.moving_rook.change_col_number(undoing_move.rook_starting_square[1])
                if undoing_move.moving_piece is Player.PLAYER_1:
                    if undoing_move.rook_starting_square[1] == 0:
                        self.white_king_can_castle[0] = True
                        self.white_king_can_castle[1] = True
                    elif undoing_move.rook_starting_square[1] == 7:
                        self.white_king_can_castle[0] = True
                        self.white_king_can_castle[2] = True
                else:
                    if undoing_move.rook_starting_square[1] == 0:
                        self.black_king_can_castle[0] = True
                        self.black_king_can_castle[1] = True
                    elif undoing_move.rook_starting_square[1] == 7:
                        self.black_king_can_castle[0] = True
                        self.black_king_can_castle[2] = True
            elif undoing_move.pawn_promoted is True:
                self.board[undoing_move.starting_square_row][
                    undoing_move.starting_square_col] = undoing_move.moving_piece
                self.get_piece(undoing_move.starting_square_row, undoing_move.starting_square_col).change_row_number(
                    undoing_move.starting_square_row)
                self.get_piece(undoing_move.starting_square_row, undoing_move.starting_square_col).change_col_number(
                    undoing_move.starting_square_col)

                self.board[undoing_move.ending_square_row][undoing_move.ending_square_col] = undoing_move.removed_piece
                if undoing_move.removed_piece != Player.EMPTY:
                    self.get_piece(undoing_move.ending_square_row, undoing_move.ending_square_col).change_row_number(
                        undoing_move.ending_square_row)
                    self.get_piece(undoing_move.ending_square_row, undoing_move.ending_square_col).change_col_number(
                        undoing_move.ending_square_col)
            elif undoing_move.en_passaned is True:
                self.board[undoing_move.starting_square_row][
                    undoing_move.starting_square_col] = undoing_move.moving_piece
                self.board[undoing_move.ending_square_row][undoing_move.ending_square_col] = undoing_move.removed_piece
                self.get_piece(undoing_move.starting_square_row, undoing_move.starting_square_col).change_row_number(
                    undoing_move.starting_square_row)
                self.get_piece(undoing_move.starting_square_row, undoing_move.starting_square_col).change_col_number(
                    undoing_move.starting_square_col)

                self.board[undoing_move.en_passant_eaten_square[0]][
                    undoing_move.en_passant_eaten_square[1]] = undoing_move.en_passant_eaten_piece
                self.can_en_passant_bool = True
            else:
                self.board[undoing_move.starting_square_row][
                    undoing_move.starting_square_col] = undoing_move.moving_piece
                self.get_piece(undoing_move.starting_square_row, undoing_move.starting_square_col).change_row_number(
                    undoing_move.starting_square_row)
                self.get_piece(undoing_move.starting_square_row, undoing_move.starting_square_col).change_col_number(
                    undoing_move.starting_square_col)

                self.board[undoing_move.ending_square_row][undoing_move.ending_square_col] = undoing_move.removed_piece
                if undoing_move.removed_piece != Player.EMPTY:
                    self.get_piece(undoing_move.ending_square_row, undoing_move.ending_square_col).change_row_number(
                        undoing_move.ending_square_row)
                    self.get_piece(undoing_move.ending_square_row, undoing_move.ending_square_col).change_col_number(
                        undoing_move.ending_square_col)

            self.white_turn = not self.white_turn
            # if undoing_move.in_check:
            #     self._is_check = True
            if undoing_move.moving_piece.get_name() == 'k' and undoing_move.moving_piece.get_player() is Player.PLAYER_1:
                self._white_king_location = (undoing_move.starting_square_row, undoing_move.starting_square_col)
            elif undoing_move.moving_piece.get_name() == 'k' and undoing_move.moving_piece.get_player() is Player.PLAYER_2:
                self._black_king_location = (undoing_move.starting_square_row, undoing_move.starting_square_col)

            return undoing_move
        else:
            print("Back to the beginning!")

    # true if white, false if black
    def whose_turn(self):
        return self.white_turn

    '''
    kiểm tra chiếu ngay lập tức
    - kiểm tra 8 hướng và 8 ô theo kiểu di chuyển của mã
    kiểm tra ghim
    - bất kỳ quân cờ nào bị chặn bởi quân cờ phía trên là bị ghim

     - nếu bị chiếu ngay lập tức, thay đổi giá trị check thành true
     - liệt kê các nước đi hợp lệ để tránh chiếu nhưng không loại bỏ ghim
     - nếu không có nước đi hợp lệ để tránh chiếu, chiếu hết
    '''

    def check_for_check(self, king_location, player):
        """
        Kiểm tra xem vua của người chơi có đang bị chiếu không, đồng thời xác định các quân bị ghim và quân đang chiếu
        Giải thích dễ hiểu:
        - Dò 8 hướng (trên, dưới, trái, phải, chéo) quanh vua để tìm quân đối phương có thể chiếu
        - Nếu có quân ta chắn giữa vua và quân đối phương, đó là quân bị ghim (pin)
        - Kiểm tra các ô di chuyển kiểu mã (knight) quanh vua
        - Trả về danh sách quân đang chiếu, quân bị ghim, quân đối phương có thể chiếu
        """
        _checks = []
        _pins = []
        _pins_check = []

        king_location_row = king_location[0]
        king_location_col = king_location[1]

        _up = 1
        _down = 1
        _left = 1
        _right = 1

        # Left of the king
        _possible_pin = ()
        while king_location_col - _left >= 0 and self.get_piece(king_location_row,
                                                                king_location_col - _left) is not None:
            if self.is_valid_piece(king_location_row, king_location_col - _left) and \
                    self.get_piece(king_location_row, king_location_col - _left).is_player(player) and \
                    self.get_piece(king_location_row, king_location_col - _left).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row, king_location_col - _left)
                else:
                    break
            elif self.is_valid_piece(king_location_row, king_location_col - _left) and \
                    not self.get_piece(king_location_row, king_location_col - _left).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row,
                                                                                king_location_col - _left).get_valid_piece_takes(
                            self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row, king_location_col - _left))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row,
                                                                                king_location_col - _left).get_valid_piece_takes(
                            self):
                        _checks.append((king_location_row, king_location_col - _left))
                break
            _left += 1

        # right of the king
        _possible_pin = ()
        while king_location_col + _right < 8 and self.get_piece(king_location_row,
                                                                king_location_col + _right) is not None:
            if self.is_valid_piece(king_location_row, king_location_col + _right) and \
                    self.get_piece(king_location_row, king_location_col + _right).is_player(player) and \
                    self.get_piece(king_location_row, king_location_col + _right).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row, king_location_col + _right)
                else:
                    break
            elif self.is_valid_piece(king_location_row, king_location_col + _right) and \
                    not self.get_piece(king_location_row, king_location_col + _right).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row,
                                                                                king_location_col + _right).get_valid_piece_takes(
                            self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row, king_location_col + _right))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row,
                                                                                king_location_col + _right).get_valid_piece_takes(
                        self):
                        _checks.append((king_location_row, king_location_col + _right))
                break
            _right += 1

        # below the king
        _possible_pin = ()
        while king_location_row + _down < 8 and self.get_piece(king_location_row + _down,
                                                               king_location_col) is not None:
            if self.is_valid_piece(king_location_row + _down, king_location_col) and \
                    self.get_piece(king_location_row + _down, king_location_col).is_player(player) and \
                    self.get_piece(king_location_row + _down, king_location_col).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row + _down, king_location_col)
                else:
                    break
            elif self.is_valid_piece(king_location_row + _down, king_location_col) and \
                    not self.get_piece(king_location_row + _down, king_location_col).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row + _down,
                                                                                king_location_col).get_valid_piece_takes(
                            self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row + _down, king_location_col))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row + _down,
                                                                                king_location_col).get_valid_piece_takes(
                        self):
                        _checks.append((king_location_row + _down, king_location_col))
                break
            _down += 1

        # above the king
        _possible_pin = ()
        while king_location_row - _up >= 0 and self.get_piece(king_location_row - _up, king_location_col) is not None:
            if self.is_valid_piece(king_location_row - _up, king_location_col) and \
                    self.get_piece(king_location_row - _up, king_location_col).is_player(player) and \
                    self.get_piece(king_location_row - _up, king_location_col).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row - _up, king_location_col)
                else:
                    break
            elif self.is_valid_piece(king_location_row - _up, king_location_col) and \
                    not self.get_piece(king_location_row - _up, king_location_col).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row - _up,
                                                                                king_location_col).get_valid_piece_takes(
                            self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row - _up, king_location_col))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row - _up,
                                                                                king_location_col).get_valid_piece_takes(
                            self):
                        _checks.append((king_location_row - _up, king_location_col))
                break
            _up += 1

        # left up
        _up = 1
        _left = 1
        _possible_pin = ()
        while king_location_col - _left >= 0 and king_location_row - _up >= 0 and \
                self.get_piece(king_location_row - _up, king_location_col - _left) is not None:
            if self.is_valid_piece(king_location_row - _up, king_location_col - _left) and \
                    self.get_piece(king_location_row - _up, king_location_col - _left).is_player(player) and \
                    self.get_piece(king_location_row - _up, king_location_col - _left).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row - _up, king_location_col - _left)
                else:
                    break
            elif self.is_valid_piece(king_location_row - _up, king_location_col - _left) and \
                    not self.get_piece(king_location_row - _up, king_location_col - _left).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row - _up,
                                                                                king_location_col - _left).get_valid_piece_takes(
                            self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row - _up, king_location_col - _left))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row - _up,
                                                                                king_location_col - _left).get_valid_piece_takes(
                        self):
                        _checks.append((king_location_row - _up, king_location_col - _left))
                break
            _left += 1
            _up += 1

        # right up
        _up = 1
        _right = 1
        _possible_pin = ()
        while king_location_col + _right < 8 and king_location_row - _up >= 0 and \
                self.get_piece(king_location_row - _up, king_location_col + _right) is not None:
            if self.is_valid_piece(king_location_row - _up, king_location_col + _right) and \
                    self.get_piece(king_location_row - _up, king_location_col + _right).is_player(player) and \
                    self.get_piece(king_location_row - _up, king_location_col + _right).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row - _up, king_location_col + _right)
                else:
                    break
            elif self.is_valid_piece(king_location_row - _up, king_location_col + _right) and \
                    not self.get_piece(king_location_row - _up, king_location_col + _right).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row - _up,
                                                                                king_location_col + _right).get_valid_piece_takes(
                            self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row - _up, king_location_col + _right))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row - _up,
                                                                                king_location_col + _right).get_valid_piece_takes(
                        self):
                        _checks.append((king_location_row - _up, king_location_col + _right))
                break
            _right += 1
            _up += 1

        # left down
        _down = 1
        _left = 1
        _possible_pin = ()
        while king_location_col - _left >= 0 and king_location_row + _down < 8 and \
                self.get_piece(king_location_row + _down, king_location_col - _left) is not None:
            if self.is_valid_piece(king_location_row + _down, king_location_col - _left) and \
                    self.get_piece(king_location_row + _down, king_location_col - _left).is_player(player) and \
                    self.get_piece(king_location_row + _down, king_location_col - _left).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row + _down, king_location_col - _left)
                else:
                    break
            elif self.is_valid_piece(king_location_row + _down, king_location_col - _left) and \
                    not self.get_piece(king_location_row + _down, king_location_col - _left).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row + _down,
                                                                                king_location_col - _left).get_valid_piece_takes(
                            self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row + _down, king_location_col - _left))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row + _down,
                                                                                king_location_col - _left).get_valid_piece_takes(
                        self):
                        _checks.append((king_location_row + _down, king_location_col - _left))
                break
            _left += 1
            _down += 1

        # right down
        _down = 1
        _right = 1
        _possible_pin = ()
        while king_location_col + _right < 8 and king_location_row + _down < 8 and \
                self.get_piece(king_location_row + _down, king_location_col + _right) is not None:
            if self.is_valid_piece(king_location_row + _down, king_location_col + _right) and \
                    self.get_piece(king_location_row + _down, king_location_col + _right).is_player(player) and \
                    self.get_piece(king_location_row + _down, king_location_col + _right).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row + _down, king_location_col + _right)
                else:
                    break
            elif self.is_valid_piece(king_location_row + _down, king_location_col + _right) and \
                    not self.get_piece(king_location_row + _down, king_location_col + _right).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row + _down,
                                                                                king_location_col + _right).get_valid_piece_takes(
                            self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row + _down, king_location_col + _right))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in self.get_piece(king_location_row + _down,
                                                                                king_location_col + _right).get_valid_piece_takes(
                        self):
                        _checks.append((king_location_row + _down, king_location_col + _right))
                break
            _right += 1
            _down += 1

        # knights
        row_change = [-2, -2, -1, -1, +1, +1, +2, +2]
        col_change = [-1, +1, -2, +2, -2, +2, +1, -1]
        for i in range(0, 8):
            if self.is_valid_piece(king_location_row + row_change[i], king_location_col + col_change[i]) and \
                    not self.get_piece(king_location_row + row_change[i], king_location_col + col_change[
                        i]).is_player(player):
                if (king_location_row, king_location_col) in self.get_piece(king_location_row + row_change[i],
                                                                            king_location_col + col_change[
                                                                                i]).get_valid_piece_takes(self):
                    _checks.append((king_location_row + row_change[i], king_location_col + col_change[i]))
        return [_checks, _pins, _pins_check]


class chess_move():
    def __init__(self, starting_square, ending_square, game_state, in_check):
        self.starting_square_row = starting_square[0]
        self.starting_square_col = starting_square[1]
        self.moving_piece = game_state.get_piece(self.starting_square_row, self.starting_square_col)
        self.in_check = in_check

        self.ending_square_row = ending_square[0]
        self.ending_square_col = ending_square[1]
        if game_state.is_valid_piece(self.ending_square_row, self.ending_square_col):
            self.removed_piece = game_state.get_piece(self.ending_square_row, self.ending_square_col)
        else:
            self.removed_piece = Player.EMPTY

        self.castled = False
        self.rook_starting_square = None
        self.rook_ending_square = None
        self.moving_rook = None

        self.pawn_promoted = False
        self.replacement_piece = None

        self.en_passaned = False
        self.en_passant_eaten_piece = None
        self.en_passant_eaten_square = None

    def castling_move(self, rook_starting_square, rook_ending_square, game_state):
        self.castled = True
        self.rook_starting_square = rook_starting_square
        self.rook_ending_square = rook_ending_square
        self.moving_rook = game_state.get_piece(rook_starting_square[0], rook_starting_square[1])

    def pawn_promotion_move(self, new_piece):
        self.pawn_promoted = True
        self.replacement_piece = new_piece

    def en_passant_move(self, eaten_piece, eaten_piece_square):
        self.en_passaned = True
        self.en_passant_eaten_piece = eaten_piece
        self.en_passant_eaten_square = eaten_piece_square

    def get_captured_piece(self):
        # Nếu là nước en passant, trả về quân bị ăn qua đường en passant
        if self.en_passaned and self.en_passant_eaten_piece is not None:
            return self.en_passant_eaten_piece
        # Nếu là nước đi thường, trả về quân bị ăn ở ô đích
        if self.removed_piece is not None and self.removed_piece != Player.EMPTY:
            return self.removed_piece
        return None

    def get_moving_piece(self):
        return self.moving_piece
