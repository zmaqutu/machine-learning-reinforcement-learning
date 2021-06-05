import sys
import matplotlib.pyplot as plt
import numpy as np
import random
from Animate import generateAnimat


class ValueIteration: 

	def __init__(self):
		self.width =  int(sys.argv[1])
		self.height = int(sys.argv[2])

		self.start_x = sys.argv[4]
		self.start_y = sys.argv[5]

		self.end_x = sys.argv[7]
		self.end_y = sys.argv[8]

		self.k = int(sys.argv[10])

		self.gamma = float(sys.argv[12])

		self.records = []
		#self.start_state = (self.start_y, self.start_x)
		#self.end_state = (self.end_y, self.end_x)
		self.start_state = (0,0)
		self.end_state = (9,9)
		self.rewards = {}
		self.actions = {}
		self.values = []
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
			if state in self.mines:
				print("reward for goin here is zero")
				self.rewards[state] = -100
			if state != self.end_state and state not in self.mines:
				self.rewards[state] = 0

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
	def initialize_mines(self):
		for i in range(self.k):
			mine_state = self.states[np.random.choice(range(len(self.states)))]
			print(mine_state)
			if mine_state == self.end_state or mine_state == self.start_state:
				print("Couldn't generate mine due to state assignment clash")
				i-=1
				continue
			else:
				self.mines.append(mine_state)
		print("Mines")
		print(self.mines)

	def initialize_values(self):
		for row in range(self.height):
			row_list = []
			for col in range(self.width):
				if (col,row) == self.end_state:
					row_list.append(100)
				if (col,row) in self.mines:
					print("miiiiiiiiiiiiiinnnnnnnnnnnnneeeeeeeeee")
					row_list.append(-100)
				else:
					row_list.append(0)
			self.values.append(row_list)

	def initialize_records(self):
		record = [[0 for x in range(self.width)] for y in range(self.height)]
		for state in self.states:
			if state == self.end_state:
				record[state[1]][state[0]] = 100
			if state in self.mines:
				record[state[1]][state[0]] = -100
			if state != self.end_state and state not in self.mines:
				record[state[1]][state[0]] = 0
		print("THe THECord is ")
		print(record)
		self.records.append(record)

	def is_valid_state(self,next_state):
		if next_state[0] < 0 or next_state[0] >= self.width or next_state[1] < 0 or next_state[1] >= self.height:
			return False
		return True

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
				next_state = (self.actions[action][0] + current_state[0],self.actions[action][1] + current_state[1])
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
			if current_state == self.end_state or current_state in self.mines:
				break
			#i += 1
			#if i == 100:
			#	break
		for state in policy_set:
			if self.opt_pol.count(state) < 1:
				self.opt_pol.append(state)
		print(self.opt_pol)


	def get_record(self):
		record = [[0 for x in range(self.width)] for y in range(self.height)]
		for state in self.states:
			record[state[1]][state[0]] = self.values[state[1]][state[0]]
		return record
	def value_iteration(self):
		temp_values = self.values.copy()
		iterations = 0
		while True:
			for state in self.states:
				adjacent_values = []
				if state == self.end_state or state in self.mines:
					continue
				for action in self.actions:
					next_state = (self.actions[action][0]+state[0],self.actions[action][1]+state[1])
					if self.is_valid_state(next_state):
						#print(str(next_state) + " is a valid state")
						value = self.calculate_value(state,next_state)
						adjacent_values.append(value)
					# calculate value at that state
					else:
						#print(str(next_state) + " is not a state")
						continue
				temp_values[state[1]][state[0]] = round(max(adjacent_values),2)
			self.values = temp_values.copy()
			self.records.append(self.get_record())
			print(self.records)
			if iterations == 20:
				break
			iterations += 1

		print("This runs once")
		self.find_optimal_policy()



	def start_value_iteration(self):
		#print(self.width)
		self.initialize_states()
		self.generate_actions()
		self.initialize_mines()
		self.initialize_values()
		self.set_rewards()
		#print(self.rewards)
		#print(self.values)
		self.initialize_records()
		self.value_iteration()
		#print(self.records)
		self.animate()
		print("Youre going to work at google kiddo")

class driverClass:
	def main ():
		valueIt = ValueIteration()
		valueIt.start_value_iteration()
	if __name__ == "__main__":
		main()
