# Copyright (C) 2016 Henrique Pereira Coutada Miranda
# All rights reserved.
#
# This file is part of yamboparser
# 
from yamboparser import *
import os
import numpy as np

class YamboFolder():
    """
    Takes as input a folder name that is the folder where yambo saved r-* o-* l-* and netcdf files
    """

    def __init__(self,path):
        """
        List all the files in the folder and to each of them call YamboFile class
        """
        self.path = path
        self.yambofiles = [] #list of YamboFile instances

        for dirname, dirnames, filenames in os.walk(path):
            # iterate over all the files in the folder
            for filename in filenames:
                y = YamboFile(filename, folder=dirname)
                if y: #checks if the file is of a known type
                    self.yambofiles.append(y)

    def get_data(self):
        """
        Return a dictionary with all the relevant data in this folder
        """
        data = {}
        for yambofile in self.yambofiles:
            print yambofile.filename
            print yambofile.data.keys()
       
    def __str__(self):
        s = ''
        for yambofile in self.yambofiles:
            s += "%s\n"%str(yambofile)
        return s