import torch.utils.data as data
from os.path import join
from os import listdir
from torchvision.transforms import Compose, ToTensor
from PIL import Image
import numpy as np


# def img_modcrop(image, modulo):
#     sz = image.size
#     w = (sz[0] / modulo) * modulo #np.int32
#     h = (sz[1] / modulo) * modulo
#     out = image.reshape((0, 0, w, h))
#     return out

def img_modcrop(data, modulo):
    h, w, _ = data.shape
    h = (h // modulo) * modulo
    w = (w // modulo) * modulo
    out = data[:h, :w]
    return out


def np2tensor():
    return Compose([
        ToTensor(),
    ])


def is_image_file(filename):
    return any(filename.endswith(extension) for extension in [".bmp",".jpg", ".npy"])


def load_image(filepath):
    image = np.load(filepath)
    return image
    # return Image.open(filepath).convert('RGB')


class DatasetFromFolderVal(data.Dataset):
    def __init__(self, hr_dir, lr_dir, upscale):
        super(DatasetFromFolderVal, self).__init__()
        self.hr_filenames = sorted([join(hr_dir, x) for x in listdir(hr_dir) if is_image_file(x)])
        self.lr_filenames = sorted([join(lr_dir, x) for x in listdir(lr_dir) if is_image_file(x)])
        self.upscale = upscale

    def __getitem__(self, index):
        input = load_image(self.lr_filenames[index])
        target = load_image(self.hr_filenames[index])
        input = np2tensor()(input)
        target = np2tensor()(img_modcrop(target, self.upscale))

        return input, target

    def __len__(self):
        return len(self.lr_filenames)
