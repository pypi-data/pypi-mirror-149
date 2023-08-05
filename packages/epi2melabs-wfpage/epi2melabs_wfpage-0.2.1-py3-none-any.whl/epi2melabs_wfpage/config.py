from traitlets.traitlets import Unicode, Bool
from traitlets.config import Configurable


class Epi2melabsWFPage(Configurable):
    """
    Allows configuration of the epi2melabs_wfpage launcher
    """
    remote = Bool(
        False, config=True,
        help="Launch wf_page in remote execution mode via labslauncher."
    )

    base_dir = Unicode(
        config=True,
        help="Sets the base directory to be used for storing server data."
    )

    workflows_dir = Unicode(
        config=True,
        help="Sets the directory to be used for storing workflows."
    )

    ip = Unicode(
        'localhost', config=True,
        help="Sets the host name for accessing labslauncher's api."
    )

    port = Unicode(
        '9993', config=True,
        help="Sets the comms port for accessing labslauncher's api."
    )