""".. module:: ACTDR6MFLike

:Synopsis: Definition of python-native CMB likelihood for ACT DR6 data release.

:Author: ACT Collaboration

"""

from mflike.mflike import _MFLike


class ACTDR6MFLike(_MFLike):
    """
    Likelihood for ACT DR6 data release (2022)
    """

    file_base_name = "act_dr6"

    _url = "https://portal.nersc.gov/cfs/sobs/users/xgarrido/act_dr6_sim"
    _release = "v0.1"
    install_options = {"download_url": f"{_url}/{_release}.tar.gz"}
