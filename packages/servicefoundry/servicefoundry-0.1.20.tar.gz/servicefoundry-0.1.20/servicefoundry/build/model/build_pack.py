class BuildPack:
    def __init__(self, type, dependency, docker, ignorePatterns, localRunCommand):
        self.type = type
        self.dependency = Dependency(**dependency)
        self.docker = Docker(**docker)
        self.ignore_patterns = ignorePatterns
        self.local_run_command = localRunCommand


class Dependency:
    def __init__(self, autoUpdate):
        self.auto_update = autoUpdate


class Docker:
    def __init__(self, dockerFileContent, fileName, overwrite):
        self.docker_file_content = dockerFileContent
        self.file_name = fileName
        self.overwrite = overwrite
