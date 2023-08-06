import logging
import os
from io import StringIO
from ruamel.yaml import YAML, CommentedMap
from yamlhparams import VersionController

logger = logging.getLogger(__name__)


def _check_and_set_version(hparams, package_name, package_info_group='__package_info__'):
    vc = VersionController(package_name)
    package_version = vc.find_package_version()
    info = {"package": package_name, "version": str(package_version)}
    if vc.check_git():
        info.update({'git': {'commit': vc.current_commit, 'branch': vc.branch}})
    else:
        logger.warning(f"Parent directory of the '{package_name}' package is not a git repository or "
                       f"Git is not installed. Git information will not be added to this hyperparameter file.")
    if package_info_group not in hparams:
        e = f"Could not infer the software version used to produce the " \
            f"hyperparameter file of this project as the '{package_info_group}' " \
            f"group is not specified in the file. Using a later " \
            f"version of the '{package_name}' package software with this project " \
            f"may produce unexpected results. " \
            f"Package info: {info} will be automatically " \
            f"added to the hyperparameter file now."
        logger.warning(e)
        hparams.insert(0, f"{package_info_group}", info)
    hp_version = hparams.get_group(f"{package_info_group}/version")
    if isinstance(hp_version, str) and package_version != hp_version:
        e = f"Parameter file indicates that this project was created " \
            f"under {package_name} version {hp_version}, but the current " \
            f"version is {package_version}. If you wish to continue " \
            f"using this software version on this project dir, " \
            f"manually update to the following lines in the hyperparameter " \
            f"file:\n\n{package_info_group}:\n  version: {package_version}\n"
        logger.warning(e)
        raise RuntimeWarning(e)
    hparams.set_group(f"{package_info_group}", info, overwrite=True)
    hparams.save_current()
    return hp_version


class YAMLHParams(CommentedMap):
    def __init__(self, yaml_path: str,
                 version_control_package_name: str = None,
                 check_deprecated_params_func: callable = None):
        self.yaml_path = os.path.abspath(yaml_path)
        if not os.path.exists(yaml_path):
            raise OSError(f"YAML path '{self.yaml_path}' does not exist")
        with open(self.yaml_path, "r", encoding="utf-8") as in_f:
            temp_map = YAML(typ='rt').load(in_f)
            super().__init__(temp_map)
            temp_map.copy_attributes(self)
        logger.info(f"YAMLHParams path: {self.yaml_path}")
        if callable(check_deprecated_params_func):
            check_deprecated_params_func(self)
        if version_control_package_name:
            logger.info(f"Running version control check on package '{version_control_package_name}'")
            _check_and_set_version(self, version_control_package_name)

    @classmethod
    def new(cls, yaml_path, make_parents=False, overwrite=False, **init_kwargs):
        yaml_path = os.path.abspath(yaml_path)
        parent_dir = os.path.split(yaml_path)[0]
        if not os.path.exists(parent_dir):
            if make_parents:
                os.makedirs(parent_dir)
            else:
                raise OSError(f"Parent directory {parent_dir} does not exist, "
                              f"and 'make_parents=False' was passed.")
        if not os.path.splitext(yaml_path)[-1] == ".yaml":
            raise ValueError(f"Got yaml_path '{yaml_path}' with extension != '.yaml'.")
        if os.path.exists(yaml_path) and not overwrite:
            raise OSError(f"File already exists at path {yaml_path}.")
        with open(yaml_path, "w") as out_f:
            out_f.write("{}\n")
        return YAMLHParams(yaml_path, **init_kwargs)

    def __str__(self):
        string_rep = StringIO()
        temp_map = CommentedMap(self)
        self.copy_attributes(temp_map)
        YAML(typ="rt").dump(temp_map, string_rep)
        string_rep = string_rep.getvalue().split("\n")
        processed = []
        for i, line in enumerate(string_rep):
            # Separate each top-level group by 1 newline
            if len(line) > 0 \
                    and line[0] != " " \
                    and i != 0 \
                    and len(string_rep[i-1]) > 0 \
                    and string_rep[i-1][0] not in ("#", "\n"):
                line = f"\n{line}"
            processed.append(line)
        return "\n".join(processed)

    @staticmethod
    def _standardized_path(path):
        return "/" + path.lstrip("/").rstrip("/").strip()

    def get_group(self, path, make_if_missing=False):
        path = self._standardized_path(path)
        if path == "/":
            return self
        keys = list(filter(None, path.split('/')))
        group = self
        for i, key in enumerate(keys):
            value = group.get(key, None) if hasattr(group, "get") else None
            if value is None:
                if make_if_missing:
                    group[key] = CommentedMap()
                    value = group[key]
                else:
                    raise KeyError(f"Missing group '{key}' in path '{path}' and "
                                   f"parameter 'make_if_missing' is set False.")
            group = value
        return group

    def set_group(self, key_or_path, value, overwrite=True, missing_parents_ok=True):
        org_key_or_path = key_or_path
        key_or_path = self._standardized_path(key_or_path)
        path_to_group, key = key_or_path.rsplit('/', 1)
        if not key:
            raise ValueError("Must specify a path with a key, e.g., '/my_group' and not e.g., '/'. "
                             f"Got full path '{org_key_or_path}'")
        group = self.get_group(path_to_group or "/", make_if_missing=missing_parents_ok)
        if group.get(key, None) is not None and not overwrite:
            raise ValueError(f"A value already exists at path '{org_key_or_path}' "
                             f"and parameter 'overwrite' is set False")
        logger.info(f"Setting group with value '{value}' at path '{org_key_or_path}'")
        group[key] = value

    def delete_group(self, key_or_path, non_existing_ok=False):
        key_or_path = self._standardized_path(key_or_path)
        parent, key = key_or_path.rsplit("/", 1)
        if not parent:
            group = self
        else:
            group = self.get_group(parent, non_existing_ok)
        try:
            group.__delitem__(key)
        except KeyError:
            if not non_existing_ok:
                raise KeyError(f"Key '{key}' does not exist in requested group and cannot be deleted. "
                               f"If this is ok, specify 'non_existing_ok=True'.")

    def save_current(self, out_path=None, return_copy=True):
        # Write current hparams version to file
        out_path = os.path.abspath(out_path or self.yaml_path)
        logger.info(f"Saving current YAMLHParams to file: {out_path}")
        with open(out_path, "w") as out_f:
            out_f.write(str(self))
        if return_copy:
            return YAMLHParams(out_path)
