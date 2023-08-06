#!/usr/bin/env python3
import json

import cv2
import datetime
import detectron2
from detectron2.config import get_cfg
from detectron2.modeling import GeneralizedRCNN, build_model
from detectron2.engine import DefaultPredictor
from detectron2.data import dataset_mapper
import logging
import numpy as np
import os
import shutil
import torch
from typing import List, Tuple, Dict


IMG_FORMATS = ("tif", "tiff", "jpg", "jpeg", "png", "bmp", "gif")


def load_model(fpath_model, use_cpu=True) -> dict:
    device_params = {}
    if use_cpu:
        device_params["map_location"] = torch.device('cpu')
    try:
        model = torch.load(fpath_model, **device_params)
    except FileNotFoundError:
        raise FileNotFoundError(f"Model not found: {fpath_model}")
    else:
        return model


def create_img_dict(fpath_img, inference_output_dims_wh: Tuple[int, int] = None) -> Dict:
    assert fpath_img.endswith(IMG_FORMATS)
    _, img_name = os.path.split(fpath_img)
    img = np.array(cv2.imread(fpath_img))
    img_CHW = np.transpose(img, (2, 0, 1))  # Transpose from H, W, C to C, H, W
    img_tensor = torch.tensor(img_CHW)
    logging.debug(f"Loaded image {img_name} as tensor with shape {img_tensor.shape}")

    if inference_output_dims_wh is None:
        channels, img_height, img_width = tuple(img_tensor.shape)
    else:
        assert len(inference_output_dims_wh) == 2
        channels, (img_height, img_width) = 3, inference_output_dims_wh

    out_dict = {"image": img_tensor,
                "img_name": img_name,
                "height": img_height,
                "width": img_width}
    return out_dict


def initiate_cfg(fpath_model_pth, use_cpu=True, conf_threshold=0.6):
    cfg = get_cfg()
    if use_cpu:
        cfg.MODEL.DEVICE = "cpu"
    else:
        cfg.MODEL.DEVICE = "gpu"
    cfg.MODEL.WEIGHTS = fpath_model_pth
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = conf_threshold
    # cfg.MODEL.BATCH_SIZE =
    return cfg


def create_output_dir(fdir_predictions):
    try:
        os.makedirs(fdir_predictions)
    except FileExistsError:
        raise FileExistsError(f"Predictions output directory already exists: {fdir_predictions}")
    else:
        logging.info(f"Created output dir. {fdir_predictions}")


def load_imgs(fdir, inference_output_dims_wh=None) -> List[dict]:
    """
    Loads all images from one folder into a List[dict]. Can require a lot of memory.
    :param fdir:
    :param inference_output_dims_wh:
    :return:
    """
    files = sorted(os.listdir(fdir))
    imgs = []
    for file in files:
        if file.endswith(IMG_FORMATS):
            img_fpath = os.path.join(fdir, file)
            logging.debug(f"Loading img. {img_fpath}")
            imgs.append(create_img_dict(img_fpath, inference_output_dims_wh))
        else:
            logging.info(f"Skipped  loading img '{file}' because format is not among {IMG_FORMATS}.")
    return imgs


def predict_single_img(fpath_img, fpath_model, fdir_prediction_output, conf_threshold=0.6,
                       inference_output_dims_wh=None, use_cpu=True):
    if not os.path.isdir(fdir_prediction_output):
        os.makedirs(fdir_prediction_output)
    # Create input dict
    input_img = create_img_dict(fpath_img)
    # Load model into cfg
    cfg = initiate_cfg(fpath_model, use_cpu=use_cpu, conf_threshold=conf_threshold)
    model = detectron2.modeling.build_model(cfg)
    predictor = DefaultPredictor(cfg)
    # Run prediction
    # result = model([input_img])
    result = predictor.model([input_img])
    return result


def predict_multiple_imgs(fdir_imgs, fpath_model, fdir_predictions=None,
                          conf_threshold=0.6, inference_output_dims_wh=None, use_cpu=True):
    # Create output dir
    if fdir_predictions is None:
        fdir_predictions = f"{fdir_imgs}/output"
    create_output_dir(fdir_predictions)

    input_img_paths = [os.path.join(fdir_imgs, path) for path in sorted(os.listdir(fdir_imgs)) if path.endswith(IMG_FORMATS)]

    # Load model into cfg
    cfg = initiate_cfg(fpath_model, use_cpu=use_cpu, conf_threshold=conf_threshold)
    predictor = DefaultPredictor(cfg)
    # model = detectron2.modeling.build_model(cfg)

    predictions = []
    for img_path in input_img_paths:
        result = (0,)
        img_name = os.path.split(img_path)[-1]
        logging.info(f"Processing image {img_name}")
        # img = create_img_dict(fpath_img=img_path, inference_output_dims_wh=inference_output_dims_wh)
        img = cv2.imread(img_path)
        # result = predictor.model([img])[0]
        # result = predictor.model([img])[0]
        result = predictor(img)
        logging.info(f"Prediction: {result}")
        # result = model([img])[0]
        result["img_name"] = img_name
        predictions.append(result)
        del img
        # logging.debug(result)
        # img_name_body = img_name.split(".")[0]
        # fpath_prediction = os.path.join(fdir_predictions, img_name_body + ".json")
        # with open(fpath_prediction, "w") as f:
        #     f.write(json.dumps(result, indent=4))
    return predictions


    # model = load_model(fpath_model, use_cpu=use_cpu)
    # img_dicts = load_imgs(fdir_imgs, inference_output_dims_wh)
    # model.eval()
    # with torch.no_grad():
    #     outputs = model(img_dicts)
    # predictions = model(img_dicts)
    # return predictions


if __name__ == "__main__":
    print(f"torch: {torch.__version__}")
    os.environ["LRU_CACHE_CAPACITY"] = "1"

    loglevel = logging.DEBUG
    logformat = "[%(levelname)s]\t%(funcName)15s: %(message)s"
    logging.basicConfig(level=loglevel, format=logformat)

    fpath_model = "/media/findux/DATA/Documents/Malta_II/results/5148_2022-05-01_225524/model_final.pth"
    imgs_fdir = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_04_gnejna_with_duplicates_detectron/test/"
    # fpath_cfg = "/media/findux/DATA/Documents/Malta_II/results/5148_2022-05-01_225524/dataset_cfg.json"
    preds = predict_multiple_imgs(imgs_fdir, fpath_model=fpath_model, conf_threshold=0.2)

    # fpath_img = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_04_gnejna_with_duplicates_detectron/test/Gnejna_DJI_0698_1-0.tif"
    # fpath_output = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_04_gnejna_with_duplicates_detectron/test/output/"
    # prediction = predict_single_img(fpath_img, fpath_model, fpath_output)