from typing import Optional, Dict, List, Union

import numpy as np

import ROOT

from quickstats.interface.cppyy.vectorize import list2vec

def unfold_constraints(constraint_pdfs:ROOT.RooArgSet, observables:ROOT.RooArgSet,
                       nuisance_parameters:ROOT.RooArgSet, constraint_cls:Optional[List[str]]=None,
                       recursion_limit:int=50, strip_disconnected:bool=False):
    result = ROOT.RooArgSet()
    if constraint_cls is None:
        constraint_cls = ROOT.RooFitExt.kConstrPdfClsList
    else:
        
        constraint_cls = list2vec(constraint_cls)
    ROOT.RooFitExt.unfoldConstraints(constraint_pdfs, observables, nuisance_parameters, result,
                                     constraint_cls, 0, recursion_limit, strip_disconnected)
    return result

def pair_constraints(constraint_pdfs:ROOT.RooArgSet, nuisance_parameters:ROOT.RooArgSet,
                     global_observables:ROOT.RooArgSet, fmt:str="list", to_str:bool=False, sort:bool=False):
    if sort:
        ROOT.RooArgSet.sort(constraint_pdfs)
    paired_constraints = ROOT.RooFitExt.pairConstraints(constraint_pdfs, nuisance_parameters, global_observables)
    paired_pdfs  = paired_constraints.pdfs
    paired_nuis  = paired_constraints.nuis
    paired_globs = paired_constraints.globs
    if to_str and (fmt == "arglist"):
        raise ValueError("arglist format does not support to_str")
    if fmt in ["list", "dict", "series"]:
        if fmt in ["list", "dict"]:
            if to_str:
                paired_pdfs  = [i.GetName() for i in paired_pdfs]
                paired_nuis  = [i.GetName() for i in paired_nuis]
                paired_globs = [i.GetName() for i in paired_globs]
            else:
                paired_pdfs  = [i for i in paired_pdfs]
                paired_nuis  = [i for i in paired_nuis]
                paired_globs = [i for i in paired_globs]
            if fmt == "list":
                return paired_pdfs, paired_nuis, paired_globs
            elif fmt == "dict":
                result = {
                    "pdf"  : paired_pdfs,
                    "nuis" : paired_nuis,
                    "globs": paired_globs
                }
                return result
        elif fmt == "series":
            size = len(paired_pdfs)
            if to_str:
                result = [(a.GetName(), b.GetName(), c.GetName()) for a, b, c in zip(paired_pdfs, paired_nuis, paired_globs)]
            else:
                result = [(a, b, c) for a, b, c in zip(paired_pdfs, paired_nuis, paired_globs)]
            return result
    elif fmt == "arglist":
        return paired_pdfs, paired_nuis, paired_globs
    else:
        raise ValueError(f"format '{fmt}' not supported")