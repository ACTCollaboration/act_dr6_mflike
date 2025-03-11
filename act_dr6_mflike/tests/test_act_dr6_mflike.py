import os
import tempfile
import unittest

packages_path = os.environ.get("COBAYA_PACKAGES_PATH") or os.path.join(
    tempfile.gettempdir(), "act_dr6_packages"
)

# Best fit values ACT DR6
cosmo_params = {
    "cosmomc_theta": 1.040547237e-02,
    "As": 2.127445742e-09,
    "ombh2": 2.261650205e-02,
    "omch2": 1.240404189e-01,
    "ns": 9.663813976e-01,
    "tau": 5.655092745e-02,
}

foregrounds_params = {
    "a_tSZ": 3.50114277,
    "alpha_tSZ": -0.4597721879,
    "a_kSZ": 0.986604682,
    "a_p": 7.647742104,
    "beta_p": 1.86490755,
    "a_c": 3.805341822,
    "beta_c": 1.86490755,
    "a_s": 2.886594272,
    "beta_s": -2.7567784,
    "a_gtt": 7.974213801,
    "a_gte": 0.4184588365,
    "a_gee": 0.1676466062,
    "a_psee": 0.003755819497,
    "a_pste": -0.02500092711,
    "xi": 0.06424293336,
    "alpha_s": 1.0,
    "T_effd": 19.6,
    "beta_d": 1.5,
    "alpha_dT": -0.6,
    "alpha_dE": -0.4,
    "alpha_p": 1.0,
    "T_d": 9.60,
}

systematics_params = {
    "calG_all": 1.001567048,
    "cal_dr6_pa4_f220": 0.9808084654,
    "cal_dr6_pa5_f090": 1.000098497,
    "cal_dr6_pa5_f150": 0.9991342522,
    "cal_dr6_pa6_f090": 0.9998031382,
    "cal_dr6_pa6_f150": 1.001407626,
    "calE_dr6_pa4_f220": 1.0,
    "calE_dr6_pa5_f090": 0.9874026803,
    "calE_dr6_pa5_f150": 0.9975776488,
    "calE_dr6_pa6_f090": 0.9975750142,
    "calE_dr6_pa6_f150": 0.9968551529,
    "bandint_shift_dr6_pa4_f220": 6.399328024,
    "bandint_shift_dr6_pa5_f090": -0.2911716302,
    "bandint_shift_dr6_pa5_f150": -1.056426408,
    "bandint_shift_dr6_pa6_f090": 0.3121747872,
    "bandint_shift_dr6_pa6_f150": -0.4252785128,
}

nuisance_params = foregrounds_params | systematics_params
all_params = cosmo_params | nuisance_params

chi2s = {
    "tt": dict(chi2=926.36, nbin=937),
    "te-et": dict(chi2=1144.62, nbin=1175),
    "ee": dict(chi2=923.49, nbin=937),
    "tt-te-et-ee": dict(chi2=1626.42, nbin=1651),
}

likelihood_name = "act_dr6_mflike.ACTDR6MFLike"


class ACTDR6MFLikeTest(unittest.TestCase):
    def setUp(self):
        from cobaya.install import install

        install({"likelihood": {likelihood_name: None}}, path=packages_path)

    def test_act_dr6_like(self):
        import camb
        from mflike import BandpowerForeground

        camb_cosmo = cosmo_params.copy()
        camb_cosmo.update(lmax=9000, lens_potential_accuracy=1)
        pars = camb.set_params(**camb_cosmo)
        results = camb.get_results(pars)
        powers = results.get_cmb_power_spectra(pars, CMB_unit="muK")
        cl_dict = {k: powers["total"][:, v] for k, v in {"tt": 0, "ee": 1, "te": 3}.items()}

        for select, meta in chi2s.items():
            from act_dr6_mflike import ACTDR6MFLike

            my_like = ACTDR6MFLike(
                {
                    "packages_path": packages_path,
                    "data_folder": "ACTDR6MFLike/v1.0",
                    "input_file": "dr6_data.fits",
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
            fg = BandpowerForeground(my_like.get_fg_requirements())
            fg_totals = fg.get_foreground_model_totals(**nuisance_params)

            loglike = my_like.loglike(cl_dict, fg_totals, **systematics_params)
            self.assertEqual(my_like.data_vec.size, meta.get("nbin"))
            self.assertAlmostEqual(-2 * (loglike - my_like.logp_const), meta.get("chi2"), 2)

    def test_cobaya(self):
        info = {
            "debug": True,
            "likelihood": {likelihood_name: None},
            "theory": {
                "camb": {"extra_args": {"lens_potential_accuracy": 1}},
                "mflike.BandpowerForeground": {
                    "experiments": [
                        "dr6_pa4_f220",
                        "dr6_pa5_f090",
                        "dr6_pa5_f150",
                        "dr6_pa6_f090",
                        "dr6_pa6_f150",
                    ],
                    "bandint_freqs": [220, 90, 150, 90, 150],
                },
            },
            "params": all_params,
            "packages_path": packages_path,
        }
        from cobaya.model import get_model

        model = get_model(info)
        my_like = model.likelihood[likelihood_name]
        chi2 = -2 * (model.loglike(all_params, return_derived=False) - my_like.logp_const)

        self.assertEqual(my_like.data_vec.size, chi2s["tt-te-et-ee"].get("nbin"))
        self.assertAlmostEqual(chi2, chi2s["tt-te-et-ee"].get("chi2"), 2)
