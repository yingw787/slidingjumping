

class SlidingJumping():

    def __init__(self, board = None, backward_allowed = False):
        if board == None:
            self.board = 'ttt_hhh'
        else:
            self.board = board
        self.start_state = self.board
        self.backward_allowed = backward_allowed
        self.move_types = ['jump', 'slide']
        self.move_directions = ['left', 'right']
        self.move_history = []

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
        return self.start_state == self.board[::-1]

if __name__ == '__main__':
    game = SlidingJumping('tt_hh')
    res = game.gen_moves()
    print(res)