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

from ..datasets import converted_run1_pidcalib_datasets_dstar_k as ds_run1
from ..datasets import legacy_run2_pidcalib_datasets as ds_run2

from itertools import product

common_params = {
    "calib_cache_branches" : ["pt", "eta", "ntr", "sw"],          # Names of variable branches in ROOT tree of the cache file 
    "data_ranges" : [ (2.4, 4.4), (1.9, 5.0), (0.7, 3.1) ],       # Ranges of each variable after transformation
    "labels" : [r"PID", r"$p_T$", r"$\eta$", r"$N_{\rm tr}$"],    # Labels for plots
    "names" : ["pid", "pt", "eta", "ntr"],                        # Short names of each variable for plot file names
    "max_weights" : None, 
    "smear" : [ None, None, (-0.5, 0.5) ], 
    "transform" : [                                               # Transformation functions for each variable
      "np.log10(x)",   # pT transformation
      "x",             # eta
      "np.log10(x)",   # number of tracks
    ], 
    "normalise_bins" : [100, 100, 100],                           # Number of bins for normalisation of each variable
    "normalise_methods" : ["scale", "scale", "flatten"],          # Normalisation method for each variable ("scale", "normalise", "flatten")
    "normalise_ranges" : 2*[ (0., 1.) ] + [ (0., 1.) ],           # Ranges of each variable after normalisation
    "template_bins" : [70, 70, 20],                               # Number of bins for each variable in the template 
    "template_sigma" : { 
      "default" : [2., 4., 4.],                                   # Smearing parameter for the template for each variable. 
      "syst1"   : [3., 6., 6.], 
    }
}

sample_run2 = {
  f"{pol}_{year}" : { 
    "sample" : ds_run2[f"{pol}_{year}"], 
    "branches" : [ 
      "probe_Brunel_PT", 
      "probe_Brunel_ETA", 
      "nTracks_Brunel", 
      "probe_sWeight" 
    ], 
    "trees" : ['DSt_KPTuple/DecayTree'], 
    **common_params, 
  } 
  for pol in ["MagUp", "MagDown"] for year in ["2015", "2016", "2017", "2018"]
}

sample_run1 = {
  f"{pol}_{year}" : { 
    "sample" : ds_run1[f"{pol}_{year}"], 
    "branches" : [ 
      "probe_PT", 
      "probe_ETA", 
      "nTracks", 
      "probe_sWeight" 
    ], 
    "trees" : ['DecayTree'], 
    "cut" : "probe_trackcharge>0", 
    **common_params, 
  } 
  for pol in ["MagUp", "MagDown"] for year in ["2011", "2012"]
}

sample = {**sample_run1, **sample_run2}
