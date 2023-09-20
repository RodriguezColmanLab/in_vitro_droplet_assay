Script to detect droplets (circular bright spots) in 2D images, originally by Jonathan Henninger.

# Requirements

To run the script, you'll need to install the following packages:

    numpy, matplotlib, pandas, xlsxwriter, scikit-image, opencv

A snapshot of my Anaconda environment can be found in the `environment.yml` file.

# Usage
You need a folder containing the files and each condition in subfolders:

    Script > condition 1 > all images from condition 1
           > condition 2 > all images from condition 2
           > condition 3 > all images from condition 3

Every image needs to be present twice: once as ND2 file, once as TIFF file. The TIFF file can have multiple channels, stored as CYX.

If you got the images from a different microscope without nd2 extension, you need to change it on the files. Just ctrl + F "Nd2" and swap for whatever file extension you have

To run the script, open Anaconda Prompt and run the following code:

    python main.py pathtofolder pathtooutput


See [IN VITRO DROPLET INSTRUCTIONS.txt](IN VITRO DROPLET INSTRUCTIONS.txt) for optional parameters.

