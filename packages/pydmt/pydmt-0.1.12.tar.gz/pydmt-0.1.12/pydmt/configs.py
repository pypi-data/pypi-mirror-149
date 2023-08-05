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
