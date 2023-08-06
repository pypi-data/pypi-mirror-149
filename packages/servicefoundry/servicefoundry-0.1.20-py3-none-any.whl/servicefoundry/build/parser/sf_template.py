import os
import re
import yaml
import shutil
from jsonschema.exceptions import ValidationError
from mako.template import Template

from .generated_definition import GeneratedDefinition
from .sf_definition import SFDefinition
from .template_parameters import get_template_parameter
from .util import get_template_file, load_yaml_from_file, validate_schema
from ..exceptions import ConfigurationException

SPEC = "spec"
OVERWRITES = "overwrites"


class Parameters(dict):
    def __init__(self, *args, **kwargs):
        super(Parameters, self).__init__(*args, **kwargs)
        self.__dict__ = self


class SfTemplate:
    def __init__(self, template_id, template_folder, template):
        self.template_id = template_id
        self.template_folder = template_folder
        try:
            validate_schema(template, "schema/template_schema.json")
        except ValidationError as err:
            raise ConfigurationException(f"Template validation failed. {err.message}")

        spec = template[SPEC]
        self.base_build = spec["baseBuild"]
        self.base_component = spec["baseComponent"]
        self.post_init_instruction = spec["postInitInstruction"]
        self.overwrite = spec[OVERWRITES]
        self.parameters = [
            get_template_parameter(parameter) for parameter in spec["parameters"]
        ]

    def generate_service_def(self, sf_definition: SFDefinition):
        parameters = Parameters(sf_definition.parameters)
        base_build_id = self.base_build
        base_component_id = self.base_component
        resolved_overrides = self._resolve_variables(self.overwrite, parameters)
        if sf_definition.overwrites:
            resolved_overrides.extend(
                self._resolve_variables(sf_definition.overwrites, parameters)
            )

        definition = GeneratedDefinition(
            base_build_id, base_component_id, resolved_overrides
        )
        return definition

    def generate_project(self, parameters):
        # Create new folder to hold template and rendered values.
        project_folder = parameters.get("service_name", f"{self.template_id}_service")

        if os.path.exists(project_folder):
            raise ConfigurationException(
                f"Failed to initialize project. Directory {project_folder} already exist."
            )
        else:
            shutil.copytree(self.template_folder, project_folder)
            os.remove(f"{project_folder}/template.yaml")
            # Write parameters into servicefoundry.yaml
            with open(f"{project_folder}/servicefoundry.yaml", "w") as template_file:
                yaml.dump(
                    {
                        "template": f"truefoundry.com/v1/{self.template_id}",
                        "parameters": parameters,
                    },
                    template_file,
                    sort_keys=False,
                )
            return project_folder

    def _resolve_variables(self, overwrite_dict, parameters):
        resolved_values = []
        for overwrite_key, overwrite_value in overwrite_dict.items():
            resolved_values.append(
                (
                    overwrite_key,
                    self._resolve_variable(overwrite_key, overwrite_value, parameters),
                )
            )
        return resolved_values

    def _resolve_variable(self, key, value, parameters):
        if isinstance(value, dict):
            ret_value = {}
            for k, v in value.items():
                ret_value[k] = self._resolve_variable(key, v, parameters)
            return ret_value
        if isinstance(value, list):
            ret_value = []
            for item in value:
                ret_value.append(self._resolve_variable(key, item, parameters))
            return ret_value
        if isinstance(value, (int, float)):
            return value
        # Check if it's a simple substitution
        match = re.match("^\$\{parameters\.([A-Za-z0-9]+)\}$", value)
        if match:
            variable = match.group(1)
            if variable in parameters:
                return parameters[variable]
            else:
                raise ConfigurationException(
                    f"Failed to parse {key}. Parameters doesn't have {variable}"
                )
        try:
            template = Template(value)
            return template.render(parameters=parameters)
        except AttributeError as e:
            raise ConfigurationException(f"Failed to parse {key}. {e}")

    @classmethod
    def get_template(cls, template_name):
        split = template_name.split("/")
        if len(split) != 3:
            raise ConfigurationException(f"Incorrect template {template_name}")
        template_id = split[2]
        template_folder = get_template_file(template_id)
        template_yaml = load_yaml_from_file(f"{template_folder}/template.yaml")
        return cls(template_id, template_folder, template_yaml)
