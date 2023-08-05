"""
Container for object classes used in cs18-api-client
"""
import abc
from typing import List, Optional
import dateutil.parser


class AccessLink:
    def __init__(self, protocol: str, link: str):
        self.link = link
        self.protocol = protocol


class Commit:
    def __init__(self, data: dict):
        self.sha = data["sha"]
        self.author = data["commit"]["author"]["name"]
        self.date = dateutil.parser.parse(data["commit"]["author"]["date"])
        self.comment = data["commit"]["message"]

    def __str__(self):
        return "{0}: [{1}] {2}".format(self.date, self.sha[:7], self.comment)


class ColonyAccount:
    def __init__(
            self, account: str, email: str, password: str, first_name: str, last_name: str
    ):
        self.account = account
        self.default_space = "Trial"
        self.sample_space = "Sample"
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    @property
    def display_first_name(self):
        return self.first_name or self.email

    @property
    def display_last_name(self):
        return self.last_name



class BlueprintRepositoryDetails:
    def __init__(self, repository_url: str, access_token: str, repository_type: str, branch: str = None):
        self.repository_url = repository_url
        self.repository_type = repository_type
        self.access_token = access_token
        self.branch = branch


class BitbucketBlueprintRepositoryDetails:
    def __init__(self, auth_code: str, redirect_url: str, blueprint_repository_details: BlueprintRepositoryDetails):
        self.blueprint_repository_details = blueprint_repository_details
        self.auth_code = auth_code
        self.redirect_url = redirect_url


class GitlabBlueprintRepositoryDetails:
    def __init__(self, auth_code: str, redirect_url: str, blueprint_repository_details: BlueprintRepositoryDetails):
        self.blueprint_repository_details = blueprint_repository_details
        self.auth_code = auth_code
        self.redirect_url = redirect_url


class AddAccountBlueprintRepositoryRequest(abc.ABC):
    def __init__(self, name: str, repository_url: str, allow_sharing: bool,
                 open_access: bool):
        self.name = name
        self.repository_url = repository_url
        self.open_access = open_access
        self.allow_sharing = allow_sharing


class AddBlueprintUsingTokenRepositoryRequest(AddAccountBlueprintRepositoryRequest):
    def __init__(self, name: str, repository_url: str, allow_sharing: bool,
                 open_access: bool, access_token: str, repository_type: str):
        super().__init__(name, repository_url, allow_sharing, open_access)
        self.repository_type = repository_type
        self.access_token = access_token


class AddBlueprintGithubRepositoryRequest(AddAccountBlueprintRepositoryRequest):
    def __init__(self, name: str, repository_url: str, allow_sharing: bool,
                 open_access: bool, code: str, state: str):
        super().__init__(name, repository_url, allow_sharing, open_access)
        self.code = code
        self.state = state


class AddBlueprintBitbucketRepositoryRequest(AddAccountBlueprintRepositoryRequest):
    def __init__(self, name: str, repository_url: str, allow_sharing: bool,
                 open_access: bool, code: str, redirection_url: str):
        super().__init__(name, repository_url, allow_sharing, open_access)
        self.code = code
        self.redirection_url = redirection_url


class AddBlueprintGitlabRepositoryRequest(AddAccountBlueprintRepositoryRequest):
    def __init__(self, name: str, repository_url: str, allow_sharing: bool,
                 open_access: bool, code: str, redirection_url: str):
        super().__init__(name, repository_url, allow_sharing, open_access)
        self.code = code
        self.redirection_url = redirection_url


class TerraformModuleInput(abc.ABC):
    def __init__(self, name: str, value: str,
                 optional: bool,
                 overridable: bool, display_style: str, description: str = None):
        self.display_style = display_style
        self.overridable = overridable
        self.optional = optional
        self.description = description
        self.value = value
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, TerraformModuleInput):
            return NotImplemented

        return self.display_style == other.display_style and \
               self.overridable == other.overridable and \
               self.optional == other.optional and \
               self.description == other.description and \
               self.value == other.value and \
               self.name == other.name


class TerraformModuleOutput(abc.ABC):
    def __init__(self, name: str, display_style: str, description: str = None):
        self.description = description
        self.display_style = display_style
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, TerraformModuleInput):
            return NotImplemented

        return self.display_style == other.display_style and \
               self.description == other.description and \
               self.name == other.name


class TerraformModuleComputeService(abc.ABC):
    def __init__(self, cloud_account_name: str, compute_service_name: str, permissions: dict = None):
        self.cloud_account_name = cloud_account_name
        self.compute_service_name = compute_service_name
        self.permissions = permissions

    def __eq__(self, other):
        if not isinstance(other, TerraformModuleComputeService):
            return NotImplemented

        return self.cloud_account_name.lower() == other.cloud_account_name.lower() and \
               self.compute_service_name.lower() == other.compute_service_name.lower() and \
               self.permissions == other.permissions


class TerraformModuleDescriptor:
    def __init__(self, module_name: str, module_repo_name: str, terraform_version: str, enable_auto_tagging: bool,
                 exclude_from_tagging: List[str], inputs: List[TerraformModuleInput],
                 outputs: List[TerraformModuleOutput], compute_services: List[TerraformModuleComputeService],
                 module_root_path: str = None, description: str = None, allowed_spaces: List[str] = None):
        self.name = module_name
        self.module_repo_name = module_repo_name
        self.module_root_path = module_root_path
        self.description = description
        self.terraform_version = terraform_version
        self.enable_auto_tagging = enable_auto_tagging
        self.exclude_from_tagging = exclude_from_tagging
        self.allowed_spaces = allowed_spaces
        self.compute_services = compute_services
        self.outputs = outputs
        self.inputs = inputs


class SpaceHelmChartComputeService:
    def __init__(self, cloud_account_name: str, compute_service_name: str, service_account_name: Optional[str] = None):
        self.cloud_account_name = cloud_account_name
        self.compute_service_name = compute_service_name
        self.service_account_name = service_account_name

    def __eq__(self, other):
        if not isinstance(other, TerraformModuleComputeService):
            return NotImplemented

        return self.cloud_account_name.lower() == other.cloud_account_name.lower() and \
               self.compute_service_name.lower() == other.compute_service_name.lower() and \
               self.service_account_name.lower() == other.service_account_name.lower()


class SpaceTerraformModuleInput:
    def __init__(self, name: str, value: Optional[str], overridable: bool) -> None:
        self.name = name
        self.value = value
        self.overridable = overridable

    def clone(self):
        """
        :return: SpaceTerraformModuleInput
        """
        return SpaceTerraformModuleInput(name=self.name, value=self.value, overridable=self.overridable)


class SpaceHelmChartInput:
    def __init__(self, name: str, path: str, value: Optional[str], description: Optional[str],
                 overridable: bool, optional: bool, display_style: str,
                 possible_values: [Optional[List[str]]] = None) -> None:
        self.name = name
        self.path = path
        self.value = value
        self.description = description
        self.overridable = overridable
        self.optional = optional
        self.display_style = display_style
        self.possible_values = possible_values

    def clone(self):
        return SpaceHelmChartInput(name=self.name, path=self.path, value=self.value, description=self.description,
                                   overridable=self.overridable, optional=self.optional,
                                   display_style=self.display_style, possible_values=self.possible_values)


class SpaceHelmChartOutput:
    def __init__(self, name: str, description: Optional[str], display_style: str, value: str) -> None:
        self.name = name
        self.description = description
        self.display_style = display_style
        self.value = value

    def clone(self):
        return SpaceHelmChartOutput(name=self.name, description=self.description,
                                    display_style=self.display_style, value=self.value)


class HelmChartDescriptor:
    def __init__(self, name: str, perform_helm_test: bool, enable_logs: bool, inputs: List[SpaceHelmChartInput],
                 outputs: List[SpaceHelmChartOutput], compute_service: SpaceHelmChartComputeService,
                 chart_root_path: Optional[str] = None, git_branch: Optional[str] = None,
                 description: Optional[str] = None, override_values_yaml: Optional[str] = None,
                 commands: Optional[List[str]] = None):
        self.name = name
        self.chart_root_path = chart_root_path
        self.git_branch = git_branch
        self.description = description
        self.enable_logs = enable_logs
        self.perform_helm_test = perform_helm_test
        self.override_values_yaml = override_values_yaml
        self.compute_service = compute_service
        self.outputs = outputs
        self.inputs = inputs
        self.commands = commands
