from battlehack20.stubs import *

# This is an example bot written by the developers!
# Use this to help write your own code, or run it against your bot to see how well you can do!

DEBUG = 0


def dlog(*s):
    s = list(s)
    for i, v in enumerate(s):
        s[i] = str(v)

    if DEBUG > 0:
        log(" ".join(s))


def dulog(*s):
    s = list(s)
    for i, v in enumerate(s):
        s[i] = str(v)

    log(" ".join(s))


def check_space_wrapper(r, c, board_size):
    # check space, except doesn't hit you with game errors
    if r < 0 or c < 0 or c >= board_size or r >= board_size:
        return False
    try:
        return check_space(r, c)
    except:
        return None


def transpose(li):
    return [[row[i] for row in li] for i in range(len(li[0]))]


def min(a, b):
    return a if a < b else b


def max(a, b):
    return a if a > b else b


NEED_SPACE = False


def turn():
    """
    MUST be defined for robot to run
    This function will be called at the beginning of every turn and should contain the bulk of your robot commands
    """
    dlog('Starting Turn!')
    board_size = get_board_size()

    team = get_team()
    opp_team = Team.WHITE if team == Team.BLACK else team.BLACK
    dlog('Team: ' + str(team))

    robottype = get_type()
    dlog('Type: ' + str(robottype))

    if robottype == RobotType.PAWN:
        row, col = get_location()
        dlog('My location is: ' + str(row) + ' ' + str(col))

        if team == Team.WHITE:
            forward = 1
            target = board_size - 1
        else:
            forward = -1
            target = 0

        sens = sense()

        # try catpuring pieces
        if check_space_wrapper(row + forward, col + 1, board_size) == opp_team:  # up and right
            capture(row + forward, col + 1)
            dlog('Captured at: (' + str(row + forward) + ', ' + str(col + 1) + ')')
            return

        elif check_space_wrapper(row + forward, col - 1, board_size) == opp_team:  # up and left
            capture(row + forward, col - 1)
            dlog('Captured at: (' + str(row + forward) + ', ' + str(col - 1) + ')')
            return

        # otherwise try to move forward
        if 0 < row + forward < board_size and not check_space_wrapper(row + forward, col, board_size):
            #               ^  not off the board    ^            and    ^ directly forward is empty
            if True:
                if not (
                        check_space_wrapper(row + 2 * forward, col + 1, board_size) == opp_team
                        #              ^ Attack Right ^
                        or
                        check_space_wrapper(row + 2 * forward, col - 1, board_size) == opp_team):
                # if True:
                    #                  ^ Attack Left ^
                    move_forward()
                    dlog('Moved forward!')
                    return

            ally = 0
            foe = 0
            for x in sens:
                if x[2] == team:
                    ally += 1
                elif x[2] == opp_team:
                    foe += 1

            # if ally > 12:  # foe + 10:
            if ally > foe + 8:
                move_forward()
                dlog('Moved forward! by group')
                return

            if check_space_wrapper(row - forward, col, board_size) and \
                    check_space_wrapper(row - 2 * forward, col, board_size) and \
                    check_space_wrapper(row - 2 * forward, col + 1, board_size) and \
                    check_space_wrapper(row - 2 * forward, col + 1, board_size) and \
                    check_space_wrapper(row - 2 * forward, col - 1, board_size) and \
                    check_space_wrapper(row - 2 * forward, col - 1, board_size):
                move_forward()
                dlog('Moved forward! by backing')
                return

            if row + forward == target:
                move_forward()
                dlog('Moved forward! by closeness')

    else:
        if team == Team.WHITE:
            index = 0
        else:
            index = board_size - 1

        board = get_board()

        row_sum = [{True: 0, False: 0} for _ in range(board_size)]
        tboard = transpose(board)
        for i, row in enumerate(tboard):
            for j, col in enumerate(row):
                if col:
                    row_sum[i][col == team] = row_sum[i][col == team] + 1

        dlog("Row Summary: ", row_sum)

        row_pc_sum = [0.0 for _ in range(board_size)]
        for i, row in enumerate(row_sum):
            # row_pc_sum[i] = (row[True] - row[False]) / (row[False] + row[True] + 0.000000001)
            row_pc_sum[i] = max(row[False], 0.1) / (max(row[True], 0.1) * max(row[True] + row[False], 0.2))
            dulog("Row: ", i)
            dulog(max(row[False], 0.1), max(row[True], 0.1), max(row[True] + row[False], 0.2))

        dulog("Row Percentile Summary: ", row_pc_sum)

        m = -float("inf")
        mr = -1
        for i in range(board_size):
            pc = row_pc_sum[i]
            if not check_space(index, i):
                if pc > m:
                    m = pc
                    mr = i

        if mr != -1:
            spawn(index, mr)
            dlog('Spawned unit at: (' + str(index) + ', ' + str(mr) + ')')
