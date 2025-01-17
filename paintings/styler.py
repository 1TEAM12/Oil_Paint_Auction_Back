import cv2
import numpy as np
import datetime
import sys
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_back.settings")
django.setup()

from paintings.models import STYLE_CHOICES


def painting_styler(img_url, style_id):
    model = STYLE_CHOICES[int(style_id) - 1][1]
    net = cv2.dnn.readNetFromTorch(f"./paintings/models/{model}.t7")
    img = cv2.imread("./media/" + str(img_url))

    # pre-processing
    h, w, c = img.shape
    img = cv2.resize(img, dsize=(500, int(h / w * 500)))

    MEAN_VALUE = [103.939, 116.779, 123.680]
    blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)

    # inference
    net.setInput(blob)
    output = net.forward()

    # post-processing
    output = output.squeeze().transpose((1, 2, 0))
    output += MEAN_VALUE

    output = np.clip(output, 0, 255)
    output = output.astype("uint8")

    date = datetime.datetime.now()
    saving_path = f"./media/after_img/img_{date:%y%m%d}_{date:%H%M%S}.png"
    cv2.imwrite(saving_path, output)
    img_path = saving_path[8:]
    return img_path


"""
01_eccv16_composition_vii.t7
02_eccv16_la_muse.t7
03_eccv16_starry_night.t7
04_eccv16_the_wave.t7
05_instance_norm_candy.t7
06_instance_norm_feathers.t7
07_instance_norm_la_muse.t7
08_instance_norm_mosaic.t7
09_instance_norm_starry_night.t7
10_instance_norm_the_scream.t7
11_instance_norm_udnie.t7
"""
