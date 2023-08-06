import argparse
import pathlib
import os

import numpy as np
import cv2
from scipy.spatial.transform import Rotation as SciRot
from matplotlib import pyplot as plt

from projection import Camera, RadialPolyCamProjection, CylindricalProjection, read_cam_from_json, \
    create_img_projection_maps, PinholeLens


def make_cylindrical_cam(cam: Camera):
    """generates a cylindrical camera with a centered horizon"""
    assert isinstance(cam.lens, RadialPolyCamProjection)
    # creates a cylindrical projection
    #lens = CylindricalProjection(cam.lens.coefficients[0])
    lens = PinholeLens(cam.lens.coefficients[0])
    rot_zxz = SciRot.from_matrix(cam.rotation).as_euler('zxz')
    # adjust all angles to multiples of 90 degree
    rot_zxz = np.round(rot_zxz / (np.pi / 2)) * (np.pi / 2)
    # center horizon
    rot_zxz[1] = np.pi / 2
    # noinspection PyArgumentList
    return Camera(
        rotation=SciRot.from_euler(angles=rot_zxz, seq='zxz').as_matrix(),
        translation=cam.translation,
        lens=lens,
        size=cam.size, principle_point=(cam.cx_offset, cam.cy_offset),
        aspect_ratio=cam.aspect_ratio
    )



def preprocess(img, json, dst):
    # generate camera instances
    fisheye_cam = read_cam_from_json(json)
    cylindrical_cam = make_cylindrical_cam(fisheye_cam)

    # load example image and re-project it to a central cylindrical projection
    fisheye_image = cv2.imread(img)
    map1, map2 = create_img_projection_maps(fisheye_cam, cylindrical_cam)
    perspective_image = cv2.remap(fisheye_image, map1, map2, cv2.INTER_CUBIC)

    cv2.imwrite(dst, perspective_image)


def To_prespective():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', help="input fisheye image path")
    parser.add_argument('json_path', help = "input json file path which correspond to fisheye image")
    parser.add_argument('output_path', help = "output file path")

    args = parser.parse_args()

    preprocess(args.image_path, args.json_path, args.output_path)