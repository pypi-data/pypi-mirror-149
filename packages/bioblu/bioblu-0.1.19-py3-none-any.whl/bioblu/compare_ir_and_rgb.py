#!/usr/bin/env python3

import os

import cv2
import matplotlib.pyplot as plt
import pandas as pd

import image_fusing

RGB_DIR = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/RGB images and video/"
IR_DIR = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/Thermal images and video/20211216_122012/"
PAIRS_TABLE = "/opt/local/data/rpfei01/image_pairs_for_fusing.csv"

RGB_IMG = "DJI_0572.JPG"
IR_IMG = "20211216_122846_R.jpg"

resize_factor = 6.9
padding = (300, 400, 300, 400)
rotation = -4.0
shift = (20, 100)
alpha = 0.5
beta = 0.7

rgb_fpath = os.path.join(RGB_DIR, RGB_IMG)
ir_fpath = os.path.join(IR_DIR, IR_IMG)

img_pairs = pd.read_csv(PAIRS_TABLE)
print(img_pairs.shape)
img_pairs = img_pairs[["rgb_fname", "ir_fname"]]
img_pairs.dropna(inplace=True)
print(img_pairs.shape)

for i, row in enumerate(img_pairs.iterrows()):
    rgb_fname = row[1]["rgb_fname"]
    ir_fname = row[1]["ir_fname"]
    rgb_fpath = os.path.join(RGB_DIR, rgb_fname)
    ir_fpath = os.path.join(IR_DIR, ir_fname)
    fused_img = image_fusing.fuse_images(rgb_fpath, ir_fpath,
                                         resize_factor_ir=resize_factor,
                                         padding_ltrb=padding,
                                         rotation_angle=rotation,
                                         shift_yx=shift,
                                         alpha=alpha, beta=beta,
                                         show_result=True)

# fused_img = image_fusing.fuse_images(rgb_fpath, ir_fpath,
#                                      resize_factor_ir=resize_factor,
#                                      padding_ltrb=padding,
#                                      rotation_angle=rotation,
#                                      shift_yx=shift,
#                                      alpha=alpha, beta=beta,
#                                      show_result=True)
#
# plt.imsave("/opt/users/rpfei01/Desktop/fused_image_61-24.tiff", cv2.cvtColor(fused_img, cv2.COLOR_BGR2RGB))