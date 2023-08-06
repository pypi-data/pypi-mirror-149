import os

from .const import SERVICE_DEF_FILE_NAME, BUILD_DIR
from .deploy.local_deploy import deploy as local_deploy
from .deploy.remote_deploy import deploy as remote_deploy
from .output_callback import OutputCallBack
from .package.packaging_factory import package
from .parser.parser import parse
from .exceptions import ConfigurationException

LOCAL = "local"
REMOTE = "remote"


def build_and_deploy(
    base_dir="./",
    service_def_file_name=SERVICE_DEF_FILE_NAME,
    build=REMOTE,
    callback=OutputCallBack(),
):
    current_dir = os.getcwd()
    if not base_dir.endswith("/"):
        base_dir = f"{base_dir}/"
    # We will set it back to olf directory once done.
    os.chdir(base_dir)

    try:
        if not os.path.isfile(service_def_file_name):
            raise ConfigurationException(
                f"Service definition {service_def_file_name} doesn't exist in {base_dir}"
            )

        service_defs = parse(service_def_file_name)
        service_defs.write()

        build_pack = service_defs.get_build_pack()
        component = service_defs.get_component()

        callback.print_header("Packaging")
        build_dir = BUILD_DIR
        package_dir = package(build_dir, build_pack, callback)

        if build == LOCAL:
            return local_deploy(build_pack, component, package_dir, build_dir, callback)
        elif build == REMOTE:
            return remote_deploy(component, package_dir, build_dir, callback)
        else:
            raise RuntimeError(f"Unrecognised build type {build}")
    finally:
        os.chdir(current_dir)
