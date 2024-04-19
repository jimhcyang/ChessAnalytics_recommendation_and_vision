Alpha Vision +
==============================

Chess board state detection and move recommendation system

Computer Vision
---------------

Attempt 1: 3D Transfer Learning with chesscog
---------------

This project extends the work of Georg Wölflein and Patrick Lindemann and their [chesscog](https://github.com/georg-wolflein/chesscog) project. 

We were unable to successfully install this package using setup instructions, via pip, poetry, or docker. All methods failed in various ways. We were able to piece together a requirements.txt that can be used to install the necessary libraries and versions in your python 3.10 environment to be able to use some but not all of the functionality.

Using venv from the root dir:

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

Attempt 2: 3D Occupancy Detection
---------------



Attempt 3: 2D Occupancy Detection
---------------

