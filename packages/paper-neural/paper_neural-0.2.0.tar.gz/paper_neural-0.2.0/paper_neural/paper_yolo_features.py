from PIL import Image
import numpy as np
import torch
from torchvision import transforms

from paper_neural.siamese_util import get_model_siamese_feature
from paper_neural.yolo_util import get_model_yolo_fibers

preprocess = transforms.Compose([
    transforms.Resize(64),
    transforms.CenterCrop(60),
    transforms.ToTensor()
])


class PaperYoSiam:

    def __init__(self, path_yolo, path_feature, device):
        self.device = device
        self.paper_model_yolo = get_model_yolo_fibers(path_yolo).to(device)
        self.paper_feature_model = get_model_siamese_feature(path_feature).to(device)


    def get_features(self,crops):
        # TODO mock features with neural network
        boxs = []
        points = []

        fibras = [crop['im'][:, :, ::-1] for crop in crops]
        # padroniza a entrada semelhante ao treinamento
        imgs_pil = [Image.fromarray(img) for img in fibras]  # numpy to PIL
        imgs_pre = [preprocess(img).to(self.device).unsqueeze(0) for img in imgs_pil]  # aplica transform
        imgs_pre = torch.cat(imgs_pre)  # (list of tensor) in tensor

        for idx, crop in enumerate(crops):
            box = np.array([item.cpu().detach().numpy() for item in crop['box']])
            boxs.append(box)
            point = [(box[0] + box[2]) / 2, (box[1] + box[3]) / 2]
            points.append(point)

        # descreve cada fibra com rede siamesa
        with torch.no_grad():
            features = self.paper_feature_model(imgs_pre)

        features = features.cpu().detach().numpy()
        boxs = np.array(boxs)
        points = np.array(points)
        return {'features': features, 'boxs': boxs, 'points': points}

    def detect(self, img: np.ndarray or Image):
        results = self.paper_model_yolo(img, size=640)  # reduce size=320 for faster inference
        crops = results.crop(save=False)
        desc_dict = None
        if crops:
            desc_dict = self.get_features(crops)
        return desc_dict


if __name__ == '__main__':
    from definitions import MODEL_YOLO_PATH, MODEL_SIAMESE_PATH

    device = torch.device('cuda') if torch.cuda.is_available else torch.device('cpu')
    paper_yolo_siamese = PaperYoSiam(MODEL_YOLO_PATH,MODEL_SIAMESE_PATH,device)
    paper_yolo_siamese.detect(np.zeros(shape=(120, 120, 3)))
