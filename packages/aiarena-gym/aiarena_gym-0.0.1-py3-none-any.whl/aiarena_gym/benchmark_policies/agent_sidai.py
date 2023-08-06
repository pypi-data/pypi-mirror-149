#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 15:15:15 2022

@author: brandinho, unholycucumber
"""

import numpy as np

actions_list = [
    "Run Left",
    "Run Right",
    "Single Punch",
    "Double Punch",
    "Defend",
    "Jump",
    "Jump Left",
    "Jump Right",
    "Jump Punch",
    "Low Kick"
]

action_to_idx_mapping = {}
for i in range(len(actions_list)):
    action_to_idx_mapping[actions_list[i]] = i


class RulesBasedAgentSidai():
  def __init__(self):
      self.type = "rules-based-agent"
      self.random_policy = False

  def select_action(self, state):
      
    (
        relative_distance,
        you_facing_opponent,
        opponent_facing_you,
        your_health,
        opponent_health,
        relative_strength,
        relative_speed,
        relative_defence,
        relative_accuracy
    ) = state[0]

    action = "Single Punch"
    right_side = np.sign(relative_distance) > 0
    abs_distance = abs(relative_distance)
    
    if abs_distance > 0.1:
        if right_side:
            action = "Run Left"
        else:
            action = "Run Right"

    return action_to_idx_mapping[action]
