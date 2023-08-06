## TFlash

A quick way to practice object detection on images and videos for common classes using TensorFlow. Fully operational by any user without Machine Learning experience.


### Requirements
``imageio``<br>
``imageio-ffmpeg`` (for videos)<br>
``tensorflow``<br>
``tqdm``

### Installation
``pip install tflash``<br>

Note: due to the incompatibility of numpy versions, in some cases tensorflow needs to be (re-)installed after installing imageio

### Usage

``import tflash``<br>

``flash = tflash.Detector()``<br>
``result = flash.detect("a_pic.jpg", print_output="a_result.jpg")``  # can be set to ``False``<br>
``result = flash.detect("mypic.jpg", min_score=0.75)``  # default: 0.5<br>

``my_pics = ["pic001.jpg", "pic002.jpg", "pic004.jpg"]``<br>
``result = flash.detect_multiple(my_pics)``<br>

Output:
* Dict of detection results
* Labeled image(s)

``detections = result["detections"]``  # formatted as dict<br>
``print("Saved to {}".format(result["output"])``  # output filename

### Font

Alter font (default is Roboto size 20):<br>
``flash.set_font("arial.ttf")``<br>
``flash.set_font_size(12)``<br>
``flash.set_font("dosis.ttf", size=15)``

### Own Model File

Some good ones are provided at Tensorflow model zoo:
https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md

Download a file with output "Boxes" from the link above, extract and use only the one with *.pb extension, e.g., frozen_inference_graph.pb

Load in TFlash using the command:<br>
``flash.load_model("frozen_inference_graph.pb")``<br>
or<br>
``flash = tflash.Detector("any_other_model_file.pb")``
