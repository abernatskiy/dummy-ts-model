from torch import nn

class NeuralNetwork(nn.Module):
	def __init__(self):
		super().__init__()
		self.linear_relu_stack = nn.Sequential(
			nn.Conv1d(1, 5, 100, stride=10),
			nn.Flatten(),
			nn.ReLU(),
			nn.Linear(405, 200),
			nn.ReLU(),
			nn.Linear(200, 25)
		)

	def forward(self, x):
		prediction = self.linear_relu_stack(x)
		return prediction
