import tkinter as tk
import time
from tkinter import messagebox
from generator import SudokuGenerator
from ui import SudokuUI


class SudokuGame:
    """Основной класс игры"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Судоку")
        self.root.geometry("650x750")

        # Инициализация
        self.generator = SudokuGenerator()
        self.ui = SudokuUI(self.root)

        # Данные игры
        self.board = None
        self.solution = None
        self.user_board = [[0 for _ in range(9)] for _ in range(9)]
        self.mistakes = 0
        self.start_time = None
        self.timer_running = False
        self.difficulty = 'medium'

        # Настройка
        self.setup_menu()
        self.setup_stats()
        self.setup_bindings()

        # Начинаем игру
        self.new_game()

    def setup_menu(self):
        """Настройка меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Меню Игра
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Игра", menu=game_menu)
        game_menu.add_command(label="Новая игра", command=self.new_game)
        game_menu.add_separator()
        game_menu.add_command(label="Решить", command=self.solve_puzzle)
        game_menu.add_command(label="Проверить", command=self.check_solution)
        game_menu.add_command(label="Очистить", command=self.clear_user_input)
        game_menu.add_separator()
        game_menu.add_command(label="Выход", command=self.root.quit)

        # Меню Сложность
        difficulty_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Сложность", menu=difficulty_menu)
        difficulty_menu.add_radiobutton(label="Легкая",
                                        command=lambda: self.set_difficulty('easy'))
        difficulty_menu.add_radiobutton(label="Средняя",
                                        command=lambda: self.set_difficulty('medium'))
        difficulty_menu.add_radiobutton(label="Сложная",
                                        command=lambda: self.set_difficulty('hard'))

        # Меню Справка
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="Правила", command=self.show_rules)
        help_menu.add_command(label="О программе", command=self.show_about)

    def setup_stats(self):
        """Настройка статистики"""
        stats_frame = tk.Frame(self.root, bg="#f0f0f0")
        stats_frame.pack(fill=tk.X, padx=10, pady=5)

        self.mistakes_label = tk.Label(stats_frame, text="Ошибок: 0",
                                       bg="#f0f0f0", font=("Arial", 10))
        self.mistakes_label.pack(side=tk.LEFT, padx=20)

        self.timer_label = tk.Label(stats_frame, text="Время: 00:00",
                                    bg="#f0f0f0", font=("Arial", 10))
        self.timer_label.pack(side=tk.RIGHT, padx=20)

    def setup_bindings(self):
        """Настройка привязок клавиш"""
        self.root.bind("<Key>", self.on_key_press)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_key_press(self, event):
        """Обработка нажатия клавиш"""
        if event.char.isdigit() and event.char != '0':
            self.ui.on_number_click(int(event.char))
        elif event.keysym in ['Delete', 'BackSpace']:
            self.clear_selected_cell()
        elif event.keysym == 'Escape':
            self.ui.selected_cell = None

    def new_game(self):
        """Начать новую игру"""
        try:
            self.board, self.solution = self.generator.create_puzzle(self.difficulty)
            self.user_board = [[0 for _ in range(9)] for _ in range(9)]
            self.mistakes = 0
            self.mistakes_label.config(text="Ошибок: 0")

            # Заполняем поле
            for i in range(9):
                for j in range(9):
                    cell = self.ui.cells[i][j]
                    if self.board[i][j] != 0:
                        cell.delete(0, tk.END)
                        cell.insert(0, str(self.board[i][j]))
                        cell.config(bg=self.ui.fixed_color, fg="black")
                        self.user_board[i][j] = self.board[i][j]
                    else:
                        cell.delete(0, tk.END)
                        bg_color = self.ui.cell_color
                        if (i // 3 + j // 3) % 2 == 0:
                            bg_color = "#f5f5f5"
                        cell.config(bg=bg_color, fg="blue")

            # Запускаем таймер
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

            self.ui.selected_cell = None

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать игру: {str(e)}")

    def set_difficulty(self, difficulty):
        """Установка сложности"""
        self.difficulty = difficulty
        self.new_game()

    def solve_puzzle(self):
        """Решить головоломку"""
        if messagebox.askyesno("Решить", "Показать решение?"):
            for i in range(9):
                for j in range(9):
                    cell = self.ui.cells[i][j]
                    cell.delete(0, tk.END)
                    cell.insert(0, str(self.solution[i][j]))
                    cell.config(bg=self.ui.fixed_color, fg="green")

            self.timer_running = False

    def check_solution(self):
        """Проверить решение"""
        correct = True
        for i in range(9):
            for j in range(9):
                cell = self.ui.cells[i][j]
                value = cell.get()

                if value:
                    try:
                        num = int(value)
                        if self.solution and num != self.solution[i][j]:
                            cell.config(bg=self.ui.error_color)
                            correct = False
                            self.mistakes += 1
                        else:
                            bg_color = self.ui.cell_color
                            if (i // 3 + j // 3) % 2 == 0:
                                bg_color = "#f5f5f5"
                            cell.config(bg=bg_color)
                    except ValueError:
                        cell.config(bg=self.ui.error_color)
                        correct = False

        self.mistakes_label.config(text=f"Ошибок: {self.mistakes}")

        if correct:
            messagebox.showinfo("Проверка", "Все правильно!")
            self.timer_running = False
        else:
            messagebox.showwarning("Проверка", f"Найдены ошибки! Ошибок: {self.mistakes}")

    def clear_user_input(self):
        """Очистить введенные пользователем данные"""
        if messagebox.askyesno("Очистить", "Очистить все введенные числа?"):
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == 0:
                        self.ui.cells[i][j].delete(0, tk.END)
                        self.user_board[i][j] = 0
                        bg_color = self.ui.cell_color
                        if (i // 3 + j // 3) % 2 == 0:
                            bg_color = "#f5f5f5"
                        self.ui.cells[i][j].config(bg=bg_color)

            self.mistakes = 0
            self.mistakes_label.config(text="Ошибок: 0")

    def clear_selected_cell(self):
        """Очистить выбранную ячейку"""
        if self.ui.selected_cell:
            row, col = self.ui.selected_cell
            if self.board[row][col] == 0:
                self.ui.cells[row][col].delete(0, tk.END)
                self.user_board[row][col] = 0

    def update_timer(self):
        """Обновление таймера"""
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer_label.config(text=f"Время: {minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)

    def show_rules(self):
        """Показать правила"""
        rules = """ПРАВИЛА СУДОКУ:

1. Цель: заполнить сетку 9×9 цифрами от 1 до 9
2. Каждая строка должна содержать все цифры от 1 до 9 без повторений
3. Каждый столбец должен содержать все цифры от 1 до 9 без повторений
4. Каждый квадрат 3×3 должен содержать все цифры от 1 до 9 без повторений

УПРАВЛЕНИЕ:
• ЛКМ - выбрать ячейку
• Цифры 1-9 - ввести число
• Delete/BackSpace - очистить ячейку
• Esc - снять выделение
• Кнопки управления для дополнительных действий"""
        messagebox.showinfo("Правила игры", rules)

    def show_about(self):
        """О программе"""
        about_text = """Судоку v1.0

Функции:
• Генерация уникальных головоломок
• 3 уровня сложности
• Проверка решений
• Таймер и статистика"""
        messagebox.showinfo("О программе", about_text)

    def on_closing(self):
        """Обработка закрытия окна"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.timer_running = False
            self.root.destroy()

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


if __name__ == "__main__":
    try:
        game = SudokuGame()
        game.run()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить приложение: {str(e)}")