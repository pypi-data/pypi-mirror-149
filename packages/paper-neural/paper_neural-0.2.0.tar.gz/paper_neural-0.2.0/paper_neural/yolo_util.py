import torch

def get_model_yolo_fibers(path):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path)
    model.max_det = 25
    model.training = False
    model.conf = 0.70
    model.iou = 0.45
    model.crop = False
    model.visualize = False
    print(model)
    return model