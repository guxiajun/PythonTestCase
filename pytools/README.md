# Video-lag-tool
Video transition analysis

## Packages
OpenCV, pandas, numpy, bokeh

## Extract data from video
Usage:
```
python3 gaussian.py -i <input file> -n <optional threshold value>
```
To filter out lagging start time, end time and time period from raw csv file and save to **result.csv**, cleaned data files, and visualization graph html file . Optional threshold value controls number of frames need to be filtered out, default value: 6.

# Avsync

## Packages
OpenCV, pytesseract, ffmpy

Usage:
```
python avsync.py <input file>
```
