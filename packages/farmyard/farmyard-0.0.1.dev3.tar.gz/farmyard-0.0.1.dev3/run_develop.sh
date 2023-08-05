#!/bin/bash

# you can use this file as a before launch compile script in PyCharm
# - just make sure that you set $ `pyenv local <env_name>` to the
#   same environment that pycharm uses to launch your python code!

# we need to use the latest bash version
# 1. source the bash rc because pycharm doesn't use our environment...
# 2. find the path to our python environment
# 3. compile using maturin
/usr/local/bin/bash -c '
    source "$HOME/.bashrc"
    export VIRTUAL_ENV="$(pyenv prefix)"
    maturin develop --rustc-extra-args="-C opt-level=3"
'
