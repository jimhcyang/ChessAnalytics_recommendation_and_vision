Alpha Vision +
==============================

Chess board state detection and move recommendation system

Computer Vision
---------------

Attempt 1: 3D Transfer Learning with chesscog
---------------

This project extends the work of Georg Wölflein and Patrick Lindemann and their [chesscog](https://github.com/georg-wolflein/chesscog) project. 

We were unable to successfully install this package using setup instructions, via pip, poetry, or docker. All methods failed in various ways. We were able to piece together a requirements.txt that can be used to install the necessary libraries and versions in your python 3.10 environment to be able to use some but not all of the functionality.

Installation

```
# create environment using python 3.10 (install if you don't have it already)
python3.10 -m venv .venv

source .venv/bin/activate

# validate the correct version of python
✗ python --version        
Python 3.10.13

# install dependencies
pip install -r requirements.txt
```

The file `notebooks/chesscog.ipynb` can be used to see the prediction functionality from the base models. Transfer learning failed to run due to the installation issues with chesscog.

Attempt 2: 3D Occupancy Detection using chesscog board localization
---------------
Installation from Attempt 1

`occupancy_predict.py` is the main file but was abandoned quickly, may not be functional.


Attempt 3: 2D Occupancy Detection
---------------

Project Overview

```
attempt_3_2d_occupancy_detection
├── data						# generated image files
│   ├── corner_detection		# corner detection output
│   ├── generated				# simulated games
│   ├── logs					# project logs including simulated games
│   ├── occupancy_detection		# final occupancy detection
│   └── square_extraction		# square extraction example (from 1 game image)
├── notebooks
│   └── wip.ipynb				# notebook used for masking/transformation experiments
├── occupancy_detection.py		# main execution script
├── requirements.txt			# dependencies
└── src
    ├── corners.py			# core corner detection
    ├── data.py				# data initialization and game simualation / data generation
    ├── evaluate.py			# evaluation of results
    ├── occupancy.py		# core occupancy detection
    ├── squares.py			# core square extraction
    ├── utils.py				# misc utility functions
    └── visualization.py	# visualization functions
```

Installation

```
# create virtual environment
python -m venv .venv

source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

Run Data Synthesis and Occupancy Detection

```
python occupancy_detection.py
```

Sample log output in data/logs/occupancy_detection.log

```
2024-04-21 12:13:41 - root - INFO - Data folders have been initialized.
2024-04-21 12:13:41 - root - INFO - =========== Playing simulated games ===========
2024-04-21 12:13:41 - root - INFO - 10 CPUs available, simulating 10 games
2024-04-21 12:13:41 - root - INFO - playing 10 in parallel
2024-04-21 12:13:41 - root - INFO - saving images to data/generated
2024-04-21 12:18:57 - root - INFO - Game 0 over after 141 moves.
2024-04-21 12:18:57 - root - INFO - Game 6 over after 320 moves.
2024-04-21 12:18:57 - root - INFO - Game 2 over after 303 moves.
2024-04-21 12:18:57 - root - INFO - Game 9 over after 363 moves.
2024-04-21 12:18:57 - root - INFO - Game 4 over after 367 moves.
2024-04-21 12:18:57 - root - INFO - Game 5 over after 399 moves.
2024-04-21 12:18:57 - root - INFO - Game 8 over after 446 moves.
2024-04-21 12:18:57 - root - INFO - Game 1 over after 416 moves.
2024-04-21 12:18:57 - root - INFO - Game 3 over after 734 moves.
2024-04-21 12:18:57 - root - INFO - Game 7 over after 688 moves.
2024-04-21 12:18:57 - root - INFO - Processing images...
2024-04-21 12:19:37 - root - INFO - Total samples: 4133
2024-04-21 12:19:37 - root - INFO - Successful occupancy detection: 4133
```


