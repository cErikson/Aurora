# -*- coding: utf-8 -*-
#!/bin/python
"""
Project: Aurora
@author: Christian Erikson

A

"""
##### Debug #####
testing=True

###### Imports #####
import argparse as arg
import pdb
import sys

##### Args #####
if __name__ == "__main__" and testing != True:
    parser = arg.ArgumentParser()
    # Positional mandatory arguments
    parser.add_argument("seq_file", help="Sequence File", type=str)
    # Optional arguments
    parser.add_argument("-d", "--indel", help="Gap Penalty", type=int, default=None)
    parser.add_argument("-a", "--alignment", help="Output Alignment", action='store_true')
    # Parse arguments
    ARGS = parser.parse_args()
##### Testing #####
else:   # Else test
    sys.stderr.writelines("!!!!!___RUNNING_IN_TESTING_MODE_WITH_TEST_ARGS___!!!!!\n")
    sys.stderr.flush()
    class test_args(object):
        pass
    ARGS = test_args()

###### Const #####

##### Class #####

##### Defs #####

###### MAIN ######
