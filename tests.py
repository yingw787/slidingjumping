from sliding_and_jumping import SlidingJumping
from sliding_and_jumping import gen_state_tree, \
    play_all_possible_games, enum_states, traverse_state_tree
import unittest

class TestAPIRouteUnitTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_gen_valid_moves(self):

        game = SlidingJumping('t_h')
        res = game.gen_moves()
        self.assertEqual(res, [(0, 't', 'slide', 'right'), (2, 'h', 'slide', 'left')])

        game = SlidingJumping('_th')
        res = game.gen_moves()
        self.assertEqual(res, [(2, 'h', 'jump', 'left')])

        game = SlidingJumping('th_')
        res = game.gen_moves()
        self.assertEqual(res, [(0, 't', 'jump', 'right')])

        game = SlidingJumping('th')
        res = game.gen_moves()
        self.assertEqual(res, [])

        game = SlidingJumping('ht')
        res = game.gen_moves()
        self.assertEqual(res, [])

        game = SlidingJumping('ttt_hh')
        res = game.gen_moves()
        self.assertEqual(res, [(2, 't', 'slide', 'right'), (4, 'h', 'slide', 'left')])

        game = SlidingJumping('tt_thhh')
        res = game.gen_moves()
        self.assertEqual(res, [(1, 't', 'slide', 'right'), (4, 'h', 'jump', 'left')])

    def test_move_history(self):
        game = SlidingJumping('t_h')
        game.make_move(0, 'slide', 'right')
        self.assertEqual(game.move_history, [(0, 'slide', 'right')])

        game = SlidingJumping('t_h')
        game.make_move(2, 'slide', 'left')
        self.assertEqual(game.move_history, [(2, 'slide', 'left')])
        game.make_move(0, 'jump', 'right')
        self.assertEqual(game.move_history, [(2, 'slide', 'left'), (0, 'jump', 'right')])

    def test_make_move(self):
        game = SlidingJumping('t_h')
        game.make_move(0, 'slide', 'right')
        self.assertEqual(game.move_history, [(0, 'slide', 'right')])
        self.assertEqual(game.board, '_th')

        game = SlidingJumping('th_')
        game.make_move(0, 'jump', 'right')
        self.assertEqual(game.move_history, [(0, 'jump', 'right')])
        self.assertEqual(game.board, '_ht')

        game = SlidingJumping('t_h')
        game.make_move(2, 'slide', 'left')
        self.assertEqual(game.move_history, [(2, 'slide', 'left')])
        self.assertEqual(game.board, 'th_')
        
        game = SlidingJumping('_th')
        game.make_move(2, 'jump', 'left')
        self.assertEqual(game.move_history, [(2, 'jump', 'left')])
        self.assertEqual(game.board, 'ht_')

    def test_game_over(self):

        game = SlidingJumping('t_h')
        game.board = 'h_t'
        self.assertEqual(game.game_over(), True)

        game = SlidingJumping('tt_hh')
        game.board = 'hh_tt'
        self.assertEqual(game.game_over(), True)

        game = SlidingJumping('t_h')
        self.assertEqual(game.game_over(), False)

        game = SlidingJumping('t_h')
        game.board = 'ht_'
        self.assertEqual(game.game_over(), False)
        game.board = '_th'
        self.assertEqual(game.game_over(), False)

        game = SlidingJumping('tt_hh')
        game.board = 'hhtt_'
        self.assertEqual(game.game_over(), False)

        game = SlidingJumping('tt_hh')
        game.board = 'hh_tt'
        self.assertEqual(game.game_over(), True)

    def test_gen_state_tree(self):
        tree = gen_state_tree('t_h')
        self.assertIn('t_h', tree)
        self.assertIn('_th', tree)
        self.assertIn('th_', tree)
        self.assertIn('h_t', tree)
        self.assertEqual(tree['h_t'], enum_states[2])
        self.assertIn('_th', tree['t_h'])
        self.assertIn('th_', tree['t_h'])
        self.assertEqual(len(tree), 6)

        tree = gen_state_tree('tt_h', False)
        self.assertIn('h_tt', tree)
        self.assertIn('h_tt', tree['_htt'])
        self.assertEqual(len(tree), 11)
        self.assertNotIn(set(), tree.values())
        self.assertEqual(tree['_tth'], enum_states[1])
        
        tree = gen_state_tree('ttt_hhh')
        self.assertIn('hhh_ttt', tree)
        self.assertEqual(tree['hhh_ttt'], enum_states[2])

    def test_traverse_state_tree(self):
        tree = gen_state_tree('t_h', False)
        ts = list(traverse_state_tree(tree, 't_h', ['t_h']))
        self.assertIsInstance(ts, list)
        self.assertEqual(len(ts), 2)
        self.assertIn(['t_h', '_th', 'ht_', 'h_t', 'VICTORY'], ts)
        self.assertIn(['t_h', 'th_', '_ht', 'h_t', 'VICTORY'], ts)

if __name__ == '__main__':
    unittest.main()
    