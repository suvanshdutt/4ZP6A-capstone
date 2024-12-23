# https://stackoverflow.com/questions/66678052/how-to-calculate-the-mean-and-the-std-of-cifar10-data
import torch
from tqdm import tqdm


def get_mean_std(trainLoader):
    imgs = None
    for batch in tqdm(trainLoader):
        image_batch = batch[0]
        if imgs is None:
            imgs = image_batch.cpu()
        else:
            imgs = torch.cat([imgs, image_batch.cpu()], dim=0)
    imgs = imgs.numpy()

    # calculate mean over each channel (r,g,b)
    mean_r = imgs[:, 0, :, :].mean()
    mean_g = imgs[:, 1, :, :].mean()
    mean_b = imgs[:, 2, :, :].mean()
    print(mean_r, mean_g, mean_b)

    # calculate std over each channel (r,g,b)
    std_r = imgs[:, 0, :, :].std()
    std_g = imgs[:, 1, :, :].std()
    std_b = imgs[:, 2, :, :].std()
    print(std_r, std_g, std_b)
