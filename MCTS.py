#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 13:06:40 2022

@author: nathanwang
"""
import numpy as np
from collections import defaultdict

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
	
	#def main():
		#root = MCTS_Node(state = initial_state)
		#selected_node = root.best_action()
		#return
		