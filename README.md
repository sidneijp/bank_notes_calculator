# Bank notes calculator

It alculates the minimun amount of each available notes are necessary to reach a requested monetary value.

## Setup

In order to be able to run the software, some dependecies must be be installed:

- python >= 3.6

Some python packages dependencies must be installed as well. We suggest use `pipenv` + `pyenv` for a better and isolated enviroment, but `pip` may also be used.

To install pipenv and pyenv follow the instructions:

1. pyenv >= 1.2.7 (https://github.com/pyenv/pyenv-installer#installation--update--uninstallation)
2. pipenv >= 2018.10.13 (https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)

Then you will be able to install the python dependecies using pipenv:

`pipenv install`

or using `pip` with it's your case:

`pip install -r requirements.txt`

## To run the software

After the environment is set, to run the software you just need to:

`python main.py`

## How to use

Each input prompted asks for a bank note to be made available. After you finish input as much as you want, type -1 and hit enter to finish . Then you will be prompt for a monetary value. Based on this value the software will calculate the minimum amount of each avaliable bank note necessary to the correspondent value then show it to the user. You can test different values as you like. To finish the software execution just type -1 again and hit enter.

## To run automated tests

In case you are participating on the software development, you can run the automated tests like this:

`python -m unittest discover tests -b`
