import logging
import re
import pkg_resources
from pkg_resources import Requirement

from .package_docker import PackageDocker
from ..output_callback import OutputCallBack
from ..util import read_text_from_file, create_file_from_content, manage_file_diff

logger = logging.getLogger()

NEWLINE = "\n"
REQUIREMENTS_TXT = "requirements.txt"
MANAGED_MESSAGE = """
# ServicefoundryManaged
# Below this line dependencies are managed by servicefoundry.
# Any package mentioned after this will get auto updated from installed packages.
# If you install a new package, that would also be auto added.
# If you uninstall a package, u have to remove them manually.
""".splitlines()

NOT_INSTALLED_MESSAGE = """
# Below package are not installed. You can safely remove these.

""".splitlines()


class SfPackage:
    def __init__(self, package_name, package_version, is_installed=False):
        self.package_name = package_name
        self.package_version = package_version
        self.is_installed = is_installed

    def update_version(self, version):
        self.is_installed = True
        self.package_version = version

    def to_str(self):
        return f"{self.package_name}=={self.package_version}"


class PackagePython(PackageDocker):
    def package(self, callback: OutputCallBack):
        if self.build_pack.dependency.auto_update:
            source_lines = read_text_from_file(REQUIREMENTS_TXT)
            target_lines = self._update_requirements_txt(source_lines)
            manage_file_diff(source_lines, target_lines, REQUIREMENTS_TXT, callback)
            create_file_from_content(REQUIREMENTS_TXT, NEWLINE.join(target_lines))

        super().package(callback)

    def _update_requirements_txt(self, source_lines):
        user_lines = []
        user_packages = set()
        sf_packages = {}
        is_managed_block = False

        # Parse source lines
        for line in source_lines:
            if re.match("^\s*#\s*ServicefoundryManaged\s*$", line):
                is_managed_block = True
            if not is_managed_block:
                user_lines.append(line)
            sline = line.strip()
            if sline.strip() != "" and re.match("^\s*#", line) is None:
                requirement = Requirement(line)
                package_name = requirement.key.lower()
                if not is_managed_block:
                    user_packages.add(package_name)
                else:
                    sf_packages[package_name] = SfPackage(
                        package_name, requirement.specs[0][1]
                    )

        # Add and update installed packages
        installed_packages = {
            d.project_name.lower(): d.version for d in pkg_resources.working_set
        }
        for package_name, package_version in installed_packages.items():
            if package_name not in user_packages:
                if package_name in sf_packages:
                    sf_packages[package_name].update_version(package_version)
                else:
                    sf_packages[package_name] = SfPackage(
                        package_name, package_version, is_installed=True
                    )

        # Generate lines.
        ret_lines = []
        for line in user_lines:
            ret_lines.append(line)
        ret_lines.extend(MANAGED_MESSAGE)
        for package_name, package in sorted(sf_packages.items()):
            if package.is_installed:
                ret_lines.append(package.to_str())
        ret_lines.extend(NOT_INSTALLED_MESSAGE)
        for package_name, package in sorted(sf_packages.items()):
            if not package.is_installed:
                ret_lines.append(package.to_str())
        return ret_lines
