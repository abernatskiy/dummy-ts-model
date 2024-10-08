#!/usr/bin/env python3

inputLength = 900
outputLength = 25
mevThreshold = 5000

timeKey = 'block'
valueKey = 'price'

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
import pandas as pd
import numpy as np
import torch
import matplotlib.pyplot as plt
from network import NeuralNetwork
from timeSeriesDataset import toTensor

transport = RequestsHTTPTransport(url='https://void.squids.live/weth-usdt-squid:prod/api/graphql')
client = Client(transport=transport)
recentPricesResponse = client.execute(gql(f'''
query {{
	blockPrices(
		limit: {inputLength+outputLength},
		orderBy: {timeKey}_DESC
	) {{
		{timeKey}
		{valueKey}
	}}
}}
'''))

df = pd.DataFrame(recentPricesResponse['blockPrices']).iloc[::-1]

df.loc[df[valueKey]>mevThreshold, valueKey] = mevThreshold
df[valueKey] /= mevThreshold

df.index = pd.Index(df[timeKey])
df = df.reindex(pd.RangeIndex(df[timeKey].iloc[0], df[timeKey].iloc[-1]+1, 1), method='ffill')
df[timeKey] = df.index

inputs = toTensor(df.iloc[-outputLength-inputLength:-outputLength][valueKey].values).unsqueeze(0).unsqueeze(0)
outputs = toTensor(df.iloc[-outputLength:][valueKey].values).unsqueeze(0)

model = NeuralNetwork()
model.load_state_dict(torch.load('model.pth', weights_only=True))
model.eval() # optional for this model

with torch.no_grad():
	pred = model(inputs)

tin = df.iloc[-outputLength-inputLength:-outputLength][timeKey].values
npin = inputs.flatten(0, 2).detach().cpu().numpy()*mevThreshold

tout = df.iloc[-outputLength:][timeKey].values
npout = outputs.flatten().detach().cpu().numpy()*mevThreshold
nppred = pred.flatten().detach().cpu().numpy()*mevThreshold

fig, axs = plt.subplots(2, 1)
axs[0].plot(tin, npin, label='input', color='blue')
axs[0].plot(tout, npout, label='reality', color='green')
axs[0].plot(tout, nppred, label='predition', color='orange')
axs[0].set_xlabel('block')
axs[0].set_ylabel('ETH price')
axs[0].legend(loc='lower left')

axs[1].plot(tout, npout, label='reality', color='green')
axs[1].plot(tout, nppred, label='predition', color='orange')
axs[1].set_xlabel('block')
axs[1].set_ylabel('ETH price')
axs[1].legend(loc='lower left')
axs[1].set_xticklabels(tout, rotation=30)

fig.tight_layout()
plt.show()
