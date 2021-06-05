import sys
import numpy as np
import matplotlib.pyplot as plt
import random
from Animate import generateAnimat


class QLearning:

	def __init__(self):
		self.width =  int(sys.argv[1])
		self.height = int(sys.argv[2])

		self.start_x = sys.argv[4]
		self.start_y = sys.argv[5]

		self.end_x = sys.argv[7]
		self.end_y = sys.argv[8]

		self.k = sys.argv[10]

		self.gamma = float(sys.argv[12])
		self.epochs = int(sys.argv[14])

		self.records = set()
		#self.start_state = (self.start_y, self.start_x)
		#self.end_state = (self.end_y, self.end_x)
		self.start_state = (0,0)
		self.end_state = (2,1)
		self.q_table = []
		self.rewards = {}
		self.actions = {}
		self.mines = []
		self.states = []
		self.opt_pol = []

	def initialize_states(self):
		self.opt_pol.append(self.start_state)
		for row in range(self.height):
			for col in range(self.width):
				self.states.append((col,row))
		#print(self.states)

	def set_rewards(self):
		for state in self.states:
			if state == self.end_state:
				self.rewards[state] = 100
			else:
				self.rewards[state] = -1

	def animate(self):
		anim, fig, ax = generateAnimat(self.records, self.start_state, self.end_state, mines=self.mines, opt_pol=self.opt_pol,
									   start_val=-10, end_val=100, mine_val=150, just_vals=False, generate_gif=False,
									   vmin=-10, vmax=150)
		plt.show()


	def generate_actions(self):
		self.actions = {
			"left":(-1,0),
			"down": (0,1),
			"right":(1,0),
			"up":(0,-1)
		}
	def initialize_q_table(self):
		for row in range(self.height):
			row_list = []
			for col in range(self.width):
				row_list.append(0)
			self.q_table.append(row_list)

	def is_valid_state(self,next_state):
		if next_state[0] < 0 or next_state[0] >= self.width or next_state[1] < 0 or next_state[1] >= self.height:
			return False
		return True

	def choose_action(self, current_state, epsilon = 0.2):
		using_random_action = np.random.choice([True,False], p=[epsilon, 1 - epsilon])
		print(using_random_action)

		if using_random_action:
			print("We are using a random action")
		else:
			print("We are using a greedy action")
			policy_candidates = {}
			for action in self.actions:
				next_state = (self.actions[action][0]+current_state[0],self.actions[action][1]+current_state[1])
				if is_valid_state(next_state):
					policy_candidates[next_state] = self.q_table[next_state[1]][next_state[0]]

			max_state = max(policy_candidates, key=policy_candidates.get)
			max_q_value = policy_candidates[current_action]
			list_of_max = []
			for candidate in policy_candidates:
				if policy_candidates[candidate] == max_q_value:
					list_of_max.append(candidate)

			random_index = random.randint(0, len(list_of_max) - 1)
			max_state = list_of_max[random_index]
			#Now we can use the max_state(state with the maximum q value to find the actioned perfomed to get there)
			action_dx = max_state[0] - current_state[1]
			action_dy = max_state[1] - current_state[1]

			for action in self.actions:
				if self.actions[action] == (action_dx,action_dy):
					print(action)
					return action


			q_value = self.get_q_value()
			adjasent_q_values.append(q_value)
			max_q = round(max(adjacent_values),2)

	def calculate_value(self, state, next_state):
		value = self.rewards[state] + (self.gamma * (self.values[next_state[1]][next_state[0]]) )
		#print(str(state) +" has a rvalue of" + str(self.values[state[1]][state[0]]))
		return value

	def find_optimal_policy(self):
		policy_set = set()
		policy_set.add(self.start_state)
		policy_candidates = {}
		current_state = self.start_state
		i = 0
		while True:
			for action in self.actions:
				next_state = (self.actions[action][0] + current_state[0],
							  self.actions[action][1] + current_state[1])
				if self.is_valid_state(next_state):
					policy_candidates[next_state] = self.values[next_state[1]][next_state[0]]
			#currently equals to the first key with maximum value
			current_state = max(policy_candidates,key=policy_candidates.get)
			max_value = policy_candidates[current_state]
			list_of_max = []
			for candidate in policy_candidates:
				if policy_candidates[candidate] == max_value:
					list_of_max.append(candidate)

			random_index = random.randint(0,len(list_of_max)-1)
			#round(random_index)
			current_state = list_of_max[random_index]

			policy_set.add(current_state)
			policy_candidates.clear()
			if current_state == self.end_state:
				break
			#i += 1
			#if i == 100:
			#	break
		for state in policy_set:
			if self.opt_pol.count(state) < 1:
				self.opt_pol.append(state)
		print(self.opt_pol)


	def q_learn(self):
		#temp_values = self.values.copy()
		for iterations in range(self.epochs):

			current_state = self.states[random.randint(0,len(self.states)-1)]
			print(current_state)
			self.choose_action(current_state)
			break
			while current_state != end_state:
				action = choose_action(current_state)
				print()
		print("This runs once")
		#self.find_optimal_policy()



	def start_q_learning(self):
		#print(self.width)
		self.initialize_q_table()
		self.initialize_states()
		self.set_rewards()
		print(self.q_table)
		self.generate_actions()
		self.q_learn()
		#self.animate()
		print("Youre going to work at google kiddo")

class driverClass:
	def main ():
		q = QLearning()
		q.start_q_learning()
	if __name__ == "__main__":
		main()
