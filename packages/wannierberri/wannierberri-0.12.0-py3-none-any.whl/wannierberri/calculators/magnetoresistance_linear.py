##################################################
### Magnetoresistance (linear in B and E)   ######
##################################################


from .classes import StaticCalculator
from wannierberri import covariant_formulak as frml
from wannierberri import fermiocean
from wannierberri.formula import Formula_ln,FormulaProduct, FormulaSum
from scipy.constants import  elementary_charge, hbar, electron_mass, physical_constants, angstrom
from wannierberri.covariant_formulak_basic import factor_morb
from wannierberri.__utility import  TAU_UNIT
from .static import AHC
import numpy as np




class _formula_t1E1B1_fsurf(FormulaProduct):

    def __init__(self,data_K,**kwargs_formula):
        O = frml.Omega(data_K,**kwargs_formula)
        v = data_K.covariant('Ham',commader=1)
        super().__init__( [ v,v,O] )

    def nn(self,ik,inn,out):
        vvo=super().nn(ik,inn,out)
        res = vvo
        vvo1 = np.einsum('mnabb->mna',vvo)
        for i in range(3):
            res[:,:,i,:,i] -= vvo1
            res[:,:,:,i,i] -= vvo1
        return res

class Berry(StaticCalculator):

    def __init__(self,**kwargs):
        self.Formula = _formula_t1E1B1_fsurf
        # we get the integral in eV*ang. first convert to SI (J*m), : e*1e-10
        # then multiply by tau*e^3/hbar^3
        self.factor =  TAU_UNIT*elementary_charge**4*angstrom/(hbar**3)
        self.fder = 1
        super().__init__(**kwargs)



class _formula_t1E1B1_zee_fsurf(FormulaSum):

    def __init__(self,data_K,spin=True,orb=True,**kwargs_formula):
        o = frml.Omega(data_K,**kwargs_formula)
        v = data_K.covariant('Ham', gender=1)
        w = data_K.covariant('Ham', gender=2)
        m=  data_K.covariant('magmom',gender=0,spin=spin,orb=orb,**kwargs_formula)
        dm=  data_K.covariant('magmom',gender=1,spin=spin,orb=orb,**kwargs_formula)
                
        term1 = FormulaProduct([w,m])
        term2 = FormulaProduct([v,dm],transpose=(0,2,1))
        term3 = FormulaProduct([v,dm],transpose=(2,0,1))
        super().__init__( [term1,term2,term3],[-1,0.5,0.5])


class Zeemann(StaticCalculator):

    def __init__(self,**kwargs):
        self.Formula = _formula_t1E1B1_zee_fsurf
        # we get the integral in magneton per Angstrom
        # then multiply by tau*e^3/hbar^3
        self.factor =  elementary_charge**4*angstrom/(hbar**3) # to be clarified
        self.fder = 1
        super().__init__(**kwargs)
    



class _formula_t1E1B1_zee_fsurf(FormulaSum):

    def __init__(self,data_K,spin=True,orb=True,**kwargs_formula):
        o = frml.Omega(data_K,**kwargs_formula)
        v = data_K.covariant('Ham', gender=1)
        w = data_K.covariant('Ham', gender=2)
        m=  data_K.covariant('magmom',gender=0,spin=spin,orb=orb,**kwargs_formula)
        dm=  data_K.covariant('magmom',gender=1,spin=spin,orb=orb,**kwargs_formula)
                
        term1 = FormulaProduct([w,m])
        term2 = FormulaProduct([v,dm],transpose=(0,2,1))
        term3 = FormulaProduct([v,dm],transpose=(2,0,1))
        super().__init__( [term1,term2,term3],[-1,0.5,0.5])


class Zeemann_ChemPotShift(StaticCalculator):

    class Formula(Formula_ln):
        def __init__(self):
            return data_K.covariant('Ham',gender=2)

    def __init__(self,**kwargs):
#        self.Formula = _formuula
        # we get the integral in eV per Angstrom
        # multiply by e/Ang
        # then multiply by tau*e^2/hbar^2
        self.factor =  -TAU_UNIT*elementary_charge**2/(hbar**2*angstrom) # to be clarified
        self.fder = 1
        super().__init__(**kwargs)
    


class chargeDOS(StaticCalculator):

    def __init__(self,**kwargs):
        self.Formula = frml.Identity
        self.factor =  - elementary_charge
        self.fder = 1
        super().__init__(**kwargs)




class __magmom(Formula_ln):

    def __init__(self,data_K,**kwargs):
        m = data_K.covariant('magmom', gender=0,**kwargs)
        self.update(m)

class CehmPotShift_numerator_magmom (StaticCalculator):

    def __init__(self,**kwargs):
        self.Formula = __magmom
        self.factor =  - elementary_charge
        self.fder = 1
        super().__init__(**kwargs)



class chargeDOS(StaticCalculator):

    def __init__(self,**kwargs):
        self.Formula = frml.Identity
        self.factor =  - elementary_charge
        self.fder = 1
        super().__init__(**kwargs)

# it is just a renaming
CehmPotShift_denominator = chargeDOS
    
ChemPotShooft_numerator_berry = AHC
