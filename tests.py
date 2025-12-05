import unittest
from src.generator import SudokuGenerator


class TestSudokuGenerator(unittest.TestCase):
    """Тесты генератора Судоку"""

    def setUp(self):
        self.generator = SudokuGenerator()

    def test_board_generation(self):
        """Тест генерации доски"""
        board = self.generator.generate_full_board()

        # Проверяем размер
        self.assertEqual(len(board), 9)
        for row in board:
            self.assertEqual(len(row), 9)

        # Проверяем, что все ячейки заполнены
        for row in board:
            for cell in row:
                self.assertGreater(cell, 0)
                self.assertLessEqual(cell, 9)

    def test_puzzle_creation(self):
        """Тест создания головоломки"""
        puzzle, solution = self.generator.create_puzzle('medium')

        # Проверяем, что решение полное
        for row in solution:
            for cell in row:
                self.assertGreater(cell, 0)

        # Проверяем, что в головоломке есть пустые клетки
        empty_cells = sum(1 for row in puzzle for cell in row if cell == 0)
        self.assertGreater(empty_cells, 0)

    def test_difficulty_levels(self):
        """Тест разных уровней сложности"""
        for difficulty in ['easy', 'medium', 'hard']:
            puzzle, _ = self.generator.create_puzzle(difficulty)
            empty_cells = sum(1 for row in puzzle for cell in row if cell == 0)

            if difficulty == 'easy':
                self.assertGreaterEqual(empty_cells, 35)
            elif difficulty == 'medium':
                self.assertGreaterEqual(empty_cells, 45)
            else:  # hard
                self.assertGreaterEqual(empty_cells, 55)


if __name__ == '__main__':
    unittest.main()