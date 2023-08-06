import enum
import io
import logging
import time
from typing import List

import requests
from PIL import Image
from masksdk.mask import blurring, pixelating, blackening
from requests import RequestException

logger = logging.getLogger('masksdk')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class ModelName(enum.IntEnum):
    face_ai = 0
    plate_ai = 1


class MaskName(enum.IntEnum):
    blur = 0
    pixel = 1
    black = 2


def _infer_one_image(infer_host, img_rb, model_name):
    try:
        files = {"input_data": img_rb}
        uri = '{}/models/{}/predict'.format(infer_host, model_name)
        start_time = time.time()
        resp = requests.post(url=uri, files=files, timeout=10)
        if resp.status_code == requests.codes["ok"] and len(resp.content) > 0:
            logger.debug("infer with resp_len {} total time: {:.4f}s".format(len(resp.content), time.time() - start_time))
            return resp.json()
        elif resp.status_code >= requests.codes["bad"]:
            raise RequestException('infer request error_code={}, infer_host={}, model_name={}'.format(resp.status_code, infer_host, model_name))
        else:
            logger.warning('failed to get mask with error={}'.format(resp.content))
        return {}

    except RequestException as error:
        logger.error(error)
        raise

    except Exception as error:
        logger.error('error to get mask error={}'.format(str(error)))
        return {}


def _parse_infer_response_box(response, down_sampling_ratio, pixel_gap):
    boxes = []
    for bbox in response['data']['bounding-boxes']:
        box = dict()
        coord = bbox['coordinates']
        score = bbox.get('confidence', -1)
        class_name = bbox['ObjectClassName']
        box['score'] = score
        box['class_name'] = class_name

        # pixel gap check
        if coord['right'] - coord['left'] < pixel_gap:
            continue
        if coord['bottom'] - coord['top'] < pixel_gap:
            continue

        # convert
        box['x_min'] = int(coord['left'] / down_sampling_ratio)
        box['y_min'] = int(coord['top'] / down_sampling_ratio)
        box['x_max'] = int(coord['right'] / down_sampling_ratio)
        box['y_max'] = int(coord['bottom'] / down_sampling_ratio)
        boxes.append(box)
    return boxes


def mask_one_image(infer_host, image_file, model_names: List[ModelName], mask_name: MaskName, degree: float, down_sampling_ratio: float = 1, pixel_gap: int = 10):
    """mask an image with specific parameters

    :param infer_host: infer server address [ip:port]
    :param image_file: the absolute image file
    :param model_names: use which mode to infer
    :param mask_name: use which mask technology to mask
    :param degree: the mask degree, 1 is most
    :param down_sampling_ratio: down sampling the infer input image, but won't affect the final mask image size, 1 is most
    :param pixel_gap: skip the bbox if the gap between max axis and min axis is less than it
    :return: image with mask
    """

    # checker
    if not 0 < degree <= 1:
        raise NotImplementedError('not support this degree={}'.format(degree))
    if not 0 < down_sampling_ratio <= 1:
        raise NotImplementedError('not support this down_sampling_ratio={}'.format(down_sampling_ratio))

    # load image
    with Image.open(image_file) as img:
        img_ds = img
        if down_sampling_ratio < 1:
            width, height = img.size
            w, h = int(width * down_sampling_ratio), int(height * down_sampling_ratio)
            img_ds = img.resize((w, h))

        # open image in bytes
        with io.BytesIO() as output:
            img_ds.save(output, format="JPEG")
            img_rb = output.getvalue()

        # start to infer via server
        bboxes = []
        for one_model_name in model_names:
            if one_model_name not in [ModelName.face_ai, ModelName.plate_ai]:
                raise NotImplementedError('not support this model={}'.format(one_model_name))
            infer_resp = _infer_one_image(infer_host, img_rb, ModelName(one_model_name).name)
            if infer_resp.get('data'):
                one_boxes = _parse_infer_response_box(infer_resp, down_sampling_ratio, pixel_gap)
                bboxes += one_boxes

        # select mask tech
        if mask_name == MaskName.blur:
            func = blurring
        elif mask_name == MaskName.pixel:
            func = pixelating
        elif mask_name == MaskName.black:
            func = blackening
        else:
            raise NotImplementedError('not support this mask tech={}'.format(mask_name))

        # start to mask image locally
        start_time = time.time()
        mask_img = func(img, bboxes, degree)
        logger.debug("pure mask with bboxes size {} total time: {:.4f}s".format(len(bboxes), time.time() - start_time))

        return mask_img
