import pandas as pd
from torch.utils.data import Dataset
from torch import tensor
import torch

def toTensor(seq):
	return tensor(seq).type(torch.FloatTensor)

class TimeSeriesDataset(Dataset):
	'''One-dimensional time series data set with gap filling and normalization. Assumes integer time.'''
	def __init__(self, dataFrame, timeKey, valueKey, inputLength, outputLength, mevThreshold=5000):
		super(TimeSeriesDataset).__init__()

		dfcopy = dataFrame.copy()
		# this definitely should be done in the main code explicitly, refactor
		dfcopy.loc[dfcopy[valueKey]>mevThreshold, valueKey] = mevThreshold
		dfcopy[valueKey] /= mevThreshold
		dfcopy.index = pd.Index(dfcopy[timeKey])
		self.data = dfcopy.reindex(pd.RangeIndex(dfcopy[timeKey].iloc[0], dfcopy[timeKey].iloc[-1]+1, 1), method='ffill')
		# the result is a gapless dataframe indexed with time integers in sequence (with step of 1)
		# gaps are forward filled

		self.valueKey = valueKey
		self.inputLength = inputLength
		self.outputLength = outputLength
		self.sampleLength = inputLength + outputLength

	def __len__(self):
		return len(self.data) - self.sampleLength + 1

	def __getitem__(self, i):
		if i >= len(self):
			raise IndexError(f'Index {i} is out of bounds (dataset length {len(self)}')
		startIdx = self.data.index[i]
		input = self.data.loc[startIdx:startIdx+self.inputLength-1][self.valueKey].values
		output = self.data.loc[startIdx+self.inputLength:startIdx+self.sampleLength-1][self.valueKey].values
		return toTensor(input).unsqueeze(0), toTensor(output)
