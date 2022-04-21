#!/usr/bin/env python3

"""
File Name:      nwang309_chuang371_avitale6.py
Authors:        Nathan Wang + Celina Huang + Alex Vitale
Date:           4/2/22

Description:    Python file for my agent.
Source:         Adapted from recon-chess (https://pypi.org/project/reconchess/)
"""

import random
import chess
from player import Player
#from collections import defaultdict
import numpy as np
#from MCTS import *
import MCTS
import time

#MCTS_Node = MCTS.MCTS_Node()


# TODO: Rename this class to what you would like your bot to be named during the game.
class TheRookies(Player):

    def __init__(self):
        
        self.game_board = None #chess.BaseBoard()
        
        self.board = None
        self.color = None
        self.captured = None
        
        self.game_reward = 0
        
        self.root = None
        self.curr = None
        
        self.num_moves = 0
        
        self.opponent_castled = False
        
        
        # Holds array of [piece location, whether it's moved]
        self.opponent_king_loc = None
        self.opponent_knights = None
        self.opponent_bishops = None
        self.opponent_queens = None
        self.opponent_rooks = None
        self.opponent_pawns = None
        
        self.chess_dict = None
        
        self.piece_reward = {
            "q" : 8,
            "n" : 3,
            "r" : 5,
            "p" : 1,
            "b" : 3
        }
        
        #self.keys = ["k", "q", "n", "r", "p", "b"]
        
        self.pawns = None
        pass
        
    def handle_game_start(self, color, board):
        """
        This function is called at the start of the game.

        :param color: chess.BLACK or chess.WHITE -- your color assignment for the game
        :param board: chess.Board -- initial board state
        :return:
        """
        # TODO: implement this method
        
        '''
        if (color == chess.WHITE):
            return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        else:
            return "RNBKQBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbkqbnr"
        '''
        self.game_board = chess.BaseBoard()
        #self.game_board = chess.Board()
        
        self.board = board
        self.color = color
        
        # Create root node for MCTS
        '''
        self.root = MCTS(board, 0)
        self.curr = self.root
        '''
        
        # Set king location
        if self.color == chess.WHITE:
            self.opponent_king_loc = [[chess.E8, False]]
            self.opponent_pawns = [[chess.square(x, 6), False] for x in range(8)]
            self.opponent_queens = [[chess.D8, False]]
            self.opponent_bishops = [[chess.C8, False], [chess.F8, False]]
            self.opponent_rooks = [[chess.A8, False], [chess.H8, False]]
            self.opponent_knights = [[chess.B8, False], [chess.G8, False]]
            
            self.pawns = [chess.square(x, 1) for x in range(8)]
            '''
            self.king = [chess.E1]
            self.queens = [chess.D1]
            self.bishops = [chess.C1, chess.F1]
            self.opponent_rooks = [[chess.A1, False], [chess.H1, False]]
            self.opponent_knights = [[chess.B1, False], [chess.G1, False]]
            '''
            
            
        else:
            self.opponent_king_loc = [[chess.E1, False]]
            self.opponent_pawns = [[chess.square(x, 1), False] for x in range(8)]
            self.opponent_queens = [[chess.D1, False]]
            self.opponent_bishops = [[chess.C1, False], [chess.F1, False]]
            self.opponent_rooks = [[chess.A1, False], [chess.H1, False]]
            self.opponent_knights = [[chess.B1, False], [chess.G1, False]]
            
            
            self.pawns = [chess.square(x, 6) for x in range(8)]
        
        self.chess_dict = {
            "k" : self.opponent_king_loc,
            "q" : self.opponent_queens,
            "n" : self.opponent_knights,
            "r" : self.opponent_rooks,
            "p" : self.opponent_pawns,
            "b" : self.opponent_bishops
        }
        
        pass
    
    def find_piece(self, location):
        
    
        for key in self.chess_dict:
            if self.chess_dict[key] is not None:
                
                for piece in self.chess_dict[key]:
                    
                    # if not limbo mode and locations match
                    if not piece[1] and piece[0] == location:
                        # found it
                        return (key, piece)
        
        return (None, None)
        
        
    def handle_opponent_move_result(self, captured_piece, captured_square):
        """
        This function is called at the start of your turn and gives you the chance to update your board.

        :param captured_piece: bool - true if your opponents captured your piece with their last move
        :param captured_square: chess.Square - position where your piece was captured
        """
        piece = None
        
        if captured_piece:
            self.board.remove_piece_at(captured_square)
            
            piece = self.game_board.piece_at(captured_square).symbol().lower()
                
            
            self.game_board.remove_piece_at(captured_square)
            
            if captured_piece in self.pawns:
                self.pawns.remove(captured_piece)
                
            
        
        self.captured = captured_square
        
        if piece is not None:
            return self.piece_reward[piece]
        return None
        
        #pass

    def choose_sense(self, possible_sense, possible_moves, seconds_left):
        """
        This function is called to choose a square to perform a sense on.

        :param possible_sense: List(chess.SQUARES) -- list of squares to sense around
        :param possible_moves: List(chess.Moves) -- list of acceptable moves based on current board
        :param seconds_left: float -- seconds left in the game

        :return: chess.SQUARE -- the center of 3x3 section of the board you want to sense
        :example: choice = chess.A1
        """
        # TODO: update this method
        
        
        # IMPLEMENT Q LEARNING? reward = points from pieces sensed
        
        
        print(chess.square_name(self.chess_dict['k'][0][0]))
        # Sense around last captured piece
        if self.captured is not None:
        
            #location = chess.parse_square(chess.square_name(self.captured))
            file = chess.square_file(self.captured)
            rank = chess.square_rank(self.captured)
            
            
            # Fully utilize all 9 squares for sense
            if file == 0:
                file = 1
            elif file == 7:
                file = 6
                
            if rank == 0:
                rank = 1
            elif rank == 7:
                rank = 6
                
            return chess.square(file, rank)
        
        
        
        # If no castling occured, keep eye on king
        if not self.opponent_castled:
            
            file = chess.square_file(self.chess_dict['k'][0][0])
            rank = chess.square_rank(self.chess_dict['k'][0][0])
            
            # Fully utilize all 9 squares for sense
            if file == 0:
                file = 1
            elif file == 7:
                file = 6
                
            if rank == 0:
                rank = 1
            elif rank == 7:
                rank = 6
            
            
            
            return chess.square(file, rank)
        
        # If castled, keep track of 
        else:
            
            # Check king location every other time
            if self.num_moves % 2 == 0 or len(self.pawns) == 0:
                
                file = chess.square_file(self.chess_dict['k'][0][0])
                rank = chess.square_rank(self.chess_dict['k'][0][0])
                
                # Fully utilize all 9 squares for sense
                if file == 0:
                    file = 1
                elif file == 7:
                    file = 6
                    
                if rank == 0:
                    rank = 1
                elif rank == 7:
                    rank = 6
                
                return chess.square(file, rank)
                
            else:
                
                distances = [chess.square_distance(self.chess_dict['k'][0][0], x) for x in self.pawns]
                
                closest_pawn = self.pawns[np.argmin(distances)]
                
                direction = 2
                if self.color == chess.BLACK:
                    direction = -2
                
                file = chess.square_file(closest_pawn)
                
                if file == 0:
                    file = 1
                elif file == 7:
                    file = 6
                    
                rank = chess.square_rank(closest_pawn)
                
                if self.color == chess.WHITE and rank == 6:
                    
                    return chess.square(file, rank)
                
                elif self.color == chess.BLACK and rank == 1:
                    
                    return chess.square(file, rank)
                
                else:
                    
                    rank = rank + direction
                    
                    if rank == 0:
                        rank = 1
                    elif rank == 7:
                        rank = 6
                        
                    return chess.square(file, rank)
                
                
                
                #return 
            
        
        #move = self.choose_move(possible_moves, seconds_left)
        
        #if move is not None and self.board.piece_at(move) is not None:
        #    return move.to_square
        
        #for location, piece in self.board.piece_map().items():
        #    if piece.color == self.color:
        #        possible_sense.remove(location)
    
        #return random.choice(possible_sense)
        
    def handle_sense_result(self, sense_result):
        """
        This is a function called after your picked your 3x3 square to sense and gives you the chance to update your
        board.

        :param sense_result: A list of tuples, where each tuple contains a :class:`Square` in the sense, and if there
                             was a piece on the square, then the corresponding :class:`chess.Piece`, otherwise `None`.
        :example:
        [
            (A8, Piece(ROOK, BLACK)), (B8, Piece(KNIGHT, BLACK)), (C8, Piece(BISHOP, BLACK)),
            (A7, Piece(PAWN, BLACK)), (B7, Piece(PAWN, BLACK)), (C7, Piece(PAWN, BLACK)),
            (A6, None), (B6, None), (C8, None)
        ]
        """
        # iterate over every square in sense_result
        for location, piece in sense_result:
            #print(type(piece))
            #print("current piece in sense:")
            #print(piece)
            
            self.board.set_piece_at(location, piece)
            self.game_board.set_piece_at(location, piece)
            
            # result[0] is piece type (key), result[1] is a specific piece
            result = self.find_piece(location)

            # we think there's a piece there
            # result[0] is the key ('p', 'q', etc.)
            # result[1] is the piece, result[1][0] is the location, result[1][1] is the limbo mode toggle
            if result[0] is not None and (piece is None or result[0] != piece.symbol()):
                result[1][1] = True
                # update board by removing piece at square where nothing was sensed
                if piece is None:
                    self.game_board.remove_piece_at(location)
                
                
            # if there's a piece there, and it is not our piece 
            if piece is not None and piece.color != self.color:
                
                piece_symbol = piece.symbol().lower()
                
                # if the piece matches what we think is there, then okay
                if result[0] is not None and piece_symbol == result[0]:
                    
                    continue
                # if piece doesn't match what is there
                else:
                    
                    # look through dictionary to check all pieces of that type, and add the ones that are in limbo to list
                    limbo = []
                    #print(type(piece_type))
                    for chess_piece in self.chess_dict[piece_symbol]:
                    
                        if chess_piece[1] == True:
                            
                            limbo.append(chess_piece)
                    
                    # if nothing is in limbo, add all of them
                    if len(limbo) == 0:
                        
                        limbo = self.chess_dict[piece_symbol]
                    
                    print(limbo)
                    # find closest piece out of possible options
                    distance = [chess.square_distance(location, x[0]) for x in limbo]
                    
                    self.game_board.remove_piece_at(limbo[np.argmin(distance)][0])
                    
                    limbo[np.argmin(distance)] = [location, False]
                    # add guess piece back into board
                    self.game_board.set_piece_at(location, piece)
                    
                    
        
        
        # If unique piece was sensed and does not match previous board sense, update (King, Queen)
        
        
        # TODO: implement this method
        # Hint: until this method is implemented, any senses you make will be lost.
        pass

    def choose_move(self, possible_moves, seconds_left):
        """
        Choose a move to enact from a list of possible moves.

        :param possible_moves: List(chess.Moves) -- list of acceptable moves based only on pieces
        :param seconds_left: float -- seconds left to make a move
        
        :return: chess.Move -- object that includes the square you're moving from to the square you're moving to
        :example: choice = chess.Move(chess.F2, chess.F4)
        
        :condition: If you intend to move a pawn for promotion other than Queen, please specify the promotion parameter
        :example: choice = chess.Move(chess.G7, chess.G8, promotion=chess.KNIGHT) *default is Queen
        """
        # TODO: update this method
        #choice = random.choice(possible_moves)
        
        # Win condition
        '''
        if self.board.king(not self.color):
            
            valid_wins = self.board.attackers(self.color, self.board.king(not self.color))
            if valid_wins:
                
                return chess.Move(valid_wins.pop(), self.board.king(not self.color))
        '''
        
    
        
        # Run MCTS while time still available
        # Selection, Expansion, Simulation, Backprop
        # Need to make tree of data
        curr_fen = self.game_board.board_fen()
        #print(curr_fen)
        initial_state = chess.Board(curr_fen)
        start_time = time.perf_counter()
        
        #MCTS_Node = MCTS.MCTS_Node()
        print()
        print("about to do MCTS. current game_board:")
        print(self.game_board)
        
        
        root = MCTS.MCTS_Node(state = initial_state, reward_val = 0, color = self.color, width_iter = 0, depth_iter = 0, start_time = start_time)
        #print("initialized root")
        # return an action
        test_time = time.perf_counter()
        selected_move = root.best_action().parent_action
        print(time.perf_counter()-test_time)
        #print("have selected the best action")
        #print(selected_move)
        
        
        
        #if seconds_left == 0:
             # Choose node of same height with best updated reward   
        #choice = random.choice(possible_moves)
        choice = selected_move
        # Either Promote to Queen or Knight
            
        return choice
        
    def handle_move_result(self, requested_move, taken_move, reason, captured_piece, captured_square):
        """
        This is a function called at the end of your turn/after your move was made and gives you the chance to update
        your board.

        :param requested_move: chess.Move -- the move you intended to make
        :param taken_move: chess.Move -- the move that was actually made
        :param reason: String -- description of the result from trying to make requested_move
        :param captured_piece: bool - true if you captured your opponents piece
        :param captured_square: chess.Square - position where you captured the piece
        """
        # TODO: implement this method
        
        if taken_move is not None:
            self.board.push(taken_move)
            
            old_square = chess.parse_square(taken_move.uci()[0:2])
            new_square = chess.parse_square(taken_move.uci()[2:4])
            
            if (len(taken_move.uci()) == 4):
                self.game_board.set_piece_at(new_square, self.game_board.piece_at(old_square))
                
            else:
                self.game_board.set_piece_at(new_square, self.game_board.piece_at(old_square))
                self.game_board.set_piece_at(new_square, chess.QUEEN, True)
                
            self.game_board.set_piece_at(old_square, None)
                
            
            
        self.num_moves = self.num_moves + 1
            
        pass
        
    def handle_game_end(self, winner_color, win_reason):  # possible GameHistory object...
        """
        This function is called at the end of the game to declare a winner.

        :param winner_color: Chess.BLACK/chess.WHITE -- the winning color
        :param win_reason: String -- the reason for the game ending
        """
        # TODO: implement this method
        if winner_color == chess.BLACK:
            print("Black wins due to " + win_reason)
            
        else:
            print("White wins due to " + win_reason)
            
            
        # Use for learning (-1 for loss and 1 for win) and update here
        # DO NOT RETURN!
        
        pass
    
    
    
	

		
	
	
