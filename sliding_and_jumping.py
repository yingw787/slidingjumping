from pprint import pprint

enum_states = ['PLAYING', 'DEAD END', 'VICTORY']

class SlidingJumping():

    def __init__(self, board, start_board = None, backward_allowed = False, move_history = None):
        self.board = board
        self.start_board = board if start_board == None else start_board
        self.backward_allowed = backward_allowed
        self.move_types = ['jump', 'slide']
        self.move_directions = ['left', 'right']
        self.move_history = [] if move_history == None else move_history

    def display(self):
        print(self.board)

    def is_valid_move(self, i, move_type, move_direction):
        if self.board[i] == None:
                return False
        if not self.backward_allowed:
            if self.board[i] == 't' and move_direction == 'left':
                return False
            if self.board[i] == 'h' and move_direction == 'right':
                return False
        if move_type == 'slide':
            if move_direction == 'left':
                if i == 0:
                    return False
                elif self.board[i-1] != '_':
                    return False
                else:
                    return True
            elif move_direction == 'right':
                if i == len(self.board)-1:
                    return False
                elif self.board[i+1] != '_':
                    return False
                else:
                    return True
        elif move_type == 'jump':
            if move_direction == 'left':
                if i <= 1:
                    return False
                elif self.board[i-1] == self.board[i]:
                    return False
                elif self.board[i-1] == '_':
                    return False
                elif i-2 < 0:
                    return False
                elif self.board[i-2] != '_':
                    return False
                else:
                    return True
            elif move_direction == 'right':
                if i >= len(self.board)-1:
                    return False
                elif self.board[i+1] == self.board[i]:
                    return False
                elif self.board[i+1] == '_':
                    return False
                elif i+2 >= len(self.board):
                    return False
                elif self.board[i+2] != '_':
                    return False
                else:
                    return True
        else:
            return False

    def gen_moves(self):
        moves = []
        for i in range(len(self.board)):
            for mt in self.move_types:
                for md in self.move_directions:
                    if self.is_valid_move(i, mt, md):
                        moves.append((i, self.board[i], mt, md))
        return moves

    def make_move(self, i, move_type, move_direction):
        self.move_history.append((i, move_type, move_direction))
        temp = list(self.board)
        if move_type == 'slide':
            if move_direction == 'left':
                temp[i-1], temp[i] = temp[i], temp[i-1]
            elif move_direction == 'right':
                temp[i+1], temp[i] = temp[i], temp[i+1]
            else:
                pass
        elif move_type == 'jump':
            if move_direction == 'left':
                temp[i-2], temp[i] = temp[i], temp[i-2]
            elif move_direction == 'right':
                temp[i+2], temp[i] = temp[i], temp[i+2]
            else:
                pass
        else:
            pass
        self.board = ''.join(temp)

    def game_over(self):
        return self.start_board == self.board[::-1]

def gen_state_tree(start_board = 't_h', verbose = False):
    if verbose:
        print('starting board:  {}'.format(start_board))
        print('finishing board: {}'.format(start_board[::-1]))
    tree = dict()
    unvisited_states = [start_board]
    while len(unvisited_states) > 0:
        board = unvisited_states.pop(0)
        if board not in tree:
            tree[board] = set()
        game = SlidingJumping(board=board[:], start_board=start_board[:])
        moves = game.gen_moves()
        if moves == []:
            tree[board] = enum_states[1]
            continue
        for m in moves:
            game = SlidingJumping(board=board[:], start_board=start_board[:])
            game.make_move(m[0], m[2], m[3])
            new_board = game.board[:]
            tree[board].add(new_board)
            if game.game_over():
                tree[new_board] = enum_states[2]
                continue

            if new_board not in tree:
                unvisited_states.append(new_board)
            else:
                tree[board].add(new_board)
    if verbose:
        pprint(tree)
    return tree

def traverse_state_tree(tree, state, history):
    if type(tree[state]) != set:
        yield history + [tree[state]]
    else:
        for next_state in tree[state]:
            for h in traverse_state_tree(tree, next_state, history + [next_state]):
                yield h

def play_all_possible_games(start_board = 'ttt_hhh'):
    finished_games = []
    games = []
    game = SlidingJumping(start_board[:], start_board[:])
    games.append(game)
    while len(games) > 0:
        g = games.pop(0)
        moves = g.gen_moves()
        for m in moves:
            new_g = SlidingJumping(board=g.board[:], start_board = start_board[:],
                move_history=g.move_history[:])
            new_g.make_move(m[0], m[2], m[3])
            if new_g.game_over():
                print('\ngame over in {} moves'.format(len(new_g.move_history)))
                print('game start state: {}'.format(new_g.start_board))
                print('game end state: {}'.format(new_g.board))
                print('move history:')
                print(new_g.move_history)
                #aggregate_move_history(new_g)
                finished_games.append(new_g)
            else:
                games.append(new_g)

def make_traversals(start_state = 't_h'):
    print('\nmaking traversals for {}'.format(start_state))
    tree = gen_state_tree(start_state, False)
    print('tree:')
    pprint(tree)
    print()
    ts = list(traverse_state_tree(tree, start_state, [start_state]))
    print('num valid games: {}'.format(len(ts)))
    print('valid games:')
    for t in ts:
        print('{} ({} in {} moves)'.format(t, 'won' if t[-1] == enum_states[2] else 'lost', len(t)))

def aggregate_move_history(game):
    res = dict()
    for move in game.move_history:
        key = move[1] + move[2]
        if key not in res:
            res[key] = 0
        res[key] += 1
    print('aggregated move history:')
    pprint(res)

if __name__ == '__main__':
    #game = SlidingJumping('tt_hh')
    #res = game.gen_moves()
    #print(res)
    start_state = 't_h'
    play_all_possible_games(start_state)
    make_traversals(start_state)
