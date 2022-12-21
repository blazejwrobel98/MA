def display_board(board):
    board_sample = ["+-------+-------+-------+",
                    "|       |       |       |",
                    "|   {}   |   {}   |   {}   |"]
    for i in range(13):
        if i % 4 == 0:
            print(board_sample[0])
        elif i in [2, 6, 10]:
            print(board_sample[2].format(*board[i // 4]))
        else:
            print(board_sample[1])


def enter_move(board):
    while True:
        move = input('Enter your move: ')
        if move in [str(x) for x in range(1, 10)]:
            move = int(move)
            break
    for row in board:
        for i, x in enumerate(row):
            if x == move:
                row[i] = 'O'


def make_list_of_free_fields(board):
    free_fields = []
    for row in board:
        for x in row:
            if x not in ['X', 'O']:
                free_fields.append(x)
    return free_fields


def victory_for(board, sign):
    # check rows
    for row in board:
        if row.count(sign) == 3:
            return True
    # check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == sign:
            return True
    # check diagonals
    if board[0][0] == board[1][1] == board[2][2] == sign:
        return True
    if board[0][2] == board[1][1] == board[2][0] == sign:
        return True
    return False


def draw_move(board):
    import random
    free_fields = make_list_of_free_fields(board)
    move = random.choice(free_fields)
    for row in board:
        for i, x in enumerate(row):
            if x == move:
                row[i] = 'X'


def main():
    board = [[1, 2, 3], [4, 'X', 6], [7, 8, 9]]
    while True:
        display_board(board)
        enter_move(board)
        display_board(board)
        if victory_for(board, 'O'):
            print('You won!')
            break
        make_list_of_free_fields(board)
        draw_move(board)
        display_board(board)
        if victory_for(board, 'X'):
            print('You lost!')
            break
        make_list_of_free_fields(board)
        if len(make_list_of_free_fields(board)) == 0:
            print('Draw!')
            break


if __name__ == '__main__':
    main()
