import random


class SudokuGenerator:
    """Генератор головоломок Судоку"""

    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def generate_full_board(self):
        """Генерирует полное решение Судоку"""
        self.solve_board()
        return [row[:] for row in self.board]

    def solve_board(self):
        """Решает доску методом backtracking"""
        find = self.find_empty()
        if not find:
            return True
        row, col = find

        numbers = list(range(1, 10))
        random.shuffle(numbers)

        for num in numbers:
            if self.is_valid(row, col, num):
                self.board[row][col] = num

                if self.solve_board():
                    return True

                self.board[row][col] = 0
        return False

    def find_empty(self):
        """Находит пустую клетку"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, row, col, num):
        """Проверяет валидность числа в позиции"""
        # Проверка строки
        for j in range(9):
            if self.board[row][j] == num:
                return False

        # Проверка столбца
        for i in range(9):
            if self.board[i][col] == num:
                return False

        # Проверка квадрата 3x3
        box_row = row // 3 * 3
        box_col = col // 3 * 3

        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def create_puzzle(self, difficulty='medium'):
        """Создает головоломку заданной сложности"""
        self.generate_full_board()
        solution = [row[:] for row in self.board]

        # Определяем количество убираемых чисел
        if difficulty == 'easy':
            cells_to_remove = 40
        elif difficulty == 'medium':
            cells_to_remove = 50
        else:  # hard
            cells_to_remove = 60

        # Убираем числа
        attempts = cells_to_remove
        while attempts > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            if self.board[row][col] != 0:
                backup = self.board[row][col]
                self.board[row][col] = 0

                # Проверяем уникальность решения
                temp_board = [row[:] for row in self.board]
                if not self.has_unique_solution(temp_board):
                    self.board[row][col] = backup
                else:
                    attempts -= 1

        return [row[:] for row in self.board], solution

    def has_unique_solution(self, board):
        """Проверяет, имеет ли доска единственное решение"""
        count = [0]
        self.count_solutions(board, count)
        return count[0] == 1

    def count_solutions(self, board, count):
        """Считает количество решений"""
        if count[0] > 1:
            return

        find = self.find_empty_in_board(board)
        if not find:
            count[0] += 1
            return

        row, col = find
        for num in range(1, 10):
            if self.is_valid_in_board(board, row, col, num):
                board[row][col] = num
                self.count_solutions(board, count)
                board[row][col] = 0

    def find_empty_in_board(self, board):
        """Находит пустую клетку в заданной доске"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid_in_board(self, board, row, col, num):
        """Проверка валидности для заданной доски"""
        # Проверка строки
        for j in range(9):
            if board[row][j] == num:
                return False

        # Проверка столбца
        for i in range(9):
            if board[i][col] == num:
                return False

        # Проверка квадрата
        box_row = row // 3 * 3
        box_col = col // 3 * 3

        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False

        return True


if __name__ == "__main__":
    # Тест генератора
    generator = SudokuGenerator()
    puzzle, solution = generator.create_puzzle('medium')
    print("Puzzle:")
    for row in puzzle:
        print(row)
    print("\nSolution:")
    for row in solution:
        print(row)