#!/usr/bin/env python3

import cv2
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
from typing import Tuple


def compare_rgb_gray_ir(fpath_thermal):
    img_ir = cv2.imread(fpath_thermal)
    img_ir_rgb = cv2.cvtColor(img_ir, cv2.COLOR_BGR2RGB)
    img_ir_gray = cv2.cvtColor(img_ir, cv2.COLOR_BGR2GRAY)
    fig_1, (ax1, ax2) = plt.subplots(ncols=2)
    ax1.imshow(img_ir_rgb)
    ax2.imshow(img_ir_gray, cmap="gray")
    plt.show()


def cut_to_shape(src, target_yxc_dims):
    """
    Adds buffers if necessary
    :param src:
    :param target_yxc_dims:
    :return:
    """
    logging.debug(f"cut_to_shape(<source: {src.shape}>, {target_yxc_dims}")
    src_height, src_width, src_channels = src.shape
    out_height, out_width, out_channels = target_yxc_dims
    out_img = np.zeros([out_height, out_width, src_channels])

    sx = int(0.5 * (out_width - src_width))
    sy = int(0.5 * (out_height - src_height))

    width_from_sx = 2 * sx + src_width
    height_from_sy = 2 * sy + src_height
    width_error = width_from_sx - out_width
    height_error = height_from_sy - out_height

    logging.debug(f"Width error: {width_error}")
    logging.debug(f"Height error: {height_error}")
    logging.debug(f"target_yxc_dims: {target_yxc_dims}")
    logging.debug(f"source height: {src_height} | source width: {src_width} | source channels: {src_channels}")
    logging.debug(f"out height: {out_height} | out width: {out_width} | out channels: {out_channels}")
    logging.debug(f"source dims: {src.shape}")
    logging.debug(f"out img. dims: {out_img.shape}")
    logging.debug(f"sx {sx} | sy: {sy}")
    if src_width < out_width:
        logging.info("Padding x")
    elif src_width == out_width:
        logging.info("Leaving x unchanged (identical x dimension).")
    elif src_width > out_width:
        logging.info("Cutting x.")
    if src_height < out_height:
        logging.info("Padding y.")
    elif src_height == out_height:
        logging.info("Leaving y unchanged (identical y dimension).")
    elif src_height > out_height:
        logging.info("Cutting y.")
    logging.debug(f"SRC size before potential cutting {src.shape}")

    if sx >= 0:
        x0, x1 = sx, sx + src_width
        logging.debug(f"x0: {x0} | x1: {x1}")
    if sy >= 0:
        y0, y1 = sy, sy + src_height
        logging.debug(f"y0: {y0} | y1: {y1}")
    if sx < 0:
        logging.debug(f"Cutting source width. Indices (0|1): ({abs(sx)}|{-abs(sx)})")
        src = src[:, abs(sx):sx - width_error, :]
        x0 = 0  # NOTE: This marks where the merging window is located in the target array
        x1 = out_width  # As shape is not zero indexing this is ok w/o a +1
    if sy < 0:
        logging.debug(f"Cutting source height. Indices (0|1): ({abs(sy)}|{-abs(sy)})")
        src = src[abs(sy):sy - height_error, :, :]
        y0 = 0   # NOTE: This marks where the merging window is located in the target array
        y1 = out_height  # As shape is not zero indexing this is ok w/o a +1

    logging.debug(f"x0: {x0} | x1: {x1} | x diff.: {x1 - x0}")
    logging.debug(f"y0: {y0} | y1: {y1} | y diff.: {y1 - y0}")
    logging.debug(f"SRC size after cutting {src.shape}")
    logging.debug(f"Merging window size: {out_img[y0:y1, x0:x1, :].shape}")

    out_img[y0:y1, x0:x1, :] = src
    return out_img.astype(np.uint8)


def fuse_images(fpath_rgb: str, fpath_thermal: str, resize_factor_ir: float, padding_ltrb: tuple = (0, 0, 0, 0),
                rotation_angle: float = 0, shift_yx: Tuple[int, int] = None,
                alpha: float = 0.8, beta: float = 1.0, gamma: float = 0.0,
                show_result=False):
    img_rgb = cv2.imread(fpath_rgb)
    if img_rgb.shape[-1] == 3:
        img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2BGRA)
    logging.debug(f"RGB shape: {img_rgb.shape}")
    img_thermal = cv2.imread(fpath_thermal)
    logging.debug(f"Thermal shape: {img_thermal.shape}")
    y, x, c = img_thermal.shape
    x_new, y_new = int(x * resize_factor_ir), int(y * resize_factor_ir)

    # Processing the thermal image
    img_thermal = cv2.resize(img_thermal, (x_new, y_new))
    img_thermal = pad_image_manually(img_thermal, padding_ltrb)
    img_thermal = rotate_img_cropping(img_thermal, rotation_angle)
    img_thermal = shift_img(img_thermal, shift_yx)
    logging.debug(f"Thermal shape: {img_thermal.shape}")
    img_thermal = cut_to_shape(img_thermal, img_rgb.shape)

    # Overlaying RGB and thermal
    if img_thermal.shape[-1] == 3:
        img_thermal = cv2.cvtColor(img_thermal, cv2.COLOR_BGR2BGRA)
    logging.debug(f"Thermal shape: {img_thermal.shape} | RGB shape: {img_rgb.shape}")
    assert img_thermal.shape == img_rgb.shape
    img_fused = cv2.addWeighted(img_rgb, alpha, img_thermal, beta, gamma)

    ir_fname = os.path.split(fpath_thermal)[-1]
    rgb_fname = os.path.split(fpath_rgb)[-1]
    window_name = "OVERLAY: " + rgb_fname + ", " + ir_fname

    if show_result:
        cv2.namedWindow(window_name, cv2.WINDOW_GUI_EXPANDED)
        # cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, 1)
        cv2.resizeWindow(window_name, 1440, 900)
        cv2.imshow(window_name, img_fused)
        cv2.waitKey()
        cv2.destroyWindow(window_name)

    return img_fused


def pad_image(src_bgra: np.array, target_yxc_dim, shift_yx: Tuple[int, int] = (0, 0)):
    # ToDo: Add handling of the case when output is smaller than input (i.e. cropping)
    """
    Expects src to be a bgra
    :param src_bgra:
    :param target_yxc_dim:
    :param shift_yx:
    :return:
    """
    target_y_dim, target_x_dim, target_channels = target_yxc_dim
    y_shift, x_shift = shift_yx
    if src_bgra.shape[-1] == 3:
        src_bgra = cv2.cvtColor(src_bgra, cv2.COLOR_BGR2BGRA)
    source_y_size, source_x_size, *_ = src_bgra.shape
    logging.debug(f"Source: width: {source_x_size} | height: {source_y_size}")
    assert source_x_size <= target_x_dim
    assert source_y_size <= target_y_dim
    # Calculate symmetric buffer sizes
    sx = np.round(0.5 * (target_x_dim - source_x_size))
    sy = np.round(0.5 * (target_y_dim - source_y_size))
    # Assert that the shift is not bigger than the available space, given the target dimensions
    assert abs(x_shift) <= sx
    assert abs(y_shift) <= sy
    new_array = np.zeros([target_y_dim, target_x_dim, 4])
    logging.debug(f"New array shape: {new_array.shape}")
    y_start = np.uint16(sy + y_shift)      # Negative y shift will narrow the top buffer
    y_stop = np.uint16(sy + source_y_size + y_shift)
    x_start = np.uint16(sx + x_shift)      # Negative x shift will narrow the left buffer
    x_stop = np.uint16(sx + source_x_size + x_shift)
    logging.debug(f"\nxstart\t{x_start}\nxstop\t{x_stop}\nystart\t{y_start}\nystop\t{y_stop}")
    new_array[y_start:y_stop, x_start:x_stop, :] = src_bgra
    return new_array.astype(np.uint8)


def pad_image_manually(src, padding_left_top_right_bottom: tuple):
    left, top, right, bottom = padding_left_top_right_bottom
    src_dims = src.shape
    target_dimensions = (src_dims[0] + top + bottom,
                         src_dims[1] + left + right,
                         src_dims[2])
    img_out = np.zeros(target_dimensions)
    img_out[top:top + src_dims[0], left: left + src_dims[1], :] = src
    return img_out.astype(np.uint8)


def resize_img(src, factor=None, target_yxc_dims=None):
    """
    target_yxc_dims overrides factor!
    :param src:
    :param factor:
    :param target_yxc_dims:
    :return:
    """
    logging.info(f"Source img. proportions: {src.shape[1] / src.shape[0]}")
    src_y, src_x, _ = src.shape
    if factor is not None:
        target_x, target_y = np.uint32(src_x * factor), np.uint32(src_y * factor)
        logging.debug(f"Source: width: {src_x} | height: {src_y}")
        logging.debug(f"Target: width: {target_x} | height: {target_y}")
    elif target_yxc_dims is not None:
        target_y, target_x, _ = target_yxc_dims
    else:
        raise ValueError("Provide at least factor or target dimensions")
    img_resized = cv2.resize(src, (target_x, target_y))
    logging.info(f"Target img. proportions: {img_resized.shape[1] / img_resized.shape[0]}")
    return img_resized


def rotate_img_cropping(src, angle_deg):
    image_center = tuple(np.array(src.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, - angle_deg, 1.0)
    result = cv2.warpAffine(src, rot_mat, src.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def shift_img(src, shift_yx):
    """
    Shifts image within itself. Note that areas moved out of the image will be cut off.
    :param src:
    :param shift_yx:
    :return:
    """
    y_shift, x_shift = shift_yx
    logging.debug(f"x shift {x_shift}")
    logging.debug(f"y shift {y_shift}")
    logging.debug(f"Source shape: {src.shape}")
    img_out = np.zeros(src.shape)
    logging.debug(f"Target shape: {img_out.shape}")

    src_height, src_width, src_channels = src.shape
    logging.debug(f"Source height: {src_height}")
    logging.debug(f"Source width: {src_width}")

    if not abs(x_shift) < src_width and abs(y_shift) < src_height:
        raise ValueError("Shift exceeds image dimensions (i.e. pushing image out of the image).")

    out_x_0 = (x_shift + abs(x_shift)) / 2  # Is 0 if x_shift < 0
    out_x_0 = np.uint16(out_x_0)
    out_x_1 = src_width - (- x_shift + abs(x_shift)) / 2  # Not + 1 because shape is not zero intexed
    out_x_1 = np.uint16(out_x_1)
    out_y_0 = (y_shift + abs(y_shift)) / 2  # Is 0 if y_shift < 0
    out_y_0 = np.uint16(out_y_0)
    out_y_1 = src_height - (- y_shift + abs(y_shift)) / 2
    out_y_1 = np.uint16(out_y_1)

    src_x_0 = (- x_shift + abs(x_shift)) / 2
    src_x_0 = np.uint16(src_x_0)
    src_x_1 = src_width - (x_shift + abs(x_shift)) / 2
    src_x_1 = np.uint16(src_x_1)
    src_y_0 = (- y_shift + abs(y_shift)) / 2
    src_y_0 = np.uint16(src_y_0)
    src_y_1 = src_height - (y_shift + abs(y_shift)) / 2
    src_y_1 = np.uint16(src_y_1)

    logging.debug(f"out_x_0 {out_x_0}")
    logging.debug(f"out_x_1 {out_x_1}")
    logging.debug(f"out_y_0 {out_y_0}")
    logging.debug(f"out_y_1 {out_y_1}")
    logging.debug(f"src_x_0 {src_x_0}")
    logging.debug(f"src_x_1 {src_x_1}")
    logging.debug(f"src_y_0 {src_y_0}")
    logging.debug(f"src_y_1 {src_y_1}")

    img_out[out_y_0:out_y_1, out_x_0:out_x_1, :] = src[src_y_0:src_y_1, src_x_0:src_x_1]
    return img_out.astype(np.uint8)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s]\t%(funcName)15s: %(message)s")
    # logging.disable()

    resize_factor = 7.1
    padding = (300, 400, 300, 400)
    rotation = -5
    shift = (120, 150)
    alpha = 0.6
    beta = 1

    RGB_0515 = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/fusing_tests/DJI_0515.JPG"
    IR_0515 = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/fusing_tests/20211216_122648_R.jpg"

    RGB_0641 = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/RGB images and video/DJI_0641.JPG"
    IR_0641 = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/Thermal images and video/20211216_122012/20211216_123110_R.jpg"

    RGB_0631 = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/RGB images and video/DJI_0631.JPG"
    IR_0631 = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/Thermal images and video/20211216_122012/20211216_123050_R.jpg"

    RGB_0622 = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/RGB images and video/DJI_0622.JPG"
    IR_0622 = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/Thermal images and video/20211216_122012/20211216_123032_R.jpg"

    RGB = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/RGB images and video/DJI_0496.JPG"
    IR = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/Thermal images and video/20211216_122012/20211216_122608_R.jpg"

    ir_dir = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/Thermal images and video/20211216_122012"
    rgb_dir = "/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/RGB images and video/"

    ir_imgs = sorted(os.listdir("/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/Thermal images and video/20211216_122012/"))
    rgb_imgs = sorted(os.listdir("/opt/nfs/shared/scratch/bioblu/labelling/2021-12-16_paradise_bay_5m/RGB images and video/"))

    first_ir_i = ir_imgs.index("20211216_122608_R.jpg")
    first_rgb_i = rgb_imgs.index("DJI_0496.JPG")

    ir_imgs = ir_imgs[first_ir_i:]
    rgb_imgs = rgb_imgs[first_rgb_i:]

    fuse_images(RGB_0641, IR_0641,
                resize_factor_ir=7.1,
                padding_ltrb=(300, 400, 300, 400),
                rotation_angle=5.0,
                shift_yx=(200, 50),
                alpha=0.7, beta=0.7)