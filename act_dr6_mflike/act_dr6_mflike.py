""".. module:: ACTDR6MFLike

:Synopsis: Definition of python-native CMB likelihood for ACT DR6 data release.

:Author: ACT Collaboration

"""
from mflike import MFLike

class ACTDR6MFLike(MFLike):
    """
    Likelihood for ACT DR6 data release (2022)
    """

    file_base_name = "act_dr6"

    _url = "https://portal.nersc.gov/cfs/sobs/users/xgarrido/act_dr6_sim"
    _release = "v0.1"
    install_options = {"download_url": f"{_url}/{_release}.tar.gz"}

    # finding correspondence between the general MFLike naming convention
    # and specific ACT DR6 one
    renames: dict

    def initialize(self):
        super().initialize()

        self.renames = {}
        # calE corresponds to the polarization efficiency
        self.renames.update({f"calE_{exp}": f"pol_eff_{exp}" for exp in self.experiments}) 
        # calG_all is the dipole calibration of Planck
        self.renames.update({"calG_all": "A_Planck"})
        
        self.expected_params_nuis = [
                self.translate_param(par) for par in self.expected_params_nuis
         ]
        


    def translate_param(self, p):
        # Translates parameters with the above conventions
        return self.renames.get(p, p)

    def find_translation(self, p: str) -> str:
        """
        Checks if a parameter can be renamed, and returns the source param if so.
        In other words, if find_translation(p) == q, then translate_param(q) = p.
        """
        for k, v in self.renames.items():
            if v == p:
                return k
        return p


    def loglike(self, cl, **params_values_nocosmo):
        # Translating back params to the LAT_MFLike convention to pass them to the 
        # inherited class

        params_values_nocosmo_translated = {self.find_translation(k): params_values_nocosmo[k] 
            for k in params_values_nocosmo.keys()}
        
        return super().loglike(cl, **params_values_nocosmo_translated)
