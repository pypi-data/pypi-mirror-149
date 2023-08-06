#!/usr/bin/env python3

import cv2
import json
import logging
import numpy as np
import os
import random
from typing import List
import torch

import detectron2
from detectron2.data.datasets import register_coco_instances
from detectron2.utils.logger import setup_logger

# import some common detectron utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.structures import BoxMode
from detectron2.engine import DefaultTrainer

from detectron2.structures import BoxMode
from detectron2.evaluation import COCOEvaluator
from detectron2.modeling import build_model
from detectron2.checkpoint import DetectionCheckpointer
from bioblu.ds_manage import ds_annotations


def load_json(json_fpath: str) -> dict:
    """Returns json data as a dict."""
    with open(json_fpath, 'r') as f:
        data = json.load(f)
    logging.debug(f'Loaded json object (type): {type(data)}')
    return data


def create_detectron_img_dict_list(coco_json_fpath, bbox_format = BoxMode.XYWH_ABS) -> List[dict]:
    """
    Creates a list of dictionaries to be used in detectron.
    :param coco_json_fpath:
    :return:
    """
    json_data = load_json(coco_json_fpath)
    images = json_data.get("images", [])
    logging.debug(f"Images: {images}")
    annotations = json_data.get("annotations", [])
    dict_list = []
    for img in images:
        current_img = {"file_name": img["file_name"],
                       "image_id": img["id"],
                       "width": img["width"],
                       "height": img["height"],
                       "annotations": []}
        for annotation in annotations:
            if annotation["image_id"] == current_img["image_id"]:
                current_img["annotations"].append({"segmentation": [],
                                                   "area": None,  # ToDo: Check if this might have to be box area.
                                                   "iscrowd": 0,
                                                   "category_id": annotation["category_id"],
                                                   "bbox_mode": bbox_format,
                                                   "bbox": annotation["bbox"]})
        dict_list.append(current_img)
    return dict_list


if __name__ == "__main__":
    model_fpath = "/media/findux/DATA/Documents/Malta_II/colab_outputs/2022-04-25_0002/model_final.pth"
    cfg = model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_C4_1x.yaml")
    model = torch.load(model_fpath,
                       map_location=torch.device('cpu'))  # remove this line when running on gpu / with CUDA enabled
    # ds_json = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_04_gnejna_with_duplicates_coco/coco/annotations/instances_train2017.json"
    # results_dir = "/home/findux/Desktop/tmp/detectron_eval_output"
    # evaluator = COCOEvaluator(dataset_name=ds_json,  # name of ds to be eval'ed. must have metadata: ”json_file”: path to COCO format annotation, or must be in detectron2’s standard dataset format.
    #                           tasks=("bbox",),       # tasks that can be evaluated under the given configuration. A task is one of “bbox”, “segm”, “keypoints”. By default, will infer this automatically from predictions.
    #                           distributed=True,
    #                           output_dir=results_dir)