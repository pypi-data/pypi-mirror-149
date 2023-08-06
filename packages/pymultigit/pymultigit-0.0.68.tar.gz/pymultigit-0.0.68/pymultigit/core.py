import glob
import os
import os.path
import subprocess
import sys
from typing import Tuple, Generator

import git

from pymultigit.configs import ConfigOutput, ConfigDebug, ConfigGrep, ConfigPull, ConfigMain


def projects(sort: bool) -> Generator[Tuple[str, str], None, None]:
    """
    the method returns tuples of (project_name, project_dir)
    """
    if ConfigMain.use_glob:
        repos_list = [os.path.dirname(x) for x in glob.glob('*/.git')]
    else:
        repos_list = ConfigMain.folders
    if sort:
        repos_list.sort()
    for x in repos_list:
        yield x, x


def run(args, do_exit=True) -> Tuple[str, str, int]:
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        (res_out, res_err) = p.communicate()
        res_out = res_out.decode()
        res_err = res_err.decode()
        if p.returncode:
            print(f'errors while running [{args}]...')
            print(res_out, end='', file=sys.stderr)
            print(res_err, end='', file=sys.stderr)
            if do_exit:
                sys.exit(p.returncode)
    return res_out, res_err, p.returncode


def do_count(fnc, attr_name, not_attr_name, attr_plural, print_attr, print_not_attr) -> None:
    count = 0
    count_attr = 0
    for (project_name, project_dir) in projects(sort=ConfigMain.sort):
        count += 1
        repo = git.Repo(project_dir)
        attr = fnc(repo)
        if attr:
            count_attr += 1
        if attr:
            if print_attr:
                if ConfigOutput.terse:
                    print(project_name)
                else:
                    print(f'project [{project_name}] {attr_name}')
        else:
            if print_not_attr:
                if ConfigOutput.terse:
                    print(project_name)
                else:
                    print(f'project [{project_name}] {not_attr_name}')
    if ConfigOutput.stats:
        print(f'scanned [{count}] projects')
        print(f'[{count_attr}] projects {attr_plural}')


def do_for_all_projects(fnc) -> None:
    count = 0
    count_not_found = 0
    count_error = 0
    count_ok = 0
    orig_dir = os.getcwd()
    for (project_name, project_dir) in projects(sort=ConfigMain.sort):
        if ConfigOutput.output:
            print(f"[{project_name}] at [{project_dir}]...")
        count += 1
        if os.path.isdir(project_dir):
            os.chdir(project_dir)
            try:
                fnc(project_name, project_dir)
                count_ok += 1
                if ConfigDebug.debug_verbose:
                    print('OK')
            # this is one of the rare cases in which we really want to catch all exceptions.
            # pylint: disable=broad-except
            # noinspection PyBroadException
            except Exception:
                count_error += 1
                if ConfigDebug.debug_verbose:
                    print('ERROR')
            os.chdir(orig_dir)
        else:
            if ConfigDebug.debug_verbose:
                print('NOT FOUND')
            count_not_found += 1
    if ConfigOutput.stats:
        print(f'scanned [{count}] projects')
        print(f'[{count_not_found}] not found')
        print(f'[{count_error}] error')
        print(f'[{count_ok}] ok')


def print_projects_that_return_true(fnc) -> None:
    orig_dir = os.getcwd()
    for (project_name, project_dir) in projects(sort=ConfigMain.sort):
        if os.path.isdir(project_dir):
            os.chdir(project_dir)
            res, extra = fnc()
            if res:
                if ConfigOutput.terse:
                    print(project_name)
                else:
                    print(f"project [{project_name}] at folder [{project_dir}]")
                if not ConfigOutput.terse:
                    print(extra, end="")
            os.chdir(orig_dir)


def is_dirty(repo) -> bool:
    return repo.is_dirty()


def has_untracked_files(repo) -> bool:
    return len(repo.untracked_files) > 0


def non_synchronized_with_upstream(_repo: str) -> bool:
    return False


def do_build_bootstrap(_project_name: str, _project_dir: str) -> None:
    disable = ".build.disable"
    if os.path.isfile(disable):
        return True
    if os.path.isfile("bootstrap"):
        ret = subprocess.call(["./bootstrap"])
        return ret == 0
    print("not a boostrap folder (bootstrap not there)")
    return True


def do_build_pydmt(_project_name: str, _project_dir: str) -> None:
    disable = ".build.disable"
    if os.path.isfile(disable):
        return True
    if os.path.isfile(".pydmt.config"):
        ret = subprocess.call([
            "pydmt",
            "build",
        ])
        return ret == 0
    print("not a pydmt folder (.pydmt.config not there)")
    return True


def do_build_venv_make(_project_name: str, _project_dir: str) -> None:
    disable = ".build.disable"
    if os.path.isfile(disable):
        return True
    if os.path.isfile("Makefile") and os.path.isdir(".venv/default"):
        ret = subprocess.call([
            "venv-run",
            "--venv",
            ".venv/default",
            "--",
            "make",
        ])
        return ret == 0
    print("not a make venv folder (either Makefile or .venv/default is not there)")
    return True


def do_build_make(_project_name: str, _project_dir: str) -> None:
    disable = ".build.disable"
    if os.path.isfile(disable):
        return True
    if os.path.isfile("Makefile"):
        ret = subprocess.call(["make"])
        return ret == 0
    print("not a make folder (Makefile not there)")
    return True


def do_pull(_project_name: str, _project_dir: str) -> int:
    args = ['git', 'pull']
    if ConfigDebug.git_verbose:
        args.append('--verbose')
    if ConfigPull.pull_quiet:
        args.append('--quiet')
    return subprocess.call(args)


def do_check_workflow_exists_for_makefile() -> Tuple[bool, str]:
    if os.path.isfile("Makefile"):
        if not os.path.isfile(".github/workflows/build.yml"):
            return True, ""
    return False, ""


def do_grep(_project_name: str, project_dir: str) -> None:
    args = ['git', 'grep']
    if ConfigDebug.git_verbose:
        args.append('--verbose')
    if ConfigDebug.git_quiet:
        args.append('--quiet')
    args.append(ConfigGrep.regexp)
    if ConfigGrep.files is not None:
        args.extend([
            "--",
            ConfigGrep.files
        ])
    with subprocess.Popen(
        args,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as pipe:
        for line in pipe.stdout:
            print(f"{project_dir}/{line.decode()}", end="")
        if pipe.returncode:
            raise subprocess.CalledProcessError(
                returncode=pipe.returncode,
                cmd=' '.join(args),
            )


def do_local_branch(_project_name: str, _project_dir: str) -> int:
    args = ['git', 'branch', '--show-current']
    if ConfigDebug.git_verbose:
        args.append('--verbose')
    if ConfigDebug.git_quiet:
        args.append('--quiet')
    return subprocess.check_output(args).decode().strip()


def do_remote_branch(_project_name: str, _project_dir: str) -> int:
    args = ['git', 'branch', '--remotes', '--show-current']
    if ConfigDebug.git_verbose:
        args.append('--verbose')
    if ConfigDebug.git_quiet:
        args.append('--quiet')
    return subprocess.check_output(args).decode().strip()


def do_github_branch(_project_name: str, _project_dir: str) -> int:
    """
    https://stackoverflow.com/questions/28666357/git-how-to-get-default-branch
    """
    args = ['gh', 'repo', 'view', '--json', 'defaultBranchRef', '--jq', '.defaultBranchRef.name',]
    return subprocess.check_output(args).decode().strip()


def do_clean(_project_name: str, _project_dir: str) -> int:
    args = ['git', 'clean', '-ffxd']
    # if ConfigDebug.git_verbose:
    #     args.append('--verbose')
    # if ConfigDebug.git_quiet:
    #     args.append('--quiet')
    return subprocess.check_call(args)


def do_status() -> Tuple[bool, str]:
    (res_out, res_err, _) = run([
        'git',
        'status',
        # porcelain is guaranteed to have parsable output and not
        # change across git versions
        '--porcelain',
        # when using --porcelain branch information is not shown,
        # this flag makes it not so, the problem with it is that
        # it produces output which should be parsed and that is
        # why we do not used it and use the 'git rev-list' that follows...
        # '--branch'
        # '--short',
    ])
    if res_out != '' or res_err != '':
        return True, res_out + res_err
    (res_out, res_err, _) = run([
        'git',
        'rev-list',
        '--left-only',
        '--count',
        '@...@{upstream}',
    ])
    if res_out != '0\n' or res_err != '':
        return True, res_out + res_err
    return False, ""


def do_dirty() -> Tuple[bool, str]:
    args = ['git', 'status', '--porcelain']
    if ConfigDebug.git_verbose:
        args.append('--verbose')
    if ConfigDebug.git_quiet:
        args.append('--quiet')
    output = subprocess.check_output(args, stderr=subprocess.DEVNULL).decode()
    return output != '', output
