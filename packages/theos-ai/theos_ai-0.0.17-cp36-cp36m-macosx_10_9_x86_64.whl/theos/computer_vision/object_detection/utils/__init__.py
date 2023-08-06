from theos.__internal.utils.system import get_os_name
from theos.__internal.data import config
from theos.__internal.utils import log
from theos.__internal.utils.io import info as io_info
from theos.__internal.utils.io import operations as io_operations
from theos.__internal.utils import system
from theos.computer_vision import exceptions as computer_vision_exceptions
from theos.__internal.utils import http
from theos.__internal.connectors import config as connectors_config
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import threading
import requests
import time
import math
import cv2
import sys
import json
import asyncio
import httpx
from PIL import Image as PILImage
import tempfile


def draw_border(image, top_left_point, bottom_right_point, color, thickness, radius=5, length=5):
    x1, y1 = top_left_point
    x2, y2 = bottom_right_point
    res_scale = (image.shape[0] + image.shape[1])/2000
    radius = int(radius * res_scale)
 
    # Top left
    cv2.line(image, (x1 + radius, y1), (x2 - radius - length, y1), color, thickness, cv2.LINE_AA)
    cv2.line(image, (x1, y1 + radius), (x1, y2 - radius - length), color, thickness, cv2.LINE_AA)
    cv2.ellipse(image, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness, cv2.LINE_AA)
 
    # Top right
    cv2.line(image, (x2 - radius, y1), (x1 + radius + length, y1), color, thickness, cv2.LINE_AA)
    cv2.line(image, (x2, y1 + radius), (x2, y2 - radius - length), color, thickness, cv2.LINE_AA)
    cv2.ellipse(image, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness, cv2.LINE_AA)
 
    # Bottom left
    cv2.line(image, (x1 + radius, y2), (x2 - radius - length, y2), color, thickness, cv2.LINE_AA)
    cv2.line(image, (x1, y2 - radius), (x1, y1 + radius + length), color, thickness, cv2.LINE_AA)
    cv2.ellipse(image, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness, cv2.LINE_AA)
 
    # Bottom right
    cv2.line(image, (x2 - radius, y2), (x1 + radius + length, y2), color, thickness, cv2.LINE_AA)
    cv2.line(image, (x2, y2 - radius), (x2, y1 + radius + length), color, thickness, cv2.LINE_AA)
    cv2.ellipse(image, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness, cv2.LINE_AA)

def plot_box(image, top_left_point, bottom_right_point, width, height, label, color=(210,240,0), padding=6, font_scale=0.375, alpha=0.15):
    label = label.title()
    if alpha > 1:
        alpha = 1
    if alpha > 0:
        box_crop = image[top_left_point['y']:top_left_point['y']+height, top_left_point['x']:top_left_point['x']+width]
        colored_rect = np.ones(box_crop.shape, dtype=np.uint8)
        colored_rect[:,:,0] = color[0] - 90 if color[0] - 90 >= 0 else 0
        colored_rect[:,:,1] = color[1] - 90 if color[1] - 90 >= 0 else 0
        colored_rect[:,:,2] = color[2] - 90 if color[2] - 90 >= 0 else 0
        box_crop_weighted = cv2.addWeighted(box_crop, 1 - alpha, colored_rect, alpha, 1.0)
        image[top_left_point['y']:top_left_point['y']+height, top_left_point['x']:top_left_point['x']+width] = box_crop_weighted

    draw_border(image, (top_left_point['x'] - 1, top_left_point['y']), (bottom_right_point['x'], bottom_right_point['y']), color, thickness=1, radius=5, length=5)
    res_scale = (image.shape[0] + image.shape[1])/1600
    font_scale = font_scale * res_scale
    font_width, font_height = 0, 0
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(label, font_face, fontScale=font_scale, thickness=1)[0]

    if text_size[0] > font_width:
        font_width = text_size[0]
    if text_size[1] > font_height:
        font_height = text_size[1]
    if top_left_point['x'] - 1 < 0:
        top_left_point['x'] = 1
    if top_left_point['x'] + font_width + padding*2 > image.shape[1]:
        top_left_point['x'] = image.shape[1] - font_width - padding*2
    if top_left_point['y'] - font_height - padding*2  < 0:
        top_left_point['y'] = font_height + padding*2
    
    p3 = top_left_point['x'] + font_width + padding*2, top_left_point['y'] - font_height - padding*2
    cv2.rectangle(image, (top_left_point['x'] - 1, top_left_point['y']), p3, color, -1, lineType=cv2.LINE_AA)
    x = top_left_point['x'] + padding
    y = top_left_point['y'] - padding
    cv2.putText(image, label, (x, y), font_face, font_scale, [0, 0, 0], thickness=1, lineType=cv2.LINE_AA)
    return image

def draw(image, detections, classes=None, alpha=0.15):
    image_copy = image.copy()
    for box in detections:
        draw_box = False
        class_name = box['class_name']
        conf = box['confidence']
        label = class_name + ' ' + str(int(conf*100)) + '%'
        width = box['width']
        height = box['height']
        if (classes is None) or (classes is not None and class_name in classes):
            draw_box = True
        if draw_box:
            image_copy = plot_box(image_copy, box['top_left_point'], box['bottom_right_point'], width, height, label, alpha=alpha)
    return image_copy

def show_frame(frame):
    cv2.imshow('Theos', frame)
    cv2.waitKey(10)

def save_frame(frame, path):
    cv2.imwrite(system.join_paths(config.outputs_folder_path, path), frame)


class URLImage:
    def __init__(self, url):
        self.url = url
        self.filename = system.get_filename_from_url(url)
        self.path = self.filename
        self.full_path = system.join_paths(config.inputs_folder_path, self.filename)
        
    async def download(self, retry=False):
        if io_info.file_exists(self.full_path):
            io_operations.remove_file(self.full_path)
        log.info(f'downloading image {self.filename}:')
        await http.download_file_from_url(self.url, self.full_path, retry=retry)

    async def load(self):
        return cv2.imread(self.full_path)

    def delete(self):
        system.delete_file(self.full_path)


class Image:
    def __init__(self, path):
        self.path = path
        self.host_path = system.join_paths(config.inputs_folder_path, path)

        if not io_info.file_exists(self.host_path):
            error = f'file {self.host_path} not found.'
            log.error(error)
            raise computer_vision_exceptions.ImageNotFound(error)

        self.image = cv2.imread(self.host_path)
        self.raw = self.image.copy()
        self.width = self.raw.shape[1]
        self.height = self.raw.shape[0]

    def draw(self, detections, alpha=0.15):
        self.image = draw(self.raw, detections, alpha=alpha)

    def erase(self):
        self.image = self.raw.copy()

    def show(self, detections=None):
        if detections is not None:
            self.draw(detections)
        img_extension = io_info.get_file_extension(self.host_path)
        temp_img_name = next(tempfile._get_candidate_names())
        full_img_name = f'{temp_img_name}{img_extension}'
        img_path = system.join_paths(config.outputs_folder_path, full_img_name)
        cv2.imwrite(img_path, self.image)
        im = PILImage.open(img_path)
        im.show()
        io_operations.remove_file(img_path)

    def save(self, path):
        cv2.imwrite(system.join_paths(config.outputs_folder_path, path), self.image)
        log.info(f'{path} saved succesfully')


class Video:
    def __init__(self, path):
        self.path = path
        self.host_path = system.join_paths(config.inputs_folder_path, path)
       
        if not io_info.file_exists(self.host_path):
            error = f'file {self.host_path} not found.'
            log.error(error)
            raise computer_vision_exceptions.VideoNotFound(error)

        self.video = cv2.VideoCapture(self.host_path)
        self.width  = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.video.get(cv2.CAP_PROP_FPS))
        self.save = False
        self.cache = []
        self.video_ended = False
        self.show_progress = False
        self.draw_update_time = 0
        self.frame_number = 1
        self.frames_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.callback = None
        self.drawing_thread = threading.Thread(target=self.draw_from_cache, daemon=True)

    def start(self, field_name, subfield_name, algorithm_name, output_path, show_progress, alpha):
        self.drawing_alpha = alpha
        self.field_name = field_name
        self.subfield_name = subfield_name
        self.algorithm_name = algorithm_name
        self.output_path = output_path
        self.frames_since_last_tracking = 0
        self.tracking_interval = 1
        self.last_tracking_time = time.time()

        if output_path is not None:
            self.save = True
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            self.output = cv2.VideoWriter(system.join_paths(config.outputs_folder_path, output_path), fourcc, self.fps, (self.width, self.height))
        
        self.show_progress = show_progress

        if self.show_progress:
            print()
            ascii_bar = True if get_os_name() == 'Windows' else False
            self.pbar = tqdm(total=self.frames_count, ascii=ascii_bar, unit=' frames', dynamic_ncols=True, file=sys.stdout)
        
        self.drawing_thread.start()

    def set_callback(self, callback):
        self.callback = callback

    def __reload_video(self):
        self.video = cv2.VideoCapture(self.host_path)
        self.width  = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = math.ceil(self.video.get(cv2.CAP_PROP_FPS))
        self.save = False
        self.cache = []
        self.video_ended = False
        self.show_progress = False
        self.draw_update_time = 0
        self.frame_number = 1
        self.frames_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.callback = None
        del self.drawing_thread
        self.drawing_thread = threading.Thread(target=self.draw_from_cache, daemon=True)

    def abort(self):
        self.video_ended = True
        if self.show_progress:
            self.pbar.close()
            print()
        if self.drawing_thread.is_alive():
            self.drawing_thread.join()
        if self.save:
            self.output.release()
        self.video.release()
        self.__reload_video()
        
    def close(self):
        self.video_ended = True
        if self.show_progress:
            self.pbar.update(self.frames_count - self.pbar.n)
            self.pbar.close()
            print()
        if self.drawing_thread.is_alive():
            self.drawing_thread.join()
        if self.save:
            self.output.release()
        self.video.release()
        self.__reload_video()

    def draw_from_cache(self):
        while not self.video_ended or len(self.cache) > 0:
            if len(self.cache) > 0:
                detections = self.cache.pop(0)
                if self.video.isOpened():
                    ok, frame = self.video.read()
                    if ok:
                        detected_frame = draw(frame, detections, alpha=self.drawing_alpha)
                        if self.callback is not None:
                            self.callback(frame, detected_frame, detections, self.frame_number, self.frames_count)
                        if self.save:
                            self.output.write(detected_frame)
                        if self.show_progress:
                            self.pbar.update(1)
                    self.frame_number += 1
                    self.frames_since_last_tracking += 1
                time_since_last_tracking = time.time() - self.last_tracking_time
                if time_since_last_tracking >= self.tracking_interval:
                    self.last_tracking_time = time.time()
                    self.frames_since_last_tracking = 0

    def draw(self, detections):
        self.cache.append(detections)

    def process(self, detections, alpha, draw_detections=False):
        result = {}
        if self.video.isOpened():
            ok, frame = self.video.read()
            if ok:
                result['frame'] = frame
                if draw_detections:
                    detected_frame = draw(frame, detections, alpha=alpha)
                    result['detected_frame'] = detected_frame
                result['detections'] = detections
                result['frame_number'] = self.frame_number
                result['frames_count'] = self.frames_count
            self.frame_number += 1
        return result


class ObjectDetectionWebsocketLogger:
    def __init__(self, sio):
        self.sio = sio
    
    def info(self, message):
        self.sio.emit('new_info', message)

    def detected(self, detections):
        self.sio.emit('detected', detections)

    def metrics(self, data):
        self.sio.emit('new_metrics', data)

    def finished_training(self):
        self.sio.emit('finished_training')

    def video_loaded(self):
        self.sio.emit('video_loaded')

    def video_ended(self):
        self.sio.emit('video_ended')

    def error(self, message):
        self.sio.emit('error_ocurred', message)


class ObjectDetectionLogger:
    def __init__(self, create_task, user_auth_token, project_id, training_session_key, experiment_id, max_parallel_bytes=5*1e8):
        self.create_task = create_task
        self.user_auth_token = user_auth_token
        self.project_id = project_id
        self.training_session_key = training_session_key
        self.experiment_id = experiment_id
        self.max_parallel_bytes = max_parallel_bytes
        self.buffer = []
        self.weights_buffer = []
        self.weights_paths_to_remove = []
        self.uploading_weights = True
        self.create_task(self.__upload_weights())
    
    def metrics(self, data):
        self.buffer.append(data)

    def weights(self, weights_path, metrics, types=['last']):
        if len(self.weights_buffer) > 0:
            if 'best' in types:
                for weight in self.weights_buffer:
                    self.weights_paths_to_remove.append(weight['path'])
                self.weights_buffer = []
            else:
                new_weights = []
                for weight in self.weights_buffer:
                    if 'best' in weight['types']:
                        weight['types'] = ['best']
                        new_weights.append(weight)
                    else:
                        self.weights_paths_to_remove.append(weight['path'])
                self.weights_buffer = new_weights
        weights_folder_path = io_info.get_path_folder(weights_path)
        x_name = metrics['x']['name']
        x_value = metrics['x']['value']
        temp_weights_path = system.join_paths(weights_folder_path, f'{x_name}{x_value}.weights')
        io_operations.copy_file(weights_path, temp_weights_path)
        self.weights_buffer.append({
            'path':temp_weights_path,
            'metrics':metrics,
            'types':types
        })

    async def __upload_weights(self):
        weights_uploaded = False
        max_tries = 1000
        httpx_client = httpx.AsyncClient()

        async def upload_weight_part(part_number, part_url, data):
            tries = 0
            ok = False
            while not ok and tries < max_tries:
                try:
                    response = await httpx_client.put(part_url, content=data, headers={'Content-Type': 'application/octet-stream'}, timeout=300)
                    ok = True
                except:
                    tries += 1
                    log.error('weights upload part error. Trying again...')
                    await asyncio.sleep(1)
            uploaded_part = {
                'PartNumber':part_number,
                'ETag':response.headers['ETag'].replace('"', '')
            }
            return uploaded_part

        while self.uploading_weights or len(self.weights_buffer) > 0:
            for path in self.weights_paths_to_remove:
                try:
                    io_operations.remove_file(path)
                except:
                    log.error(f'couldn\'t remove temporal weight file: {path}')
            
            self.weights_paths_to_remove = []
            
            if len(self.weights_buffer) > 0:
                weight = self.weights_buffer.pop(0)
                file_size = io_info.get_file_size(weight['path'])
                weight_upload_data = {}
                chunk_size = None
                part_count = 0
                parts_requests = {}
                parts_uploaded = {}
                
                for weight_type in weight['types']:
                    data = {'type':weight_type, 'file_size':file_size, 'metrics':json.dumps(weight['metrics'])}
                    headers = {'Authorization': f'Token {self.user_auth_token}'}
                    ok = False
                    tries = 0
                    while not ok and tries < max_tries:
                        try:
                            response = await httpx_client.post(f'{connectors_config.API_BASE_URL}/projects/{self.project_id}/training/sessions/{self.training_session_key}/experiments/{self.experiment_id}/weight/upload/start/', headers=headers, data=data, timeout=300)
                            ok = True
                            response_json = response.json()
                            if response_json['can_upload']:
                                upload_manifest = response_json['manifest']
                                chunk_size = upload_manifest['chunk_size']
                                part_count = len(upload_manifest['parts'])
                                weight_upload_data[weight_type] = {
                                    'can_upload':True,
                                    'upload_path':upload_manifest['upload_path'],
                                    'upload_id':upload_manifest['upload_id'],
                                    'parts':upload_manifest['parts']
                                }
                                parts_requests[weight_type] = []
                                parts_uploaded[weight_type] = []
                            else:
                                weight_upload_data[weight_type] = {'can_upload': False}
                        except:
                            tries += 1
                            log.error('weights upload start error. Trying again...')
                            await asyncio.sleep(1)

                try:
                    with open(weight['path'], 'rb') as f:
                        i = 0
                        for data in io_operations.read_file_in_chunks(f, chunk_size):
                            for weight_type in weight['types']:
                                if weight_upload_data[weight_type]['can_upload']:
                                    upload_path = weight_upload_data[weight_type]['upload_path']
                                    part = weight_upload_data[weight_type]['parts'][i]
                                    part_number = part['number']
                                    part_url = part['url']
                                    parts_requests[weight_type].append(upload_weight_part(part_number, part_url, data))
                                    if len(parts_requests[weight_type])*chunk_size >= self.max_parallel_bytes:
                                        parts_responses = await asyncio.gather(*parts_requests[weight_type])
                                        parts_requests[weight_type] = []
                                        for part_response in parts_responses:
                                            parts_uploaded[weight_type].append(part_response)
                            i += 1

                        for weight_type in weight['types']:
                            if weight_upload_data[weight_type]['can_upload']:
                                if len(parts_requests[weight_type]) > 0:
                                    parts_responses = await asyncio.gather(*parts_requests[weight_type])
                                    parts_requests[weight_type] = []
                                    for part_response in parts_responses:
                                        parts_uploaded[weight_type].append(part_response)
                                upload_path = weight_upload_data[weight_type]['upload_path']
                                upload_id = weight_upload_data[weight_type]['upload_id']
                                weight_parts_uploaded = parts_uploaded[weight_type]
                                weight_parts_uploaded = sorted(weight_parts_uploaded, key=lambda x:x['PartNumber'])
                                data = {'type':weight_type, 'upload_path':upload_path, 'upload_id':upload_id, 'parts':json.dumps(weight_parts_uploaded), 'metrics':json.dumps(weight['metrics'])}
                                ok = False
                                tries = 0
                                while not ok and tries < max_tries:
                                    try:
                                        response = await httpx_client.post(f'{connectors_config.API_BASE_URL}/projects/{self.project_id}/training/sessions/{self.training_session_key}/experiments/{self.experiment_id}/weight/upload/end/', headers=headers, data=data, timeout=300)
                                        ok = True
                                    except:
                                        tries += 1
                                        log.error('weights upload end error. Trying again...')
                                        await asyncio.sleep(1)
                                weights_uploaded = True
                    
                    io_operations.remove_file(weight['path'])
                except FileNotFoundError:
                    weight_path = weight['path']
                    log.error(f'weight file not found: {weight_path}')

            await asyncio.sleep(1)

        await httpx_client.aclose()
        if weights_uploaded:
            log.info('weights uploaded successfully')
    
    def close(self):
        self.uploading_weights = False