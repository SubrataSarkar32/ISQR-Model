# ISQR-Model
Implementation of ISQR model and its simulation

In this file we have shown the implementation of ISQR algorithm using Python Google Colab. in this file images are stored in google drive and the output are also stored in different directory of google drive. In this code we mainly focus on encoding pixel states instead of creating image matrix. The image matrix we thought of has already been created using several unitary gates. 


## Datasets

Coal Mines images dataset have been taken from internet and respective output is also shown 

ExDark Dataset have been taken from Github repository [Dark Image Dataset](https://github.com/cs-chan/Exclusively-Dark-Image-Dataset)

DOI: (https://doi.org/10.1016/j.cviu.2018.10.010)


## Theory

The superposition state we have created is:  `\cos\theta|0\rangle+\sin\theta|1\rangle`, which is represented as a 1*2 array in conv_img1_arcsin function. 

The angle of encoding is defined in conv_rgb3_arcsin function. The equivalent superposition state is obtaned after the classical to quantum encodingin this phase using conv1_rgb_arcsin function where the angle valu `\theta` is obtained from conv_img3_arcsin.  

convert_a function is used to choose random outcomes from the superposition states. While measuring, the state `|0\rangle` is obtained with probability `\alpha^2` and state `|1\rangle` is obtained with probability `\beta^2`
After the random image is obtained, the images are stored in convshots_bw_arcsin, to obtain the mean of the measured images. During measurement, in this case, we have performed the measurement operation for 500 times to obtain clearer images. 

To get accurate image we have performed controlled measurement operation and the comparison between the classical image and the measured image is obtained and are stored in an excel file.

## Usage

To run this file you need to follow below steps:

1. Create venv in repo root directory. Use `python -m venv venv`
2. Activate it with `venv\Scripts\activate` on windows and `source venv\bin\activate` on linux.
3. Install the requirements with the activated venv as `pip install -r requirements.txt`
4. To run on provided sample folder use `python isqr_grayscale.py --input_folder E:\projects\ISQR-Model\sample_run_folder\input` on windows or `python isqr_grayscale.py --input_folder /home/user/ISQR-Model/sample_run_folder/input` on linux. Change the input directory name as per your requirement. Available options for `isqr_grayscale.py` are:

    - `--input_folder` : Specify full path to your input folder
    - `--plot`: Toggle to plot the image with matplotlib, expects True/False
    - `--number_of_shots`: number of times to perform measurement.



