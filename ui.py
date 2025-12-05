import tkinter as tk
from tkinter import messagebox


class SudokuUI:
    """Пользовательский интерфейс для Судоку"""

    def __init__(self, root):
        self.root = root
        self.root.title("Судоку")
        self.root.geometry("600x700")

        # Цвета
        self.bg_color = "#f0f0f0"
        self.cell_color = "#ffffff"
        self.selected_color = "#e0e0ff"
        self.fixed_color = "#e0e0e0"
        self.error_color = "#ffcccc"

        # Инициализация
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.selected_cell = None

        self.setup_ui()

    def setup_ui(self):
        """Настройка интерфейса"""
        # Основной фрейм
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Заголовок
        title_label = tk.Label(main_frame, text="СУДОКУ",
                               font=("Arial", 24, "bold"),
                               bg=self.bg_color, fg="#333333")
        title_label.pack(pady=(0, 20))

        # Фрейм для доски
        self.board_frame = tk.Frame(main_frame, bg="black")
        self.board_frame.pack(pady=(0, 20))

        # Создаем сетку
        self.create_grid()

        # Фрейм для кнопок
        buttons_frame = tk.Frame(main_frame, bg=self.bg_color)
        buttons_frame.pack(pady=10)

        # Кнопки управления
        tk.Button(buttons_frame, text="Новая игра", width=12,
                  command=self.on_new_game, bg="#4CAF50", fg="white",
                  font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        tk.Button(buttons_frame, text="Проверить", width=12,
                  command=self.on_check, bg="#2196F3", fg="white",
                  font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        tk.Button(buttons_frame, text="Очистить", width=12,
                  command=self.on_clear, bg="#FF9800", fg="white",
                  font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        tk.Button(buttons_frame, text="Справка", width=12,
                  command=self.on_help, bg="#9C27B0", fg="white",
                  font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        # Панель чисел
        numbers_frame = tk.Frame(main_frame, bg=self.bg_color)
        numbers_frame.pack(pady=10)

        tk.Label(numbers_frame, text="Выберите число:",
                 bg=self.bg_color, font=("Arial", 10)).pack()

        numbers_buttons = tk.Frame(numbers_frame, bg=self.bg_color)
        numbers_buttons.pack(pady=5)

        for i in range(1, 10):
            btn = tk.Button(numbers_buttons, text=str(i), width=3,
                            command=lambda num=i: self.on_number_click(num),
                            bg="#607D8B", fg="white", font=("Arial", 12))
            btn.pack(side=tk.LEFT, padx=2)

    def create_grid(self):
        """Создание сетки 9x9"""
        for i in range(9):
            for j in range(9):
                # Определяем цвет фона
                bg_color = self.cell_color
                if (i // 3 + j // 3) % 2 == 0:
                    bg_color = "#f5f5f5"

                # Создаем Entry
                cell = tk.Entry(self.board_frame, width=3,
                                font=("Arial", 18, "bold"),
                                justify='center', bg=bg_color,
                                relief=tk.SOLID, borderwidth=1)
                cell.grid(row=i, column=j,
                          padx=(1 if j % 3 != 0 else 3),
                          pady=(1 if i % 3 != 0 else 3))

                # Привязываем события
                cell.bind("<Button-1>", lambda e, row=i, col=j: self.cell_clicked(row, col))
                cell.bind("<FocusIn>", lambda e, row=i, col=j: self.cell_clicked(row, col))

                self.cells[i][j] = cell

    def cell_clicked(self, row, col):
        """Обработка клика по ячейке"""
        if self.selected_cell:
            old_row, old_col = self.selected_cell
            old_bg = self.cells[old_row][old_col].cget('bg')
            if old_bg != self.fixed_color and old_bg != self.error_color:
                normal_bg = self.cell_color
                if (old_row // 3 + old_col // 3) % 2 == 0:
                    normal_bg = "#f5f5f5"
                self.cells[old_row][old_col].config(bg=normal_bg)

        self.selected_cell = (row, col)
        current_bg = self.cells[row][col].cget('bg')
        if current_bg != self.fixed_color and current_bg != self.error_color:
            self.cells[row][col].config(bg=self.selected_color)

        self.cells[row][col].focus_set()

    def on_number_click(self, number):
        """Обработка нажатия цифры"""
        if self.selected_cell:
            row, col = self.selected_cell
            cell = self.cells[row][col]

            # Проверяем, можно ли редактировать
            current_value = cell.get()
            if cell.cget('bg') == self.fixed_color:
                messagebox.showwarning("Внимание", "Это число нельзя изменить!")
                return

            # Вставляем число
            cell.delete(0, tk.END)
            cell.insert(0, str(number))

            # Сбрасываем цвет ошибки
            normal_bg = self.cell_color
            if (row // 3 + col // 3) % 2 == 0:
                normal_bg = "#f5f5f5"
            cell.config(bg=normal_bg)

    def on_new_game(self):
        """Новая игра"""
        messagebox.showinfo("Новая игра", "Начинаем новую игру!")
        self.clear_board()

    def on_check(self):
        """Проверка решения"""
        messagebox.showinfo("Проверка", "Проверяем решение...")

    def on_clear(self):
        """Очистка доски"""
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].cget('bg') != self.fixed_color:
                    self.cells[i][j].delete(0, tk.END)

    def on_help(self):
        """Справка"""
        help_text = """ПРАВИЛА СУДОКУ:

1. Заполните сетку цифрами от 1 до 9
2. В каждой строке все цифры должны быть разными
3. В каждом столбце все цифры должны быть разными
4. В каждом квадрате 3x3 все цифры должны быть разными

УПРАВЛЕНИЕ:
• Кликните на ячейку для выбора
• Нажмите кнопку с цифрой для ввода
• Используйте кнопки управления для действий"""
        messagebox.showinfo("Справка", help_text)

    def clear_board(self):
        """Очистка всех изменяемых ячеек"""
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].cget('bg') != self.fixed_color:
                    self.cells[i][j].delete(0, tk.END)
                    normal_bg = self.cell_color
                    if (i // 3 + j // 3) % 2 == 0:
                        normal_bg = "#f5f5f5"
                    self.cells[i][j].config(bg=normal_bg)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuUI(root)
    root.mainloop()