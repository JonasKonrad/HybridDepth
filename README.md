<div align="center">
<h1>Hybrid Depth: Robust Depth Fusion for Mobile AR </br> By Leveraging Depth from Focus and Single-Image Priors</h1>

[**Ashkan Ganj**](https://ashkanganj.me/)<sup>1</sup> · [**Hang Su**](https://suhangpro.github.io/)<sup>2</sup> · [**Tian Guo**](https://tianguo.info/)<sup>1</sup>

<sup>1</sup>Worcester Polytechnic Institute
&emsp;&emsp;&emsp;<sup>2</sup>Nvidia Research

<a href=""><img src='https://img.shields.io/badge/arXiv-Hybrid Depth-red' alt='Paper PDF'></a>
<a href=''><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-yellow'></a>
</div>


This work presents HybridDepth. HybridDepth is a practical depth estimation solution based on focal stack images captured from a camera. This approach outperforms state-of-the-art models across several well-known datasets, including NYU V2, DDFF12, and ARKitScenes.
![teaser](assets/teaser.png)


## News
- **2024-07-23:** Model and Github repository is online.

## TODOs
- [ ] Add pre-trained models.
- [ ] Add Hugging Face model.
- [ ] Add single input image prediction.
- [ ] Release Android Mobile Client for HybridDepth.

## Pre-trained Models

We provide **three models** trained on different datasets. You can download them from the links below:

| Model | Checkpoint |
|:-|:-:|
| Hybrid-Depth-NYU | [Coming soon]() |
| Hybrid-Depth-DDFF12 | [Coming soon]() |
| Hybrid-Depth-ARKitScenes | [Coming soon]() |

## Usage

### Prepraration

```bash
git clone 
cd HybridDepth
conda env create -f environment.yml
conda activate hybriddepth
```

Download the checkpoints listed [here](#pre-trained-models) and put them under the `checkpoints` directory.

### Using HybridDepth model for prediction
For inference you can run the provided notebook `test.ipynb` or use the following command:

```python
# Load the model checkpoint
model_path = './checkpoints/NYUBestScaleInv5Full.pth'
model = DepthNetModule()
# Load the weights
model.load_state_dict(torch.load(model_path))

model.eval()
model = model.to('cuda')
```

after loading the model, you can use the following code process the input images and get the depth map:

```python

from utils.io import prepare_input_image

data_dir = 'focal stack images directory'

# Load the focal stack images
focal_stack, rgb_img, focus_dist = prepare_input_image(data_dir)

# inference
with torch.no_grad():
   out = model(rgb_img, focal_stack, focus_dist)

metric_depth = out[0].squeeze().cpu().numpy() # The metric depth
```

### Evaluation

First setup the configuration file `config.yaml` in the `configs` directory. We already provide the configuration files for the three datasets in the `configs` directory. In the configuration file, you can specify the path to the dataloader, the path to the model, and other hyperparameters. here is an example of the configuration file:

```yaml
data:
  class_path: dataloader.dataset.NYUDataModule
  init_args:
    nyuv2_data_root: 'path to the NYUv2 dataset'
    img_size: [480, 640]  # Adjust if your NYUDataModule expects a tuple for img_size
    remove_white_border: True
    batch_size: 1
    num_workers: 0  # due to the synthetic data, we don't need multiple workers
    use_labels: True
    num_cluster: 5

model:
  invert_depth: True # If the model outputs inverted depth

ckpt_path: checkpoints/hybrid_depth_nyu.pth
```
Then specify the configuration file in the `evaluate.sh` script. Finally, run the following command:

```bash
cd scripts
sh evaluate.sh
```

### Training

First setup the configuration file `config.yaml` in the `configs` directory. you only need to specify the path to the dataset and the batch size. The rest of the hyperparameters are already set.
For example, you can use the following configuration file for training on the NYUv2 dataset:

```yaml
...
model:
  invert_depth: True
  # learning rate
  lr: 3e-4
  # weight decay
  wd: 0.001

data:
  class_path: dataloader.dataset.NYUDataModule
  init_args:
    nyuv2_data_root: 'root to the NYUv2 dataset'
    img_size: [480, 640]  # Adjust if your NYUDataModule expects a tuple for img_size
    remove_white_border: True
    batch_size: 24
    num_workers: 0  # based on the synthetic data, we don't need multiple workers
    use_labels: True
    num_cluster: 5
ckpt_path: null
```


Then specify the configuration file in the `train.sh` script. Finally, run the following command:

```bash
cd scripts
sh train.sh
```
