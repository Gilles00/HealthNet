========================

## Ensure sqlite3 is installed

# Setup

## Install miniconda
Miniconda is a portable python distribution,
which allows us to install dependencies on systems where we
don't have admin rights (i.e. SE machines)

It can be found here: conda.pydata.org/miniconda.html
Download the version appropriate for your operating system, and install it.

Once installed, open the anaconda prompt, create a new environment, and install pip.
Run `conda create --name 261-10-b python=3`
Run `activate 261-10-b`
Run `conda install pip`


## Extract source code

Decompress the Healthnet.zip folder. This will vary by operating system.

## Install Dependencies 

Navigate into the Healthnet folder, find the file called `requiremnts.txt` and run.
`pip install -r requirments.txt`

Once those dependencies are installed, run:
`python manage.py runserver -p localhost:8000`

Now the site should be available in your browser from `localhost:8000/login`

A list of username and password combinations may be found: users.txt
