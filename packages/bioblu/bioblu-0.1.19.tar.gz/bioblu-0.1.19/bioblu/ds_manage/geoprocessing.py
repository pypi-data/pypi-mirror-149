#!/usr/bin/env python3
import glob
import logging
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image
from PIL.Image import Exif
import pyproj
import pyexiv2
from typing import Tuple, Union


DELTA_STR = "\u0394"


def calc_abs_angle(px_shift_yx, yaw) -> float:
    """
    Calculates absolute angle of the shift, based on original pixel shift and drone yaw.
    :param px_shift_yx:
    :param yaw:
    :return: absolute angle of the shift
    """
    # assert abs(yaw) not in [0, 90, 180, 270, 360]  # Because in these cases the angle is not needed.
    assert px_shift_yx != (0, 0)
    logging.info(f"Yaw: {yaw}")
    _px_angle = calc_px_shift_angle(px_shift_yx)
    abs_angle = _px_angle + yaw
    logging.info(f"Abs angle {abs_angle}")
    return transform_to_positive_degrees(abs_angle)


def calc_abs_px_shift(px_shift_yx, yaw):
    if px_shift_yx == (0, 0):
        return px_shift_yx
    abs_angle = calc_abs_angle(px_shift_yx, yaw)
    shift_len = calc_shift_len(px_shift_yx)
    abs_delta_y, abs_delta_x = get_px_delta_from_hypotenuse_and_angle(shift_len, abs_angle)
    return abs_delta_y, abs_delta_x


def calc_gsd(altitude_m, focal_length_mm=8.6, sensor_width_mm=12.8333, img_width=5472, img_height=3648):
    """
    Returns the GSD in cm based on camera focal length. Default values taken from: https://community.pix4d.com/t/dji-phantom-4-pro-v2-0-gsd-and-camera-parameters/7478/2
    :param altitude_m:
    :param focal_length_mm: real focal length, not 35 mm equivalent.
    :param sensor_width_mm:
    :param img_width:
    :param img_height:
    :return:
    """
    gsd = (sensor_width_mm * altitude_m * 100) / (focal_length_mm * img_width)
    return gsd


def calc_latlong_shift_from_px_shift(px_offset_yx: Tuple[int, int], gsd_cm: float,
                                     yaw_angle_deg: float = 0.0, degree_constant=111_139) -> Tuple[float, float]:
    """
    Returns the shift in latitude, longitude (y, x)
    :param px_offset_yx:
    :param gsd_cm:
    :param yaw_angle_deg:
    :param degree_constant: Amount of meters that constitute 1 degree shift of either latitude or longitude.
    :return:
    """
    delta_y_abs, delta_x_abs = calc_abs_px_shift(px_offset_yx, yaw_angle_deg)
    delta_lat = (- delta_y_abs * gsd_cm) / (degree_constant * 100)
    delta_long = (delta_x_abs * gsd_cm) / (degree_constant * 100)

    logging.debug(f"Px offset: {px_offset_yx}")
    logging.debug(f"GSD: {gsd_cm}")
    logging.info(f"Yaw angle deg.: {yaw_angle_deg}")
    logging.debug(f"Abs. px shift yx: {delta_y_abs, delta_x_abs}")
    logging.info(f"Delta lat long: {delta_lat, delta_long}")
    return delta_lat, delta_long


def calc_px_shift_angle(px_shift_yx: Tuple[int, int]) -> float:
    """
    Returns the angle of the pixel shift in degrees.
    :param px_shift_yx:
    :return:
    """
    angle = None
    if px_shift_yx == (0, 0):
        raise ArithmeticError("No pixel shift. Both shifts are zero.")
    delta_y, delta_x = px_shift_yx
    # Cover right angles:
    if delta_y == 0 and delta_x < 0:
        angle = 0.0
    elif delta_y < 0 and delta_x == 0:
        angle = 90.0
    elif delta_y == 0 and delta_x > 0:
        angle = 180.0
    elif delta_y > 0 and delta_x == 0:
        angle = 270.0
    # Cover angles that are not in [0, 90, 180, 270, 360]
    elif delta_y < 0 and delta_x < 0:
        logging.info("Top-left quadrant.")
        angle = trigonometry_angle_from_adjacent_and_opposite(abs(delta_x), abs(delta_y))
    elif delta_y < 0 and delta_x > 0:
        logging.info("Top-right quadrant.")
        angle = 90 + (90 - trigonometry_angle_from_adjacent_and_opposite(delta_x, abs(delta_y)))
    elif delta_y > 0 and delta_x > 0:
        logging.info("Bottom-right quadrant.")
        angle = 180 + trigonometry_angle_from_adjacent_and_opposite(delta_x, delta_y)
    elif delta_y > 0 and delta_x < 0:
        logging.info("Bottom-left quadrant")
        angle = 270 + (90 - trigonometry_angle_from_adjacent_and_opposite(abs(delta_x), delta_y))
    else:
        raise ArithmeticError(f"Could not calculate angle for shift {px_shift_yx}")
    return angle


def get_px_delta_from_hypotenuse_and_angle(hypotenuse: float, alpha_deg):
    """
    Calculates the x- and y-shift between points a and b of a right triangle from hypotenuse length and alpha
    angle value (in degrees). Assumes that CA is the X axis and CB is the Y axis.
    :param hypotenuse: length of the hypotenuse
    :param alpha_deg:
    :return:
    """
    delta_y = - math.sin(math.radians(alpha_deg)) * hypotenuse
    delta_x = - math.cos(math.radians(alpha_deg)) * hypotenuse
    logging.info(f"{DELTA_STR}y: {delta_y}, {DELTA_STR}x: {delta_x}")
    return delta_y, delta_x


def calc_shift_len(px_shift_yx):
    """Calculates total length of shift (i.e. hypotenuse) based on delta x and delta y."""
    dy, dx = px_shift_yx
    return math.sqrt(dy ** 2 + dx ** 2)


def dd_to_dms(dd: float) -> Tuple[int, int, float]:
    """
    Converts a decimal degree value into degrees, minutes and decimal seconds.
    :param dd: decimal degrees
    :return: Tuple (dd, mm, ss.ss)
    """
    degrees = int(dd)  # int always rounds down
    dminutes = (dd - degrees) * 60
    minutes = int(dminutes)
    seconds = (dminutes - minutes) * 60
    return degrees, minutes, seconds


def dms_to_dd(deg_min_sec: tuple):
    assert len(deg_min_sec) == 3
    _deg, _min, _sec = deg_min_sec
    dd_coordinate = float(_deg) + float(_min) / 60 + float(_sec) / 3600
    return dd_coordinate


def extract_all_img_coordinates(fdir_img) -> pd.DataFrame:
    """
    Extracts the coordinates for all image files in one folder.
    :param img_path:
    :return:
    """
    img_list = sorted(os.listdir(fdir_img))
    # Exclude non-files (i.e. directories)
    img_list = [img for img in img_list if os.path.isfile(os.path.join(fdir_img, img))]

    logging.info(img_list)
    img_df = pd.DataFrame({"file_name": img_list})
    img_df["path"] = [os.path.join(fdir_img, fname) for fname in img_df["file_name"]]
    latitudes = []
    longitudes = []
    for fpath in img_df["path"]:
        logging.info(f"fpath: {fpath}")
        coords = extract_coordinates_from_img(fpath)
        if coords is not None:
            lat = extract_coordinates_from_img(fpath)[0]
            lon = extract_coordinates_from_img(fpath)[1]
            latitudes.append(lat)
            longitudes.append(lon)
    img_df["latitude"] = latitudes
    img_df["longitude"] = longitudes
    return img_df


def extract_coordinates_from_img(fpath_img) -> tuple:
    """
    Returns (lat, long) of the image.
    :param fpath_img:
    :return: tuple (lat, lon)
    """
    exif_raw = extract_raw_exif(fpath_img)
    if exif_raw is not None:
        geoinfo = get_geo_info_from_exif(exif_raw)
        return geoinfo["latitude"], geoinfo["longitude"]
    else:
        return None, None


def extract_uav_yaw(fpath_img: str):
    """
    Extracts UAV yaw from DJI jpeg images. This does not work for images from the FLIR camera.
    ToDo: Create a function that does this for video files.
    :param fpath_img: image filepath
    :return: yaw degrees (float)
    """
    try:
        with open(fpath_img, "rb") as f:
            img_bytes = f.read()
    except FileNotFoundError:
        print(f"Could not find file to extract uav yaw from: {fpath_img}")
    else:
        img_metadata = pyexiv2.ImageData(img_bytes)
        logging.debug(type(img_metadata))
        yaw_degrees = img_metadata.read_xmp()["Xmp.drone-dji.FlightYawDegree"]
        return float(yaw_degrees)


def extract_raw_exif(fpath: str) -> Exif:
    try:
        with Image.open(fpath) as f:  # Ensure file closing
            img = f
    except IsADirectoryError:
        print(f"Could not open the following image: {fpath}")
    else:
        return img.getexif()


def get_geo_info_from_exif(raw_exif: Exif) -> dict:
    """
    Extracts the gps info from raw exif data and returns a dictionary
    :param raw_exif:
    :return:
    """
    geo_readable = extract_readable_geoinfo(raw_exif)
    geo_out = {"crs": "NONE",
               "hemisphere_N_S": geo_readable["GPSLatitudeRef"],
               "hemisphere_E_W": geo_readable["GPSLongitudeRef"],
               "latitude": dms_to_dd(geo_readable["GPSLatitude"]),
               "longitude": dms_to_dd(geo_readable["GPSLongitude"])}
    logging.info(geo_out)
    return geo_out


def extract_readable_geoinfo(raw_exif):
    for key, value in TAGS.items():
        if value == "GPSInfo":
            break
    gps_info = raw_exif.get_ifd(key)
    geo_readable = {GPSTAGS.get(key, key): value for key, value in gps_info.items()}
    return geo_readable


def print_exif_data(fpath):
    raw_exif = extract_raw_exif(fpath)
    for tag_no, name in TAGS.items():
        info_package = raw_exif.get_ifd(tag_no)
        package_contents = {GPSTAGS.get(tag_no, tag_no): value for key, value in info_package.items()}
        print(f"{tag_no}\t{name}\t{package_contents}")


def transform_to_positive_degrees(raw_degree):
    """Transforms a degree value that can be negative or above 360 into a degree value between of (0<= value < 360)"""
    sign = 1
    if raw_degree < 0:
        raw_degree = 360 - abs(raw_degree) % 360
        sign *= -1
    actual = raw_degree % 360
    return actual


def trigonometry_angle_from_adjacent_and_opposite(adjacent, opposite) -> float:
    """
    Returns the angle between adjacent and hypotenuse of a right triangle (in degrees).
    :param adjacent: length of adjacent edge
    :param opposite: length of opposite edge
    :return: angle in degrees (btw. hypotenuse and adjacent edge).
    """
    angle = math.degrees(math.atan(opposite / adjacent))
    return angle


def geolocate_point_deprecated(pixel_xy: Tuple[int, int],
                    img_dims_wh: Tuple[int, int],
                    img_lat_lon: Tuple[float, float],
                    gsd_cm: float, drone_yaw_deg: float) -> Tuple[float, float]:
    """
    Calculates the latitude/longitude of a given point on an image.
    :param pixel_xy: point location in image.
    :param img_dims_wh: Image width and height in pixels.
    :param img_lat_lon: Img. latitude and longitude in decimal degrees.
    :param gsd_cm: Ground sampling distance (cm).
    :param drone_yaw_deg: drone rotation in degrees. Straight north = 0.
    :return: (latitude, longitude) in decimal degrees (WGS84).
    """
    px_x, px_y = pixel_xy
    img_width, img_height = img_dims_wh
    img_latitude, img_longitude = img_lat_lon

    img_center_x = int(img_width * 0.5)
    img_center_y = int(img_height * 0.5)

    delta_x = px_x - img_center_x
    delta_y = px_y - img_center_y

    delta_lat, delta_lon = calc_latlong_shift_from_px_shift(px_offset_yx=(delta_y, delta_x),
                                                             gsd_cm=gsd_cm,
                                                             yaw_angle_deg=drone_yaw_deg)
    point_lat = img_latitude + delta_lat
    point_lon = img_longitude + delta_lon

    return point_lat, point_lon


def geolocate_point(pixel_xy: Tuple[int, int],
                    img_dims_wh: Tuple[int, int],
                    img_lat_lon: Tuple[float, float],
                    gsd_cm: float, drone_yaw_deg: float) -> Tuple[float, float]:
    """
    Calculates the latitude/longitude of a given point on an image.
    :param pixel_xy: point location in image.
    :param img_dims_wh: Image width and height in pixels.
    :param img_lat_lon: Img. latitude and longitude in decimal degrees.
    :param gsd_cm: Ground sampling distance (cm).
    :param drone_yaw_deg: drone rotation in degrees. Straight north = 0.
    :return: (latitude, longitude) in decimal degrees (WGS84).
    """
    px_x, px_y = pixel_xy
    img_width, img_height = img_dims_wh
    img_latitude, img_longitude = img_lat_lon

    img_center_x = int(img_width * 0.5)
    img_center_y = int(img_height * 0.5)

    delta_x = px_x - img_center_x
    delta_y = px_y - img_center_y

    delta_lat, delta_lon = calc_latlong_shift_from_px_shift(px_offset_yx=(delta_y, delta_x),
                                                            gsd_cm=gsd_cm,
                                                            yaw_angle_deg=drone_yaw_deg)
    point_lat = img_latitude + delta_lat
    point_lon = img_longitude + delta_lon

    return point_lat, point_lon


def point_picker(img_fpath: str) -> Tuple[int, int]:
    """
    Lets the user pick a point on the image using the mouse and returns the x and y coordinates as a tuplle
    :param img_fpath:
    :return: (x, y)
    """
    img = plt.imread(img_fpath)
    plt.imshow(img)
    point_coords = plt.ginput(1)[0]
    point_coords = int(point_coords[0]), int(point_coords[1])
    print(f"Picked x,y coordinates: {point_coords}")
    return point_coords


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s]\t%(message)s")
    # print(calc_latlong_shift_from_px_shift(px_offset_yx=(111_139_00, 111_139_00), gsd_cm=1))
    # print(calc_latlong_shift_from_px_shift(px_offset_yx=(-111_139_00, 111_139_00), gsd_cm=1))

    # Test 1
    gsd = 10
    drone_yaw = 0
    img_dims_wh = (520_000, 400_000)
    pt_xy = (515_520, 380_120)
    img_lat_long = (35.98188, 14.33238)
    point_coordinates = geolocate_point_deprecated(pt_xy, img_dims_wh, img_lat_long, gsd, drone_yaw)
    # print(point_coordinates)

    # Test 2
    gsd = 10
    drone_yaw = 35.18060113378763
    img_dims_wh = (800_000, 400_000)
    pt_xy = (400_000 + 312_624, 200_000)
    img_lat_long = (35.98188, 14.33238)
    point_coordinates = geolocate_point_deprecated(pt_xy, img_dims_wh, img_lat_long, gsd, drone_yaw)
    # print(point_coordinates)

    # Test w/ GCP
    fpath_img_500 = "/media/findux/DATA/Documents/Malta_II/surveys/2021-12-16_paradise_bay_5m/RGB images and video/DJI_0500.JPG"
    fpath_img_504 = "/media/findux/DATA/Documents/Malta_II/surveys/2021-12-16_paradise_bay_5m/RGB images and video/DJI_0504.JPG"
    gcp_49_504 = (794, 3031)
    gcp_49_500 = (2892, 3185)

    latitudes = []
    longitudes = []
    imgs = []
    altitudes = []

    for i in range(11):
        # 500
        img_dims = Image.open(fpath_img_500).size
        yaw_angle = extract_uav_yaw(fpath_img_500)
        img_coords_latlon = extract_coordinates_from_img(fpath_img_500)
        gsd = calc_gsd(i)
        calc_lat, calc_lon = geolocate_point(gcp_49_500, img_dims_wh, img_lat_long, gsd, yaw_angle)


def geolocate_point(pixel_xy: Tuple[int, int],
                    fpath_img: str, altitude_m: Union[float, int],
                    focal_length_mm=8.6, sensor_width_mm=12.8333) -> Tuple[float, float]:
    """
    Calculates the latitude/longitude of a given point on an image.
    :param pixel_xy: point location in image.
    :param img_dims_wh: Image width and height in pixels.
    :param img_lat_lon: Img. latitude and longitude in decimal degrees.
    :param gsd_cm: Ground sampling distance (cm).
    :param drone_yaw_deg: drone rotation in degrees. Straight north = 0.
    :return: (latitude, longitude) in decimal degrees (WGS84).
    """
    px_x, px_y = pixel_xy
    img_width, img_height = Image.open(fpath_img).size
    img_latitude, img_longitude = extract_coordinates_from_img(fpath_img)
    drone_yaw_deg = extract_uav_yaw(fpath_img)
    gsd_cm = calc_gsd(altitude_m, focal_length_mm, sensor_width_mm, img_width, img_height)

    img_center_x = int(img_width * 0.5)
    img_center_y = int(img_height * 0.5)

    delta_x = px_x - img_center_x
    delta_y = px_y - img_center_y

    delta_lat, delta_lon = calc_latlong_shift_from_px_shift(px_offset_yx=(delta_y, delta_x),
                                                             gsd_cm=gsd_cm,
                                                             yaw_angle_deg=drone_yaw_deg)
    point_lat = img_latitude + delta_lat
    point_lon = img_longitude + delta_lon

    return point_lat, point_lon


def point_picker(img_fpath: str) -> Tuple[int, int]:
    """
    Lets the user pick a point on the image using the mouse and returns the x and y coordinates as a tuplle
    :param img_fpath:
    :return: (x, y)
    """
    img = plt.imread(img_fpath)
    plt.imshow(img)
    point_coords = plt.ginput(1)[0]
    point_coords = int(point_coords[0]), int(point_coords[1])
    print(f"Picked x,y coordinates: {point_coords}")
    return point_coords


if __name__=="__main__":
    # logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s]\t%(message)s")
    # print(calc_latlong_shift_from_px_shift(px_offset_yx=(111_139_00, 111_139_00), gsd_cm=1))
    # print(calc_latlong_shift_from_px_shift(px_offset_yx=(-111_139_00, 111_139_00), gsd_cm=1))

    # Test 1
    gsd = 10
    drone_yaw = 0
    img_dims_wh = (520_000, 400_000)
    pt_xy = (515_520, 380_120)
    img_lat_long = (35.98188, 14.33238)
    point_coordinates = geolocate_point_deprecated(pt_xy, img_dims_wh, img_lat_long, gsd, drone_yaw)
    # print(point_coordinates)

    # Test 2
    gsd = 10
    drone_yaw = 35.18060113378763
    img_dims_wh = (800_000, 400_000)
    pt_xy = (400_000 + 312_624, 200_000)
    img_lat_long = (35.98188, 14.33238)
    point_coordinates = geolocate_point_deprecated(pt_xy, img_dims_wh, img_lat_long, gsd, drone_yaw)
    # print(point_coordinates)

    # Test w/ GCP
    fpath_img_500 = "/media/findux/DATA/Documents/Malta_II/surveys/2021-12-16_paradise_bay_5m/RGB images and video/DJI_0500.JPG"
    fpath_img_504 = "/media/findux/DATA/Documents/Malta_II/surveys/2021-12-16_paradise_bay_5m/RGB images and video/DJI_0504.JPG"
    fpath_img_637 = "/media/findux/DATA/Documents/Malta_II/surveys/2021-12-16_paradise_bay_5m/RGB images and video/DJI_0637.JPG"
    gcp_49_504 = (794, 3031)
    gcp_49_500 = (2892, 3185)
    gcp_49_637 = (1678, 856)

    lats, lons, source, altitudes = [], [], [], []
    # for i in range(11):
    #     gcp_500 = geolocate_point(gcp_49_500, fpath_img_500, i)
    #     lats.append(gcp_500[0])
    #     lons.append(gcp_500[1])
    #     source.append(500)
    #     altitudes.append(i)
    #     gcp_504 = geolocate_point(gcp_49_504, fpath_img_504, i)
    #     lats.append(gcp_504[0])
    #     lons.append(gcp_504[1])
    #     source.append(504)
    #     altitudes.append(i)
    altitude = 5
    gcp_500 = geolocate_point(gcp_49_500, fpath_img_500, altitude)
    lats.append(gcp_500[0])
    lons.append(gcp_500[1])
    source.append(500)
    altitudes.append(altitude)
    gcp_504 = geolocate_point(gcp_49_504, fpath_img_504, altitude)
    lats.append(gcp_504[0])
    lons.append(gcp_504[1])
    source.append(504)
    altitudes.append(altitude)
    gcp_637 = geolocate_point(gcp_49_637, fpath_img_637, altitude)
    lats.append(gcp_637[0])
    lons.append(gcp_637[1])
    source.append(637)
    altitudes.append(altitude)


    data = pd.DataFrame({"latitude": lats, "longitude": lons, "altitude": altitudes, "source": source})
    data.to_csv("/home/findux/Desktop/GCP_calculation_results.csv", index=False)

