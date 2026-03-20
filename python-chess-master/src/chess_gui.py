import chess_engine
import pygame as py
import os
import time
import datetime
import sys
import copy

import ai_engine
from enums import Player
# Thêm import hàm vẽ mặt
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from face_pixel.faces import draw_baby_face, draw_adult_face, draw_old_face

"""Các biến cấu hình cho giao diện"""
STATUS_BAR_HEIGHT = 50  # Chiều cao thanh trạng thái
WIDTH = HEIGHT = 565    # Chiều rộng và chiều cao của bàn cờ
BOARD_WIDTH = 565       # Chiều rộng bàn cờ
BOARD_HEIGHT = 565      # Chiều cao bàn cờ
SIDEBAR_WIDTH = 200     # Chiều rộng cột bên phải
TOTAL_WIDTH = BOARD_WIDTH + SIDEBAR_WIDTH  # Tổng chiều rộng cửa sổ
DIMENSION = 8          # Kích thước bàn cờ (8x8)
SQ_SIZE = HEIGHT // DIMENSION  # Kích thước mỗi ô trên bàn cờ
MAX_FPS = 60          # FPS cho các hiệu ứng animation
IMAGES = {}           # Dictionary chứa hình ảnh các quân cờ
colors = [(240, 217, 181), (181, 136, 99)]  # Màu gỗ sáng và tối cho bàn cờ

# TODO: AI cho quân đen đã được hoàn thiện. Cần phát triển tương tự cho các chế độ khác

PADDING_LEFT = 28   # Đủ cho số 8-1
PADDING_BOTTOM = 28 # Đủ cho chữ a-h
# Xóa PADDING_TOP

# Cập nhật lại TOTAL_WIDTH, TOTAL_HEIGHT
TOTAL_WIDTH = PADDING_LEFT + BOARD_WIDTH + SIDEBAR_WIDTH
TOTAL_HEIGHT = BOARD_HEIGHT + PADDING_BOTTOM

def load_images():
    """
    Tải hình ảnh cho tất cả các quân cờ
    Hình ảnh được scale nhỏ hơn kích thước ô (80%)
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(current_dir, "..", "images")
    icon_size = int(SQ_SIZE * 0.8)
    for p in Player.PIECES:
        image_path = os.path.join(images_dir, p + ".png")
        IMAGES[p] = py.transform.smoothscale(py.image.load(image_path), (icon_size, icon_size))

def draw_game_state(screen, game_state, valid_moves, square_selected, hint_valid_moves=None, best_moves_with_scores=None, board_flipped=False):
    """
    Vẽ toàn bộ bàn cờ với các quân cờ
    
    Args:
        screen: Màn hình pygame
        game_state: Trạng thái hiện tại của trò chơi cờ vua
        valid_moves: Danh sách các nước đi hợp lệ
        square_selected: Ô được chọn hiện tại
        hint_valid_moves: Danh sách các ô hợp lệ để highlight khi nhấn Hint
        best_moves_with_scores: Danh sách [(move, score)] nước đi tốt nhất và điểm số
    """
    # Fill nền trắng toàn bộ
    screen.fill((255, 255, 255))
    draw_squares(screen, board_flipped)
    draw_labels(screen, board_flipped)
    highlight_square(screen, game_state, valid_moves, square_selected, board_flipped)  # Đánh dấu ô được chọn và nước đi hợp lệ
    # Highlight các ô hợp lệ khi nhấn Hint
    if hint_valid_moves:
        for move in hint_valid_moves:
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(120)
            s.fill(py.Color(30, 144, 255))  # Xanh dương nhạt
            r, c = move
            if board_flipped:
                r = 7 - r
            screen.blit(s, (PADDING_LEFT + c * SQ_SIZE, r * SQ_SIZE))
    # Highlight các ô nước đi tốt nhất (màu cam)
    if best_moves_with_scores:
        for move, score in best_moves_with_scores:
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(180)
            s.fill(py.Color(255, 140, 0))  # Cam
            r, c = move
            if board_flipped:
                r = 7 - r
            screen.blit(s, (PADDING_LEFT + c * SQ_SIZE, r * SQ_SIZE))
    # Highlight các ô mà nếu bạn đi vào, đối phương có thể ăn lại quân bạn ngay lập tức
    if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]) and hint_valid_moves:
        threatened_next_moves = set()
        my_piece = game_state.get_piece(square_selected[0], square_selected[1])
        my_player = my_piece.get_player()
        opponent_player = Player.PLAYER_2 if my_player == Player.PLAYER_1 else Player.PLAYER_1
        for move in hint_valid_moves:
            temp_state = copy.deepcopy(game_state)
            temp_state.move_piece(square_selected, move, True)
            # Sau khi đi, kiểm tra đối phương có thể ăn lại quân mình không
            for r in range(8):
                for c in range(8):
                    if temp_state.is_valid_piece(r, c):
                        piece = temp_state.get_piece(r, c)
                        if piece is not None and piece != Player.EMPTY and piece.is_player(opponent_player):
                            opp_moves = temp_state.get_valid_moves((r, c))
                            if opp_moves and (move[0], move[1]) in opp_moves:
                                threatened_next_moves.add(move)
        for sq in threatened_next_moves:
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(180)
            s.fill(py.Color(255, 140, 0))  # Cam
            r, c = sq
            if board_flipped:
                r = 7 - r
            screen.blit(s, (PADDING_LEFT + c * SQ_SIZE, r * SQ_SIZE))
    draw_pieces(screen, game_state, board_flipped)  # Vẽ các quân cờ

def draw_squares(screen, board_flipped=False):
    """
    Vẽ bàn cờ với các ô xen kẽ hai màu, có padding trái và dưới
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            draw_r = 7 - r if board_flipped else r
            color = colors[(r + c) % 2]  # Xen kẽ màu sáng và tối
            rect = py.Rect(PADDING_LEFT + c * SQ_SIZE, draw_r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            py.draw.rect(screen, color, rect)
            py.draw.rect(screen, (100, 100, 100), rect, 1)  # Vẽ viền màu xám đậm, dày 1 px



def draw_pieces(screen, game_state, board_flipped=False):
    """
    Vẽ các quân cờ lên bàn cờ, căn giữa icon trong ô vuông, có padding trái
    """
    icon_size = int(SQ_SIZE * 0.8)
    offset = (SQ_SIZE - icon_size) // 2
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            draw_r = 7 - r if board_flipped else r
            piece = game_state.get_piece(r, c)
            if piece is not None and piece != Player.EMPTY:
                img = IMAGES[piece.get_player() + "_" + piece.get_name()]
                screen.blit(img, (PADDING_LEFT + c * SQ_SIZE + offset, draw_r * SQ_SIZE + offset))


def highlight_square(screen, game_state, valid_moves, square_selected, board_flipped=False):
    """
    Đánh dấu ô được chọn và các nước đi hợp lệ
    
    Args:
        screen: Màn hình pygame
        game_state: Trạng thái hiện tại của trò chơi
        valid_moves: Danh sách các nước đi hợp lệ
        square_selected: Ô được chọn hiện tại
    """
    if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]):
        row, col = square_selected
        draw_row = 7 - row if board_flipped else row
        # Kiểm tra xem quân cờ được chọn có thuộc về người chơi hiện tại không
        if (game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_1)) or \
           (not game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_2)):
            
            # Đánh dấu ô được chọn bằng màu xanh dương
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(150)  # Tăng độ trong suốt để rõ hơn
            s.fill(py.Color(0, 0, 255))  # Màu xanh dương cho ô được chọn
            screen.blit(s, (PADDING_LEFT + col * SQ_SIZE, draw_row * SQ_SIZE))

            # Đánh dấu các ô có thể di chuyển bằng màu xanh lá
            s.fill(py.Color(0, 255, 0, 100))  # Màu xanh lá nhạt cho các ô có thể đi
            for move in valid_moves:
                r, c = move
                draw_r = 7 - r if board_flipped else r
                screen.blit(s, (PADDING_LEFT + c * SQ_SIZE, draw_r * SQ_SIZE))



def main(game_mode, player_color=None, difficulty=None):
    """
    Hàm chính của trò chơi
    Xử lý logic chính và vòng lặp game

    Args:
        game_mode (str): Chế độ chơi ('ai' hoặc 'solo').
        player_color (str, optional): Màu của người chơi ('white' hoặc 'black'). Mặc định là None.
        difficulty (str, optional): Độ khó ('easy', 'medium', 'hard').
    """
    number_of_players = 1 if game_mode == 'ai' else 2
    human_player = ''
    ai_depth = 3
    player_at_bottom = 'white'
    board_flipped = False
    if number_of_players == 1:
        human_player = 'w' if player_color == 'white' else 'b'
        player_at_bottom = player_color
        if player_color == 'white':
            board_flipped = True
        else:
            board_flipped = False
        if difficulty == 'easy':
            ai_depth = 2
        elif difficulty == 'medium':
            ai_depth = 3
        elif difficulty == 'hard':
            ai_depth = 4

    py.init()
    screen = py.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
    clock = py.time.Clock()
    game_state = chess_engine.game_state(player_at_bottom=player_at_bottom)
    load_images()

    # Các biến trạng thái game
    running = True
    square_selected = ()  # Theo dõi ô được chọn cuối cùng
    player_clicks = []    # Theo dõi các lần click của người chơi (hai tuple)
    valid_moves = []      # Danh sách các nước đi hợp lệ
    game_over = False     # Trạng thái kết thúc game
    
    # Biến theo dõi thời gian chơi
    game_start_time = datetime.datetime.now()
    game_end_time = None
    surrendered = False   # Trạng thái đầu hàng
    
    # Biến điều khiển luồng sau khi game kết thúc
    restart_ui = False
    
    # Biến lưu trữ vùng chữ nhật của các nút khi game kết thúc
    tro_lai_rect, thoat_rect = None, None

    # Khởi tạo AI nếu cần
    ai = None
    if number_of_players == 1:
        ai = ai_engine.chess_ai()
        game_state = chess_engine.game_state()

    # Nếu người chơi chọn quân đen và chơi với AI, AI đi trước
    if number_of_players == 1 and human_player == 'b':
        ai_move = ai.minimax_black(game_state, ai_depth, -100000, 100000, True, Player.PLAYER_1, ai_depth)
        game_state.move_piece(ai_move[0], ai_move[1], True)

    # --- Thêm biến lưu gợi ý ---
    hint_valid_moves = []  # Danh sách các ô hợp lệ để highlight khi nhấn Hint
    best_moves_with_scores = []  # Danh sách [(move, score)] nước đi tốt nhất và điểm số

    # Vòng lặp chính của game
    promotion_pending = None  # Lưu trạng thái phong cấp nếu cần
    move_times = []  # Lưu thời gian từng nước đi
    move_time_start = datetime.datetime.now()
    scroll_offset = 0
    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
            elif e.type == py.MOUSEBUTTONDOWN:
                location = py.mouse.get_pos()
                # Ưu tiên xử lý popup phong cấp trước
                if promotion_pending:
                    popup_w, popup_h = 340, 120
                    popup_x = (PADDING_LEFT + BOARD_WIDTH) // 2 - popup_w // 2
                    popup_y = BOARD_HEIGHT // 2 - popup_h // 2
                    btn_size = 70
                    btn_gap = 10
                    btns = []
                    for i, piece in enumerate(['q', 'r', 'n', 'b']):
                        btn_rect = py.Rect(popup_x + 20 + i * (btn_size + btn_gap), popup_y + 25, btn_size, btn_size)
                        btns.append((btn_rect, piece))
                    for btn_rect, piece in btns:
                        if btn_rect.collidepoint(location):
                            from_sq = promotion_pending['from']
                            to_sq = promotion_pending['to']
                            color = promotion_pending['color']
                            moved_piece = game_state.get_piece(from_sq[0], from_sq[1])
                            game_state.promote_pawn_gui(from_sq, moved_piece, to_sq, piece)
                            promotion_pending = None
                            break
                    continue  # Không xử lý gì thêm khi đang chọn phong cấp
                
                if game_over:
                    # Xử lý click cho các nút khi game kết thúc
                    if tro_lai_rect and tro_lai_rect.collidepoint(location):
                        running = False
                        restart_ui = True
                    elif thoat_rect and thoat_rect.collidepoint(location):
                        running = False
                        restart_ui = False # Thoát hoàn toàn
                    # Không xử lý gì khác khi game_over, tránh bug
                    
                elif not game_over:
                    # Kiểm tra xem click có nằm trong vùng bàn cờ không
                    if PADDING_LEFT <= location[0] < PADDING_LEFT + BOARD_WIDTH and location[1] < BOARD_HEIGHT:
                        col = (location[0] - PADDING_LEFT) // SQ_SIZE   # Chuyển đổi thành tọa độ cột, đã trừ padding
                        row = location[1] // SQ_SIZE   # Chuyển đổi thành tọa độ hàng
                        if board_flipped:
                            row = 7 - row
                        
                        # Xử lý click chuột
                        if square_selected == (row, col):
                            # Nếu click vào ô đã chọn, bỏ chọn
                            square_selected = ()
                            player_clicks = []
                            hint_valid_moves = []
                            best_moves_with_scores = []
                        else:
                            # Chọn ô mới
                            square_selected = (row, col)
                            player_clicks.append(square_selected)
                            hint_valid_moves = []
                            best_moves_with_scores = []
                        
                        # Khi đã chọn đủ 2 ô (ô nguồn và ô đích)
                        if len(player_clicks) == 2:
                            # Kiểm tra xem nước đi có hợp lệ không
                            if (player_clicks[1][0], player_clicks[1][1]) not in valid_moves:
                                # Nước đi không hợp lệ, reset
                                square_selected = ()
                                player_clicks = []
                                valid_moves = []
                                hint_valid_moves = []
                                best_moves_with_scores = []
                            else:
                                # Thực hiện nước đi
                                move_result = game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
                                                      (player_clicks[1][0], player_clicks[1][1]), False)
                                # Lưu tổng thời gian đã trôi qua kể từ lúc bắt đầu ván cho mỗi nước đi
                                move_time_end = datetime.datetime.now()
                                move_times.append(int((move_time_end - game_start_time).total_seconds()))
                                move_time_start = move_time_end
                                if isinstance(move_result, dict) and move_result.get('promotion'):
                                    # Đang chờ chọn quân phong cấp
                                    promotion_pending = move_result
                                else:
                                    promotion_pending = None
                                square_selected = ()
                                player_clicks = []
                                valid_moves = []
                                hint_valid_moves = []
                                best_moves_with_scores = []

                                # Cập nhật màn hình ngay lập tức để hiển thị nước đi của người chơi
                                draw_game_state(screen, game_state, valid_moves, square_selected, hint_valid_moves, best_moves_with_scores, board_flipped)
                                py.display.flip()

                                # AI thực hiện nước đi của mình nếu là chế độ chơi với máy
                                if number_of_players == 1:
                                    # Hiển thị thông báo AI đang suy nghĩ
                                    overlay = py.Surface((PADDING_LEFT + BOARD_WIDTH, BOARD_HEIGHT + PADDING_BOTTOM), py.SRCALPHA)
                                    overlay.fill((255, 255, 255, 128))  # Màu trắng mờ với alpha 128
                                    screen.blit(overlay, (0, 0))
                                    font = py.font.SysFont("Arial", 40, True, False)
                                    text_object = font.render("AI is thinking...", True, py.Color("black"))
                                    center_x = (PADDING_LEFT + BOARD_WIDTH) // 2
                                    center_y = (BOARD_HEIGHT + PADDING_BOTTOM) // 2
                                    text_location = text_object.get_rect(center=(center_x, center_y))
                                    screen.blit(text_object, text_location)
                                    # Vẽ lại sidebar để không bị overlay che mất
                                    draw_sidebar(screen, game_start_time, surrendered, game_over, game_end_time, number_of_players, difficulty)
                                    # VẼ LẠI MOVE HISTORY ĐỂ KHÔNG BỊ CHE MẤT
                                    draw_move_history(screen, game_state.move_log, number_of_players == 1, move_times, scroll_offset, game_over, board_flipped)
                                    py.display.flip()
                                    # Đợi 2 giây để AI "suy nghĩ"
                                    time.sleep(2)
                                    if human_player == 'w':
                                        ai_move = ai.minimax_white(game_state, ai_depth, -100000, 100000, True, Player.PLAYER_2, ai_depth)
                                    elif human_player == 'b':
                                        ai_move = ai.minimax_black(game_state, ai_depth, -100000, 100000, True, Player.PLAYER_1, ai_depth)
                                    # Đảm bảo ai_move là tuple
                                    if isinstance(ai_move, tuple) and len(ai_move) == 2:
                                        game_state.move_piece(ai_move[0], ai_move[1], True)
                                    # Lưu tổng thời gian đã trôi qua kể từ lúc bắt đầu ván cho mỗi nước đi của AI
                                    move_time_end = datetime.datetime.now()
                                    move_times.append(int((move_time_end - game_start_time).total_seconds()))
                                    move_time_start = move_time_end
                        else:
                            # Lấy danh sách các nước đi hợp lệ cho quân cờ được chọn
                            valid_moves = game_state.get_valid_moves((row, col))
                            if valid_moves is None:
                                valid_moves = []
                    else:
                        # Kiểm tra click vào nút đầu hàng
                        button_rect, hint_button_rect = draw_sidebar(screen, game_start_time, surrendered, game_over, game_end_time, number_of_players, difficulty)
                        if button_rect and button_rect.collidepoint(location) and not surrendered and not game_over:
                            surrendered = True
                            game_over = True
                        # Kiểm tra click vào nút Hint (chỉ khi chơi với AI, không game_over)
                        if number_of_players == 1 and not game_over and hint_button_rect and hint_button_rect.collidepoint(location):
                            # Đảm bảo không làm gì với game_over hay restart_ui ở đây
                            # Chỉ highlight nếu đã chọn quân
                            if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]):
                                moves = game_state.get_valid_moves(square_selected)
                                hint_valid_moves = moves if moves else []
                                # Tìm nước đi tốt nhất (cam) nhưng KHÔNG reset bàn cờ, không hiển thị điểm số
                                best_moves_with_scores = []
                                if moves:
                                    ai_hint = ai_engine.chess_ai()
                                    scored_moves = []
                                    minimax_depth = 2
                                    for move in moves:
                                        # Sử dụng deepcopy để không làm thay đổi trạng thái bàn cờ thật
                                        temp_state = copy.deepcopy(game_state)
                                        temp_state.move_piece(square_selected, move, True)
                                        if human_player == 'w':
                                            score = ai_hint.minimax_white(temp_state, minimax_depth-1, -100000, 100000, False, 'white', minimax_depth)
                                        else:
                                            score = ai_hint.minimax_black(temp_state, minimax_depth-1, -100000, 100000, False, 'black', minimax_depth)
                                        # Không cần undo_move vì temp_state là bản sao
                                        if isinstance(score, (int, float)):
                                            scored_moves.append((move, score))
                                    scored_moves.sort(key=lambda x: x[1], reverse=(human_player=='w'))
                                    best_moves_with_scores = scored_moves[:2]
                                else:
                                    hint_valid_moves = []
                                    best_moves_with_scores = []
                        else:
                            pass
            elif e.type == py.KEYDOWN:
                if e.key == py.K_r:  # Phím R để reset game
                    game_over = False
                    game_state = chess_engine.game_state()
                    valid_moves = []
                    square_selected = ()
                    player_clicks = []
                    valid_moves = []
                    surrendered = False
                    game_start_time = datetime.datetime.now()
                    game_end_time = None
                    hint_valid_moves = []
                    best_moves_with_scores = []
                    move_times = []
                    move_time_start = datetime.datetime.now()
                    scroll_offset = 0
                elif e.key == py.K_u:  # Phím U để undo nước đi
                    game_state.undo_move()
                    print(len(game_state.move_log))
                    hint_valid_moves = []
                    best_moves_with_scores = []
                    move_times = []
                    move_time_start = datetime.datetime.now()
                    scroll_offset = 0
                    square_selected = ()
                    player_clicks = []
                    valid_moves = []
                    # Cập nhật lại valid_moves cho lượt hiện tại
                    if game_state.whose_turn():
                        # Lượt trắng
                        for r in range(8):
                            for c in range(8):
                                if game_state.is_valid_piece(r, c) and game_state.get_piece(r, c).is_player(Player.PLAYER_1):
                                    valid_moves += game_state.get_valid_moves((r, c))
                    else:
                        # Lượt đen
                        for r in range(8):
                            for c in range(8):
                                if game_state.is_valid_piece(r, c) and game_state.get_piece(r, c).is_player(Player.PLAYER_2):
                                    valid_moves += game_state.get_valid_moves((r, c))
                elif e.key == py.K_s:  # Phím S để đầu hàng
                    if not game_over:
                        surrendered = True
                        game_over = True

            elif e.type == py.MOUSEWHEEL:
                # Scroll move history bằng chuột
                if e.y > 0:  # Lăn lên
                    scroll_offset = max(0, scroll_offset - 1)
                elif e.y < 0:  # Lăn xuống
                    scroll_offset = min(scroll_offset + 1, max(0, len(game_state.move_log)-1))

        # Vẽ trạng thái game (truyền board_flipped)
        draw_game_state(screen, game_state, valid_moves, square_selected, hint_valid_moves, best_moves_with_scores, board_flipped)
        # Nếu đang chờ chọn quân phong cấp, vẽ popup
        if promotion_pending:
            popup_w, popup_h = 340, 120
            popup_x = (PADDING_LEFT + BOARD_WIDTH) // 2 - popup_w // 2
            popup_y = BOARD_HEIGHT // 2 - popup_h // 2
            # Nền popup: màu đen mờ
            s = py.Surface((popup_w, popup_h), py.SRCALPHA)
            s.fill((0, 0, 0, 180))
            screen.blit(s, (popup_x, popup_y))
            btn_size = 70
            btn_gap = 10
            color = promotion_pending['color']
            piece_names = ['q', 'r', 'n', 'b']
            for i, piece in enumerate(piece_names):
                btn_rect = py.Rect(popup_x + 20 + i * (btn_size + btn_gap), popup_y + 25, btn_size, btn_size)
                # Đặt màu nền xen kẽ như bàn cờ
                btn_color = colors[i % 2]
                py.draw.rect(screen, btn_color, btn_rect)
                img_key = f"{color}_{piece}"
                img = IMAGES[img_key]
                screen.blit(py.transform.smoothscale(img, (btn_size, btn_size)), btn_rect.topleft)
                py.draw.rect(screen, (200, 200, 200), btn_rect, 2)

        # Vẽ cột bên phải với bảng thời gian và nút đầu hàng, nhận lại vùng click thực tế
        button_rect, hint_button_rect = draw_sidebar(screen, game_start_time, surrendered, game_over, game_end_time, number_of_players, difficulty)

        # VẼ HƯỚNG DẪN PHÍM TẮT
        # draw_controls(screen) # This line is removed as per the edit hint

        # Vẽ move history
        draw_move_history(screen, game_state.move_log, number_of_players == 1, move_times, scroll_offset, game_over, board_flipped)

        # Kiểm tra trạng thái kết thúc game và vẽ màn hình kết thúc
        was_game_running = not game_over
        # Xác định loại kết thúc game
        endgame = game_state.checkmate_stalemate_checker()
        popup_type = None
        popup_winner = None
        if surrendered:
            game_over = True
            if number_of_players == 1:
                popup_type = "AI_win"
            else:
                popup_type = "surrender"
        elif endgame == 0:  # Quân đen thắng
            game_over = True
            if number_of_players == 1:
                if human_player == 'w':
                    popup_type = "AI_win"
                else:
                    popup_type = "AI_lose"
            else:
                popup_type = "checkmate"
                popup_winner = "Black"
        elif endgame == 1:  # Quân trắng thắng
            game_over = True
            if number_of_players == 1:
                if human_player == 'b':
                    popup_type = "AI_win"
                else:
                    popup_type = "AI_lose"
            else:
                popup_type = "checkmate"
                popup_winner = "White"
        elif endgame == 2:  # Hòa (stalemate)
            game_over = True
            popup_type = "stalemate"
        # Nếu game vừa mới kết thúc, ghi lại thời gian
        if game_over and was_game_running:
            game_end_time = datetime.datetime.now()
        # Nếu game đã kết thúc, vẽ popup chuyên nghiệp
        if game_over and popup_type:
            tro_lai_rect, thoat_rect = draw_endgame_popup(screen, popup_type, popup_winner)
            
        clock.tick(MAX_FPS)  # Giới hạn FPS
        py.display.flip()    # Cập nhật màn hình
    
    # Sau khi vòng lặp kết thúc, thoát pygame
    py.quit()

    # Nếu người dùng chọn trở lại, khởi chạy lại giao diện chính
    if restart_ui:
        import chess_UX_UI
        app = chess_UX_UI.ChessInterface()
        app.run()

def draw_status_bar(screen, game_state):
    """
    Vẽ thanh trạng thái hiển thị thông tin về lượt chơi và trạng thái chiếu
    
    Args:
        screen: Màn hình pygame
        game_state: Trạng thái hiện tại của trò chơi
    """
    font = py.font.SysFont("Arial", 24, True, False)
    text = ""
    
    # Hiển thị thông tin về trạng thái chiếu hoặc lượt chơi
    if game_state.is_in_check():
        if game_state.whose_turn():
            text = "White is in Check"
        else:
            text = "Black is in Check"
    else:
        if game_state.whose_turn():
            text = "White's Turn"
        else:
            text = "Black's Turn"
    
    # Vẽ thanh trạng thái
    text_obj = font.render(text, True, py.Color("black"))
    rect = py.Rect(0, WIDTH, WIDTH, STATUS_BAR_HEIGHT)
    py.draw.rect(screen, (200, 200, 200), rect)  # Nền xám nhạt
    screen.blit(text_obj, (10, WIDTH + (STATUS_BAR_HEIGHT - text_obj.get_height()) // 2))


def draw_text(screen, text, color=py.Color("black"), background_alpha=None):
    """
    Vẽ văn bản lên màn hình, có thể có nền mờ.
    
    Args:
        screen: Màn hình pygame
        text: Văn bản cần hiển thị
        color: Màu sắc của văn bản
        background_alpha (int, optional): Độ trong suốt của lớp phủ nền (0-255).
    """
    # Vẽ lớp phủ mờ nếu được yêu cầu
    if background_alpha is not None:
        overlay_width = PADDING_LEFT + BOARD_WIDTH
        overlay_height = BOARD_HEIGHT + PADDING_BOTTOM
        overlay = py.Surface((overlay_width, overlay_height))
        overlay.set_alpha(background_alpha)
        overlay.fill((0, 0, 0))  # Lớp phủ màu đen
        screen.blit(overlay, (0, 0))
    
    font = py.font.SysFont("Arial", 40, True, False)
    text_object = font.render(text, True, color)
    # Căn giữa text theo toàn bộ vùng bàn cờ (bao gồm padding)
    center_x = (PADDING_LEFT + BOARD_WIDTH) // 2
    center_y = (BOARD_HEIGHT + PADDING_BOTTOM) // 2
    text_location = text_object.get_rect(center=(center_x, center_y))
    screen.blit(text_object, text_location)

def draw_game_time(screen, start_time):
    """
    Hiển thị thời gian đã chơi ở góc trên bên phải màn hình
    
    Args:
        screen: Màn hình pygame
        start_time: Thời điểm bắt đầu game
    """
    current_time = datetime.datetime.now()
    elapsed_time = current_time - start_time
    minutes = int(elapsed_time.total_seconds() // 60)
    seconds = int(elapsed_time.total_seconds() % 60)
    
    time_text = f"Thời gian: {minutes:02d}:{seconds:02d}"
    font = py.font.SysFont("Arial", 16, True, False)
    text_object = font.render(time_text, True, py.Color("black"))
    screen.blit(text_object, (WIDTH - text_object.get_width() - 10, 10))

def draw_controls(screen):
    """
    Hiển thị hướng dẫn phím tắt ở góc dưới bên trái màn hình
    """
    controls_text = [
        "R: Reset game",
        "U: Undo move", 
        "S: Surrender"
    ]
    
    font = py.font.SysFont("Arial", 12, True, False)
    y_position = HEIGHT - 60
    
    for i, text in enumerate(controls_text):
        text_object = font.render(text, True, py.Color("black"))
        screen.blit(text_object, (10, y_position + i * 15))

def draw_sidebar(screen, start_time, surrendered, game_over, game_end_time, number_of_players, difficulty=None):
    """
    Vẽ cột bên phải với bảng thời gian và nút đầu hàng
    """
    sidebar_left = PADDING_LEFT + BOARD_WIDTH
    # Vẽ nền cột bên phải
    sidebar_rect = py.Rect(sidebar_left, 0, SIDEBAR_WIDTH, BOARD_HEIGHT + PADDING_BOTTOM)
    py.draw.rect(screen, (240, 240, 240), sidebar_rect)  # Màu xám nhạt
    py.draw.rect(screen, (100, 100, 100), sidebar_rect, 2)  # Viền
    # Vẽ tiêu đề "Bảng Thời Gian"
    title_font = py.font.SysFont("Arial", 22, True, False)
    title_text = title_font.render("TIMER", True, py.Color("black"))
    title_rect = title_text.get_rect(center=(sidebar_left + SIDEBAR_WIDTH // 2, 30))
    screen.blit(title_text, title_rect)
    # Tính và hiển thị thời gian
    end_time = game_end_time if game_end_time else datetime.datetime.now()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time.total_seconds() // 60)
    seconds = int(elapsed_time.total_seconds() % 60)
    time_font = py.font.SysFont("Arial", 30, True, False)
    time_text = f"{minutes:02d}:{seconds:02d}"
    time_surface = time_font.render(time_text, True, py.Color("black"))
    time_rect = time_surface.get_rect(center=(sidebar_left + SIDEBAR_WIDTH // 2, 80))
    # Vẽ khung thời gian
    time_box_rect = py.Rect(sidebar_left + 20, 60, SIDEBAR_WIDTH - 40, 40)
    py.draw.rect(screen, (255, 255, 255), time_box_rect)  # Nền trắng
    py.draw.rect(screen, (0, 0, 0), time_box_rect, 2)  # Viền đen
    screen.blit(time_surface, time_rect)

    # --- Vẽ khuôn mặt động ---
    # Xác định độ khó (nếu có)
    face_size = int(SIDEBAR_WIDTH * 0.45)  # Giảm còn 45% sidebar
    face_height = int(face_size * 4 / 3)   # Tỉ lệ 3:4
    pixel_size = max(8, face_size // 10)   # Pixel lớn hơn cho mặt
    face_y = time_box_rect.bottom + pixel_size  # Cách timer đúng bằng 1 ô nhỏ của khuôn mặt
    face_x = sidebar_left + (SIDEBAR_WIDTH - face_size) // 2
    face_surface = py.Surface((face_size, face_height), py.SRCALPHA)
    mx, my = py.mouse.get_pos()
    if difficulty == 'easy':
        draw_baby_face(face_surface, mx, my, 0, 0, pixel_size=pixel_size, abs_x=face_x, abs_y=face_y)
    elif difficulty == 'medium':
        draw_adult_face(face_surface, mx, my, 0, 0, pixel_size=pixel_size, abs_x=face_x, abs_y=face_y)
    elif difficulty == 'hard':
        draw_old_face(face_surface, mx, my, 0, 0, pixel_size=pixel_size, abs_x=face_x, abs_y=face_y)
    screen.blit(face_surface, (face_x, face_y))

    # Đặt các nút bắt đầu từ dưới khuôn mặt, chỉ cách 1 ô pixel_size
    button_y_start = face_y + face_height + pixel_size  # Cách khuôn mặt đúng 1 ô pixel

    # Vẽ nút đầu hàng
    surrender_font = py.font.SysFont("Arial", 20, True, False)
    if surrendered or game_over:
        button_color = (150, 150, 150)
        text_color = (100, 100, 100)
        button_text = "Loser"
    else:
        button_color = (220, 50, 50)
        text_color = (255, 255, 255)
        button_text = "Loser"
    button_rect = py.Rect(sidebar_left + 30, button_y_start, SIDEBAR_WIDTH - 60, 50)
    py.draw.rect(screen, button_color, button_rect)
    py.draw.rect(screen, (0, 0, 0), button_rect, 2)
    surrender_surface = surrender_font.render(button_text, True, text_color)
    surrender_text_rect = surrender_surface.get_rect(center=button_rect.center)
    screen.blit(surrender_surface, surrender_text_rect)

    # Vẽ nút Hint nếu chơi với AI
    if number_of_players == 1 and not game_over:
        hint_font = py.font.SysFont("Arial", 20, True, False)
        hint_button_rect = py.Rect(sidebar_left + 30, button_rect.bottom + 8, SIDEBAR_WIDTH - 60, 50)
        py.draw.rect(screen, (50, 205, 50), hint_button_rect)
        py.draw.rect(screen, (0, 128, 0), hint_button_rect, 2)
        hint_text = hint_font.render("Hint", True, (255, 255, 255))
        hint_text_rect = hint_text.get_rect(center=hint_button_rect.center)
        screen.blit(hint_text, hint_text_rect)
        keys_y = hint_button_rect.bottom + 12
    else:
        hint_button_rect = None
        keys_y = button_rect.bottom + 12
    # Vẽ hướng dẫn phím tắt
    font_label = py.font.SysFont("Arial", 14, True, False)
    font_key = py.font.SysFont("Arial", 14, True, False)
    # Keys:    R: Reset
    screen.blit(font_label.render("Keys:    R: Reset", True, (0,0,0)), (sidebar_left + 30, keys_y))
    #          U: Undo (thụt vào 8*2=16px)
    screen.blit(font_key.render("U: Undo", True, (0,0,0)), (sidebar_left + 30 + 48, keys_y + 22))
    return button_rect, hint_button_rect

def draw_end_game_buttons(screen):
    """
    Vẽ các nút "Trở lại" và "Thoát" khi game kết thúc.
    """
    button_font = py.font.SysFont("Arial", 20, True, False)
    button_y = BOARD_HEIGHT // 2 + 80
    button_width = 150
    button_height = 50
    spacing = 30
    center_x = (PADDING_LEFT + BOARD_WIDTH) // 2

    # Nút Trở Lại
    tro_lai_rect = py.Rect(center_x - button_width - spacing // 2, button_y, button_width, button_height)
    py.draw.rect(screen, (0, 150, 50), tro_lai_rect, border_radius=8)
    py.draw.rect(screen, (255, 255, 255), tro_lai_rect, 2, border_radius=8)
    tro_lai_text = button_font.render("Tro Lai", True, py.Color("white"))
    tro_lai_text_rect = tro_lai_text.get_rect(center=tro_lai_rect.center)
    screen.blit(tro_lai_text, tro_lai_text_rect)

    # Nút Thoát
    thoat_rect = py.Rect(center_x + spacing // 2, button_y, button_width, button_height)
    py.draw.rect(screen, (200, 50, 50), thoat_rect, border_radius=8)
    py.draw.rect(screen, (255, 255, 255), thoat_rect, 2, border_radius=8)
    thoat_text = button_font.render("Thoat", True, py.Color("white"))
    thoat_text_rect = thoat_text.get_rect(center=thoat_rect.center)
    screen.blit(thoat_text, thoat_text_rect)

    return tro_lai_rect, thoat_rect

def draw_labels(screen, board_flipped=False):
    """
    Vẽ số (1-8) bên trái và chữ (a-h) bên dưới bàn cờ, có padding
    """
    font = py.font.SysFont("Arial", 18, True, False)
    # Vẽ số 1-8 bên trái từng hàng (1 ở dưới, 8 ở trên, luôn như chuẩn quốc tế)
    for r in range(DIMENSION):
        label = str(DIMENSION - r)
        text = font.render(label, True, py.Color("black"))
        y = r * SQ_SIZE + SQ_SIZE // 2 - text.get_height() // 2
        screen.blit(text, (PADDING_LEFT // 2 - text.get_width() // 2, y))
    # Vẽ chữ a-h bên dưới từng cột (không đổi)
    for c in range(DIMENSION):
        label = chr(ord('a') + c)
        text = font.render(label, True, py.Color("black"))
        x = PADDING_LEFT + c * SQ_SIZE + SQ_SIZE // 2 - text.get_width() // 2
        screen.blit(text, (x, BOARD_HEIGHT + (PADDING_BOTTOM // 2 - text.get_height() // 2)))

def draw_move_history(screen, move_log, ai_mode, move_times, scroll_offset, game_over, board_flipped=False):
    # Vẽ khung textbox
    sidebar_left = PADDING_LEFT + BOARD_WIDTH
    box_x = sidebar_left + 20
    box_y = 420  # Đẩy lịch sử nước đi xuống để không che keys
    box_w = SIDEBAR_WIDTH - 40
    box_h = 160  # Kích thước nhỏ lại như ban đầu
    box_rect = py.Rect(box_x, box_y, box_w, box_h)
    py.draw.rect(screen, (255, 255, 255), box_rect)
    py.draw.rect(screen, (0, 0, 0), box_rect, 2)
    font2 = py.font.SysFont("Arial", 14, True, False)  # In đậm
    font_center = py.font.SysFont("Arial", 16, True, False)
    line_h = 20
    max_lines = (box_h - 10) // line_h
    piece_full = {'P': 'Pawn', 'N': 'Knight', 'B': 'Bishop', 'R': 'Rook', 'Q': 'Queen', 'K': 'King'}
    lines = []
    # Thêm label Start căn giữa
    lines.append({'text': 'Start', 'center': True})
    for idx, move in enumerate(move_log):
        color = "white" if idx % 2 == 0 else "black"
        piece = move.get_moving_piece().get_name().upper()
        piece_name = piece_full.get(piece, piece)
        # Sửa lại chuyển đổi row thành số hàng (1-8) theo hướng board_flipped
        if board_flipped:
            start_row = 7 - move.starting_square_row
            end_row = 7 - move.ending_square_row
        else:
            start_row = move.starting_square_row
            end_row = move.ending_square_row
        start = chr(ord('a') + move.starting_square_col) + str(8 - start_row)
        end = chr(ord('a') + move.ending_square_col) + str(8 - end_row)
        move_str = f"{idx+1}. {color} ({piece_name}) : {start} => {end}"
        # Hiển thị thời gian theo định dạng XmYs (kể cả khi dưới phút(m) và giấy(s))
        if idx < len(move_times):
            t = move_times[idx]
            m = t // 60
            s = t % 60
            move_str += f"  {m}m{s}s"
        # Nếu là nước phong cấp tốt, hiển thị thêm vn pawn => queen/rook/bishop/knight
        if hasattr(move, 'pawn_promoted') and move.pawn_promoted and hasattr(move, 'replacement_piece') and move.replacement_piece is not None:
            promoted_name = piece_full.get(move.replacement_piece.get_name().upper(), move.replacement_piece.get_name().capitalize())
            move_str += f"   pawn => {promoted_name.lower()}"
        # Nếu có ăn quân, hiển thị theo định dạng Attacker(Captured) cách 5 dấu cách
        captured_piece = move.get_captured_piece() if hasattr(move, 'get_captured_piece') else None
        if captured_piece and hasattr(captured_piece, 'get_name'):
            captured_name = piece_full.get(captured_piece.get_name().upper(), captured_piece.get_name().capitalize())
            move_str += f' "{piece_name}({captured_name})"'
        if ai_mode and ((color == 'white' and idx % 2 == 1) or (color == 'black' and idx % 2 == 0)):
            move_str += " (AI)"
        # Tự động xuống dòng nếu quá dài
        words = move_str.split(' ')
        wrapped = []
        current = ''
        for word in words:
            test = (current + ' ' + word).strip()
            if font2.size(test)[0] > box_w - 10 and current:
                wrapped.append({'text': current, 'center': False})
                current = word
            else:
                current = test
        if current:
            wrapped.append({'text': current, 'center': False})
        lines.extend(wrapped)
    # Thêm label End căn giữa nếu game_over
    if game_over:
        lines.append({'text': 'End', 'center': True})
    # Scroll
    visible_lines = lines[max(0, len(lines)-max_lines-scroll_offset):len(lines)-scroll_offset]
    for i, line in enumerate(visible_lines):
        if line['center']:
            text = font_center.render(line['text'], True, py.Color("black"))
            text_rect = text.get_rect(center=(box_x + box_w // 2, box_y + 5 + i * line_h + line_h//2))
            screen.blit(text, text_rect)
        else:
            text = font2.render(line['text'], True, py.Color("black"))
            screen.blit(text, (box_x + 5, box_y + 5 + i * line_h))

def draw_endgame_popup(screen, result_type, winner=None):
    # Nền mờ toàn màn hình
    overlay = py.Surface((PADDING_LEFT + BOARD_WIDTH + SIDEBAR_WIDTH, BOARD_HEIGHT + PADDING_BOTTOM), py.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(overlay, (0, 0))
    # Popup trắng mờ (glassmorphism)
    popup_w, popup_h = 420, 260
    popup_x = ((PADDING_LEFT + BOARD_WIDTH + SIDEBAR_WIDTH) - popup_w) // 2 - 60  # Dời sang trái 60px
    popup_y = (BOARD_HEIGHT + PADDING_BOTTOM - popup_h) // 2
    popup_rect = py.Rect(popup_x, popup_y, popup_w, popup_h)
    # Glass effect: semi-transparent white
    popup_surface = py.Surface((popup_w, popup_h), py.SRCALPHA)
    popup_surface.fill((255, 255, 255, 100))  # Alpha 180 cho hiệu ứng mờ
    py.draw.rect(popup_surface, (255,255,255,180), popup_surface.get_rect(), border_radius=18)
    screen.blit(popup_surface, (popup_x, popup_y))
    # Glass effect: semi-transparent black
    popup_surface = py.Surface((popup_w, popup_h), py.SRCALPHA)
    popup_surface.fill((0, 0, 0, 100))  # Alpha 120 cho hiệu ứng mờ đen nhẹ hơn
    py.draw.rect(popup_surface, (0,0,0,120), popup_surface.get_rect(), border_radius=18)
    screen.blit(popup_surface, (popup_x, popup_y))
    py.draw.rect(screen, (60, 60, 60), popup_rect, 3, border_radius=18)
    # Nội dung
    title_font = py.font.SysFont("Arial", 38, True, False)
    sub_font = py.font.SysFont("Arial", 28, True, False)
    # Dòng trên
    if result_type == "checkmate":
        title = "Checkmate!"
        sub = f"{winner} win"
    elif result_type == "stalemate":
        title = "Stalemate"
        sub = "Draw"
    elif result_type == "lose":
        title = "You lose"
        sub = ""
    elif result_type == "ai_win":
        title = "Loser"
        sub = ""
    elif result_type == "ai_lose":
        title = "You are invincible  :>"
        sub = ""
    elif result_type == "surrender":
        title = "You surrendered"
        sub = ""
    else:
        title = "Game Over"
        sub = ""
    # Vẽ text
    title_surf = title_font.render(title, True, (30, 30, 30))
    title_rect = title_surf.get_rect(center=(popup_x + popup_w//2, popup_y + 60))
    screen.blit(title_surf, title_rect)
    if sub:
        sub_surf = sub_font.render(sub, True, (80, 80, 80))
        sub_rect = sub_surf.get_rect(center=(popup_x + popup_w//2, popup_y + 110))
        screen.blit(sub_surf, sub_rect)
    # Nút
    btn_font = py.font.SysFont("Arial", 22, True, False)
    btn_w, btn_h = 140, 48
    spacing = 30
    btn1_rect = py.Rect(popup_x + popup_w//2 - btn_w - spacing//2, popup_y + popup_h - 70, btn_w, btn_h)
    btn2_rect = py.Rect(popup_x + popup_w//2 + spacing//2, popup_y + popup_h - 70, btn_w, btn_h)
    py.draw.rect(screen, (0, 150, 50), btn1_rect, border_radius=10)
    py.draw.rect(screen, (255,255,255), btn1_rect, 2, border_radius=10)
    py.draw.rect(screen, (200, 50, 50), btn2_rect, border_radius=10)
    py.draw.rect(screen, (255,255,255), btn2_rect, 2, border_radius=10)
    btn1_text = btn_font.render("Tro Lai", True, (255,255,255))
    btn2_text = btn_font.render("Thoat", True, (255,255,255))
    screen.blit(btn1_text, btn1_text.get_rect(center=btn1_rect.center))
    screen.blit(btn2_text, btn2_text.get_rect(center=btn2_rect.center))
    return btn1_rect, btn2_rect

if __name__ == "__main__":
    # Giao diện chính của game được chạy từ chess_UX_UI.py
    # Bạn có thể bỏ comment ở các dòng dưới để test nhanh các chế độ
    # main('solo')
    # main('ai', 'white')
    pass
