import time

import matplotlib
import numpy as np
import torch
from matplotlib import pyplot as plt
from torch import optim, nn
from torchvision import transforms
from definitions import MODEL_SIAMESE_PATH
from siamese.fibers_siamese import FibersSiamese


def match_fibers(distances,cross_check =True,max_distance= np.inf):
    indices1 = np.arange(distances.shape[0])
    indices2 = np.argmin(distances, axis=1)
    if cross_check:
        matches1 = np.argmin(distances, axis=0)
        mask = indices1 == matches1[indices2]
        indices1 = indices1[mask]
        indices2 = indices2[mask]
    if max_distance < np.inf:
        mask = distances[indices1, indices2] < max_distance
        indices1 = indices1[mask]
        indices2 = indices2[mask]
    matches = np.column_stack((indices1, indices2))
    return matches

def plot_pair_match(match,imgs1,imgs2):
    plt.style.use('classic')
    matplotlib.use('TkAgg')
    match= match[:14]
    fig, axs = plt.subplots(2,len(match))
    for i,[x,y]  in enumerate(match):
        #caso nao seja possivel cpmverter para PIL
        try:
            im1 = transforms.ToPILImage()(imgs1[x])
            im2 = transforms.ToPILImage()(imgs2[y])
        except:
            im1 = imgs1[x]
            im2 = imgs2[y]


        axs[0][i].imshow(im1, interpolation='bilinear', cmap='viridis')
        axs[1][i].imshow(im2, interpolation='bilinear', cmap='viridis')
    # plt.tight_layout()
    plt.show()

def plot_match(img1,img2,esp,res):
  plt.style.use('classic')
  matplotlib.use('TkAgg')
  fig, (ax1, ax2) = plt.subplots(1, 2)
  # ax1.imshow(input_image.transpose(2, 0))
  ax1.imshow(transforms.ToPILImage()(img1))
  ax2.imshow(transforms.ToPILImage()(img2))
  fig.legend(title='e=>r {}=>{}'.format(esp,res))
  plt.show()

def get_model_siamese(path)->any:
    net = FibersSiamese()
    optimizer = optim.Adam(net.parameters(), lr=0.000002)
    criterion = nn.BCELoss()
    try:
        checkpoint = torch.load(path)
        net.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        epoch = checkpoint['epoch']
        best_loss = checkpoint['loss']
        print('best model epoch:{} loss:{}'.format(epoch, best_loss))
    except:
        print("Nenhum modelo salvo")
    net.eval()
    return net

def get_model_siamese_feature(path)->any:
    net = get_model_siamese(path)
    return net.feature

def get_model_siamese_discriminator(path)->any:
    net = get_model_siamese(path)
    return net.discriminator

preprocess_siamese = transforms.Compose([
    transforms.ToPILImage(),
    transforms.ToTensor()
    # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

if __name__ == '__main__':
    # Todo carregar modelos
    device = torch.device('cuda') if torch.cuda.is_available else torch.device('cpu')
    img =np.float32(np.zeros(shape=(5,30,33,3)))
    teste = transforms.Compose([
        transforms.Resize(64),
        transforms.CenterCrop(60),
        # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    img = torch.tensor(img)
    img = img.permute(0, 3, 1, 2)
    img =teste(img).to(device)
    net= get_model_siamese(device)
    # net_feat = get_model_siamese_feature(device)
    #net_dis = get_model_siamese_discriminator(device)
    features=net.feature(img)
    print(features.shape)
    print("inicio "+str(round(time.time() * 1000)))
    f = np.float32(np.zeros(shape=(500,128)))
    # f = np.array([f for i in range(5000)])
    ft = torch.tensor(f).to(device)
    match = net.discriminator(ft,ft)
    # print(match.cpu())

    print("inicio2 "+str(round(time.time() * 1000)))
    f = np.float32(np.zeros(shape=(128)))
    for i in range(5000):
        ft = torch.tensor(f).unsqueeze(0).to(device)
        match = net.discriminator(ft, ft)

    # print(match.cpu())
    print("fim2 "+ str(round(time.time() * 1000)))