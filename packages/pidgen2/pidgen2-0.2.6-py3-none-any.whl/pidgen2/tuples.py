##############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

"""
Functions to read and write numpy arrays from/to ROOT ntuples using uproot. 
"""

import uproot3 as uproot
from jax import numpy as np
import numpy as onp
from itertools import product
from timeit import default_timer as timer

from . import init

def read_array_filtered(tree, branches, selection = None, sel_branches = []) : 
  """
  Read numpy 2D array from ROOT tree with filtering applied. 

  Args: 
    tree: ROOT tree object returned by uproot.open()
    branches: list of branches to read in the array
    selection: optional selection string in pandas format
    sel_branches: List of additional selection braches if "selection" string 
                  contains branches not from "branches" list.

  Returns: 
    2D numpy array, where 1st index corresponds to event, 2nd to the variable 
    (in the order given by branches list)
  """

  '''
  arrays = []
  for data in tree.pandas.iterate(branches = branches + sel_branches) : 
      if selection : df = data.query(selection)
      else : df = data
      arr = df[list(branches)].to_numpy()
      arrays += [ arr ]
  return onp.concatenate(arrays, axis = 0)
  '''
  return t.arrays(branches, cut = selection, library = "pd")[list(branches)].to_numpy()

def read_array(tree, branches) : 
  """
  Read numpy 2D array from ROOT tree. 

  Args: 
    tree: ROOT tree object returned by uproot.open()
    branches: list of branches to read in the array

  Returns: 
    2D numpy array, where 1st index corresponds to event, 2nd to the variable 
    (in the order given by "branches" list)
  """
  a = []
  for b in branches : 
    i = tree.array(b)
    if len(i.shape)==1 : a += [ i ]
    else : a += [ i[:,0] ]
  #a = [ tree.array(b) for b in branches ]
  #print("\n".join([ f"{b} : {i.shape}" for i,b in zip(a, branches)]))
  return np.stack(a, axis = 1)

def write_array(rootfile, array, branches, tree="tree") : 
  """
     Store numpy 2D array in the ROOT file using uproot. All branches of the tree 
     are set to double precision

     Args: 
       rootfile : ROOT file name
       array: numpy array to store. The shape of the array should be (N, V), 
               where N is the number of events in the NTuple, and V is the 
               number of branches
       branches : list of V strings defining branch names
       tree : name of the tree
  """
  with uproot.recreate(rootfile, compression=uproot.ZLIB(4)) as file :  
    file[tree] = uproot.newtree( { b : "float64" for b in branches } )
    d = { b : array[:,i] for i,b in enumerate(branches) }
    file[tree].extend(d)
