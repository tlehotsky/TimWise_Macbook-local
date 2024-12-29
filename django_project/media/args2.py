#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os,sys 

os.system('clear')

import shutil, glob, time, subprocess, re, sys
import argparse

print ("args test number 1\n")
parser = argparse.ArgumentParser(description='Short sample app')

parser.add_argument('-s', action='store_false', default=False,
                    dest='fast_switch',
                    help='Set a switch to false')

parser.add_argument('-f', action='store_true', default=False,
                    dest='fast_switch',
                    help='Set a switch to true')
results = parser.parse_args()

if results.fast_switch:
	run_fast=True
	print ("program will run fast")

else:
	run_fast=False
	print ("program will run slow")










# parser.add_argument('f', action="store", default="slow")

# print ("printing the arg")
# # print ("store_true variable = ", f)
# # print (parser.parse_args())
# results = parser.parse_args()

# print ('Fast switch =', results.fast_switch)