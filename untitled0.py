# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 10:05:02 2017

@author: br_aq
"""

from __future__ import print_function
from ipywidgets import interact, interactive, fixed
import ipywidgets as widgets

def f(x):
    return x

interact(f,x=10)