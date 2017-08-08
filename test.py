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

l1 = Line(Vector(['7.204','3.182']), '8.68')
l2 = Line(Vector(['8.172','4.114']), '9.883')
print(l1.intersection_with(l2))

l1 = Line(Vector(['1.182','5.562']), '6.774')
l2 = Line(Vector(['1.773','8.343']), '9.525')
print(l1.intersection_with(l2))