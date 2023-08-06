from quickstats.utils.general_enum import GeneralEnum

class WSVariables(GeneralEnum):
    VARIABLES                         = 0
    OBSERVABLES                       = 1
    POIS                              = 2
    GLOBAL_OBSERVABLES                = 3
    NUISANCE_PARAMETERS               = 4
    CONSTRAINED_NUISANCE_PARAMETERS   = 5
    UNCONSTRAINED_NUISANCE_PARAMETERS = 6
    CONSTRAINTS                       = 7
    AUXILIARY                         = 8
    CORE                              = 9
    
class SetValueMode(GeneralEnum):
    UNCHANGED = 0
    FIX       = 1
    FREE      = 2