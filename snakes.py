import curses
from curses import textpad
import random
import time

menu = ['Home', 'Play', 'Exit']
states = ['menu', 'playing', 'gameover']
score = 0
timeout_start = 100
n_food = 2

def make_food(snake, board):
    food = None
    while food is None:
        food = [
            random.randint(board[0][0]+1, board[1][0]-1), 
            random.randint(board[0][1]+1, board[1][1]-1)
            ]
        if food in snake:
            food = None
    return food

def print_menu(stdscr, selected_row):
    #stdscr.clear()
    h, w = stdscr.getmaxyx()
    for i, row in enumerate(menu):
            x = w // 2 - len(row) // 2
            y = h // 2 + - len(menu)//2 + i
            if i == selected_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
    #stdscr.refresh()

def print_board(stdscr, snake, fruit, state, msg, score):
    #stdscr.clear()
    #assert len(snake) > 0
    # draw snake
    if len(snake) > 0:
        head = snake[0]
        stdscr.addstr(head[0], head[1], '@')
        if len(snake) > 1:
            for y,x in snake[1:]:
                try:
                    stdscr.addstr(y, x, '*')
                except:
                    pass

    # draw fruit
    for y,x in fruit:
        stdscr.addstr(y, x, '&')
    
    # draw info
    stdscr.addstr(0,0, 'state: {}, msg: {}'.format(state, msg))
    _, w = stdscr.getmaxyx()
    score_str = 'score: {}'.format(score)
    stdscr.addstr(0,w-len(score_str)-1, score_str)
    #stdscr.refresh()

def update_snake(snake, direction, eating = False):
    try:
        head = [snake[0][0], snake[0][1]]
        #if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
        #    direction = key
        #else:
        #    return snake, None
        if direction == curses.KEY_LEFT:
            #head[1] =- 1
            head = [head[0], head[1]-1]
        elif direction == curses.KEY_RIGHT: 
            head[1] += 1
        elif direction == curses.KEY_UP: 
            head[0] -= 1
        elif direction == curses.KEY_DOWN: 
            head[0] += 1
        else:
            pass
        
        tail = snake if eating else snake[:-1]
        snake = [head] + tail

        return snake, None
    except Exception as e:
        return snake, str(e)

def game_over(snake, board):
    #return False, None
    if snake[0][0] in [board[0][0],board[1][0]]:
        return True, 'out of bounds!'
    if snake[0][1] in [board[0][1],board[1][1]]: 
        return True, 'out of bounds!'
    if snake[0] in snake[1:]: 
        return True, 'bit yourself!'
    return False, None

def found_food(snake, food):
    for i, (y,x) in enumerate(food):
        if [y,x] == snake[0]:
            return True, i
    return False, None

def step(stdscr, board, snake, food: list, direction):
    
    eating, food_index = found_food(snake, food)
    if eating:
        global score
        score += 1
        food.remove(food[food_index])
    
    snake, err = update_snake(snake, direction, eating)
    if err:
        return snake, states[2], err
    
    over, reason = game_over(snake, board)
    if over:
        return snake, states[2], str(reason)

    return snake, states[1], 'ok'

def print_game_over(stdscr, score):
    pass

def new_game(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    global timeout_start
    stdscr.timeout(timeout_start)
    h, w = stdscr.getmaxyx()
    snake = [[h//2,w//2-1], [h//2,w//2], [h//2,w//2+1]] # [y,x]
    direction = curses.KEY_LEFT
    key = direction
    state = states[1]
    food = []
    msg = 'select option'
    global score
    score = 0
    return snake, direction, key, state, food, msg

def main(stdscr):
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    pad = 5
    board = [[pad,pad], [h-pad, w-pad]]
    textpad.rectangle(stdscr, board[0][0], board[0][1], board[1][0], board[1][1])
    snake, direction, key, state, food, msg = [], None, None, None, [], '' #new_game(stdscr)
    state = states[0]

    while 1:

        if state in [states[1], states[2]]:
            print_board(stdscr, snake, food, state, msg, score)
        textpad.rectangle(stdscr, board[0][0], board[0][1], board[1][0], board[1][1])
        
        direction = key if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN] else direction
        
        if key in [77, 109]: # M or m
            snake, direction, key, state, food, msg = [], None, None, None, [], ''
            stdscr.clear()
            print_board(stdscr, snake, food, state, msg, score)
            stdscr.refresh()
            state = states[0]

        elif key in [81, 113]:
            if state == states[0]: # Q or q
                return
            elif state == states[1]:
                snake, direction, key, state, food, msg = new_game(stdscr)
                while len(food) < n_food:
                    food.append(make_food(snake, board))
        if state == states[0]:
            selected_row = menu_func(stdscr, board)
            state = states[selected_row]
            if selected_row == len(menu) - 1:
                return
            elif state == states[1]:
                snake, direction, key, state, food, msg = new_game(stdscr)
                while len(food) < n_food:
                    food.append(make_food(snake, board))
        elif state == states[1]:
            snake, state, msg = step(stdscr, board, snake, food, direction)
            while len(food) < n_food:
                food.append(make_food(snake, board))

        elif state == states[2]:
            if key in [81, 113]:
                snake, direction, key, state, food, msg = new_game(stdscr)
                while len(food) < n_food:
                    food.append(make_food(snake, board))
            if key in [77, 109]: # M or m
                state = states[0]
        else:
            pass

        stdscr.refresh()
        key = stdscr.getch()
        stdscr.clear()
        
def menu_func(stdscr, board):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    #curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_RED)
    selected_row = 0
    
    while 1:

        print_menu(stdscr, selected_row)
        textpad.rectangle(stdscr, board[0][0], board[0][1], board[1][0], board[1][1])

        key = stdscr.getch()
        #stdscr.clear()
        if key in [81, 113]: # Q or q
            return -1
        if key == curses.KEY_UP:
            selected_row -= 1
            if selected_row < 0:
                selected_row = len(menu) - 1
        elif key == curses.KEY_DOWN:
            selected_row += 1
            if selected_row >= len(menu):
                selected_row = 0
        elif key == curses.KEY_ENTER or key in [10,13]:
            return selected_row
        else:
            pass
        
        stdscr.refresh()
        
curses.wrapper(main)
