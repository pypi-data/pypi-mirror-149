#!/usr/bin/env python3

import logging
import cv2
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
from PIL import Image
from typing import Tuple


def value_from_rgb(rgb_tuple):
    pass


def create_reference_scale_255(scale, steps=10000) -> Tuple[pd.DataFrame, np.array]:
    """

    :param scale:
    :param steps:
    :return: reftable, scale_array
    """
    _cmap = cm.get_cmap(scale)
    intensities = np.array(range(steps)) / (steps - 1)
    values_list = [np.uint8(np.array(_cmap(val)) * 255) for val in intensities]
    values_array = np.array(values_list)
    # Drop alpha
    values_array = values_array[:, 0:-1]
    # Remove duplicates (use pandas to keep order intact):
    pandas_array = pd.DataFrame(values_array).drop_duplicates()
    logging.info(pandas_array.head())
    values_array = np.array(pandas_array)
    logging.info(f"Scale array shape: {values_array.shape}")
    color_values = [tuple(row) for row in values_array]

    scale_out = values_array.reshape([-1, 1, 3])
    logging.info(f"Scale array final shape: {scale_out.shape}")
    final_intensities = np.array(range(len(color_values))) / (len(color_values) - 1)
    reference_table = pd.DataFrame({"color": color_values,
                                    "intensity": final_intensities})
    return reference_table, scale_out


def create_reference_scale_0_1(scale, steps=10000) -> Tuple[pd.DataFrame, np.array]:
    """

    :param scale:
    :param steps:
    :return: reftable, scale_array
    """
    _cmap = cm.get_cmap(scale)
    intensities = np.array(range(steps)) / (steps - 1)
    values_list = [_cmap(val) for val in intensities]
    values_array = np.array(values_list)
    # Drop alpha
    values_array = values_array[:, 0:-1]
    # Remove duplicates (use pandas to keep order intact):
    pandas_array = pd.DataFrame(values_array).drop_duplicates()
    logging.info(pandas_array.head())
    values_array = np.array(pandas_array)
    logging.info(f"Scale array shape: {values_array.shape}")
    color_values = [tuple(row) for row in values_array]
    scale_out = values_array.reshape([-1, 1, 3])
    logging.info(f"Scale array final shape: {scale_out.shape}")
    final_intensities = np.array(range(len(color_values))) / (len(color_values) - 1)
    reference_table = pd.DataFrame({"color": color_values,
                                    "intensity": final_intensities})
    return reference_table, scale_out


def unfold_img(fpath, rgb_output=True):
    """
    Unfolds an rgb image into a list of tuples with pixel values.
    By default, the return format is in BGR, unless to_rgb is set to True.
    :param rgb_output:
    :param fpath:
    :return:
    """
    img = cv2.imread(fpath)
    if rgb_output:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixel_values = []
    for col in img:
        for px in col:
            pixel_values.append(list(px))
    pixel_values = np.array(pixel_values)
    return pixel_values


def fold_img(unfolded_matrix, width, height):
    pass


def extract_unique_pixels(px_list):
    return list(set(px_list))


def create_intensity_table(scale_array):
    assert scale_array.ndim == 2
    tuple_array = [tuple(row) for row in scale_array]
    intensity_table = pd.DataFrame({"reference": tuple_array})
    intensities = np.array(range(len(intensity_table))) / (len(intensity_table) - 1)
    intensity_table["intensity"] = intensities
    return intensity_table


def infer_relative_intensities(fpath_img, reference_table, show_imgs=False):
    print(reference_table.columns)
    img_array = np.array(cv2.cvtColor(cv2.imread(fpath_img), cv2.COLOR_BGR2RGB))
    # img_array = np.array(Image.open(fpath_img))
    img_dims = img_array.shape

    print(img_dims)
    for row in img_array:
        for px in row:
            lookup_tuple = tuple(px)
            print(lookup_tuple)
            result = reference_table.loc[reference_table["color"] == lookup_tuple, :]
            if lookup_tuple in reference_table["color"]:
                print("Binggg!")
            if not result.empty:
                print(f"Intensity found: {result.values[0]}")
    print(img_array.shape)


def color_map_to_csv(map_name, target_path="/opt/users/rpfei01/Desktop/"):
    reftable, scalearray = create_reference_scale_255(map_name)
    reftable.to_csv(target_path + map_name + ".csv")



def extract_color_map(img_fpath):
    pass


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s]\t%(message)s")
    logging.disable()

    fpath_img = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/Thermal images and video/20211216_122012/20211216_122230_R.jpg"
    fpath_img = "/opt/users/rpfei01/Desktop/20211216_122230_R_plasma.jpg"
    fpath_img = "/opt/users/rpfei01/Desktop/plasma.jpg"
    reftable, scale_array = create_reference_scale_255("plasma")

    # infer_relative_intensities(fpath_img, reftable)

    ref01, scale01 = create_reference_scale_0_1("plasma")
    print(ref01.head())