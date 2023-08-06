#!/usr/bin/env python3
# tools.py 

#------------------------------------------------------------------------------------------------#
# This software was written in 2021/01                                                           #
# by Dominikus Brian <dominikusbrian@nyu.edu>/<domi@dominikusbrian.com>  ("the author"),         #                   
#                                                                                                #                                                                    #
#                                                                                                #   
# Copyright (C) 2021 Dominikus Brian @ Sun Group NYUSH                                           #
#------------------------------------------------------------------------------------------------#

"""tools.py @ CT Landscape """

# Importing dependencies
import os 

def survey(path,filepattern):
    '''
    Survey all files under path directory
    
    Usage example:
    -------------------
    >>> mypath = '../ArtisanKit/sample'
    >>> filepattern = '.dat'
    >>> myfilepaths= survey(mypath, filepattern)
    A total of  3 .dat  files are detected

    >>> myfilepaths
    ['../ArtisanKit/sample/test1.dat',
     '../ArtisanKit/sample/test2.dat',
     '../ArtisanKit/sample/test3.dat']

    >>> filelist
    ['test1.dat', 'test2.dat', 'test3.dat']

    '''
    filepaths_ALL = []
    file_with_pattern = []
    for root,dirs,files in os.walk(path):
        for filename in files:
            if filepattern in filename:
                filepath = "{}/{}".format(root,filename)
                mypattern = "{}".format(filename)
                filepaths_ALL.append(filepath)
                file_with_pattern.append(mypattern)
            if 'CVS' in dirs:
                dirs.remove('CVS')  # don't visit CVS metadata directories
    print("A total of ",len(filepaths_ALL),filepattern," files are detected")
    return filepaths_ALL, file_with_pattern