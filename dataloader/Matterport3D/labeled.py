"""A loader for the labeled ARKitScenes dataset."""
import os
import torch
from torch.utils.data import Dataset
from torchvision.transforms import v2 as transforms_v2
import imageio
# from .gen_focalStack import run

class Matterport3dDataset(Dataset):
    """Python interface for the labeled subset of the ARkitScenes dataset.

    To save memory, call the `close()` method of this class to close
    the dataset file once you're done using it.
    """

    def __init__(self, path, img_size=(192, 256), stage="test"):
        
        self.root_dir = path
        self.stage = stage
        
        """Opens the labeled dataset file at the given path."""
        with open(f'/home/ashkanganj/workspace/PrecisionDepthFocus/dataloader/Matterport3D/input_split/Matterport3D_{stage}_split.txt','r') as f:
                self.samples_pth= f.readlines()
        self.img_size = img_size

    def __len__(self):
        return len(self.samples_pth)

    def __getitem__(self, idx):
        # open the color image
        color_img = imageio.imread(os.path.join(self.root_dir,self.samples_pth[idx].split(' ')[0].strip()), pilmode="RGB")
        depth_img = imageio.imread(os.path.join(self.root_dir,self.samples_pth[idx].split(' ')[1].strip()), pilmode="I")
        
        # Convert to float tensor
        color_img = torch.from_numpy(color_img).float()  
        depth_img = torch.from_numpy(depth_img).float()
        depth_img = depth_img / 1000.0
        depth_img = depth_img.unsqueeze(0)
        
        color_img = color_img.permute(2, 0, 1)
        
        t_resize = transforms_v2.Resize(self.img_size, antialias=True)

        color_img = t_resize(color_img)
        depth_img = t_resize(depth_img)

        return color_img, depth_img
    
    
