"""
main
"""

from pytconf import register_endpoint
from pytconf import register_main, config_arg_parse_and_launch
import pylogconf.core


from pymultigit.configs import ConfigDebug, ConfigGrep, ConfigMain, ConfigOutput
from pymultigit.core import do_count, is_dirty, has_untracked_files, non_synchronized_with_upstream, \
    do_for_all_projects, do_clean, do_status, do_dirty, do_pull, do_grep, do_local_branch, \
    do_remote_branch, print_projects_that_return_true, do_github_branch, do_check_workflow_exists_for_makefile, \
    do_build_bootstrap, do_build_pydmt, do_build_make, do_build_venv_make
from pymultigit.static import DESCRIPTION, APP_NAME, VERSION_STR


@register_endpoint(
    configs=[ConfigDebug],
    description="Show the status of multiple git repositories",
)
def count_dirty() -> None:
    do_count(
        is_dirty,
        'is dirty',
        'is clean',
        'were dirty',
        True,
        False,
    )


@register_endpoint(
    configs=[ConfigDebug],
    description="Show which repositories have untracked files",
)
def untracked() -> None:
    do_count(
        has_untracked_files,
        'has untracked files',
        'is fully tracked',
        'have untracked files',
        True,
        False,
    )


@register_endpoint(
    configs=[
        ConfigDebug,
        ConfigMain,
        ConfigOutput,
    ],
    description="Show which local branch we are on",
)
def local_branch() -> None:
    do_for_all_projects(do_local_branch)


@register_endpoint(
    configs=[
        ConfigDebug,
        ConfigMain,
        ConfigOutput,
    ],
    description="Show which local branch we are on",
)
def remote_branch() -> None:
    do_for_all_projects(do_remote_branch)


@register_endpoint(
    configs=[
        ConfigDebug,
        ConfigMain,
        ConfigOutput,
    ],
    description="Show the branch on the github side",
)
def github_branch() -> None:
    do_for_all_projects(do_github_branch)


@register_endpoint(
    configs=[ConfigDebug],
    description="Show which repositories are synchronized with their upstream",
)
def synchronized() -> None:
    do_count(
        non_synchronized_with_upstream,
        'is behind upstream',
        'is synchronized',
        'are behind upstream',
        True,
        False,
    )


@register_endpoint(
    configs=[
        ConfigDebug,
        ConfigMain,
        ConfigOutput,
    ],
    description="Clean all projects",
)
def clean() -> None:
    do_for_all_projects(do_clean)


@register_endpoint(
    configs=[ConfigDebug],
    description="Show the status of multiple git repositories",
)
def status() -> None:
    print_projects_that_return_true(do_status)


@register_endpoint(
    configs=[ConfigDebug],
    description="Show names of project which are dirty",
)
def dirty() -> None:
    print_projects_that_return_true(do_dirty)


@register_endpoint(
    configs=[
        ConfigDebug,
        ConfigMain,
        ConfigOutput,
    ],
    description="run pydmt build on repos",
)
def build_pydmt() -> None:
    do_for_all_projects(do_build_pydmt)


@register_endpoint(
    configs=[
        ConfigDebug,
        ConfigMain,
        ConfigOutput,
    ],
    description="run bootstrap build on repos",
)
def build_bootstrap() -> None:
    do_for_all_projects(do_build_bootstrap)


@register_endpoint(
    configs=[
        ConfigDebug,
        ConfigMain,
        ConfigOutput,
    ],
    description="run make build on repos",
)
def build_make() -> None:
    do_for_all_projects(do_build_make)


@register_endpoint(
    configs=[
        ConfigDebug,
        ConfigMain,
        ConfigOutput,
    ],
    description="run make build on repos",
)
def build_venv_make() -> None:
    do_for_all_projects(do_build_venv_make)


@register_endpoint(
    configs=[
        ConfigDebug,
        ConfigOutput,
        ConfigMain,
    ],
    description="Pull changes for multiple git repositories",
)
def pull() -> None:
    do_for_all_projects(do_pull)


@register_endpoint(
    configs=[],
    description="Check various things",
)
def check_workflow_exists_for_makefile() -> None:
    print_projects_that_return_true(do_check_workflow_exists_for_makefile)


@register_endpoint(
    configs=[
        ConfigDebug,
        ConfigMain,
        ConfigOutput,
        ConfigGrep],
    description="Grep multiple repositories for pattern",
)
def grep() -> None:
    do_for_all_projects(do_grep)


@register_endpoint(
    configs=[ConfigDebug],
    description="List all projects",
)
def list_projects() -> None:
    print_projects_that_return_true(lambda: (True, ""))


@register_main(
    main_description=DESCRIPTION,
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    pylogconf.core.setup()
    config_arg_parse_and_launch()


if __name__ == '__main__':
    main()
