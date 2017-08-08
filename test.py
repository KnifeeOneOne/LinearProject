#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 20:12:21 2017

@author: wankanzhen
"""
from line import Line
from Vector import Vector
l1 = Line(Vector(['4.046','2.836']), '1.21')
l2 = Line(Vector(['10.115','7.09']), '3.025')
print(l1.intersection_with(l2))