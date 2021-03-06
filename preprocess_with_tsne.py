#!/usr/bin/env python
"""
Preprocess high dimensional data into 2-dimensional data
for visualization using t-SNE. Saves to CSV file for input
into web visualizer.

Args:
    input_data: numpy file with dimensionality num_images x num_features
        where each row corresponds to an image in input_images_list
    input_images_list: text file with each line containing image file name
    input_images_dir: path to prepend to file names in input_images_list
"""

import argparse
import numpy as np
import random

from tsne import bh_sne

def save_to_csv(output_file, image_names, xs, ys):
    """Helper function to save data to CSV.

    Preconditions:
        length of image_names, xs and ys should be the same

    Args:
        output_file: path to output file
        image_names: list of image paths corresponding to coordinates
        xs: numpy array of x-coordinates
        ys: numpy array of y-coordinates
    """
    assert xs.shape[0] == ys.shape[0]
    assert len(image_names) == xs.shape[0]

    with open(output_file, 'w') as f:
        f.write("image_name,x,y\n") # header
        for name, x, y in zip(image_names, xs, ys):
            f.write("{0},{1},{2}\n".format(name, x, y))

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description='Preprocess data using t-SNE.')
    parser.add_argument('input_data', type=str, help='Path to numpy data file')
    parser.add_argument('input_images_list', type=str, help='Path to text file listing images')
    parser.add_argument('--input_images_dir', type=str, default='public/data/', help='Path to images folder')
    parser.add_argument('--output_file', type=str, default='public/data.csv', help='Path to output CSV file')
    parser.add_argument('--max_num_points', type=int, default=1000, help='Max number of points')
    args = parser.parse_args()

    # load data
    data_load = np.load(args.input_data)
    with open(args.input_images_list, 'r') as f:
        image_names_load = [l.strip() for l in f]

    # shuffle and reduce number of data points to run faster
    # this also results in cleaner visualization
    assert len(image_names_load) > 0
    assert data_load.shape[0] == len(image_names_load)
    indices = range(data_load.shape[0])
    random.shuffle(indices)

    data = np.zeros((args.max_num_points, data_load.shape[1]))
    image_names = []
    for i, rand_index in enumerate(indices):
	if i >= args.max_num_points:
            break
        data[i,:] = data_load[rand_index,:]
        image_names.append(image_names_load[rand_index])

    assert data.shape[0] == len(image_names), '{0} and {1}'.format(data.shape[0], len(image_names))

    # run dimensionality reduction with t-SNE
    data_tsne = bh_sne(data)
    xs = data_tsne[:, 0]
    ys = data_tsne[:, 1]

    # save to csv file
    save_to_csv(args.output_file, image_names, xs, ys)

main()
