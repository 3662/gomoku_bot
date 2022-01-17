"""
dictionaries of patterns of interest according to move policies
key: pattern, value: list of moves to play in pattern
"""
BLACK_WIN = {}
BLACK_WIN["01111"] = [0]
BLACK_WIN["10111"] = [1]
BLACK_WIN["11011"] = [2]
BLACK_WIN["11101"] = [3]
BLACK_WIN["11110"] = [4]

WHITE_WIN = {}
WHITE_WIN["02222"] = [0]
WHITE_WIN["20222"] = [1]
WHITE_WIN["22022"] = [2]
WHITE_WIN["22202"] = [3]
WHITE_WIN["22220"] = [4]

OPEN_FOUR_BLACK_6 = {}
OPEN_FOUR_BLACK_6["001110"] = [1]
OPEN_FOUR_BLACK_6["010110"] = [2]
OPEN_FOUR_BLACK_6["011010"] = [3]
OPEN_FOUR_BLACK_6["011100"] = [4]

OPEN_FOUR_WHITE_6 = {}
OPEN_FOUR_WHITE_6["002220"] = [1]
OPEN_FOUR_WHITE_6["020220"] = [2]
OPEN_FOUR_WHITE_6["022020"] = [3]
OPEN_FOUR_WHITE_6["022200"] = [4]

PREVENT_OPEN_FOUR_BLACK_6 = {}
PREVENT_OPEN_FOUR_BLACK_6["010110"] = [0, 2, 5]
PREVENT_OPEN_FOUR_BLACK_6["011010"] = [0, 3, 5]
PREVENT_OPEN_FOUR_BLACK_6["001110"] = [0, 1, 5]
PREVENT_OPEN_FOUR_BLACK_6["011100"] = [0, 4, 5]

PREVENT_OPEN_FOUR_WHITE_6 = {}
PREVENT_OPEN_FOUR_WHITE_6["020220"] = [0, 2, 5]
PREVENT_OPEN_FOUR_WHITE_6["022020"] = [0, 3, 5]
PREVENT_OPEN_FOUR_WHITE_6["002220"] = [0, 1, 5]
PREVENT_OPEN_FOUR_WHITE_6["022200"] = [0, 4, 5]

PREVENT_OPEN_FOUR_BLACK_7 = {}
PREVENT_OPEN_FOUR_BLACK_7["0011100"] = [1, 5]
PREVENT_OPEN_FOUR_BLACK_7["2011100"] = [1, 5, 6]
PREVENT_OPEN_FOUR_BLACK_7["0011102"] = [0, 1, 5]

PREVENT_OPEN_FOUR_WHITE_7 = {}
PREVENT_OPEN_FOUR_WHITE_7["0022200"] = [1, 5]
PREVENT_OPEN_FOUR_WHITE_7["1022200"] = [1, 5, 6]
PREVENT_OPEN_FOUR_WHITE_7["0022201"] = [0, 1, 5]

"""
precalculated components for a 7*7 board
"""
ROWS = [[9, 10, 11, 12, 13, 14, 15], [17, 18, 19, 20, 21, 22, 23], [25, 26, 27, 28, 29, 30, 31], [33, 34, 35, 36, 37, 38, 39], [41, 42, 43, 44, 45, 46, 47], [49, 50, 51, 52, 53, 54, 55], [57, 58, 59, 60, 61, 62, 63]]
COLS = [[9, 17, 25, 33, 41, 49, 57], [10, 18, 26, 34, 42, 50, 58], [11, 19, 27, 35, 43, 51, 59], [12, 20, 28, 36, 44, 52, 60], [13, 21, 29, 37, 45, 53, 61], [14, 22, 30, 38, 46, 54, 62], [15, 23, 31, 39, 47, 55, 63]]
DIAGS = [[9, 18, 27, 36, 45, 54, 63], [10, 19, 28, 37, 46, 55], [11, 20, 29, 38, 47], [17, 26, 35, 44, 53, 62], [25, 34, 43, 52, 61], [41, 34, 27, 20, 13], [49, 42, 35, 28, 21, 14], [57, 50, 43, 36, 29, 22, 15], [58, 51, 44, 37, 30, 23], [59, 52, 45, 38, 31]]
FIVE_IN_A_ROW_GROUPS = [[9, 10, 11, 12, 13], [10, 11, 12, 13, 14], [11, 12, 13, 14, 15], [17, 18, 19, 20, 21], [18, 19, 20, 21, 22], [19, 20, 21, 22, 23], [25, 26, 27, 28, 29], [26, 27, 28, 29, 30], [27, 28, 29, 30, 31], [33, 34, 35, 36, 37], [34, 35, 36, 37, 38], [35, 36, 37, 38, 39], [41, 42, 43, 44, 45], [42, 43, 44, 45, 46], [43, 44, 45, 46, 47], [49, 50, 51, 52, 53], [50, 51, 52, 53, 54], [51, 52, 53, 54, 55], [57, 58, 59, 60, 61], [58, 59, 60, 61, 62], [59, 60, 61, 62, 63], [9, 17, 25, 33, 41], [17, 25, 33, 41, 49], [25, 33, 41, 49, 57], [10, 18, 26, 34, 42], [18, 26, 34, 42, 50], [26, 34, 42, 50, 58], [11, 19, 27, 35, 43], [19, 27, 35, 43, 51], [27, 35, 43, 51, 59], [12, 20, 28, 36, 44], [20, 28, 36, 44, 52], [28, 36, 44, 52, 60], [13, 21, 29, 37, 45], [21, 29, 37, 45, 53], [29, 37, 45, 53, 61], [14, 22, 30, 38, 46], [22, 30, 38, 46, 54], [30, 38, 46, 54, 62], [15, 23, 31, 39, 47], [23, 31, 39, 47, 55], [31, 39, 47, 55, 63], [9, 18, 27, 36, 45], [18, 27, 36, 45, 54], [27, 36, 45, 54, 63], [10, 19, 28, 37, 46], [19, 28, 37, 46, 55], [11, 20, 29, 38, 47], [17, 26, 35, 44, 53], [26, 35, 44, 53, 62], [25, 34, 43, 52, 61], [41, 34, 27, 20, 13], [49, 42, 35, 28, 21], [42, 35, 28, 21, 14], [57, 50, 43, 36, 29], [50, 43, 36, 29, 22], [43, 36, 29, 22, 15], [58, 51, 44, 37, 30], [51, 44, 37, 30, 23], [59, 52, 45, 38, 31]]
SIX_IN_A_ROW_GROUPS = [[9, 10, 11, 12, 13, 14], [10, 11, 12, 13, 14, 15], [17, 18, 19, 20, 21, 22], [18, 19, 20, 21, 22, 23], [25, 26, 27, 28, 29, 30], [26, 27, 28, 29, 30, 31], [33, 34, 35, 36, 37, 38], [34, 35, 36, 37, 38, 39], [41, 42, 43, 44, 45, 46], [42, 43, 44, 45, 46, 47], [49, 50, 51, 52, 53, 54], [50, 51, 52, 53, 54, 55], [57, 58, 59, 60, 61, 62], [58, 59, 60, 61, 62, 63], [9, 17, 25, 33, 41, 49], [17, 25, 33, 41, 49, 57], [10, 18, 26, 34, 42, 50], [18, 26, 34, 42, 50, 58], [11, 19, 27, 35, 43, 51], [19, 27, 35, 43, 51, 59], [12, 20, 28, 36, 44, 52], [20, 28, 36, 44, 52, 60], [13, 21, 29, 37, 45, 53], [21, 29, 37, 45, 53, 61], [14, 22, 30, 38, 46, 54], [22, 30, 38, 46, 54, 62], [15, 23, 31, 39, 47, 55], [23, 31, 39, 47, 55, 63], [9, 18, 27, 36, 45, 54], [18, 27, 36, 45, 54, 63], [10, 19, 28, 37, 46, 55], [17, 26, 35, 44, 53, 62], [49, 42, 35, 28, 21, 14], [57, 50, 43, 36, 29, 22], [50, 43, 36, 29, 22, 15], [58, 51, 44, 37, 30, 23]]
SEVEN_IN_A_ROW_GROUPS = [[9, 10, 11, 12, 13, 14, 15], [17, 18, 19, 20, 21, 22, 23], [25, 26, 27, 28, 29, 30, 31], [33, 34, 35, 36, 37, 38, 39], [41, 42, 43, 44, 45, 46, 47], [49, 50, 51, 52, 53, 54, 55], [57, 58, 59, 60, 61, 62, 63], [9, 17, 25, 33, 41, 49, 57], [10, 18, 26, 34, 42, 50, 58], [11, 19, 27, 35, 43, 51, 59], [12, 20, 28, 36, 44, 52, 60], [13, 21, 29, 37, 45, 53, 61], [14, 22, 30, 38, 46, 54, 62], [15, 23, 31, 39, 47, 55, 63], [9, 18, 27, 36, 45, 54, 63], [57, 50, 43, 36, 29, 22, 15]]

"""
return the type of moves and set of moves to consider for a policy of 
random selection of moves
"""
def random_policy_moves(board, color):
    move_type = "Random"
    list_of_moves = board.get_empty_points()

    return move_type, list_of_moves 

"""
return the type of moves and set of moves to consider for a policy of 
rulebased selection of moves
"""
def rulebased_policy_moves(board, color):
    move_type = ""
    list_of_moves = []

    five_in_a_row_groups_pos = board.five_in_a_row_groups
    five_in_a_row_groups_color = []

    for group in five_in_a_row_groups_pos:
        temp = []
        for c in group:
            temp.append(board.get_color(c))
        five_in_a_row_groups_color.append(temp)

    # rule 1: win in one move
    if color == 1:
        for i in range(len(five_in_a_row_groups_color)):
            pattern = "".join([str(c) for c in five_in_a_row_groups_color[i]])

            if pattern in BLACK_WIN.keys():
                for j in BLACK_WIN[pattern]:
                    list_of_moves.append(five_in_a_row_groups_pos[i][j])

    if color == 2:
        for i in range(len(five_in_a_row_groups_color)):
            pattern = "".join([str(c) for c in five_in_a_row_groups_color[i]])

            if pattern in WHITE_WIN.keys():
                for j in WHITE_WIN[pattern]:
                    list_of_moves.append(five_in_a_row_groups_pos[i][j]) 

    if len(list_of_moves) > 0:
        move_type = "Win"

        return move_type, list_of_moves

    # rule 2: block the win of opponent
    if color == 2:
        for i in range(len(five_in_a_row_groups_color)):
            pattern = "".join([str(c) for c in five_in_a_row_groups_color[i]])

            if pattern in BLACK_WIN.keys():
                for j in BLACK_WIN[pattern]:
                    list_of_moves.append(five_in_a_row_groups_pos[i][j])

    if color == 1:
        for i in range(len(five_in_a_row_groups_color)):
            pattern = "".join([str(c) for c in five_in_a_row_groups_color[i]])

            if pattern in WHITE_WIN.keys():
                for j in WHITE_WIN[pattern]:
                    list_of_moves.append(five_in_a_row_groups_pos[i][j])  

    if len(list_of_moves) > 0:
        move_type = "BlockWin"

        return move_type, list_of_moves

    six_in_a_row_groups_pos = board.six_in_a_row_groups
    six_in_a_row_groups_color = []

    for group in six_in_a_row_groups_pos:
        temp = []
        # print(group)
        for c in group:
            temp.append(board.get_color(c))
        six_in_a_row_groups_color.append(temp)

    # rule 3: moves that creates an open four .XXXX.
    if color == 1:
        for i in range(len(six_in_a_row_groups_color)):
            pattern = "".join([str(c) for c in six_in_a_row_groups_color[i]])

            if pattern in OPEN_FOUR_BLACK_6.keys():
                for j in OPEN_FOUR_BLACK_6[pattern]:
                    list_of_moves.append(six_in_a_row_groups_pos[i][j])

    if color == 2:
        for i in range(len(six_in_a_row_groups_color)):
            pattern = "".join([str(c) for c in six_in_a_row_groups_color[i]])

            if pattern in OPEN_FOUR_WHITE_6.keys():
                for j in OPEN_FOUR_WHITE_6[pattern]:
                    list_of_moves.append(six_in_a_row_groups_pos[i][j]) 

    if len(list_of_moves) > 0:
        move_type = "OpenFour"

        return move_type, list_of_moves

    seven_in_a_row_groups_pos = board.seven_in_a_row_groups

    seven_in_a_row_groups_color = []

    for group in seven_in_a_row_groups_pos:
        temp = []
        # print(group)
        for c in group:
            temp.append(board.get_color(c))
        seven_in_a_row_groups_color.append(temp)

    # rule 4: moves that prevent the creation of an open four by opponent
    if color == 1:
        for i in range(len(seven_in_a_row_groups_color)):
            pattern = "".join([str(c) for c in seven_in_a_row_groups_color[i]])

            if pattern in PREVENT_OPEN_FOUR_WHITE_7.keys():
                for j in PREVENT_OPEN_FOUR_WHITE_7[pattern]:
                    list_of_moves.append(seven_in_a_row_groups_pos[i][j])

    if color == 2:
        for i in range(len(seven_in_a_row_groups_color)):
            pattern = "".join([str(c) for c in seven_in_a_row_groups_color[i]])

            if pattern in PREVENT_OPEN_FOUR_BLACK_7.keys():
                for j in PREVENT_OPEN_FOUR_BLACK_7[pattern]:
                    list_of_moves.append(seven_in_a_row_groups_pos[i][j]) 

    if len(list_of_moves) > 0:
        move_type = "BlockOpenFour"

        # remove duplicates
        list_of_moves = list(set(list_of_moves))

        return move_type, list_of_moves

    if color == 1:
        for i in range(len(six_in_a_row_groups_color)):
            pattern = "".join([str(c) for c in six_in_a_row_groups_color[i]])

            if pattern in PREVENT_OPEN_FOUR_WHITE_6.keys():
                for j in PREVENT_OPEN_FOUR_WHITE_6[pattern]:
                    list_of_moves.append(six_in_a_row_groups_pos[i][j])

    if color == 2:
        for i in range(len(six_in_a_row_groups_color)):
            pattern = "".join([str(c) for c in six_in_a_row_groups_color[i]])

            if pattern in PREVENT_OPEN_FOUR_BLACK_6.keys():
                for j in PREVENT_OPEN_FOUR_BLACK_6[pattern]:
                    list_of_moves.append(six_in_a_row_groups_pos[i][j])

    if len(list_of_moves) > 0:
        move_type = "BlockOpenFour"

        # remove duplicates
        list_of_moves = list(set(list_of_moves))

        return move_type, list_of_moves

    # rule 5: random move
    move_type, list_of_moves = random_policy_moves(board, color)
    return move_type, list_of_moves