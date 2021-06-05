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

		self.k = int(sys.argv[10])

		self.gamma = float(sys.argv[12])
		self.epochs = int(sys.argv[14])
		self.learning_rate = 0.2

		self.records = []
		#self.start_state = (self.start_y, self.start_x)
		#self.end_state = (self.end_y, self.end_x)
		self.start_state = (0,0)
		self.end_state = (9,9)
		self.q_table = []
		self.rewards = {}
		self.actions = {}
		self.visits = {}
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
				self.rewards[state] = -100
			if state != self.end_state and state not in self.mines:
				self.rewards[state] = 0

	def initialize_visits(self):
		for state in self.states:
			self.visits[state] = 0

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

	def choose_action(self, current_state, e_greedy = 0.8):
		taking_random_action = np.random.choice([True,False], p=[e_greedy, 1 - e_greedy])
		actions = ["left","down","right","up"]

		if taking_random_action:
			print("We are using a random valid action")
			while True:
				random_index = random.randint(0,len(actions) - 1)
				selected_action = actions[random_index]
				action_change = self.actions[selected_action]
				if self.is_valid_state((action_change[0] + current_state[0],action_change[1] + current_state[1])):
					#print("Start position is " + str(current_state))
					#print(selected_action)
					return selected_action
		else:
			print("We are using a greedy action")
			policy_candidates = {}
			for action in self.actions:
				next_state = (self.actions[action][0]+current_state[0],self.actions[action][1]+current_state[1])
				if self.is_valid_state(next_state):
					policy_candidates[next_state] = self.q_table[next_state[1]][next_state[0]]

			max_state = max(policy_candidates, key=policy_candidates.get)
			max_q_value = policy_candidates[max_state]
			list_of_max = []
			for candidate in policy_candidates:
				if policy_candidates[candidate] == max_q_value:
					list_of_max.append(candidate)

			random_index = random.randint(0, len(list_of_max) - 1)
			max_state = list_of_max[random_index]
			#Now we can use the max_state(state with the maximum q value to find the actioned perfomed to get there)
			action_dx = max_state[0] - current_state[0]
			action_dy = max_state[1] - current_state[1]

			#print(str((action_dx,action_dy)) )
			for action in self.actions:
				if self.actions[action] == (action_dx,action_dy):
					#print(action)
					return action


			q_value = self.get_q_value()
			adjasent_q_values.append(q_value)
			max_q = round(max(adjacent_values),2)

	def calculate_value(self, state, next_state):
		value = self.rewards[state] + (self.gamma * (self.values[next_state[1]][next_state[0]]) )
		#print(str(state) +" has a rvalue of" + str(self.values[state[1]][state[0]]))
		return value

	def find_optimal_policy(self):
		current_state = self.start_state
		policy_set = set()
		policy_set.add(self.start_state)
		while current_state != self.end_state:
			max_action = self.choose_action(current_state,e_greedy=0.2)
			action_dx = self.actions[max_action][0]
			action_dy = self.actions[max_action][1]
			next_state = (action_dx + current_state[0],action_dy + current_state[1])
			policy_set.add(next_state)
			current_state = next_state

		for state in policy_set:
			self.opt_pol.append(state)
		print(self.opt_pol)

	def get_record(self):
		record = [[0 for x in range(self.width)] for y in range(self.height)]
		for state in self.states:
			record[state[1]][state[0]] = self.q_table[state[1]][state[0]]
		return record


	def q_learn(self):
		#temp_values = self.values.copy()
		for iterations in range(self.epochs):

			current_state = self.states[random.randint(0,len(self.states)-1)]
			while current_state != self.end_state:
				action = self.choose_action(current_state)
				action_dx = self.actions[action][0]
				action_dy = self.actions[action][1]
				next_state = (action_dx + current_state[0], action_dy + current_state[1])
				#print("Current State" + str(current_state))
				#print("action performed: " + str(action))
				#print("Next State: " + str(next_state))
				current_q_value = self.q_table[current_state[1]][current_state[0]]
				maximum_action = self.choose_action(current_state,e_greedy=0)
				action_dx = self.actions[maximum_action][0]
				action_dy = self.actions[maximum_action][1]
				max_state = (action_dx + current_state[0], action_dy + current_state[1])
				max_q_value = self.q_table[max_state[1]][max_state[0]]
				#TODO add a decaying learning rate
				temporal_difference = (self.rewards[next_state] + (self.gamma * ( max_q_value - current_q_value)))
				self.learning_rate = 1 / (1 + self.visits[current_state])
				q_value = current_q_value + (self.learning_rate * temporal_difference)
				self.q_table[current_state[1]][current_state[0]] = round(q_value,2)
				print(self.q_table)
				self.visits[current_state]+=1
				current_state = next_state
			self.records.append(self.get_record())

		self.find_optimal_policy()
		print(self.records)



	def start_q_learning(self):
		#print(self.width)
		self.initialize_q_table()
		self.initialize_states()
		self.initialize_mines()
		self.set_rewards()
		print(self.q_table)
		self.initialize_visits()
		self.generate_actions()
		self.q_learn()
		self.animate()
		print("Youre going to work at google kiddo")

class driverClass:
	def main ():
		q = QLearning()
		q.start_q_learning()
	if __name__ == "__main__":
		main()
