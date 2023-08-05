"""
Utility module for plotting and printing information
"""

import matplotlib.pyplot as plt
import pandas as pd
import art
import random
import numpy as np
import csv
import matplotlib.patches as mpatches
from pathlib import Path

def export_csv(data, filename = "./data_out.csv"):
    """
    Exports prediction data as a CSV file.

    :arg data: A colection of predictions from the ml unit, with prediction
    types as keys.
    :arg filename: The name of the file to save to within data/
    """
    try:
        with open(Path(filename), "w", newline='') as csv_file:
            tmp = csv.writer(csv_file, delimiter=" ",
                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            tmp.writerow(data.keys())
            tmp.writerows(data.values())
            print(f'Saved output as {filename}')
    except Exception as e:
        print(f'Could not write output file: {e}')

def print_motd():
    """
    Prints the motd with asci art.

    :return: None
    """
    print(art.text2art("Welcome to Crypto Util", "cybermedum"))

def plot_and_save_price_graph(data, filename, file_extension, crypto):
	"""
	Saves the historical price data as an image file in `figures/`

	:arg data: Time ordered list of prices to plot (assumed to be in USD based on the API sources)
	:arg filename: Filename under which to save the data in the directory `figures/`
	:arg file_extension: file extension to save the image as. Either png, jpg, or pdf
	:arg crypto: The name of cryptocurrency being plotted. Typically the symbol of the cryptocurrency (e.g. BTC)
	:return: None
	"""
	data = list(data)
	assert file_extension in ["pdf", "png", "jpg"], "Supported file extensions are pdf, png and jpg"
	assert isinstance(filename, Path)
	assert type(file_extension) is str
	assert type(data) is list
	assert type(crypto) is str
	plt.plot([a for a in range(len(data))], data, "-b.", label=crypto)
	fig = plt.gcf()
	fig.set_size_inches(12, 8)
	plt.title("Historical price data of "+crypto)
	plt.ylabel("USD price")
	plt.xlabel("Time index")
	plt.legend()
	plt.savefig(Path(f'./{filename}.{file_extension}'))
	plt.close()
	print("Figure of historical price data has been written to" + str(filename)+ "."+file_extension)
	return None

def plot_and_save_price_graph_with_predictions(data, filename, file_extension, crypto, predictions):
	"""
	Saves the prediction price data as an image file. 50 days of historical data is also plotted to show in the near term where the prediction trends are going. 
	If there are multiple ML model predictions, all of the model predictions are plotted. Image is saved to `figures/`

	:arg data: Time ordered list of prices to plot (assumed to be in USD based on the API sources)
	:arg filename: Filename under which to save the data in the directory `figures/`
	:arg file_extension: file extension to save the image as. Either png, jpg, or pdf
	:arg crypto: The name of cryptocurrency being plotted. Typically the symbol of the cryptocurrency (e.g. BTC)
	:arg predictions: Dictionary where the keys are ML model names (e.g. random_forest) and the values are lists of time ordered price predictions
	:return: None
	"""
	assert file_extension in ["pdf", "png", "jpg"], "Supported file extensions are pdf, png and jpg"
	assert isinstance(filename, Path)
	assert type(file_extension) is str
	assert (type(data) is list) or (type(data) is np.ndarray)
	assert type(crypto) is str
	assert type(predictions) is dict
	truncate_data = 50
	data = data[-truncate_data:]
	fig, ax = plt.subplots()
	k = list(predictions.keys())[0]
	ax.axvspan(len(data), len(data)+len(predictions[k]), alpha=0.1, color='green')
	plt.plot([a for a in range(len(data))], data, "-b.", label=crypto)
	fig = plt.gcf()
	fig.set_size_inches(12, 8)
	plt.ylabel("USD price")
	plt.xlabel("Time index")
	plt.title(crypto+" predicted USD price over the next "+str(len(predictions[k]))+" days")
	for k in predictions:
		plt.plot([i+len(data) for i in range(len(predictions[k]))], predictions[k], color=(random.randint(1, 255)/255.0, random.randint(1, 255)/255.0, random.randint(1, 255)/255.0), marker=random.choice(["^", "o", "*", "P"]), label=k)
	red_patch = mpatches.Patch(color='green', label='Future prediction region', alpha=0.1)
	h, l = ax.get_legend_handles_labels()
	plt.legend(handles=[red_patch]+h)
	plt.savefig(f'./{filename}_prediction.{file_extension}')
	plt.close()
	print("Figure of (truncated) price data for the last 50 days with predictions has been written to "+f'./{filename}_prediction.{file_extension}')
	return None

def print_summary_statistics_of_predicted_prices(predictions_for_different_models):
	"""
	Prints summary statistics for the predicted daily prices across the ensemble of ML models

	:arg predictions_for_different_models: A dictionary where keys are ML model names and values are the predicted prices over time
	:return: None
	"""
	print("\n=== Model Ensemble Statistics ===")
	N = len(predictions_for_different_models[list(predictions_for_different_models.keys())[0]])
	for i in range(N):
		vector = []
		for k in predictions_for_different_models:
			vector.append(predictions_for_different_models[k][i])
		print("Day "+str(i+1)+" mean predicted price across all ML models is "+str(round(np.mean(vector), 4))+" USD with a standard deviation of "+str(round(np.std(vector), 4)))
	print("=================\n")
	return None
