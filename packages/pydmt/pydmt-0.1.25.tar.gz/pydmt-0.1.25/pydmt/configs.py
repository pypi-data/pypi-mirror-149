"""
All configurations for pydmt
"""


from pytconf import Config, ParamCreator


class ConfigSudo(Config):
    """
    Parameters to control whether we use 'sudo' or not
    """
    sudo = ParamCreator.create_bool(
        help_string="use sudo?",
        default=True,
    )


class ConfigFlow(Config):
    """
    Parameters to configure the flow of pydmt
    """
    stop_after_error = ParamCreator.create_bool(
        help_string="Should pydmt stop after first error?",
        default=True,
    )


class ConfigOutput(Config):
    """
    Parameters to configure the output of pydmt
    """
    verbose = ParamCreator.create_bool(
        help_string="Should output be verbose?",
        default=False,
    )
