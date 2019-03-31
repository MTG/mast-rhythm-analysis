# MAST Rhythmic Analysis 

This repository contains a set of Jupyter notebooks that will guide us through some analysis over the MAST Rhythmic Dataset.  To run the notebooks, you will need to install docker and run the Jupyter server available in the docker image.

## Instructions

### Docker
In order to install docker you must follow the OS-specific instructions:

#### Windows
https://docs.docker.com/docker-for-windows/install/

#### Mac OS
https://docs.docker.com/docker-for-mac/install/

#### Ubuntu
https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce

### Docker Compose
See https://docs.docker.com/compose/install/ on how to install Docker Compose

## Running Server

In the root of your project, run:
`docker-compose up`

On Linux, run the following (this command ensures that any files you create are owned by your own user):
`JUPYTER_USER_ID=$(id -u) docker-compose up`

The first time you run this command it will download the required docker images (about 2GB in size). If you have previously downloaded the images and would like to update them with the last version, run:

`docker-compose pull`

Then, you can access the notebooks from the browser and run them. All the notebooks contain their user guides, but you must to make sure to run them in a specific order, since one notebook might use outputs from a previous notebook. The correct sequence is: _DownloadDataFromMASTDataset.ipynb_ -> _PreProcessDataFromMASTDataset.ipynb_ -> _BaselineRhythmicAssessmentSystem.ipynb_
