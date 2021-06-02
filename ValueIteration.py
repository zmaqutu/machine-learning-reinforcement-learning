import sys
import matplotlib.pyplot as plt
from Animate import generateAnimat


class ValueIteration: 

	def __init__(self):
		self.width =  int(sys.argv[1])
		self.height = int(sys.argv[2])

		self.start_x = sys.argv[4]
		self.start_y = sys.argv[5]

		self.end_x = sys.argv[7]
		self.end_y = sys.argv[8]

		self.k = sys.argv[10]

		self.gamma = sys.argv[12]

		self.records = [
		[
			[0, 0,  0 ],
			[0, 0, 100]
		],
		[
			[0,   0,  80],
			[0,  80, 100]
		],
		[
			[ 0, 64,  80],
			[64, 80, 100]
		],
		[
			[51.2, 64,  80],
			[  64, 80, 100]
		],
		[
			[51.2, 64,  80],
			[  64, 80, 100]
		]
	]
		#self.start_state = (self.start_y, self.start_x)
		#self.end_state = (self.end_y, self.end_x)
		self.start_state = (0,0)
		self.end_state = (2,1)
		self.mines = []
		self.states = []
		self.opt_pol = [(0,0), (1, 0), (2, 0), (2, 1)]


	def initialize_states(self):
		for row in range(self.height):
			for col in range(self.width):
				self.states.append((row,col))
		print(self.states)

	def animate(self):
		anim, fig, ax = generateAnimat(self.records, self.start_state, self.end_state, mines=self.mines, opt_pol=self.opt_pol,
									   start_val=-10, end_val=100, mine_val=150, just_vals=False, generate_gif=False,
									   vmin=-10, vmax=150)

	def start_value_iteration(self):
		print(self.width)
		self.initialize_states()
		self.animate()
		plt.show()
	print("Youre going to work at google kiddo")

class driverClass:
	def main():
		valueIt = ValueIteration()
		valueIt.start_value_iteration()
	if __name__ == "__main__":
		main()
