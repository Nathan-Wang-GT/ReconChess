#!/usr/bin/env python3

"""
File Name:      nwang309_chuang371.py
Authors:        Nathan Wang + Celina Huang
Date:           4/2/22

Description:    Python file for my agent.
Source:         Adapted from recon-chess (https://pypi.org/project/reconchess/)
"""

import random
import chess
from player import Player
from collections import defaultdict
import numpy as np


# TODO: Rename this class to what you would like your bot to be named during the game.
class TheRookies(Player):

    def __init__(self):
        self.board = None
        self.color = None
        self.captured = None
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
        self.board = board
        self.color = color
        
        pass
        
    def handle_opponent_move_result(self, captured_piece, captured_square):
        """
        This function is called at the start of your turn and gives you the chance to update your board.

        :param captured_piece: bool - true if your opponents captured your piece with their last move
        :param captured_square: chess.Square - position where your piece was captured
        """
        
        if captured_piece:
            self.board.remove_piece_at(captured_square)
        
        self.captured = captured_square
        
        pass

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
        
        if self.captured:
            return self.captured
        
        
        # CHOOSE A SENSE OUT OF ALL POSSIBLE ACTIONS
        
        move = self.choose_move(possible_moves, seconds_left)
        
        if move is not None and self.board.piece_at(move) is not None:
            return move.to_square
        
        for location, piece in self.board.piece_map().items():
            if piece.color == self.color:
                possible_sense.remove(location)
    
        return random.choice(possible_sense)
        
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
        
        for location, piece in sense_result:
            
            self.board.set_piece_at(location, piece)
            
        
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
        if self.board.king(not self.color):
            
            valid_wins = self.board.attackers(self.color, self.board.king(not self.color))
            if valid_wins:
                
                return chess.Move(valid_wins.pop(), self.board.king(not self.color))
        
        
        # Run MCTS while time still available
        # Selection, Expansion, Simulation, Backprop
        # Need to make tree of data
        
        
        #if seconds_left == 0:
             # Choose node of same height with best updated reward   
        choice = random.choice(possible_moves)
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
    
    
    
	
class MCTS_Node():
	
	def __init__(self, state, parent=None, parent_action=None):
		self.state = state
		self.parent = parent
		self.parent_action = parent_action
		self.children = []
		self.num_visits = 0
		self.results = defaultdict(int)
		self.results[1] = 0
		self.results[-1] = 0
		self.untried_actions = None
		self.untried_actions = self.get_untried_actions()
		return
	
	def get_untried_actions(self):
		"""
		returns list of untried actions from a given state 
		"""
		self.untried_actions = self.state.get_legal_actions()
		return self.untried_actions
	
	def q(self):
		"""
		returns difference of wins - losses
		"""
		wins = self.results[1]
		losses = self.results[-1]
		return wins-losses
	
	def n(self):
		"""
		return number of visits
	   """
		return self.num_visits
	
	def expand(self):
		"""
		next state depends on which action is chosen
		append all possible child nodes (correspond to generated states) to children array,
		return child_node
		"""
		action = self.untried_actions.pop()
		next_state = self.state.move(action)
		child_node = MCTS_Node(next_state, parent=self, parent_action=action)
		self.children.append(child_node)
		return child_node
	
	def is_terminal_node(self):
		"""
		check if current node is terminal or not (terminal node indicates game is over)
		"""
		return self.state.is_game_over()
	
	def rollout(self):
		"""
		from current state, entire game is simulated until end
		win -> 1, loss -> -1, draw -> 0
		"""
		current_rollout_state = self.state
		while not current_rollout_state.is_game_over():
			possible_moves = current_rollout_state.get_legal_actions()
			action = self.rollout_policy(possible_moves)
			current_rollout_state = current_rollout_state.move(action)
		return current_rollout_state.game_result()
	
	def backprop(self, result):
		"""
		update statistics for all nodes
		until parent node is reached, for each node, num_visits += 1
		if result is 1 (win), increment win by 1
		otherwise if result is loss, increment loss by 1
		"""
		self.num_visits += 1
		self.results[result] += 1
		if self.parent:
			self.parent.backprop(result)
			
	def is_fully_expanded(self):
		"""
		all actions are popped out of get_untried_actions() one by one
		when it is empty (size is 0), it is fully expanded
		"""
		return len(self.untried_actions) == 0
	
	def best_child(self, c_param=0.1):
		"""
		once fully expanded, select best child out of children array
		weighs exploitation (c.q()) and exploration (c.n())
		"""
		choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
		return self.children[np.argmax(choices_weights)]
	
	def rollout_policy(self, possible_moves):
		"""
		randomly selects a move out of possible moves, AKA random playout
		"""
		return possible_moves[np.random.randint(len(possible_moves))]
	
	def tree_policy(self):
		"""
		select node to run rollout
		"""
		current_node = self
		while not current_node.is_terminal_node():
			if not current_node.is_fully_expanded():
				return current_node.expand()
			else:
				current_node = current_node.best_child()
		return current_node
	
	def best_action(self):
		"""
		returns node corresponding to best possible move
		carries out expansion, simulation, and backpropagation
		"""
		num_simulations = 100
		for i in range(num_simulations):
			v = self.tree_policy()
			reward = v.rollout()
			v.backprop(reward)
		return self.best_child(c_param=0)
		
	
	'''
	NEED TO IMPLEMENT:
		get_legal_actions(self)
		is_game_over(self)
		game_result(self)
		move(self, action)
	'''
	
	def main():
		root = MCTS_Node(state = initial_state)
		selected_node = root.best_action()
		return
		
		
	
	
