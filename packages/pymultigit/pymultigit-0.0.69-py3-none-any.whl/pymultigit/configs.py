"""
All configurations for pymultigit
"""


from pytconf import Config, ParamCreator


class ConfigOutput(Config):
    """
    Parameters to control output
    """
    terse = ParamCreator.create_bool(
        help_string="be terse?",
        default=False,
    )
    stats = ParamCreator.create_bool(
        help_string="show statistics are the end?",
        default=False,
    )
    output = ParamCreator.create_bool(
        help_string="show projects?",
        default=True,
    )
    print_not = ParamCreator.create_bool(
        help_string="print what the project is not",
        default=False,
    )


class ConfigDebug(Config):
    """
    Parameters for debug
    """
    debug_verbose = ParamCreator.create_bool(
        help_string="be verbose?",
        default=False,
    )
    git_verbose = ParamCreator.create_bool(
        help_string="add --verbose when running git?",
        default=False,
    )
    git_quiet = ParamCreator.create_bool(
        help_string="add --quiet when running git?",
        default=False,
    )


class ConfigMain(Config):
    """
    Main parameters
    """
    sort = ParamCreator.create_bool(
        help_string="sort results by project name?",
        default=True,
    )
    glob = ParamCreator.create_str(
        help_string="what glob to use?",
        default="*/*.git"
    )
    use_glob = ParamCreator.create_bool(
        help_string="Should I use glob or list of folders?",
        default=True,
    )
    folders = ParamCreator.create_list_str(
        help_string="what list of folders to use?",
        default=[],
    )


class ConfigGrep(Config):
    """
    Parameters for the grep command
    """

    regexp = ParamCreator.create_str(
        help_string="what regexp to look for?",
    )
    files = ParamCreator.create_str_or_none(
        help_string="what regexp to look for?",
        default=None,
    )


class ConfigPull(Config):
    """
    Parameters for the pull command
    """

    pull_quiet = ParamCreator.create_bool(
        help_string="add --quiet when running git?",
        default=True,
    )
