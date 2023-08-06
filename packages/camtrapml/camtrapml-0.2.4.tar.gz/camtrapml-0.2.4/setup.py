# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camtrapml',
 'camtrapml.detection',
 'camtrapml.detection.models',
 'camtrapml.embedding',
 'camtrapml.image']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9,<10',
 'PyExifTool>=0.4.13,<0.5.0',
 'font-fredoka-one>=0.0.4,<0.0.5',
 'matplotlib>=3,<4',
 'numpy>=1,<2',
 'requests>=2,<3',
 'scikit-learn==1.0.1',
 'tensorflow-hub>=0.12.0,<0.13.0',
 'tensorflow>=2,<3',
 'tqdm>=4,<5']

setup_kwargs = {
    'name': 'camtrapml',
    'version': '0.2.4',
    'description': 'CamTrapML is a Python library for Detecting, Classifying, and Analysing Wildlife Camera Trap Imagery.',
    'long_description': '# CamTrapML\n\n> CamTrapML is a Python library for Detecting, Classifying, and Analysing Wildlife [Camera Trap](https://en.wikipedia.org/wiki/Camera_trap) Imagery.\n\n## Installation\n\n    $ pip install camtrapml\n\n## Features\n\n### Loading Data\n\nSearch for images in a directory, load an image and create a thumbnail.\n\n\n```python\n%load_ext autoreload\n%autoreload\n\nfrom camtrapml.dataset import ImageDataset\nfrom camtrapml.image.utils import load_image, thumbnail\n\nimageset = ImageDataset(\n    name="Test Images",\n    path="test/fixtures/images",\n)\n\nimage_paths = list(imageset.enumerate_images())\n\nthumbnail(load_image(image_paths[0]))\n```\n\n### EXIF Extraction\n\nEXIF extraction is a common task in gathering the metadata such as each image\'s timestamp, camera model, focal length, etc. Some researchers write labelling into the EXIF data. CamTrapML doesn\'t assist with writing to EXIF. However, there is functionality for extracting it for analysis and building datasets for training new models from previously labelled images.\n\nExifTool is required for this package to work. Installation instructions can be found [here](https://exiftool.org/install.html).\n\nThree methods are available for extracting EXIF data from images. Each with different performance characteristics.\n\n**Method 1: Individual Images**\n\n\n```python\nfrom camtrapml.image.exif import extract_exif\n\nexif = extract_exif(image_paths[0])\nexif\n```\n\n**Method 2: Multiple Images**\n\n`extract_multiple_exif` passes a list of image paths to ExifTool and returns a list of dictionaries containing the EXIF data. This is faster than `extract_exif` when multiple images are being processed as it only passes the list of image paths to ExifTool once, rather than spawning a new process for each image.\n\n\n```python\nfrom camtrapml.image.exif import extract_multiple_exif\n\nexif = extract_multiple_exif(image_paths)\nexif[0]\n```\n\n**Method 3: Multiple Images, Multiple Processes**\n\nWhen processing large datasets, it\'s apparent that the bottleneck in extracting the EXIF information tends to be the CPU. This method spawns multiple versions of ExifTool in parallel, each with a batch of image paths. This is faster than `extract_multiple_exif` when processing large datasets as it allows for multiple processes to be spawned and the data extracted in parallel.\n\n\n```python\nfrom camtrapml.image.exif import extract_multiple_exif_fast\n\nexif = extract_multiple_exif_fast(image_paths)\nexif[0]\n```\n\n### Detection\n\nVarious Detection models are available in the `camtrapml.detection` subpackage. These currently include MegaDetector (v4.1, v3 and v2) and support for loading in custom Tensorflow v1.x Object Detection Frozen models.\n\n#### Detection with MegaDetector v4.1\n\n\n```python\nfrom camtrapml.detection.models.megadetector import MegaDetectorV4_1\nfrom camtrapml.detection.utils import render_detections\n\nwith MegaDetectorV4_1() as detector:\n    detections = detector.detect(image_paths[0])\n\nthumbnail(\n    render_detections(image_paths[0], detections, class_map=detector.class_map)\n)\n```\n\n#### Detection with a custom Tensorflow v1.x Object Detection Frozen model\n\n\n```python\n!cp ~/.camtrapml/models/megadetector/v4.1.0/md_v4.1.0.pb example-custom-model.pb\n\nfrom camtrapml.detection.models.tensorflow import TF1ODAPIFrozenModel\nfrom camtrapml.detection.utils import render_detections\nfrom pathlib import Path\n\nwith TF1ODAPIFrozenModel(\n    model_path=Path("example-custom-model.pb").expanduser(),\n    class_map={\n        1: "animal",\n    },\n) as detector:\n    detections = detector.detect(image_paths[1])\n\nthumbnail(\n    render_detections(image_paths[1], detections, class_map=detector.class_map)\n)\n```\n\n#### Extract Detections\n\n\n```python\nfrom camtrapml.detection.models.megadetector import MegaDetectorV4_1\nfrom camtrapml.detection.utils import extract_detections_from_image\n\nwith MegaDetectorV4_1() as detector:\n    detections = detector.detect(image_paths[0])\n\nlist(extract_detections_from_image(load_image(image_paths[0]), detections))[0]\n```\n\n#### Remove Humans from Images\n\nIn order to reduce the risks of identification of humans in line with GDPR, CamTrapML provides the ability to remove humans from images. This is achieved by using the MegaDetector v3+ models to detect humans in the image, and then replacing all pixels in each human detection.\n\n\n```python\nfrom camtrapml.detection.models.megadetector import MegaDetectorV4_1\nfrom camtrapml.detection.utils import remove_detections_from_image\nfrom camtrapml.image.utils import load_image, thumbnail\nfrom pathlib import Path\n\nct_image_with_humans = Path("test/fixtures/human_images/IMG_0254.JPG").expanduser()\n\nwith MegaDetectorV4_1() as detector:\n    detections = detector.detect(ct_image_with_humans)\n\nhuman_class_id = 2\n\nthumbnail(\n    remove_detections_from_image(\n        load_image(ct_image_with_humans),\n        [\n            detection\n            for detection in detections\n            if detection["category"] == human_class_id and detection["conf"] > 0.5\n        ],\n    )\n)\n```\n\n\n```python\n\n```\n',
    'author': 'Benjamin C. Evans',
    'author_email': 'Benjamin.Evans@brunel.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bencevans/camtrapml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
