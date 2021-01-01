# Hotword Detection with Raspberry Pi

## About / Synopsis

* Activation of certain user function after hotword detection
* Project status: prototype

See real examples:

* <https://blog.aspiresys.pl/technology/building-jarvis-nlp-hot-word-detection/>
* <https://picovoice.ai/>
* <https://github.com/Kitt-AI/snowboy/>

## Table of contents

Use for instance <https://github.com/ekalinin/github-markdown-toc>:

> * [Title / Repository Name](#hotword-detection-with-raspberry-pi)
>   * [About / Synopsis](#about--synopsis)
>   * [Table of contents](#table-of-contents)
>   * [Installation](#installation)
>   * [Usage](#usage)
>     * [Screenshots](#screenshots)
>   * [Code](#code)
>     * [Content](#content)
>     * [Requirements](#requirements)
>   * [License](#license)
>   * [About project](#about-project)

## Installation

* Git clone this repository to your Raspberry Pi [link](https://github.com/BioWar/Hotword-Detection-with-Raspberry-Pi.git).
* Create Python virtual environment and install packages from requirements.txt

## Usage
`$ python3 main.py`
### Screenshots
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Below is an example of a Mel Spectrogram, model prediction and true labels for a training example from the dataset. Dev set accuracy 97.7%. More images could be found in [images directory](https://github.com/BioWar/Hotword-Detection-with-Raspberry-Pi/tree/main/images/predictions).
![Prediction of hotword on training example](/images/predictions/899.png)

## Code

### Content

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The idea of this project was based on the real world examples, such as Alexa, Siri, Google Assistant. Also, additional knowledge was taken from [Coursera](https://www.coursera.org/learn/nlp-sequence-models)

### Requirements

See [requirements.txt](https://raw.githubusercontent.com/BioWar/Hotword-Detection-with-Raspberry-Pi/main/requirements.txt)

Additional [setup notes](https://github.com/BioWar/Hotword-Detection-with-Raspberry-Pi/tree/main/notes)

## License

[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)

## About project

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This project is part of my bachelor's degree project. The idea of not using end-to-end solution for a simple voice assistant, and filter request by the hotword was taken from real world example which were listed above. Data preprocessing step was significantly modified to improve model performance. In my case usage of Mel Spectrogram as an input data preprocessor gave me up to 8% accuracy improvement (from 89% on the dev set, up to 97% on the dev set).

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The model architecture was taken from Coursera final course in series about Deep Learning from Andrew Ng. The only difference is the amount of input and output nodes. Below you can find the complete architecture of model:
  
<p align="center">
  <img src="https://raw.githubusercontent.com/BioWar/Hotword-Detection-with-Raspberry-Pi/main/images/model/model.png" alt="Model architecture"/>
</p>


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The dataset was generated with the help of Google Cloud [Text-to-Speech](https://cloud.google.com/text-to-speech). Using Wavenets I gathered about 50 examples of 1 second audio files with trigger word phrase. Background generation was created by cutting and converting Youtube videos such as this [one](https://www.youtube.com/watch?v=BOdLmxy06H0). Half of the trigger words were recorded by myself in Jupyter Notebook scripts which will be posted in a separate directory. 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Labels were marked after every trigger word. Below are examples of such marking (the first one was taken from Coursera Sequence course, and the second one was created by myself):

<p align="center">
  <img src="https://raw.githubusercontent.com/BioWar/Hotword-Detection-with-Raspberry-Pi/main/images/input_data/label_diagram.jpeg" alt="Labeling from Coursera"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/BioWar/Hotword-Detection-with-Raspberry-Pi/main/images/input_data/899_training_example_prediction.png" alt="Labeling used in this project"/>
</p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;From the images above you may see that for the trigger word I chose the phrase "Listen comrade". The model should make the distinct [notification sound](activation_sound/activation.wav) if the trigger word was spoken by someone. 
