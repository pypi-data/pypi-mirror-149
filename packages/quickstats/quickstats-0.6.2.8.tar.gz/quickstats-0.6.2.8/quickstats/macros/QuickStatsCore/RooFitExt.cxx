#include "RooFitExt.h"

namespace RooFitExt{
    void unfoldProdPdfComponents(const RooProdPdf& prod_pdf, RooArgSet& components, int recursion_count,
                                const int& recursion_limit){
        
        if (recursion_count >= recursion_limit)
            throw std::runtime_error( "failed to unfold product pdf components: recusion limit reached" );

        const RooArgList & pdf_list = prod_pdf.pdfList();
        if (pdf_list.getSize() == 1)
            components.add(pdf_list);
        else{
            for (auto pdf : pdf_list){
                if (strcmp(pdf->ClassName(), "RooProdPdf") == 0)
                    unfoldProdPdfComponents(*((RooProdPdf*)pdf), components, recursion_count, recursion_limit);
                else
                    components.add(*pdf);
            }
        }
    }
    RooRealVar* isolateConstraintEx(const RooAbsPdf& pdf, const RooArgSet& constraints){
        RooArgSet* components =  pdf.getComponents();
        components->remove(pdf);
        if (components->getSize()){
            for (auto c1: *components){
                for (auto c2: *components){
                    if (c1 == c2)
                        continue;
                    if (c2->dependsOn(*c1))
                        components->remove(*c1);
                }
            }
            if (components->getSize() > 1)
                throw std::runtime_error("failed to isolate proper nuisance parameter");
            else if (components->getSize() == 1)
                return (RooRealVar*) components->first();
        }
        else
            return isolateConstraint(pdf, constraints);
        return NULL;
    }

    RooRealVar* isolateConstraint(const RooAbsPdf& pdf, const RooArgSet& constraints){
        for (auto np : constraints)
            if (pdf.dependsOn(*np))
                return (RooRealVar*) np;
        return NULL;        
    }
    ConstraintSet pairConstraints(const RooArgSet& constraintPdfs, const RooArgSet& nuisanceParams,
                                  const RooArgSet& globalObs){
        ConstraintSet ret;
        for (const auto pdf : constraintPdfs){
            RooArgSet* dependentNuis = pdf->getDependents(nuisanceParams);
            if ((dependentNuis->size() > 1) || (dependentNuis->size() == 0))
                throw std::runtime_error("failed to isolate proper nuisance parameter");
            RooArgSet* dependentGlobs = pdf->getDependents(globalObs);
            if ((dependentGlobs->size() > 1) || (dependentGlobs->size() == 0))
                throw std::runtime_error("failed to isolate proper global observables");
            ret.pdfs.add(*pdf);
            ret.nuis.add(*dependentNuis->first());
            ret.globs.add(*dependentGlobs->first());
        }
        return ret;
    }
    
    void unfoldConstraints(const RooArgSet& constraintPdfs, RooArgSet& observables,
                           RooArgSet& nuisanceParams, RooArgSet* unfoldedConstraintPdfs,
                           const std::vector<std::string>constrPdfClsList,
                           int recursion_count, const int& recursion_limit,
                           const bool& stripDisconnected){
        
        if (recursion_count >= recursion_limit)
            throw std::runtime_error( "failed to unfold constraints: recusion limit reached" );
        
        for (const auto pdf : constraintPdfs){
            std::string class_name = pdf->ClassName();
            if (std::find(std::begin(constrPdfClsList), std::end(constrPdfClsList), class_name) == std::end(constrPdfClsList)){
                RooArgSet* allConstraints = ((RooAbsPdf *)pdf)->getAllConstraints(observables, nuisanceParams, stripDisconnected);
                unfoldConstraints(*allConstraints, observables, nuisanceParams, unfoldedConstraintPdfs,
                                  constrPdfClsList, recursion_count + 1, recursion_limit, stripDisconnected);
            }
            else
                unfoldedConstraintPdfs->add(*pdf);
        }
    }
};

