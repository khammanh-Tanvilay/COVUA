#
# Lớp AI cho trò chơi cờ vua
# Sử dụng thuật toán minimax và alpha-beta pruning để tìm nước đi tốt nhất
#
# TODO: Chuyển đổi undo moves sang cấu trúc dữ liệu stack
import chess_engine
from enums import Player


class chess_ai:
    """
    Lớp AI cho trò chơi cờ vua
    Sử dụng thuật toán minimax với alpha-beta pruning để đánh giá bàn cờ
    và tìm nước đi tốt nhất cho AI
    """
    
    def minimax_white(self, game_state, depth, alpha, beta, maximizing_player, player_color, root_depth=None):
        """
        Thuật toán minimax cho quân trắng (AI)
        
        Args:
            game_state: Trạng thái hiện tại của bàn cờ
            depth: Độ sâu tìm kiếm
            alpha: Giá trị alpha cho alpha-beta pruning
            beta: Giá trị beta cho alpha-beta pruning
            maximizing_player: True nếu đang tối đa hóa điểm số
            player_color: Màu của người chơi hiện tại
            root_depth: Độ sâu gốc của cây tìm kiếm, mặc định None
        """
        if root_depth is None:
            root_depth = depth
        csc = game_state.checkmate_stalemate_checker()
        
        # Kiểm tra các trạng thái kết thúc trò chơi
        if maximizing_player:
            if csc == 0:  # Quân trắng thắng
                return 5000000
            elif csc == 1:  # Quân đen thắng
                return -5000000
            elif csc == 2:  # Hòa
                return 100
        elif not maximizing_player:
            if csc == 1:  # Quân đen thắng
                return 5000000
            elif csc == 0:  # Quân trắng thắng
                return -5000000
            elif csc == 2:  # Hòa
                return 100

        # Điều kiện dừng: đạt độ sâu tối đa hoặc trò chơi kết thúc
        if depth <= 0 or csc != 3:
            return self.evaluate_board(game_state, Player.PLAYER_1)

        if maximizing_player:
            max_evaluation = -10000000
            all_possible_moves = game_state.get_all_legal_moves("black")
            
            for move_pair in all_possible_moves:
                # Thực hiện nước đi
                game_state.move_piece(move_pair[0], move_pair[1], True)
                # Đánh giá nước đi này
                evaluation = self.minimax_white(game_state, depth - 1, alpha, beta, False, "white", root_depth)
                # Hoàn tác nước đi
                game_state.undo_move()

                # Cập nhật giá trị tốt nhất
                if max_evaluation < evaluation:
                    max_evaluation = evaluation
                    best_possible_move = move_pair
                
                # Alpha-beta pruning
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
                    
            # Trả về nước đi tốt nhất ở độ sâu gốc, ngược lại trả về điểm số
            if depth == root_depth:
                return best_possible_move
            else:
                return max_evaluation
        else:
            min_evaluation = 10000000
            all_possible_moves = game_state.get_all_legal_moves("white")
            
            for move_pair in all_possible_moves:
                # Thực hiện nước đi
                game_state.move_piece(move_pair[0], move_pair[1], True)
                # Đánh giá nước đi này
                evaluation = self.minimax_white(game_state, depth - 1, alpha, beta, True, "black", root_depth)
                # Hoàn tác nước đi
                game_state.undo_move()

                # Cập nhật giá trị tốt nhất
                if min_evaluation > evaluation:
                    min_evaluation = evaluation
                    best_possible_move = move_pair
                
                # Alpha-beta pruning
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
                    
            # Trả về nước đi tốt nhất ở độ sâu gốc, ngược lại trả về điểm số
            if depth == root_depth:
                return best_possible_move
            else:
                return min_evaluation

    def minimax_black(self, game_state, depth, alpha, beta, maximizing_player, player_color, root_depth=None):
        """
        Thuật toán minimax cho quân đen (AI)
        Tương tự minimax_white nhưng đánh giá từ góc nhìn của quân đen
        """
        if root_depth is None:
            root_depth = depth
        csc = game_state.checkmate_stalemate_checker()
        
        # Kiểm tra các trạng thái kết thúc trò chơi
        if maximizing_player:
            if csc == 1:  # Quân đen thắng
                return 5000000
            elif csc == 0:  # Quân trắng thắng
                return -5000000
            elif csc == 2:  # Hòa
                return 100
        elif not maximizing_player:
            if csc == 0:  # Quân trắng thắng
                return 5000000
            elif csc == 1:  # Quân đen thắng
                return -5000000
            elif csc == 2:  # Hòa
                return 100

        # Điều kiện dừng: đạt độ sâu tối đa hoặc trò chơi kết thúc
        if depth <= 0 or csc != 3:
            return self.evaluate_board(game_state, Player.PLAYER_2)

        if maximizing_player:
            max_evaluation = -10000000
            all_possible_moves = game_state.get_all_legal_moves("white")
            
            for move_pair in all_possible_moves:
                # Thực hiện nước đi
                game_state.move_piece(move_pair[0], move_pair[1], True)
                # Đánh giá nước đi này
                evaluation = self.minimax_black(game_state, depth - 1, alpha, beta, False, "black", root_depth)
                # Hoàn tác nước đi
                game_state.undo_move()

                # Cập nhật giá trị tốt nhất
                if max_evaluation < evaluation:
                    max_evaluation = evaluation
                    best_possible_move = move_pair
                
                # Alpha-beta pruning
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
                    
            # Trả về nước đi tốt nhất ở độ sâu gốc, ngược lại trả về điểm số
            if depth == root_depth:
                return best_possible_move
            else:
                return max_evaluation
        else:
            min_evaluation = 10000000
            all_possible_moves = game_state.get_all_legal_moves("black")
            
            for move_pair in all_possible_moves:
                # Thực hiện nước đi
                game_state.move_piece(move_pair[0], move_pair[1], True)
                # Đánh giá nước đi này
                evaluation = self.minimax_black(game_state, depth - 1, alpha, beta, True, "white", root_depth)
                # Hoàn tác nước đi
                game_state.undo_move()

                # Cập nhật giá trị tốt nhất
                if min_evaluation > evaluation:
                    min_evaluation = evaluation
                    best_possible_move = move_pair
                
                # Alpha-beta pruning
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
                    
            # Trả về nước đi tốt nhất ở độ sâu gốc, ngược lại trả về điểm số
            if depth == root_depth:
                return best_possible_move
            else:
                return min_evaluation

    def evaluate_board(self, game_state, player):
        """
        Đánh giá trạng thái bàn cờ
        Tính tổng điểm số của tất cả quân cờ trên bàn
        
        Args:
            game_state: Trạng thái hiện tại của bàn cờ
            player: Người chơi để đánh giá (quan điểm của ai)
        """
        evaluation_score = 0
        for row in range(0, 8):
            for col in range(0, 8):
                if game_state.is_valid_piece(row, col):
                    evaluated_piece = game_state.get_piece(row, col)
                    evaluation_score += self.get_piece_value(evaluated_piece, player)
        return evaluation_score

    def get_piece_value(self, piece, player):
        """
        Lấy giá trị điểm số của một quân cờ
        
        Args:
            piece: Quân cờ cần đánh giá
            player: Người chơi để đánh giá (quan điểm của ai)
        """
        if player is Player.PLAYER_1:  # Đánh giá từ góc nhìn quân trắng
            if piece.is_player("black"):  # Quân đen (đối thủ)
                if piece.get_name() == "k":  # Vua
                    return 1000
                elif piece.get_name() == "q":  # Hậu
                    return 100
                elif piece.get_name() == "r":  # Xe
                    return 50
                elif piece.get_name() == "b":  # Tượng
                    return 30
                elif piece.get_name() == "n":  # Mã
                    return 30
                elif piece.get_name() == "p":  # Tốt
                    return 10
            else:  # Quân trắng (đồng minh)
                if piece.get_name() == "k":  # Vua
                    return -1000
                elif piece.get_name() == "q":  # Hậu
                    return -100
                elif piece.get_name() == "r":  # Xe
                    return -50
                elif piece.get_name() == "b":  # Tượng
                    return -30
                elif piece.get_name() == "n":  # Mã
                    return -30
                elif piece.get_name() == "p":  # Tốt
                    return -10
        else:  # Đánh giá từ góc nhìn quân đen
            if piece.is_player("white"):  # Quân trắng (đối thủ)
                if piece.get_name() == "k":  # Vua
                    return 1000
                elif piece.get_name() == "q":  # Hậu
                    return 100
                elif piece.get_name() == "r":  # Xe
                    return 50
                elif piece.get_name() == "b":  # Tượng
                    return 30
                elif piece.get_name() == "n":  # Mã
                    return 30
                elif piece.get_name() == "p":  # Tốt
                    return 10
            else:  # Quân đen (đồng minh)
                if piece.get_name() == "k":  # Vua
                    return -1000
                elif piece.get_name() == "q":  # Hậu
                    return -100
                elif piece.get_name() == "r":  # Xe
                    return -50
                elif piece.get_name() == "b":  # Tượng
                    return -30
                elif piece.get_name() == "n":  # Mã
                    return -30
                elif piece.get_name() == "p":  # Tốt
                    return -10