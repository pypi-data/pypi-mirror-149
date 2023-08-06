from PIL import Image
import numpy as np
import torch
from torchvision import transforms

from paper_neural.siamese_util import get_model_siamese_discriminator, match_fibers

class PaperSiamese:

    def __init__(self,path_siamese, device):
        self.device = device
        self.paper_discriminator_model = get_model_siamese_discriminator(path_siamese).to(device)

    '''
    Compara a features das fibras de dois documentos
    '''
    def matches(self, list_a,list_b):
            size_a = list_a.shape[0]
            size_b = list_b.shape[0]
            # define mapa de distancia
            distances = np.ones(shape=(size_a, size_b))
            # para cada fibra de A procura entre todas as fibras de B
            for i in range(size_a):
                item_repeat = list_a[i].unsqueeze(0).repeat(size_b, 1)  # repito um item size_b vezes
                desc_a = self.paper_discriminator_model(item_repeat, list_b)
                desc_a = desc_a.cpu().detach().numpy()[:, 0]  # tensor para numpy
                # atualiza a distancia de uma fibra de A para todas as fibras de B
                distances[i] = desc_a
            # com base no mapa de distância calcula a correspondencia entre as fibras
            matches = match_fibers(distances, max_distance=0.50)
            return matches


if __name__ == '__main__':
    from definitions import MODEL_YOLO_PATH, MODEL_SIAMESE_PATH

    device = torch.device('cuda') if torch.cuda.is_available else torch.device('cpu')
    paper_yolo_siamese = PaperSiamese(MODEL_SIAMESE_PATH, device)
    list_a = np.zeros(shape=(3,128)).astype(np.float32)
    list_a = torch.tensor(list_a).to(device)
    matchs = paper_yolo_siamese.matches_documents(list_a,list_a)
    print(matchs)
