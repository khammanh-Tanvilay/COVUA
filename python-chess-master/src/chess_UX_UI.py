import tkinter as tk
from PIL import Image, ImageTk
import sys
import importlib
import os

class ChessInterface:
    def __init__(self):
        # Tạo cửa sổ chính
        self.root = tk.Tk()
        self.root.title("Cờ Vua")
        # Đặt kích thước ban đầu, nhưng cửa sổ có thể thay đổi kích thước
        self.root.geometry("1000x800")
        self.root.minsize(600, 480) # Đặt kích thước tối thiểu

        # Khởi tạo các biến lưu trữ widget và ảnh
        self.original_background_image = None
        self.background_photo = None
        self.button_solo = None
        self.button_play_with_AI = None
        self.button_exit = None
        # Khởi tạo các biến nút cho các màn hình khác
        self.button_white = None
        self.button_black = None
        self.button_back = None
        self.button_easy = None
        self.button_medium = None
        self.button_hard = None
        self.button_back2 = None
        self._resize_job = None
        self.current_screen = 'main_menu'  # Trạng thái màn hình hiện tại

        # Tạo Canvas để vẽ giao diện, nó sẽ lấp đầy cửa sổ
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Tải và hiển thị các thành phần UI
        self.load_background_image()
        self.create_choice_buttons()

        # Gán sự kiện thay đổi kích thước cho canvas
        self.canvas.bind("<Configure>", self.on_resize)

    def load_background_image(self):
        """Tải ảnh nền từ file và lưu ảnh gốc."""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "images", "BG.png")
            
            self.original_background_image = Image.open(image_path)
            # Tạo một item ảnh trên canvas với tag "background" để cập nhật sau
            self.canvas.create_image(0, 0, anchor="nw", tags="background")

        except FileNotFoundError:
            print(f"Không tìm thấy file ảnh nền tại: {image_path}")
            self.original_background_image = None
            self.canvas.configure(bg="white")
        except Exception as e:
            print(f"Lỗi khi tải ảnh nền: {e}")
            self.original_background_image = None
            self.canvas.configure(bg="white")

    def create_choice_buttons(self):
        self.current_screen = 'main_menu'  # Đánh dấu đang ở màn hình chính
        """Tạo tiêu đề và các nút bấm ban đầu."""
        # Widget cha là canvas
        parent_widget = self.canvas

        # --- Vẽ Tiêu đề "Chơi Cờ Vua" - sẽ được định vị lại trong on_resize ---
        parent_widget.create_text(0, 0, text="Chơi Cờ Vua",
                                  font=("Gill Sans Nova Ultra Bold", 40, "bold"),
                                  fill="black", anchor="center", tags="title")

        # --- Nút Chơi Đôi ---
        self.button_solo = tk.Button(self.root,
                                text="Người đấu Người",
                                command=self.button_clicked_solo,
                                activebackground="#3399ff", activeforeground="white",
                                anchor="center", bd=3, bg="#00FF00", cursor="hand2",
                                disabledforeground="gray", fg="black", font=("Arial", 12, "bold"),
                                height=2, highlightbackground="black", highlightcolor="green",
                                highlightthickness=2, justify="center", overrelief="raised",
                                padx=10, pady=5, width=15, wraplength=100)
        parent_widget.create_window(0, 0, window=self.button_solo, anchor="center", tags="solo_button")

        # --- Nút Chơi với AI ---
        self.button_play_with_AI = tk.Button(self.root,
                                        text="Đấu với Máy",
                                        command=self.button_clicked_AI,
                                        activebackground="#3399ff", activeforeground="white",
                                        anchor="center", bd=3, bg="#00FF00", cursor="hand2",
                                        disabledforeground="gray", fg="black", font=("Arial", 12, "bold"),
                                        height=2, highlightbackground="black", highlightcolor="green",
                                        highlightthickness=2, justify="center", overrelief="raised",
                                        padx=10, pady=5, width=15, wraplength=100)
        parent_widget.create_window(0, 0, window=self.button_play_with_AI, anchor="center", tags="ai_button")

        # --- Nút Thoát ---
        self.button_exit = tk.Button(self.root,
                                text="Thoát",
                                command=self.button_clicked_exit,
                                activebackground="#59080A", activeforeground="white",
                                anchor="center", bd=3, bg="#E33539", cursor="hand2",
                                disabledforeground="gray", fg="black", font=("Arial", 12, "bold"),
                                height=2, highlightbackground="black", highlightcolor="green",
                                highlightthickness=2, justify="center", overrelief="raised",
                                padx=10, pady=5, width=15, wraplength=100)
        parent_widget.create_window(0, 0, window=self.button_exit, anchor="center", tags="exit_button")

    def on_resize(self, event):
        """
        Xử lý sự kiện thay đổi kích thước cửa sổ.
        Sử dụng debounce để tránh gọi lại hàm quá nhiều lần khi người dùng kéo thả.
        """
        if self._resize_job:
            self.root.after_cancel(self._resize_job)
        self._resize_job = self.root.after(50, self.perform_resize)

    def perform_resize(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 10 or height < 10:
            return
        # 1. Cập nhật ảnh nền
        if self.original_background_image:
            resized_image = self.original_background_image.resize((width, height), Image.LANCZOS)
            self.background_photo = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig("background", image=self.background_photo)
            self.canvas.coords("background", 0, 0)
        # 2. Cập nhật giao diện theo màn hình hiện tại
        if self.current_screen == 'main_menu':
            # Cập nhật tiêu đề
            title_font_size = max(20, min(int(height / 15), 60))
            self.canvas.itemconfig("title", font=("Gill Sans Nova Ultra Bold", title_font_size, "bold"))
            self.canvas.coords("title", width / 2, height * 0.4)
            # Cập nhật các nút - kiểm tra sự tồn tại trước khi cập nhật
            button_font_size = max(8, min(int(height / 40), 16))
            button_y = height * 0.60
            button_spacing = width / 5.5
            button_font = ("Arial", button_font_size, "bold")
            if hasattr(self, 'button_solo') and self.button_solo:
                self.button_solo.config(font=button_font)
            if hasattr(self, 'button_play_with_AI') and self.button_play_with_AI:
                self.button_play_with_AI.config(font=button_font)
            if hasattr(self, 'button_exit') and self.button_exit:
                self.button_exit.config(font=button_font)
            center_x = width / 2
            # Kiểm tra sự tồn tại của các tag trước khi cập nhật vị trí
            if self.canvas.find_withtag("solo_button"):
                self.canvas.coords("solo_button", center_x - button_spacing, button_y)
            if self.canvas.find_withtag("ai_button"):
                self.canvas.coords("ai_button", center_x, button_y)
            if self.canvas.find_withtag("exit_button"):
                self.canvas.coords("exit_button", center_x + button_spacing, button_y)
        elif self.current_screen == 'color_select':
            # Cập nhật tiêu đề
            title_font_size = max(20, min(int(height / 15), 60))
            self.canvas.itemconfig("color_title", font=("Gill Sans Nova Ultra Bold", title_font_size, "bold"))
            self.canvas.coords("color_title", width / 2, height * 0.3)
            # Cập nhật các nút - kiểm tra sự tồn tại trước khi cập nhật
            button_font_size = max(8, min(int(height / 40), 16))
            button_font = ("Arial", button_font_size, "bold")
            if hasattr(self, 'button_white') and self.button_white:
                self.button_white.config(font=button_font)
            if hasattr(self, 'button_black') and self.button_black:
                self.button_black.config(font=button_font)
            if hasattr(self, 'button_back') and self.button_back:
                self.button_back.config(font=button_font)
            center_x = width / 2
            button_y = height * 0.6
            button_spacing = width / 6
            # Kiểm tra sự tồn tại của các tag trước khi cập nhật vị trí
            if self.canvas.find_withtag("white_button"):
                self.canvas.coords("white_button", center_x - button_spacing, button_y)
            if self.canvas.find_withtag("black_button"):
                self.canvas.coords("black_button", center_x + button_spacing, button_y)
            if self.canvas.find_withtag("back_button"):
                self.canvas.coords("back_button", center_x, button_y + 80)
        elif self.current_screen == 'difficulty_select':
            # Cập nhật tiêu đề
            title_font_size = max(20, min(int(height / 15), 60))
            self.canvas.itemconfig("difficulty_title", font=("Gill Sans Nova Ultra Bold", title_font_size, "bold"))
            self.canvas.coords("difficulty_title", width / 2, height * 0.3)
            # Cập nhật các nút - kiểm tra sự tồn tại trước khi cập nhật
            button_font_size = max(8, min(int(height / 40), 16))
            button_font = ("Arial", button_font_size, "bold")
            if hasattr(self, 'button_easy') and self.button_easy:
                self.button_easy.config(font=button_font)
            if hasattr(self, 'button_medium') and self.button_medium:
                self.button_medium.config(font=button_font)
            if hasattr(self, 'button_hard') and self.button_hard:
                self.button_hard.config(font=button_font)
            if hasattr(self, 'button_back2') and self.button_back2:
                self.button_back2.config(font=button_font)
            center_x = width / 2
            button_y = height * 0.6
            button_spacing = width / 4.5
            # Kiểm tra sự tồn tại của các tag trước khi cập nhật vị trí
            if self.canvas.find_withtag("easy_button"):
                self.canvas.coords("easy_button", center_x - button_spacing, button_y)
            if self.canvas.find_withtag("medium_button"):
                self.canvas.coords("medium_button", center_x, button_y)
            if self.canvas.find_withtag("hard_button"):
                self.canvas.coords("hard_button", center_x + button_spacing, button_y)
            if self.canvas.find_withtag("back2_button"):
                self.canvas.coords("back2_button", center_x, button_y + 80)

    def button_clicked_solo(self):
        # Chuyển đến chế độ chơi solo (2 người chơi)
        self.root.destroy()
        try:
            # Import và chạy chess_gui với chế độ 'solo'
            import chess_gui
            chess_gui.main(game_mode='solo')
        except ImportError:
            print("Không tìm thấy file chess_gui.py")
        except Exception as e:
            print(f"Lỗi khi khởi động game: {e}")

    def button_clicked_AI(self):
        # Chuyển đến màn hình chọn màu quân cờ
        self.show_color_selection_screen()

    def show_color_selection_screen(self):
        self.current_screen = 'color_select'  # Đánh dấu đang ở màn hình chọn màu
        self.selected_color = None
        self.selected_difficulty = None
        # Xóa tất cả các widget hiện tại
        self.canvas.delete("all")
        # Xóa các biến nút cũ để tránh lỗi
        if hasattr(self, 'button_easy'):
            self.button_easy = None
        if hasattr(self, 'button_medium'):
            self.button_medium = None
        if hasattr(self, 'button_hard'):
            self.button_hard = None
        if hasattr(self, 'button_back2'):
            self.button_back2 = None
        
        # Tải lại ảnh nền
        if self.original_background_image:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            if width > 10 and height > 10:
                resized_image = self.original_background_image.resize((width, height), Image.LANCZOS)
                self.background_photo = ImageTk.PhotoImage(resized_image)
                self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw", tags="background")
        
        # Tạo tiêu đề "Chọn Màu Quân Cờ"
        title_font_size = max(20, min(int(self.canvas.winfo_height() / 15), 60))
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() * 0.3, 
                               text="Chọn Màu Quân Cờ", 
                               font=("Gill Sans Nova Ultra Bold", title_font_size, "bold"),
                               fill="black", anchor="center", tags="color_title")
        
        # Tạo nút "White" (Trắng)
        button_font_size = max(8, min(int(self.canvas.winfo_height() / 40), 16))
        button_font = ("Arial", button_font_size, "bold")
        
        self.button_white = tk.Button(self.root,
                                     text="White",
                                     command=lambda: self.select_color_and_show_difficulty("white"),
                                     activebackground="#3399ff", activeforeground="white",
                                     anchor="center", bd=3, bg="#FFFFFF", cursor="hand2",
                                     disabledforeground="gray", fg="black", font=button_font,
                                     height=2, highlightbackground="black", highlightcolor="green",
                                     highlightthickness=2, justify="center", overrelief="raised",
                                     padx=10, pady=5, width=15, wraplength=100)
        
        # Tạo nút "Black" (Đen)
        self.button_black = tk.Button(self.root,
                                     text="Black",
                                     command=lambda: self.select_color_and_show_difficulty("black"),
                                     activebackground="#3399ff", activeforeground="white",
                                     anchor="center", bd=3, bg="#000000", cursor="hand2",
                                     disabledforeground="gray", fg="white", font=button_font,
                                     height=2, highlightbackground="black", highlightcolor="green",
                                     highlightthickness=2, justify="center", overrelief="raised",
                                     padx=10, pady=5, width=15, wraplength=100)
        
        # Đặt vị trí các nút
        center_x = self.canvas.winfo_width() / 2
        button_y = self.canvas.winfo_height() * 0.6
        button_spacing = self.canvas.winfo_width() / 6
        
        self.canvas.create_window(center_x - button_spacing, button_y, 
                                 window=self.button_white, anchor="center", tags="white_button")
        self.canvas.create_window(center_x + button_spacing, button_y, 
                                 window=self.button_black, anchor="center", tags="black_button")
        
        # Tạo nút "Quay Lại"
        self.button_back = tk.Button(self.root,
                                    text="Quay Lại",
                                    command=self.back_to_main_menu,
                                    activebackground="#59080A", activeforeground="white",
                                    anchor="center", bd=3, bg="#E33539", cursor="hand2",
                                    disabledforeground="gray", fg="black", font=button_font,
                                    height=2, highlightbackground="black", highlightcolor="green",
                                    highlightthickness=2, justify="center", overrelief="raised",
                                    padx=10, pady=5, width=15, wraplength=100)
        
        self.canvas.create_window(center_x, button_y + 80, 
                                 window=self.button_back, anchor="center", tags="back_button")

    def select_color_and_show_difficulty(self, color):
        """Lưu màu đã chọn và hiển thị màn hình chọn độ khó."""
        self.selected_color = color
        self.show_difficulty_selection_screen()

    def show_difficulty_selection_screen(self):
        self.current_screen = 'difficulty_select'  # Đánh dấu đang ở màn hình chọn độ khó
        self.canvas.delete("all")
        # Xóa các biến nút cũ để tránh lỗi
        if hasattr(self, 'button_white'):
            self.button_white = None
        if hasattr(self, 'button_black'):
            self.button_black = None
        if hasattr(self, 'button_back'):
            self.button_back = None
        # Tải lại ảnh nền
        if self.original_background_image:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            if width > 10 and height > 10:
                resized_image = self.original_background_image.resize((width, height), Image.LANCZOS)
                self.background_photo = ImageTk.PhotoImage(resized_image)
                self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw", tags="background")
        # Tiêu đề
        title_font_size = max(20, min(int(self.canvas.winfo_height() / 15), 60))
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() * 0.3,
                               text="Chọn Độ Khó",
                               font=("Gill Sans Nova Ultra Bold", title_font_size, "bold"),
                               fill="black", anchor="center", tags="difficulty_title")
        # Nút Dễ
        button_font_size = max(8, min(int(self.canvas.winfo_height() / 40), 16))
        button_font = ("Arial", button_font_size, "bold")
        self.button_easy = tk.Button(self.root,
                                     text="Dễ",
                                     command=lambda: self.select_difficulty_and_start("easy"),
                                     activebackground="#3399ff", activeforeground="white",
                                     anchor="center", bd=3, bg="#00FF00", cursor="hand2",
                                     disabledforeground="gray", fg="black", font=button_font,
                                     height=2, highlightbackground="black", highlightcolor="green",
                                     highlightthickness=2, justify="center", overrelief="raised",
                                     padx=10, pady=5, width=15, wraplength=100)
        # Nút Trung Bình
        self.button_medium = tk.Button(self.root,
                                     text="Trung Bình",
                                     command=lambda: self.select_difficulty_and_start("medium"),
                                     activebackground="#3399ff", activeforeground="white",
                                     anchor="center", bd=3, bg="#FFD700", cursor="hand2",
                                     disabledforeground="gray", fg="black", font=button_font,
                                     height=2, highlightbackground="black", highlightcolor="green",
                                     highlightthickness=2, justify="center", overrelief="raised",
                                     padx=10, pady=5, width=15, wraplength=100)
        # Nút Khó
        self.button_hard = tk.Button(self.root,
                                     text="Khó",
                                     command=lambda: self.select_difficulty_and_start("hard"),
                                     activebackground="#3399ff", activeforeground="white",
                                     anchor="center", bd=3, bg="#FF9900", cursor="hand2",
                                     disabledforeground="gray", fg="black", font=button_font,
                                     height=2, highlightbackground="black", highlightcolor="green",
                                     highlightthickness=2, justify="center", overrelief="raised",
                                     padx=10, pady=5, width=15, wraplength=100)
        center_x = self.canvas.winfo_width() / 2
        button_y = self.canvas.winfo_height() * 0.6
        button_spacing = self.canvas.winfo_width() / 4.5
        # Hiển thị 3 nút độ khó
        self.canvas.create_window(center_x - button_spacing, button_y,
                                 window=self.button_easy, anchor="center", tags="easy_button")
        self.canvas.create_window(center_x, button_y,
                                 window=self.button_medium, anchor="center", tags="medium_button")
        self.canvas.create_window(center_x + button_spacing, button_y,
                                 window=self.button_hard, anchor="center", tags="hard_button")
        
        # Nút Quay Lại
        self.button_back2 = tk.Button(self.root,
                                    text="Quay Lại",
                                    command=self.show_color_selection_screen,
                                    activebackground="#59080A", activeforeground="white",
                                    anchor="center", bd=3, bg="#E33539", cursor="hand2",
                                    disabledforeground="gray", fg="black", font=button_font,
                                    height=2, highlightbackground="black", highlightcolor="green",
                                    highlightthickness=2, justify="center", overrelief="raised",
                                    padx=10, pady=5, width=15, wraplength=100)
        self.canvas.create_window(center_x, button_y + 80,
                                 window=self.button_back2, anchor="center", tags="back2_button")

    def select_difficulty_and_start(self, difficulty):
        """Hiện popup xác nhận trước khi vào game với độ khó đã chọn."""
        self.selected_difficulty = difficulty
        # Nội dung mô tả theo từng độ khó
        if difficulty == "easy":
            desc = "Chế độ dễ:\nAI chỉ nhìn trước 2 lượt rất dễ thắng và chạy nhanh."
        elif difficulty == "medium":
            desc = "Chế độ trung bình:\nAI nhìn trước 3 lượt độ khó vừa phải."
        else:
            desc = "Chế độ khó:\nAI nhìn trước 4 lượt cực kì khó thắng và chạy chậm hơn dễ ngốn ram."
        self.show_confirm_popup(desc)

    def show_confirm_popup(self, desc):
        """Hiển thị popup xác nhận với mô tả chế độ, 2 nút OK và Quay lại."""
        popup = tk.Toplevel(self.root)
        popup.title("Xác nhận chế độ chơi")
        popup.geometry("400x220")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()
        # Nền trắng, viền đẹp
        popup.configure(bg="#f8f8f8")
        # Label tiêu đề
        title = tk.Label(popup, text="Xác nhận chế độ chơi", font=("Gill Sans Nova Ultra Bold", 16, "bold"), fg="#222", bg="#f8f8f8")
        title.pack(pady=(18, 8))
        # Label mô tả
        desc_label = tk.Label(popup, text=desc, font=("Arial", 12), fg="#333", bg="#f8f8f8", justify="center", wraplength=360)
        desc_label.pack(pady=(0, 18))
        # Frame cho 2 nút
        btn_frame = tk.Frame(popup, bg="#f8f8f8")
        btn_frame.pack(pady=(0, 10))
        # Nút OK
        ok_btn = tk.Button(btn_frame, text="OK", font=("Arial", 12, "bold"), bg="#00C853", fg="white",
                           width=10, height=1, relief="raised", bd=2,
                           command=lambda: [popup.destroy(), self.start_ai_game(self.selected_color, self.selected_difficulty)])
        ok_btn.grid(row=0, column=0, padx=18)
        # Nút Quay lại
        back_btn = tk.Button(btn_frame, text="Quay lại", font=("Arial", 12, "bold"), bg="#E33539", fg="white",
                             width=10, height=1, relief="raised", bd=2,
                             command=popup.destroy)
        back_btn.grid(row=0, column=1, padx=18)
        # Căn giữa popup trên màn hình
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 110
        popup.geometry(f"400x220+{x}+{y}")

    def start_ai_game(self, player_color, difficulty=None):
        """Khởi động game với AI."""
        self.root.destroy()
        try:
            import chess_gui
            if difficulty is not None:
                chess_gui.main(game_mode='ai', player_color=player_color, difficulty=difficulty)
            else:
                chess_gui.main(game_mode='ai', player_color=player_color)
        except ImportError:
            print("Không tìm thấy file chess_gui.py")
        except Exception as e:
            print(f"Lỗi khi khởi động game: {e}")

    def back_to_main_menu(self):
        """Quay lại màn hình chính."""
        # Xóa tất cả các widget hiện tại
        self.canvas.delete("all")
        # Xóa các biến nút cũ để tránh lỗi
        if hasattr(self, 'button_white'):
            self.button_white = None
        if hasattr(self, 'button_black'):
            self.button_black = None
        if hasattr(self, 'button_back'):
            self.button_back = None
        if hasattr(self, 'button_easy'):
            self.button_easy = None
        if hasattr(self, 'button_medium'):
            self.button_medium = None
        if hasattr(self, 'button_hard'):
            self.button_hard = None
        if hasattr(self, 'button_back2'):
            self.button_back2 = None
        
        # Tải lại ảnh nền
        if self.original_background_image:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            if width > 10 and height > 10:
                resized_image = self.original_background_image.resize((width, height), Image.LANCZOS)
                self.background_photo = ImageTk.PhotoImage(resized_image)
                self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw", tags="background")
        
        # Tạo lại các nút ban đầu
        self.create_choice_buttons()
        
        # Cập nhật vị trí các nút
        self.perform_resize()

    def button_clicked_exit(self):
        # Đóng cửa sổ và thoát chương trình
        self.root.destroy()
        sys.exit()

    def run(self):
        # Chạy ứng dụng
        self.root.mainloop()

if __name__ == "__main__":
    app = ChessInterface()
    app.run()