# HomeTask
This task solves a real-world problem related to ingesting a video file into Texel's system.
Freezing frames, arriving that way from the encoder, are a major artefact in users' perceived QoE. Detecting these periods in the video is a prerequisite prior to processing them.

The set of files contains:
1. excercise.py - The python code for processing the videos' data. This file defines two classes for maintaing the process:
I. VideoDataProcessor -  A class for initializing data from one video by its pathfile. The class also contains a method for orginizing the data due to a format of a dictionary, based on the requested output JSON file.
II. FreezeDetector -  A class which inputs a set of path files for numerous videos in order to collect data for the requested JSON file, based on the class of VideoDataProcessor
2. current_freeze.txt - An empty text file for storing the metadata's script of a video in order to extract information about the freeze start and end times (As a part of initializing the class object of  VideoDataProcessor)
3. output.json - The requested output JSON file for the videos' data.
4. 3 mp4 files for testing the classes (which appear in the "main" part of 'exercise.py').
