# PicParseApp

### This is a small example of using Keras deep learning to identify images on websites.  The model was trained on four classes of images:

* 0 Bombers
* 1 Missiles
* 2 Other
* 3 Submarines

Images were pulled using a combination of existing repositories (ImageNet), search engines, and the GDELT database.  There were approximately 1000 images for each class.

The model was trained and fine-tuned using the instructions contained in this tutuorial:
https://github.com/spmallick/learnopencv/blob/master/Keras-Fine-Tuning/keras-finetune-vgg.ipynb

The app uses a Flask framework and parses website inputs for images with Requests and BeautifulSoup. Additional dependencies are in the requirements.txt file.

**NB** The app will not run without a trained model (*.h5 file). The model we use is not included in this repository due to size constraints.

