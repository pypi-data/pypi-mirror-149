import cv2 as cv
import json
import time
import sys
#sys.path.insert(0, 'src')
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.modeling import build_model
import torch
import os
import numpy as np
from PIL import Image
from com_ineuron_utils.utils import encodeImageIntoBase64


class Detector:

	def __init__(self,filename, model_name):

		# set model and test set
		self.filename = filename

		# obtain detectron2's default config
		self.cfg = get_cfg() 

		# load values from a file
		# self.cfg.merge_from_file("config.yml")
		if model_name == 'faster_rcnn_R_50_C4':
			print(f'model:faster_rcnn_R_50_C4')
			self.model = 'faster_rcnn_R_50_C4_1x.yaml'
			self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/" + self.model))
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/" + self.model)

		elif model_name == 'faster_rcnn_R_50_FPN':
			print(f'model:faster_rcnn_R_50_FPN')
			self.model = 'faster_rcnn_R_50_FPN_3x.yaml'
			self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/"+self.model))
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/" + self.model)

		elif model_name == 'faster_rcnn_X_101_32x8d_FPN':
			print(f'model:faster_rcnn_X_101_32x8d_FPN')
			self.model = 'faster_rcnn_X_101_32x8d_FPN_3x.yaml'
			self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/"+self.model))
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/" + self.model)

		elif model_name == 'retinanet_R_50_FPN':
			print(f'model:retinanet_R_50_FPN')
			self.model = 'retinanet_R_50_FPN_3x.yaml'
			self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/"+self.model))
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/" + self.model)

		elif model_name == 'fast_rcnn_R_50_FPN':
			print(f'model:fast_rcnn_R_50_FPN')
			self.model = 'fast_rcnn_R_50_FPN_1x.yaml'
			self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/"+self.model))
			self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/" + self.model)

		else:
			raise ValueError

		# set device to cpu
		self.cfg.MODEL.DEVICE = "cpu"

		# get weights
		# self.cfg.MODEL.WEIGHTS = "model_final_f10217.pkl"
		# self.cfg.MODEL.WEIGHTS = "model_final.pth"

		# set the testing threshold for this model
		self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.50

		# build model from weights
		# self.cfg.MODEL.WEIGHTS = self.convert_model_for_inference()

	# build model and convert for inference

	def convert_model_for_inference(self):

		# build model
		model = build_model(self.cfg)

		# save as checkpoint
		torch.save(model.state_dict(), 'checkpoint.pth')

		# return path to inference model
		return 'checkpoint.pth'


	def inference(self):
		# self.ROI = ROI
		predictor = DefaultPredictor(self.cfg)
		im = cv.imread(self.filename)
		t0 = time.time()
		outputs = predictor(im)
		t1 = time.time()
		metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0])

		# visualise
		v = Visualizer(im[:, :, ::-1], metadata=metadata, scale=1.2)
		v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
		predicted_image = v.get_image()
		im_rgb = cv.cvtColor(predicted_image, cv.COLOR_RGB2BGR)
		cv.imwrite('output.jpg', im_rgb)
		# imagekeeper = []
		opencodedbase64 = encodeImageIntoBase64("output.jpg")
		pred_bbox = outputs['instances'].pred_boxes.to('cpu')
		pred_bbox = pred_bbox.tensor.detach().numpy().tolist()
		pred_scores = outputs['instances'].scores.to('cpu').tolist()
		pred_time = round((t1 - t0), 3)
		print(pred_time)
		print(pred_scores)
		print(pred_bbox)
		# imagekeeper.append({"image": opencodedbase64.decode('utf-8')})
		result = {"pred_bbox": str(pred_bbox),
				  "pred_scores": str(pred_scores),
				  "pred_time": str(pred_time),
			      "image" : opencodedbase64.decode('utf-8')}
		return result




