import numpy as np
import argparse
import os
import tensorflow as tf
from PIL import Image
from io import BytesIO
import pathlib
import glob
import matplotlib.pyplot as plt
import cv2
import time
import sys

#sys.path.insert(0, 'tf2/object_detection')

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from com_ineuron_utils.utils import encodeImageIntoBase64

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile


class Predictor:
    def __init__(self, filename, model_name):
        self.PATH_TO_LABELS = self.download_labels('mscoco_label_map.pbtxt')
        self.category_index = label_map_util.create_category_index_from_labelmap(self.PATH_TO_LABELS,
                                                                                 use_display_name=True)
        self.filename = filename
        self.currentpath = os.getcwd()
        if model_name == 'efficientnetdet':
            modelpath = self.download_model('efficientdet_d0_coco17_tpu-32', '20200711')
            print(modelpath)
            self.model = tf.saved_model.load(modelpath + '/saved_model')

        elif model_name == 'fatser_rcnn_resnet50_640x640':
            modelpath = self.download_model('faster_rcnn_resnet50_v1_640x640_coco17_tpu-8', '20200711')
            self.model = tf.saved_model.load(modelpath + '/saved_model')

        elif model_name == 'fatser_rcnn_resnet152_1024x1024':
            modelpath = self.download_model('faster_rcnn_resnet152_v1_1024x1024_coco17_tpu-8', '20200711')
            self.model = tf.saved_model.load(modelpath + '/saved_model')

        elif model_name == 'ssd_resnet50_640x640':
            modelpath = self.download_model('ssd_resnet50_v1_fpn_640x640_coco17_tpu-8', '20200711')
            self.model = tf.saved_model.load(modelpath + '/saved_model')

        elif model_name == 'ssd_resnet152_1024x1024':
            modelpath = self.download_model('ssd_resnet152_v1_fpn_1024x1024_coco17_tpu-8', '20200711')
            self.model = tf.saved_model.load(modelpath + '/saved_model')

        else:
            raise Exception('Unknown model')

    def download_model(self, modelname, model_date):
        base_url = 'http://download.tensorflow.org/models/object_detection/tf2/'
        model_file = modelname + '.tar.gz'
        model_dir = tf.keras.utils.get_file(fname=modelname,
                                            origin=base_url + model_date + '/' + model_file,
                                            untar=True)
        return str(model_dir)

    def download_labels(self, filename):
        base_url = 'https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/'
        label_dir = tf.keras.utils.get_file(fname=filename,
                                            origin=base_url + filename,
                                            untar=False)
        label_dir = pathlib.Path(label_dir)
        return str(label_dir)

    def load_image_into_numpy_array(self, path):
        img_data = tf.io.gfile.GFile(path, 'rb').read()
        image = Image.open(BytesIO(img_data))
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    def run_inference_for_single_image(self, model, image):
        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(image)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]

        # Run inference

        output_dict = model(input_tensor)

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(output_dict.pop('num_detections'))
        output_dict = {key: value[0, :num_detections].numpy()
                       for key, value in output_dict.items()}
        output_dict['num_detections'] = num_detections

        # detection_classes should be ints.
        output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)

        # Handle models with masks:
        if 'detection_masks' in output_dict:
            # Reframe the the bbox mask to the image size.
            detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                output_dict['detection_masks'], output_dict['detection_boxes'],
                image.shape[0], image.shape[1])
            detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5, tf.uint8)
            output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()

        return output_dict

    def run_inference(self):
        image_path = "inputImage.jpg"
        image_np = self.load_image_into_numpy_array(image_path)
        # Actual detection.
        model = self.model
        t0 = time.time()
        output_dict = self.run_inference_for_single_image(model, image_np)
        t1 = time.time()
        category_index = self.category_index
        # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            category_index,
            min_score_thresh=.5,
            instance_masks=output_dict.get('detection_masks_reframed', None),
            use_normalized_coordinates=True,
            line_thickness=8)
        output_filename = 'output.jpg'
        cv2.imwrite(output_filename, image_np)
        predict_time = round((t1 - t0), 3)
        output_scores = [scores for scores in output_dict['detection_scores'] if scores > .5]
        output_boxes = [boxes.tolist() for boxes, scores in zip(output_dict['detection_boxes'], output_dict['detection_scores']) if scores > .5]
        num_of_detections = output_dict['num_detections']
        opencodedbase64 = encodeImageIntoBase64("output.jpg")
        #listOfOutput = []
        print('time:', predict_time)
        print(type(output_boxes), type(output_scores), type(predict_time))
        print('boxes:', output_boxes)
        print('no of detections:', num_of_detections)
        print('scores:', output_scores)
        result = {"pred_time": str(predict_time),
                  "pred_scores": str(output_scores),
                  "pred_bbox": str(output_boxes),
                  "num_of_detections": str(num_of_detections),
                  "image": opencodedbase64.decode('utf-8')}
        return result

#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Detect objects inside webcam videostream')
#     parser.add_argument('-m', '--model', type=str, required=True, help='Model Path')
#     parser.add_argument('-l', '--labelmap', type=str, required=True, help='Path to Labelmap')
#     parser.add_argument('-i', '--image_path', type=str, required=True, help='Path to image (or folder)')
#     args = parser.parse_args()

# detection_model = load_model(args.model)
# category_index = label_map_util.create_category_index_from_labelmap(args.labelmap, use_display_name=True)
#
# run_inference(detection_model, category_index, args.image_path)


