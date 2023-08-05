# Visible Neuron Segmentation: ViNe-Seg (beta version)

<img align="right" width="600" height="600" src=https://gitlab.com/isyn2/idsair-neuronlabeling/uploads/749c759d23251b454ebfc072a22914e0/Vine-seg.png width="30%" height="30%" /> <br>


### GUI embedded semi-automated pipeline for AI-assisted Neuron segmentation.
This includes:
* Loading your mean images in the Graphical User Interface (GUI) based on labelme (see https://github.com/wkentaro/labelme)
* Preprocessing of the loaded images
* Prediction on preprocessed images with MONAI
* Saving of prediction
* Automatic display of the predicted polygons with the ability to edit an store those in the GUI

## Installation
We aimed to develop ViNe-Seg as user-friendly as possible. Therefor, ViNe-Seg comes with a GUI and is easily installable using pip with the command:
```
pip install vineseg
```

ViNe-Seg will be downloaded and installed with all necessary dependencies.

### Installation in a new conda environment (Alternative approach)
We recommend installing ViNe-Seg in a fresh conda environment to avoid dependency problems.
Usually it will not be necessary, but if you run into any problems, try creating a new conda environment first, e.g. running
```
conda create vineseg-env
conda activate vineseg-env
pip install vineseg
```
to create a new conda environment, e.g. called vineseg-env, to activate it and then to install ViNe-Seg using pip.

## Starting ViNe-Seg
You can start ViNe-Seg using the following command after installation (make sure not to work in an environment in which ViNe-Seg is not installed):
```
python -m vineseg
```

This command will check if you already have a version of the trained MONAI model installed and will download the default model version if none is currently in use on your machine.

After this step, the GUI will automatically be opened where you have the chance to download other models, choose between them, load your mean image in PNG or TIFF format and to run the autosegmentation using the ```Autosegmentation``` command shown in the menu bar in the top of the screen.
We embedded the ViNe-Seg functionality in the labelme GUI (see https://github.com/wkentaro/labelme) by adding a button for running the autosegmentation step of ViNe-Seg in the GUI and by changing some other underlying funtionalities such as automatic loading of the generated JSON labeling files and the option to load them from old ViNe-Seg runs using the new ```Load Polygon``` button or the possibility to manipulate the resulting JSON file by switching between enumerated Neuron labels (Neuron1, ..., NeuronX) and area-based Neuron labels (Neuron too small, ... , Neuron too big) by clicking a button. The area size from which the labels are derived can also be changed within the GUI. 


## Training your own model

Vineseg offers the possibility to integrate your own Monai model or to finetune an already existing model on your own data. The settings for the training can be specified via a config file.
The training can be started in the subfolder with python training.py --path_config_file="path to your config file".
The config file has the following options:

* path loading model: An already trained model can be used as starting point for further training. Specify here the folder where the model is located.
* paths training image folder: List of folders with the training images
* paths training masks folder: List of folders with the training masks
* paths val image folder: List of folders with the validation images
* paths val masks folder: List of folders with the validation masks 
* valiation intervall: Distance in epochs between evaluation time points during training on the validation dataset
* ROI training: Image size for training. Typically the ROI training is smaller than the original image size to get more training images.
  ROI training is only used if "SpatialCrop" is part of augementation steps.
* ROI validation: Image size for validation
* augmentation probability: probability that a augmentation steps is applied on the training images.
* preprocessing steps: List of preprocessing steps. The only option at the moment is "ScaleIntensity"
* augmentation steps: List of augmentation steps. Valid options are "SpatialCrop", "GaussianNoise"
  , "Rotate", "Flip", "Zoom", "ElasticDeformation" or "AffineTransformation" 
* postprocessing: Dictionary with key "Activation" for the activation function. Options are "Sigmoid" or "Softmax" as values.
  The other key "Threshold" specifies when the prediciton output is converted to 1.
* model type: The type of the neural network. Valid options are "U-Net big", "SegResNet" or "UNetTransformer"
* number input channel: Define how many different preprocessed duplications of one images are loaded into the network.
* channel types input: List of feature engineering techniques which should be applied. The length of the list must be equal to number input channel.
  Valid options are "identity", "clahe", "nl_means", "autolevel", "gamma low", "gamma high", "rolling ball" or "adjust sigmoid".
* number output channel: Number of output images from the neural network.
* channel types input: Further preprocessing steps, which are applied on the output from the neural network. The only valid option at the moment is ["identity"]
* optimizer: "Adam" or "AdamW"
* loss function: "Dice loss", "Focal loss", "Tversky loss", "Dice focal loss" or "Dice CE loss".
* metrics: List with metrics for evaluation. "Dice Metric" as only option at the moment.
* epochs: number of epochs
* batch size: number of training images per batch.
* learning rate: Initial learning rate. Will be decreased with factor (1 - current_epoch / max_epoch) ** 0.9 per epoch 
* weight decay: Will be applied in case optimizer "AdamW"
* path save model: folder for storing the trained neural network weights and the config file
* logging training results: Not used at the moment


## Automatic Preprocessing of images in the default model
The quality and image properties between the Calcium images differ a lot. Therefore we apply automatically
the CLAHE and NL-means algorithm before we feed the images into the neural network.
Depending of the image, the preprocessing step has a high influence to the visibility of neurons. 
Compare the original image <br>
<img src=https://gitlab.com/isyn2/idsair-neuronlabeling/uploads/6d575eb498dc61e5be3c44269d074eeb/grafik.png width="30%" height="30%" /> <br>
with the preprocessed one <br>
<img src=https://gitlab.com/isyn2/idsair-neuronlabeling/uploads/d835b683cdac48123597177792d10e6e/grafik.png width="30%" height="30%" /><br>

