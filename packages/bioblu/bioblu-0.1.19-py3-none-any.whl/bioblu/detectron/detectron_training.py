#!/usr/bin/env python3
import datetime

import cv2
import json
import logging
import numpy as np
import os
import random
from typing import List, Tuple

import detectron2
from detectron2.utils.logger import setup_logger
from detectron2.data.datasets import register_coco_instances
from detectron2.utils.logger import setup_logger
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog, datasets
from detectron2.structures import BoxMode
from detectron2.engine import DefaultTrainer
from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.data import build_detection_test_loader
from detectron2.utils.visualizer import ColorMode
import cv2
from detectron2.structures import BoxMode
# from google.colab.patches import cv2_imshow

from bioblu.detectron import detectron
from bioblu.ds_manage import ds_annotations
from bioblu.ds_manage import ds_convert
import bioblu


def run_training(yolo_ds_root_dir, model_to_use: str, output_dir, materials_dict: dict,
                 training_json=None, val_json=None,
                 iterations: int = 2500,
                 ds_cfg_savename="ds_catalog_train.json", ds_name_train="instances_detectron_train",
                 ds_name_val="instances_detectron_val", img_size_minmax: Tuple[int, int] = (1820, 1830), device="gpu",
                 keep_bg_imgs=True, max_detections_per_img=2000, number_of_workers=2, imgs_per_batch=2,
                 base_lr = 0.00025, lr_decay=None, roi_heads_batch_size_per_img=512,
                 validation_confidence_threshold=0.65, training_confidence_threshold=0.5):

    assert os.path.isdir(yolo_ds_root_dir)
    detectron_ds_target_dir = os.path.join(yolo_ds_root_dir.rstrip("/") + "_detectron")
    if training_json is None:
        training_json = os.path.join(detectron_ds_target_dir, "annotations", ds_name_train + ".json")
    if val_json is None:
        val_json = os.path.join(detectron_ds_target_dir, "annotations", ds_name_val + ".json")
    if lr_decay is None:
        lr_decay = []

    print(f"Training on dataset {yolo_ds_root_dir}")
    print(f"Using model {model_to_use}")

    ds_convert.cvt_yolo_to_detectron(yolo_ds_root_dir)

    setup_logger()  # Detectron2 logger
    ds_convert.cvt_yolo_to_detectron(yolo_ds_root_dir, materials_dict=materials_dict)
    # Extract image dict lists from jsons
    logging.info("Img. dict lists extracted.")
    # Register classes
    classes = materials_dict
    logging.info("Classes registered.")

    cfg = get_cfg()
    # Load model and model weights/checkpoint
    cfg.merge_from_file(model_zoo.get_config_file(model_to_use))
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(model_to_use)
    cfg.MODEL.DEVICE=device
    cfg.DATALOADER.FILTER_EMPTY_ANNOTATIONS = not keep_bg_imgs  # if keep_bg_imgs==True, they will NOT be filtered out.
    # Override output dir to prevent "permission denied" error during mkdir
    cfg.OUTPUT_DIR = output_dir
    # Register datasets
    DatasetCatalog.register(ds_name_train, lambda: detectron.create_detectron_img_dict_list(training_json))
    DatasetCatalog.register(ds_name_val, lambda: detectron.create_detectron_img_dict_list(val_json))
    # Register metadata
    MetadataCatalog.get(ds_name_train).set(thing_classes=list(classes.values()))
    MetadataCatalog.get(ds_name_val).set(thing_classes=list(classes.values()))
    # Allocate datasets
    cfg.DATASETS.TRAIN = (ds_name_train,)
    cfg.DATASETS.TEST = (ds_name_val,)
    # Training parameters
    cfg.TEST.DETECTIONS_PER_IMAGE = max_detections_per_img  # set max detections per img
    cfg.INPUT.MIN_SIZE_TRAIN = (img_size_minmax[0],)  # minimum image size for the train set
    cfg.INPUT.MAX_SIZE_TRAIN = img_size_minmax[1]  # maximum image size for the train set
    cfg.INPUT.MIN_SIZE_TEST = img_size_minmax[0]  # minimum image size for the test set
    cfg.INPUT.MAX_SIZE_TEST = img_size_minmax[1]  # maximum image size for the test set

    cfg.DATALOADER.NUM_WORKERS = number_of_workers
    cfg.SOLVER.IMS_PER_BATCH = imgs_per_batch
    cfg.SOLVER.BASE_LR = base_lr  # 0.00025  # pick a good LR
    cfg.SOLVER.MAX_ITER = iterations  # 300 iterations seems good enough for the tutorial dataset; you will need to train longer for a practical dataset
    cfg.SOLVER.STEPS = lr_decay  # do not decay learning rate
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = roi_heads_batch_size_per_img  # faster, and good enough for this toy dataset (default: 512)
    # cfg.DATASETS.PROPOSAL_FILES_TRAIN =     # ToDo: Perhaps add the proposal files?
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(materials_dict.keys())  # only has one class (ballon). (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)     # NOTE: this config means the number of classes, but a few popular unofficial tutorials incorrect uses num_classes+1 here.
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = training_confidence_threshold  # 0.5  # set threshold for this model
    # ToDo: check additional augmentation & hyperparameter options
    logging.info("cfg set up completed.")

    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    logging.info("Output dir created")

    # Save dataset catalog entries:
    dataset_test_out = DatasetCatalog.get(ds_name_train)
    savefile = os.path.join(cfg.OUTPUT_DIR, ds_cfg_savename)
    with open(savefile, "w") as f:
        json.dump(dataset_test_out, f, indent=4)
        logging.info(f"Dataset Catalog (training) saved as {savefile}")

    # save training config cfg to yaml
    cfg_save_path = os.path.join(cfg.OUTPUT_DIR, "cfg.yaml")
    cfg_save_string = cfg.dump()
    with open(cfg_save_path, "w") as f:
        f.write(cfg_save_string)
    print(f"Saved model/training cfg in {cfg_save_path}")

    # Set up trainer
    trainer = DefaultTrainer(cfg)
    logging.debug("Done setting up trainer.")
    trainer.resume_or_load(resume=False)
    logging.debug("Starting training.")
    trainer.train()
    print("Done training. Proceeding to evaluation.")

    # Prep evaluation
    # pretrained_model = "/content/drive/MyDrive/colab_outputs/2022-04-30_1030/model_final.pth"
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")  # path to the model we just trained
    print(f"Evaluating model {os.path.join(cfg.OUTPUT_DIR, 'model_final.pth')}")
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = validation_confidence_threshold  # set a custom testing threshold
    predictor = DefaultPredictor(cfg)
    # Evaluate
    evaluator = COCOEvaluator(ds_name_val,
                              tasks=("bbox",),
                              use_fast_impl=False,  # use a fast but unofficial implementation to compute AP
                              output_dir=output_dir)
    val_loader = build_detection_test_loader(cfg, ds_name_val)
    evaluation_results = inference_on_dataset(predictor.model, val_loader, evaluator)
    print(evaluation_results)

    # Save evaluation results
    eval_results_savepath = os.path.join(cfg.OUTPUT_DIR, "evaluation_results.txt")
    with open(eval_results_savepath, "w") as f:
        f.write(evaluation_results)
    print("Done training and evaluating.")


if __name__ == "__main__":
    loglevel = logging.INFO
    logformat = "[%(levelname)s]\t%(funcName)15s: %(message)s"
    logging.basicConfig(level=loglevel, format=logformat)
    # logging.disable

    # YOLO_DS_ROOT_DIR = "/opt/nfs/shared/scratch/bioblu/datasets/dataset_01"
    # MODEL_NAME = "/COCO-Detection/faster_rcnn_R_101_C4_3x.yaml"
    # print(f"Training on dataset {YOLO_DS_ROOT_DIR}")
    # print(f"Using model {MODEL_NAME}")
    # OUTPUT_DIR = "/opt/nfs/shared/scratch/bioblu/output"
    # CFG_SAVE_NAME = "dataset_cfg.json"
    # DS_NAME_TRAIN = "instances_detectron_train"
    # DS_NAME_VAL = "instances_detectron_val"
    # IMG_SIZE_MIN_MAX = (1824, 1828)
    #
    # detectron_ds_target_dir = os.path.join(YOLO_DS_ROOT_DIR + "_detectron")
    # img_dir_train = os.path.join(detectron_ds_target_dir, "train")
    # img_dir_valid = os.path.join(detectron_ds_target_dir, "val")
    # fpath_json_train = os.path.join(detectron_ds_target_dir, "annotations", "instances_detectron_train.json")
    # fpath_json_valid = os.path.join(detectron_ds_target_dir, "annotations", "instances_detectron_val.json")
    # fpath_json_test = os.path.join(detectron_ds_target_dir, "annotations", "instances_detectron_test.json")
    # materials_dict: dict = {0: "trash"}
    #
    # tstamp = str(datetime.date.today())
    #
    # logging.info(f"CWD: {os.getcwd()}")
    # logging.info(f"Detectron dir:\t{detectron_ds_target_dir}")
    # logging.info(f"Training images:\t{img_dir_train}")
    # logging.info(f"Validation images:\t{img_dir_valid}")
    # logging.info(f"Training json:\t{fpath_json_train}")
    # logging.info(f"Validate json:\t{fpath_json_valid}")
    # logging.info(f"Testing json:\t{fpath_json_test}")
    # print(f"bioblu version:\t{bioblu.__version__}")
    #
    # setup_logger()     # Detectron2 logger
    # ds_convert.cvt_yolo_to_detectron(YOLO_DS_ROOT_DIR, materials_dict=materials_dict)
    # # Extract image dict lists from jsons
    # train_imgs: List[dict] = detectron.create_detectron_img_dict_list(fpath_json_train)
    # valid_imgs: List[dict] = detectron.create_detectron_img_dict_list(fpath_json_valid)
    # test_imgs: List[dict] = detectron.create_detectron_img_dict_list(fpath_json_test)
    # logging.info("Img. dict lists extracted.")
    # # Register classes
    # classes = materials_dict # .values()
    # logging.info("Classes registered.")
    #
    # cfg = get_cfg()
    # # Load model and model weights/checkpoint
    # cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_C4_1x.yaml"))
    # cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_C4_1x.yaml")  # Let training initialize from model zoo
    # cfg.DATALOADER.FILTER_EMPTY_ANNOTATIONS = False  # Keep background images
    # # Override output dir to prevent "permission denied" error during mkdir
    # cfg.OUTPUT_DIR = OUTPUT_DIR
    # # Register datasets
    # DatasetCatalog.register(DS_NAME_TRAIN, lambda: detectron.create_detectron_img_dict_list(fpath_json_train))
    # DatasetCatalog.register(DS_NAME_VAL, lambda: detectron.create_detectron_img_dict_list(fpath_json_valid))
    # # Register metadata
    # MetadataCatalog.get(DS_NAME_TRAIN).set(thing_classes=list(classes.values()))
    # MetadataCatalog.get(DS_NAME_VAL).set(thing_classes=list(classes.values()))
    # # Allocate datasets
    # cfg.DATASETS.TRAIN = (DS_NAME_TRAIN,)
    # cfg.DATASETS.TEST = (DS_NAME_VAL,)
    # # Training parameters
    # cfg.TEST.DETECTIONS_PER_IMAGE = 2500  # set max detections per img
    # cfg.INPUT.MIN_SIZE_TRAIN = (IMG_SIZE_MIN_MAX[0],)  # minimum image size for the train set
    # cfg.INPUT.MAX_SIZE_TRAIN = IMG_SIZE_MIN_MAX[1]  # maximum image size for the train set
    # cfg.INPUT.MIN_SIZE_TEST = IMG_SIZE_MIN_MAX[0]  # minimum image size for the test set
    # cfg.INPUT.MAX_SIZE_TEST = IMG_SIZE_MIN_MAX[1]      # maximum image size for the test set
    #
    # cfg.DATALOADER.NUM_WORKERS = 2
    # cfg.SOLVER.IMS_PER_BATCH = 2
    # cfg.SOLVER.BASE_LR = 0.0004  # 0.00025  # pick a good LR
    # cfg.SOLVER.MAX_ITER = 3000    # 300 iterations seems good enough for the tutorial dataset; you will need to train longer for a practical dataset
    # cfg.SOLVER.STEPS = []        # do not decay learning rate
    # cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 512   # faster, and good enough for this toy dataset (default: 512)
    # # cfg.DATASETS.PROPOSAL_FILES_TRAIN =     # ToDo: Perhaps add the proposal files?
    # cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # only has one class (ballon). (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)     # NOTE: this config means the number of classes, but a few popular unofficial tutorials incorrect uses num_classes+1 here.
    # cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.3  # 0.5  # set threshold for this model
    # logging.info("cfg set up.")
    #
    # os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    # logging.info("Output dir created")
    #
    # # Save the accessible dataset version:
    # dataset_test_out = DatasetCatalog.get(DS_NAME_TRAIN)
    # with open(cfg.OUTPUT_DIR + "/dataset_cfg.json", "w") as f:
    #     json.dump(dataset_test_out, f, indent=4)
    #     logging.info(f"cfg saved as {dataset_test_out}")
    #
    # # Set up trainer
    # trainer = DefaultTrainer(cfg)
    # logging.debug("Done setting up trainer.")
    # trainer.resume_or_load(resume=False)
    # logging.debug("Starting training.")
    # trainer.train()
    #
    # # Prep evaluation
    # # pretrained_model = "/content/drive/MyDrive/colab_outputs/2022-04-30_1030/model_final.pth"
    # cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")  # path to the model we just trained
    # logging.info(f"Evaluating model {os.path.join(cfg.OUTPUT_DIR, 'model_final.pth')}")
    # cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7  # set a custom testing threshold
    # predictor = DefaultPredictor(cfg)
    # # Evaluate
    # evaluator = COCOEvaluator(DS_NAME_VAL,
    #                           tasks=("bbox",),
    #                           use_fast_impl=False, # use a fast but unofficial implementation to compute AP
    #                           output_dir=OUTPUT_DIR)
    # val_loader = build_detection_test_loader(cfg, DS_NAME_VAL)
    # print(inference_on_dataset(predictor.model, val_loader, evaluator))
    #
    # # save cfg to yaml
    # cfg_save_path = os.path.join(cfg.OUTPUT_DIR, "cfg.yaml")
    # cfg_save_string = cfg.dump()
    # with open(cfg_save_path, "w") as f:
    #     f.write(cfg_save_string)

    ds_yolo = "/media/findux/DATA/Documents/Malta_II/datasets/dataset_05_mini_gnejna/"
    output = "/home/findux/Desktop/tmp/output_test"
    model = "COCO-Detection/faster_rcnn_R_101_C4_3x.yaml"
    run_training(ds_yolo, model, output, {0: "trash"}, iterations=300, device="cpu")