#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Name:      MCTS.py
Authors:        Nathan Wang + Celina Huang + Alex Vitale
Date:           4/2/22

Description:    Python file for running MCTS.
Source:         Adapted from https://ai-boson.github.io/mcts/
"""
import numpy as np
from collections import defaultdict
import chess
import time

class MCTS_Node():

    def __init__(self, state, reward_val, color, num_iter, max_iter, start_time, parent=None, parent_action=None):
        self.state = state
        self.baseboard_state = chess.BaseBoard(state.board_fen())
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self.num_visits = 0
        self.results = defaultdict(int)
        self.results[1] = 0
        self.results[0] = 0
        self.results[-1] = 0
        #self.untried_actions = None
        self.color = color
        self.untried_actions = self.get_untried_actions()
        self.reward_val = reward_val
        self.num_iter = num_iter
        self.max_iter = max_iter
        self.start_time = start_time
        return

    def get_untried_actions(self):
        """
        returns list of untried actions from a given state 
        """
        self.untried_actions = self.get_legal_actions()
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
        next_state = self.move(action)
        
        if self.color is chess.WHITE:
            next_color = chess.BLACK
        else:
            next_color = chess.WHITE
        
        child_node = MCTS_Node(next_state, 0, color = next_color, start_time = self.start_time, parent=self, parent_action=action, num_iter = self.num_iter+1, max_iter = self.max_iter)
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
            #possible_moves = current_rollout_state.get_legal_actions()
            possible_moves = self.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            #current_rollout_state = current_rollout_state.move(action)
            current_rollout_state = self.move(action)
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
        #print(possible_moves)
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
        #num_simulations = 100
        #for i in range(num_simulations):
        while True:
            v = self.tree_policy()
            reward = v.rollout()
            v.backprop(reward)
            if (time.perf_counter() - self.start_time) > 20:
                break
        return self.best_child(c_param=0)


    ## 
    def get_legal_actions(self):
        """
        construct list of all possible actions from current state
        returns a list
        """
        #print(self.color)
        all_moves = list(self.state.legal_moves)
        #print(all_moves)
        legal_moves = []
        for move in all_moves:
            square = chess.parse_square(move.uci()[0:2])
            #print(square)
            curr_color = self.baseboard_state.piece_at(square).color
            #print(curr_color)
            
            if curr_color is self.color:
                
                legal_moves.append(move)
                #print(legal_moves)

        
        
            
        return legal_moves
            
    
    def is_game_over(self):
        """
        checks if either of the kings have been taken
        returns True or False
        """
        
        if self.state.king(chess.WHITE) is None or self.state.king(chess.BLACK) is None:
            return True
        elif self.num_iter > self.max_iter:
            return True
        return False

    
    def game_result(self):
        """
        returns integer corresponding to game result
        return reward value?
        """
        
        # get all pieces currently on board
        fen = self.state.board_fen()
        
        num_w_P = fen.count('P')
        num_w_R = fen.count('R')
        num_w_N = fen.count('N')
        num_w_B = fen.count('B')
        num_w_Q = fen.count('Q')
        num_w_K = fen.count('K')
        
        num_b_p = fen.count('p')
        num_b_r = fen.count('r')
        num_b_n = fen.count('n')
        num_b_b = fen.count('b')
        num_b_q = fen.count('q')
        num_b_k = fen.count('k')
        
        points_w = num_w_P * 1 + num_w_R * 5 + num_w_N * 3 + num_w_B * 3 + num_w_Q * 8 + num_w_K * 20
        points_b = num_b_p * 1 + num_b_r * 5 + num_b_n * 3 + num_b_b * 3 + num_b_q * 8 + num_b_k * 20

        if self.color is chess.WHITE:
            reward = points_w - points_b
        else:
            reward = points_b - points_w
            
        return np.sign(reward)
        
        
        
        
        #return self.reward_val
    
    def move(self, action):
        """
        change state of board with new action taken
        returns new state
        """
        
        # update board with chosen move
        self.state.push(action)        
        
        return self.state
