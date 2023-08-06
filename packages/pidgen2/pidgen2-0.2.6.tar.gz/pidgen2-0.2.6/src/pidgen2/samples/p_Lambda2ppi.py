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

from ..datasets import legacy_run2_pidcalib_datasets as ds_run2
from ..datasets import converted_run1_pidcalib_datasets_lam0_p as ds_run1
from itertools import product

def trees(year) : 
  #return [ ("Lam0" + ("LL" if year in ["2017", "2018"] else "") + \
  #            f"_{i}{j}Tuple/DecayTuple") for i, j in product(["", "HPT_", "VHPT_"], ["P", "Pbar"]) ]
  return [ (f"Lam0LL_{i}{j}Tuple/DecayTree") for i, j in product(["", "HPT_", "VHPT_"], ["P", "Pbar"]) ]

common_params = {
    "smear" : [ None, None, (-0.5, 0.5) ], 
    "transform" : [ 
      "np.log10(x)",   # pT transformation
      "x",             # eta
      "np.log10(x)",   # number of tracks
    ], 
    "calib_cache_branches" : ["pt", "eta", "ntr", "sw"], 
    "data_ranges" : [ (2.4, 4.4), (1.9, 5.0), (0.7, 3.1) ], 
    "labels" : [r"PID", r"$p_T$", r"$\eta$", r"$N_{\rm tr}$"],    # Labels for plots
    "names" : ["pid", "pt", "eta", "ntr"],                        # Short names of each variable for plot file names
    "max_weights" : (40., 1., 1.), 
    "normalise_bins" : [100, 100, 100], 
    "normalise_methods" : ["flatten", "flatten", "flatten"], 
    "normalise_ranges" : 3*[ (0., 1.) ], 
    "template_bins" : [70, 70, 20], 
    "template_sigma" : {
      "default" : [2., 4., 4.], 
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
    "trees" : trees(year), 
    **common_params
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
    "trees" : ["DecayTree"], 
    **common_params
  } 
  for pol in ["MagUp", "MagDown"] for year in ["2011", "2012"]
}

sample = {**sample_run1, **sample_run2}
