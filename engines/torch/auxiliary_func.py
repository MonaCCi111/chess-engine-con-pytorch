import numpy as np
from chess import Board


def board_to_matrix(board: Board):
    # 8x8 - размер шахматной доски
    # 12 каналов - количество уникальных фигур (6 белых и 6 черных)
    # 13-й канал для возможных ходов
    matrix = np.zeros((13, 8, 8))
    piece_map = board.piece_map()

    # Заполняем первые 12 каналов фигурами
    for square, piece in piece_map.items():
        row, col = divmod(square, 8)
        piece_type = piece.piece_type - 1
        piece_color = 0 if piece.color else 6
        matrix[piece_type + piece_color, row, col] = 1

    # Заполняем 13-й канал возможными ходами
    legal_moves = board.legal_moves
    for move in legal_moves:
        to_square = move.to_square
        row_to, col_to = divmod(to_square, 8)
        matrix[12, row_to, col_to] = 1

    return matrix


def create_input_for_nn(games):
    X = []
    y = []
    for game in games:
        board = game.board() # Инициализация доски
        for move in game.mainline_moves(): # Перебираем ходы партии
            X.append(board_to_matrix(board))
            y.append(move.uci()) # Добавляем ход в формате UCI
            board.push(move) # Применяем ход
    return np.array(X, dtype=np.float32), np.array(y)


def encode_moves(moves):
    move_to_int = {move: idx for idx, move in enumerate(set(moves))} # Уникальные ходы
    return np.array([move_to_int[move] for move in moves], dtype=np.float32), move_to_int
