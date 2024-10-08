An SQD-based naive ETH price predictor
======================================

This repo contains a very simple ANN model that aims to predict five minutes of ETH price history given the preceding three hours. It uses the data from [SQD](https://sqd.dev) for both training and testing.

Predictive performance is very poor, which is expected for this type of architecture.

## Inference

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
   or
   ```bash
   virtualenv --system-site-packages venv
   ```
   if you have PyTorch installed system-wide and don't want to grab another copy.

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the live inference script:
   ```bash
   ./plotPrediction.py
   ```

You should see a couple of plots that compares the model prediction for the last five minutes of data to the actual market data. The prediction is based on the data for the preceding three hours.

## Directory

- `weth-usdt-squid` contains the [squid](https://docs.sqd.dev/sdk/overview/) that was used to fetch the SQD Network data. It looks at the `Swap` events of the most popular ETH-USDT pool on Uniswap to get the price estimates. The data contains spikey noise due to the MEV activity.
- `timeSeriesDataset.py` is a simple utility module for handling per-block price time series in PyTorch.
- `network.py` defines the neural network structure.
- `training.ipynb` describes how the network was trained.
- `plotPrediction.py` fetches live data from the `weth-usdt-squid` deployed to [SQD Cloud](https://docs.sqd.dev/cloud/) and compares the model predictions for the last five minutes to what actually happened.
