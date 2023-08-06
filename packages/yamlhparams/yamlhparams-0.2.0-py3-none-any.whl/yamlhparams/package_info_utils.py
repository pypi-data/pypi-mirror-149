import logging
import subprocess
import os
import sys
import pkgutil

logger = logging.getLogger(__name__)


class VersionController(object):
    def __init__(self, package_name):
        self.package_name = package_name
        self.package_loader = pkgutil.get_loader(package_name)
        if self.package_loader is None:
            raise ImportError(f"Cannot find loader for package '{package_name}'.")
        self.git_path = os.path.split(os.path.split(self.package_loader.path)[0])[0]
        self._mem_path = None

    def __str__(self):
        return f"VersionController(package_name={self.package_name}, git_path={self.git_path})"

    def __enter__(self):
        self._mem_path = os.getcwd()
        os.chdir(self.git_path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self._mem_path)
        self._mem_path = None

    def find_package_version(self, tries=('__version__', '__VERSION__')):
        module = sys.modules.get(self.package_name) or self.package_loader.load_module()
        package_version = None
        for try_ in tries:
            package_version = getattr(module, try_, None)
            if package_version:
                break
        if not package_version:
            raise ImportError("Could not find version attribute "
                              f"in top-level of package '{self.package_name}' with tries {tries}.")
        else:
            return package_version

    def check_git(self):
        return bool(self.git_query("git status")) and \
               os.path.exists(self.git_path + "/.git")

    def git_query(self, string):
        with self:
            try:
                p = subprocess.Popen(string.split(),
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                out, err = p.communicate()
            except FileNotFoundError:
                return None
            if not out:
                return None
            out = out.decode("utf-8").strip(" \n")
        return out

    @property
    def remote_url(self):
        return self.git_query("git config --get remote.origin.url")

    @property
    def current_commit(self):
        return self.git_query("git rev-parse --short HEAD")

    @property
    def latest_remote_commit(self):
        url = self.remote_url
        commit = self.git_query("git ls-remote {} refs/heads/{}".format(
            url, self.branch
        ))
        if commit is None:
            raise OSError("Could not determine latest commit, did not find git.")
        return commit[:7]

    @property
    def branch(self):
        return self.git_query("git symbolic-ref --short HEAD")
