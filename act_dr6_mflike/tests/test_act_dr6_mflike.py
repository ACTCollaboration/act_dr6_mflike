import os
import tempfile
import unittest

packages_path = os.environ.get("COBAYA_PACKAGES_PATH") or os.path.join(
    tempfile.gettempdir(), "act_dr6_packages"
)

cosmo_params = {
    "cosmomc_theta": 0.0104085,
    "As": 2.0989031673191437e-09,
    "ombh2": 0.02237,
    "omch2": 0.1200,
    "ns": 0.9649,
    "Alens": 1.0,
    "tau": 0.0544,
}

nuisance_params = {
    "a_tSZ": 3.30,
    "a_kSZ": 1.60,
    "a_p": 6.90,
    "beta_p": 2.08,
    "a_c": 4.90,
    "beta_c": 2.20,
    "a_s": 3.10,
    "T_d": 9.60,
    "a_gtt": 8.70,
    "a_gte": 0.0,
    "a_gee": 0.0,
    "a_psee": 0.0,
    "a_pste": 0.0,
    "xi": 0.10,
    "calG_all": 1,
}
for pa in ["pa4_f150", "pa4_f220", "pa5_f090", "pa5_f150", "pa6_f090", "pa6_f150"]:
    nuisance_params.update(
        {
            f"bandint_shift_dr6_{pa}": 0,
            f"cal_dr6_{pa}": 1,
            f"calT_dr6_{pa}": 1,
            f"calE_dr6_{pa}": 1,
            f"alpha_dr6_{pa}": 0,
        }
    )

chi2s = {
    "tt": 2772.82,
    "te-et": 2554.52,
    "ee": 2382.26,
    "tt-te-et-ee": 4649.2717,
}

likelihood_name = "act_dr6_mflike.ACTDR6MFLike"


class ACTDR6MFLikeTest(unittest.TestCase):
    def setUp(self):
        from cobaya.install import install

        install({"likelihood": {likelihood_name: None}}, path=packages_path)

    def test_act_dr6_like(self):
        import camb

        camb_cosmo = cosmo_params.copy()
        camb_cosmo.update({"lmax": 9000, "lens_potential_accuracy": 1})
        pars = camb.set_params(**camb_cosmo)
        results = camb.get_results(pars)
        powers = results.get_cmb_power_spectra(pars, CMB_unit="muK")
        cl_dict = {k: powers["total"][:, v] for k, v in {"tt": 0, "ee": 1, "te": 3}.items()}

        for select, chi2 in chi2s.items():
            from act_dr6_mflike import ACTDR6MFLike

            my_like = ACTDR6MFLike(
                {
                    "packages_path": packages_path,
                    "data_folder": "ACTDR6MFLike/v0.1",
                    "input_file": "act_simu_sacc_00000.fits",
                    "defaults": {
                        "polarizations": select.upper().split("-"),
                        "scales": {
                            "TT": [2, 5000],
                            "TE": [2, 5000],
                            "ET": [2, 5000],
                            "EE": [2, 5000],
                        },
                        "symmetrize": False,
                    },
                }
            )
            loglike = my_like.loglike(cl_dict, **nuisance_params)
            self.assertAlmostEqual(-2 * (loglike - my_like.logp_const), chi2, 2)

    def test_cobaya(self):
        info = {
            "likelihood": {
                likelihood_name: {
                    "input_file": "act_simu_sacc_00000.fits",
                }
            },
            "theory": {"camb": {"extra_args": {"lens_potential_accuracy": 1}}},
            "params": cosmo_params,
            "packages_path": packages_path,
        }
        from cobaya.model import get_model

        model = get_model(info)
        my_like = model.likelihood[likelihood_name]
        chi2 = -2 * (model.loglikes(nuisance_params)[0] - my_like.logp_const)
        self.assertAlmostEqual(chi2[0], chi2s["tt-te-et-ee"], 2)
