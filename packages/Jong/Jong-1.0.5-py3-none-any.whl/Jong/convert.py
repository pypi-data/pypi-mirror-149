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



def preprocess():
    # generate camera instances
    fisheye_cam = read_cam_from_json('./front.json')
    cylindrical_cam = make_cylindrical_cam(fisheye_cam)

    # load example image and re-project it to a central cylindrical projection
    fisheye_image = cv2.imread('./test3.png')
    map1, map2 = create_img_projection_maps(fisheye_cam, cylindrical_cam)
    cylindrical_image = cv2.remap(fisheye_image, map1, map2, cv2.INTER_CUBIC)

    plt.imshow(cv2.cvtColor(fisheye_image, cv2.COLOR_BGR2RGB))
    plt.show()
    plt.imshow(cv2.cvtColor(cylindrical_image, cv2.COLOR_BGR2RGB))
    plt.show()