# Newscraper

Open up the Terminal Application and start typing the following:
1 - Install Python Tools

$ sudo apt-get update

$ sudo apt-get upgrade

$ sudo apt-get install python-pip python-virtualenv python-setuptools python-dev build-essential  python3.6

2 - Install and Create a Virtualenv

$ sudo pip install virtualenv 

$ mkdir ~/Dev - This will be your direcvory for the project

$ cd ~/Dev

$ mkdir venv && cd venv - this will be your virtual environment directory

$ virtualenv -p python3.6 . - this is dot at the end

3 - Activate Virtualenv

$ cd ~/Dev/venv/ #created above

$ source bin/activate

If activated correctly, you should see:

(venv) $

Check python version:

(venv) $ python --version #should return Python 3.6

To deactivate:

(venv) $ deactivate

To reactivate:

$ /path/to/your/virtual/env/
$ source bin/activate

4 - Install Django & Start New project

$ /path/to/your/virtual/env/here/
$ source bin/activate
(here) $ pip install django==3.0.3

(here) $  mkdir src && cd src

and add src folder from this repo 
