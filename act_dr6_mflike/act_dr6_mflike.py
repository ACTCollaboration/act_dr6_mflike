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

    def initialize_non_sampled_params(self):
        self.non_sampled_params = {"calG_all": 1}
        for exp in self.experiments:
            self.non_sampled_params.update({f"calT_{exp}": 1.0, f"alpha_{exp}": 0.0})

    def initialize_with_params(self):
        self.initialize_non_sampled_params()

        # Remove the parameters if it appears in the input/samples ones
        for par in self.input_params:
            self.non_sampled_params.pop(par, None)

        # Finally set the list of nuisance params
        self.expected_params_nuis = [
            par for par in self.expected_params_nuis if par not in self.non_sampled_params
        ]
        super().initialize_with_params()

    def loglike(self, cl, **params_values_nocosmo):
        # This is needed if someone calls the function without initializing the likelihood
        # (typically a call with a precomputed Cl and no cobaya initialization steps e.g
        # test_act_dr6_mflike)
        if not hasattr(self, "non_sampled_params"):
            self.initialize_non_sampled_params()

        params_values_nocosmo = self.non_sampled_params | params_values_nocosmo
        return super().loglike(cl, **params_values_nocosmo)
