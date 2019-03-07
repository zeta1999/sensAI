import numpy as np
import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
import torch.nn.parallel
import torch.optim as optim
import torch.utils.data as data
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import glob
import os
from cifar10class import *


def loader(class_index, batch_size=64, num_workers=2, pin_memory=True):
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform_train)

    # cat/random single classifier
    cat_dog_trainset = \
        DatasetMaker(
#            [get_class_i(x_train, y_train, classDict['cat']), get_class_i(x_train, y_train, classDict['dog'])],transform_with_aug)
            [get_class_i(x_train, y_train, class_index), get_random_images(x_train, y_train, class_index)],transform_with_aug)
    return data.DataLoader(cat_dog_trainset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory)

""" 
    Modified version of original test_loader to grab only data from specific class i
    Not compatible with other purposes aside from collecting feature map activations
"""
def test_loader(class_index, batch_size=1000, num_workers=2, pin_memory=True):
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform_test)
    cat_dog_testset  = \
        i_DatasetMaker(
            [get_class_i(x_test , y_test , class_index)], class_index, transform_no_aug)
    return data.DataLoader(cat_dog_testset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory)