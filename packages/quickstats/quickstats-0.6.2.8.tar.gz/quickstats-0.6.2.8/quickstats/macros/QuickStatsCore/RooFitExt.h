#ifndef __RooFitExtension_H__
#define __RooFitExtension_H__

#include <stdexcept>
#include <string>
#include <vector>

#include "RooArgSet.h"
#include "RooArgList.h"
#include "RooAbsArg.h"
#include "RooAbsPdf.h"
#include "RooProdPdf.h"
#include "RooProduct.h"
#include "RooDataSet.h"

namespace RooFitExt{
    struct ConstraintSet {
      RooArgList pdfs;
      RooArgList nuis;
      RooArgList globs;
      ConstraintSet(){
          pdfs = RooArgList();
          nuis = RooArgList();
          globs = RooArgList();
      }
    };
    
    const std::vector<std::string> kConstrPdfClsList{"RooGaussian", "RooLognormal", "RooGamma", "RooPoisson", "RooBifurGauss"};
    
    void unfoldProdPdfComponents(const RooProdPdf& prod_pdf, RooArgSet& components, int recursion_count=0,
                                 const int& recursion_limit=50);
    RooRealVar* isolateConstraintEx(const RooAbsPdf& pdf, const RooArgSet& constraints);
    RooRealVar* isolateConstraint(const RooAbsPdf& pdf, const RooArgSet& constraints);
    ConstraintSet pairConstraints(const RooArgSet& constraintPdfs, const RooArgSet& nuisanceParams,
                                  const RooArgSet& globalObs);
    void unfoldConstraints(const RooArgSet& constraintPdfs, RooArgSet& observables,
                           RooArgSet& nuisanceParams, RooArgSet* unfoldedConstraintPdfs,
                           const std::vector<std::string>constrPdfClsList=kConstrPdfClsList,
                           int recursion_count=0, const int& recursion_limit=50,
                           const bool &stripDisconnected=false);
};

        
#endif        
