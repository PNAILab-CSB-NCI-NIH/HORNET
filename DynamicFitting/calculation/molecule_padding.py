import pandas as pd
import math
import sys

# how to run this file: 
# python3 molecule_padding.py n abc.txt def.txt ghi.txt
# n = amount of padding around the image
# you can enter any # of .txt files (needs to be at least 1)

cols = ['x','y','z']
file_names = sys.argv[2:]

if len(file_names) > 0:
    for file_name in file_names:
        with open(file_name) as molecule_file:
            first_row = next(molecule_file).split()
        has_header = '.' not in str(first_row[0])
        skip_rows = 1 if has_header else 0
        coordinates = pd.read_csv(
            file_name,
            sep=r'\s+',
            header=None,
            names=cols,
            skiprows=skip_rows,
            float_precision='round_trip'
        )

        # find max x/y values
        x_max = coordinates['x'].max()
        y_max = coordinates['y'].max()

        # get z value for padding rows
        z = coordinates['z'].min()

        # find pixel size
        unique_values_x = coordinates['x'].unique()
        pixel_size = (unique_values_x.max() - unique_values_x.min()) / (len(unique_values_x) - 1)

        # find number of pixels to pad
        # padding_size added to beginning, padding_size added to end
        padding_size = int(
            math.ceil(
                ((max(x_max, y_max) - min(x_max, y_max)) / pixel_size) / 2
            )
        )

        # get shortest dimension
        short_dimension = 'x' if x_max < y_max else 'y'

        # get unique y values
        unique_values_y = coordinates['y'].unique()

        # pad to end first
        # if x is the shorter dimension, add rows for every unique y value where x = xmax + pixel size * n
        # where n goes from 1 to padding size + 1
        # if y is the shorter dimension, add rows for every unique x value where y = ymax + pixel size * n
        # where n goes from 1 to padding size + 1
        end_rows_to_add = []
        if short_dimension == 'x':
            for yvalue in unique_values_y:
                for pad_counter in range(1, padding_size):
                    end_rows_to_add.append([x_max + (pixel_size * pad_counter), yvalue, z])
        else:
            for xvalue in unique_values_x:
                for pad_counter in range(1, padding_size):
                    end_rows_to_add.append([xvalue, y_max + (pixel_size * pad_counter), z])
        # now concatenate rows_to_add onto existing coordinates dataframe
        end_padding = pd.DataFrame(end_rows_to_add, columns=cols)
        coordinates = coordinates.append(end_padding, ignore_index=True)        

        # shift all coordinates in shortest dimension by padding size * pixel size
        coordinates[short_dimension] += (padding_size * pixel_size)

        # now add padding at the beginning (process similar to adding padding to end)
        # assume origin is (5.0, 5.0)
        beginning_rows_to_add = []
        if short_dimension == 'x':
            for yvalue in unique_values_y:
                # use 0 to padding_size instead of 1 to padding_size + 1 because need to start at 5.0 exactly
                for pad_counter in range(0, padding_size):
                    beginning_rows_to_add.append([5.0 + (pixel_size * pad_counter), yvalue, z])
        else:
            for xvalue in unique_values_x:
                for pad_counter in range(0, padding_size):
                    beginning_rows_to_add.append([xvalue, 5.0 + (pixel_size * pad_counter), z])
        beginning_padding = pd.DataFrame(beginning_rows_to_add, columns=cols)
        coordinates = beginning_padding.append(coordinates, ignore_index=True)

        # expanding on all sides for visual purposes, will use x WLOG since x and y should be the same
        # 0 for no change
        # 1 for single extra margin etc.
        margin_size = int(sys.argv[1]) * (
            math.ceil(
                (coordinates['x'].max() - coordinates['x'].min()) / (pixel_size * 2)
            )
        )

        # expand x axis first
        # right pad
        right_margin_rows = []
        for yvalue in coordinates['y'].unique():
            for pad_counter in range(1, margin_size):
                right_margin_rows.append([coordinates['x'].max() + (pixel_size * pad_counter), yvalue, z])
        right_margin = pd.DataFrame(right_margin_rows, columns=cols)
        coordinates = coordinates.append(right_margin, ignore_index=True)

        coordinates['x'] += (margin_size * pixel_size)

        # left pad
        left_margin_rows = []
        for yvalue in coordinates['y'].unique():
            for pad_counter in range(0, margin_size):
                left_margin_rows.append([5.0 + (pixel_size * pad_counter), yvalue, z])
        left_margin = pd.DataFrame(left_margin_rows, columns=cols)
        coordinates = coordinates.append(left_margin, ignore_index=True)

        # top pad
        top_margin_rows = []
        for xvalue in coordinates['x'].unique():
            for pad_counter in range(1, margin_size):
                top_margin_rows.append([xvalue, coordinates['y'].max() + (pixel_size * pad_counter), z])
        top_margin = pd.DataFrame(top_margin_rows, columns=cols)
        coordinates = coordinates.append(top_margin, ignore_index=True)

        coordinates['y'] += (margin_size * pixel_size)

        # bottom pad
        bottom_margin_rows = []
        for xvalue in coordinates['x'].unique():
            for pad_counter in range(0, margin_size):
                bottom_margin_rows.append([xvalue, 5.0 + (pixel_size * pad_counter), z])
        bottom_margin = pd.DataFrame(bottom_margin_rows, columns=cols)
        coordinates = coordinates.append(bottom_margin, ignore_index=True)

        coordinates['x'] = round(coordinates['x'], 1)
        coordinates['y'] = round(coordinates['y'], 1)

        # sort columns for easier debugging
        coordinates.sort_values(by=['y','x'], inplace=True)

        # write data to txt file
        padded_file_name = "padded_" + file_name
        coordinates.to_csv(padded_file_name, header=None, index=None, sep=' ')
else:
    print("ERROR: You need to provide at least one filename!")