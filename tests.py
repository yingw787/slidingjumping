from sliding_and_jumping import SlidingJumping
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

        game = SlidingJumping()
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