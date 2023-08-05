'''
# cdktf-multi-stack-tfe

Setting up Terraform Cloud / Terraform Enterprise workspaces can be tiring when dealing with CDK for Terraform applications spanning multiple stacks and therefore workspaces. This library aims to automate this.

## Usage

You need to create the initial workspace yourself, in this case `my-app-base`.

```python
import * as cdktf from "cdktf";
import Construct from "constructs";
import { BaseStack, Stack, Variable } from "cdktf-multi-stack-tfe";

// We need to have an already created "base" TFE workspace as a basis.
// It will store the TFE workspace configuration and state for all stacks.
// As it creates all TFE workspaces, it's required to be created first (and as a result will scaffold out all the required workspaces).
class MyAppBaseStack extends BaseStack {
  // The name is set to my-app-base
  constructor(scope: Construct) {
    // This will configure the remote backend to use my-company/my-app-base as a workspace
    // my-company is the Terraform organization
    // my-app is the prefix to use for all workspaces
    super(scope, "my-company", "my-app", {
      hostname: "app.terraform.io", // can be set to configure a different Terraform Cloud hostname, e.g. for privately hosted Terraform Enterprise
      token: "my-token", // can be set to configure a token to use
    });

    // You can do additional things in this stack as well
  }
}

class VpcStack extends Stack {
  public vpcId: string

  // This stack will depend on the base stack and it
  // will use the my-company/my-app-$stackName workspace as a backend
  constructor(scope: Construct, stackName: string) {
    super(scope, stackName);

    // Setup an VPC, etc.

    this.vpcId = ....
  }
}

class WebStack extends Stack {
  constructor(scope: Construct, stackName: string, vpcId: string) {
    super(scope, stackName);

    // This expects a TFC variable called "password" in your base stack and
    // will create a variable called "password" in this stack. You can use
    // password.value to get the value as you would do with TerraformVariable.
    const password = new Variable(this, "password", {
      type: "string",
      sensitive: true
    });


    // Setup your webapp using the vpcId
  }
}

const app = new cdktf.App();
new MyAppBaseStack(app); // the stack name is "base"

// This cross-stack reference will lead to permissions being set up so that
// the staging-web workspace can access the staging-vpc workspace.
const vpc = new VpcStack(app, "staging-vpc"); // the stack name is "staging-vpc"
new Web(app, "staging-web", vpc.vpcId); // the stack name is "staging-web"

const prodVpc = new VpcStack(app, "production-vpc");
new Web(app, "production-web", prodVpc.vpcId);

app.synth();
```

### Configuration

#### Workspace naming

To control the workspace naming please implement the following method on the BaseStack to your liking:

```python
public getWorkspaceName(stackName: string): string {
  return `${this.prefix}-${stackName}`;
}
```

### Workspace configuration

You configure the created workspaces by settting the `defaultWorkspaceConfig` property on the BaseStack.
This config is overwritten by the one specified as the thrid argument of a `Stack` (in the super call).

## Warning

There are some potentially harmful side effects you could run into, so please always carefully read the diff before applying it.

### Renaming stacks

This is not supported by the library, if you rename an already existing stack the workspace hosting it will be destroyed and a new one with the new name will be created. This means all references to the infrastructure provisioned in the old stack will be lost, making it impossible to destroy the infrastructure through terraform. In this case we recommend destroying the stack, renaming it and then re-creating it.
There are some ways around this issue, but the library currently does not support them.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import cdktf
import cdktf_cdktf_provider_tfe
import constructs


class BaseStack(
    cdktf.TerraformStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-multi-stack-tfe.BaseStack",
):
    def __init__(
        self,
        scope: constructs.Construct,
        organization_name: builtins.str,
        prefix: builtins.str,
        *,
        default_workspace_config: typing.Optional["WorkspaceConfig"] = None,
        hostname: typing.Optional[builtins.str] = None,
        ssl_skip_verify: typing.Optional[builtins.bool] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param organization_name: -
        :param prefix: -
        :param default_workspace_config: 
        :param hostname: 
        :param ssl_skip_verify: 
        :param token: 
        '''
        options = BaseStackOptions(
            default_workspace_config=default_workspace_config,
            hostname=hostname,
            ssl_skip_verify=ssl_skip_verify,
            token=token,
        )

        jsii.create(self.__class__, self, [scope, organization_name, prefix, options])

    @jsii.member(jsii_name="baseStackOf") # type: ignore[misc]
    @builtins.classmethod
    def base_stack_of(cls, construct: constructs.IConstruct) -> "BaseStack":
        '''
        :param construct: -
        '''
        return typing.cast("BaseStack", jsii.sinvoke(cls, "baseStackOf", [construct]))

    @jsii.member(jsii_name="isBaseStack") # type: ignore[misc]
    @builtins.classmethod
    def is_base_stack(cls, x: typing.Any) -> builtins.bool:
        '''
        :param x: -
        '''
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isBaseStack", [x]))

    @jsii.member(jsii_name="bootstrapWorkspace")
    def bootstrap_workspace(
        self,
        stack_name: builtins.str,
        *,
        agent_pool_id: typing.Optional[builtins.str] = None,
        allow_destroy_plan: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        auto_apply: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_mode: typing.Optional[builtins.str] = None,
        file_triggers_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        global_remote_state: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        queue_all_runs: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        remote_state_consumer_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        speculative_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        ssh_key_id: typing.Optional[builtins.str] = None,
        structured_run_output_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        tag_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        terraform_version: typing.Optional[builtins.str] = None,
        trigger_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> cdktf_cdktf_provider_tfe.Workspace:
        '''
        :param stack_name: -
        :param agent_pool_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#agent_pool_id Workspace#agent_pool_id}.
        :param allow_destroy_plan: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#allow_destroy_plan Workspace#allow_destroy_plan}.
        :param auto_apply: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#auto_apply Workspace#auto_apply}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#description Workspace#description}.
        :param execution_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#execution_mode Workspace#execution_mode}.
        :param file_triggers_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#file_triggers_enabled Workspace#file_triggers_enabled}.
        :param global_remote_state: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#global_remote_state Workspace#global_remote_state}.
        :param queue_all_runs: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#queue_all_runs Workspace#queue_all_runs}.
        :param remote_state_consumer_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#remote_state_consumer_ids Workspace#remote_state_consumer_ids}.
        :param speculative_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#speculative_enabled Workspace#speculative_enabled}.
        :param ssh_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#ssh_key_id Workspace#ssh_key_id}.
        :param structured_run_output_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#structured_run_output_enabled Workspace#structured_run_output_enabled}.
        :param tag_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#tag_names Workspace#tag_names}.
        :param terraform_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#terraform_version Workspace#terraform_version}.
        :param trigger_prefixes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#trigger_prefixes Workspace#trigger_prefixes}.
        '''
        stack_config = WorkspaceConfig(
            agent_pool_id=agent_pool_id,
            allow_destroy_plan=allow_destroy_plan,
            auto_apply=auto_apply,
            description=description,
            execution_mode=execution_mode,
            file_triggers_enabled=file_triggers_enabled,
            global_remote_state=global_remote_state,
            queue_all_runs=queue_all_runs,
            remote_state_consumer_ids=remote_state_consumer_ids,
            speculative_enabled=speculative_enabled,
            ssh_key_id=ssh_key_id,
            structured_run_output_enabled=structured_run_output_enabled,
            tag_names=tag_names,
            terraform_version=terraform_version,
            trigger_prefixes=trigger_prefixes,
        )

        return typing.cast(cdktf_cdktf_provider_tfe.Workspace, jsii.invoke(self, "bootstrapWorkspace", [stack_name, stack_config]))

    @jsii.member(jsii_name="createSecret")
    def create_secret(
        self,
        target_stack: "Stack",
        secret_name: builtins.str,
        *,
        default: typing.Any = None,
        description: typing.Optional[builtins.str] = None,
        nullable: typing.Optional[builtins.bool] = None,
        sensitive: typing.Optional[builtins.bool] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_stack: -
        :param secret_name: -
        :param default: 
        :param description: 
        :param nullable: 
        :param sensitive: 
        :param type: (experimental) The type argument in a variable block allows you to restrict the type of value that will be accepted as the value for a variable. If no type constraint is set then a value of any type is accepted. While type constraints are optional, we recommend specifying them; they serve as easy reminders for users of the module, and allow Terraform to return a helpful error message if the wrong type is used. Type constraints are created from a mixture of type keywords and type constructors. The supported type keywords are: - string - number - bool The type constructors allow you to specify complex types such as collections: - list(<TYPE>) - set(<TYPE>) - map(<TYPE>) - object({<ATTR NAME> = <TYPE>, ... }) - tuple([<TYPE>, ...]) The keyword any may be used to indicate that any type is acceptable. For more information on the meaning and behavior of these different types, as well as detailed information about automatic conversion of complex types, see {@link https://www.terraform.io/docs/configuration/types.html|Type Constraints}. If both the type and default arguments are specified, the given default value must be convertible to the specified type.
        '''
        config = cdktf.TerraformVariableConfig(
            default=default,
            description=description,
            nullable=nullable,
            sensitive=sensitive,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "createSecret", [target_stack, secret_name, config]))

    @jsii.member(jsii_name="getRemoteBackendOptions")
    def get_remote_backend_options(
        self,
        stack_name: builtins.str,
    ) -> "RemoteBackendOptions":
        '''
        :param stack_name: -
        '''
        return typing.cast("RemoteBackendOptions", jsii.invoke(self, "getRemoteBackendOptions", [stack_name]))

    @jsii.member(jsii_name="getWorkspaceName")
    def get_workspace_name(self, stack_name: builtins.str) -> builtins.str:
        '''If you want to have more control over the workspace name, you can override this method.

        :param stack_name: -
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "getWorkspaceName", [stack_name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> cdktf_cdktf_provider_tfe.DataTfeOrganization:
        return typing.cast(cdktf_cdktf_provider_tfe.DataTfeOrganization, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: cdktf_cdktf_provider_tfe.DataTfeOrganization) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tfeProvider")
    def tfe_provider(self) -> cdktf_cdktf_provider_tfe.TfeProvider:
        return typing.cast(cdktf_cdktf_provider_tfe.TfeProvider, jsii.get(self, "tfeProvider"))

    @tfe_provider.setter
    def tfe_provider(self, value: cdktf_cdktf_provider_tfe.TfeProvider) -> None:
        jsii.set(self, "tfeProvider", value)


@jsii.data_type(
    jsii_type="cdktf-multi-stack-tfe.BaseStackOptions",
    jsii_struct_bases=[],
    name_mapping={
        "default_workspace_config": "defaultWorkspaceConfig",
        "hostname": "hostname",
        "ssl_skip_verify": "sslSkipVerify",
        "token": "token",
    },
)
class BaseStackOptions:
    def __init__(
        self,
        *,
        default_workspace_config: typing.Optional["WorkspaceConfig"] = None,
        hostname: typing.Optional[builtins.str] = None,
        ssl_skip_verify: typing.Optional[builtins.bool] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_workspace_config: 
        :param hostname: 
        :param ssl_skip_verify: 
        :param token: 
        '''
        if isinstance(default_workspace_config, dict):
            default_workspace_config = WorkspaceConfig(**default_workspace_config)
        self._values: typing.Dict[str, typing.Any] = {}
        if default_workspace_config is not None:
            self._values["default_workspace_config"] = default_workspace_config
        if hostname is not None:
            self._values["hostname"] = hostname
        if ssl_skip_verify is not None:
            self._values["ssl_skip_verify"] = ssl_skip_verify
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def default_workspace_config(self) -> typing.Optional["WorkspaceConfig"]:
        result = self._values.get("default_workspace_config")
        return typing.cast(typing.Optional["WorkspaceConfig"], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_skip_verify(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("ssl_skip_verify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseStackOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-multi-stack-tfe.RemoteBackendOptions",
    jsii_struct_bases=[],
    name_mapping={
        "organization": "organization",
        "workspaces": "workspaces",
        "hostname": "hostname",
        "token": "token",
    },
)
class RemoteBackendOptions:
    def __init__(
        self,
        *,
        organization: builtins.str,
        workspaces: "RemoteBackendOptionsWorkspace",
        hostname: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param organization: 
        :param workspaces: 
        :param hostname: 
        :param token: 
        '''
        if isinstance(workspaces, dict):
            workspaces = RemoteBackendOptionsWorkspace(**workspaces)
        self._values: typing.Dict[str, typing.Any] = {
            "organization": organization,
            "workspaces": workspaces,
        }
        if hostname is not None:
            self._values["hostname"] = hostname
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def organization(self) -> builtins.str:
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspaces(self) -> "RemoteBackendOptionsWorkspace":
        result = self._values.get("workspaces")
        assert result is not None, "Required property 'workspaces' is missing"
        return typing.cast("RemoteBackendOptionsWorkspace", result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RemoteBackendOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf-multi-stack-tfe.RemoteBackendOptionsWorkspace",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class RemoteBackendOptionsWorkspace:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RemoteBackendOptionsWorkspace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Stack(
    cdktf.TerraformStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-multi-stack-tfe.Stack",
):
    def __init__(
        self,
        scope: constructs.Construct,
        stack_name: builtins.str,
        *,
        agent_pool_id: typing.Optional[builtins.str] = None,
        allow_destroy_plan: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        auto_apply: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_mode: typing.Optional[builtins.str] = None,
        file_triggers_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        global_remote_state: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        queue_all_runs: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        remote_state_consumer_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        speculative_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        ssh_key_id: typing.Optional[builtins.str] = None,
        structured_run_output_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        tag_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        terraform_version: typing.Optional[builtins.str] = None,
        trigger_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param stack_name: -
        :param agent_pool_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#agent_pool_id Workspace#agent_pool_id}.
        :param allow_destroy_plan: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#allow_destroy_plan Workspace#allow_destroy_plan}.
        :param auto_apply: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#auto_apply Workspace#auto_apply}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#description Workspace#description}.
        :param execution_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#execution_mode Workspace#execution_mode}.
        :param file_triggers_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#file_triggers_enabled Workspace#file_triggers_enabled}.
        :param global_remote_state: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#global_remote_state Workspace#global_remote_state}.
        :param queue_all_runs: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#queue_all_runs Workspace#queue_all_runs}.
        :param remote_state_consumer_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#remote_state_consumer_ids Workspace#remote_state_consumer_ids}.
        :param speculative_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#speculative_enabled Workspace#speculative_enabled}.
        :param ssh_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#ssh_key_id Workspace#ssh_key_id}.
        :param structured_run_output_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#structured_run_output_enabled Workspace#structured_run_output_enabled}.
        :param tag_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#tag_names Workspace#tag_names}.
        :param terraform_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#terraform_version Workspace#terraform_version}.
        :param trigger_prefixes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#trigger_prefixes Workspace#trigger_prefixes}.
        '''
        config = WorkspaceConfig(
            agent_pool_id=agent_pool_id,
            allow_destroy_plan=allow_destroy_plan,
            auto_apply=auto_apply,
            description=description,
            execution_mode=execution_mode,
            file_triggers_enabled=file_triggers_enabled,
            global_remote_state=global_remote_state,
            queue_all_runs=queue_all_runs,
            remote_state_consumer_ids=remote_state_consumer_ids,
            speculative_enabled=speculative_enabled,
            ssh_key_id=ssh_key_id,
            structured_run_output_enabled=structured_run_output_enabled,
            tag_names=tag_names,
            terraform_version=terraform_version,
            trigger_prefixes=trigger_prefixes,
        )

        jsii.create(self.__class__, self, [scope, stack_name, config])

    @jsii.member(jsii_name="isMultiStackStack") # type: ignore[misc]
    @builtins.classmethod
    def is_multi_stack_stack(cls, x: typing.Any) -> builtins.bool:
        '''
        :param x: -
        '''
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isMultiStackStack", [x]))

    @jsii.member(jsii_name="multiStackOf") # type: ignore[misc]
    @builtins.classmethod
    def multi_stack_of(cls, construct: constructs.IConstruct) -> "Stack":
        '''
        :param construct: -
        '''
        return typing.cast("Stack", jsii.sinvoke(cls, "multiStackOf", [construct]))

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, dependency: cdktf.TerraformStack) -> None:
        '''
        :param dependency: -
        '''
        return typing.cast(None, jsii.invoke(self, "addDependency", [dependency]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspace")
    def workspace(self) -> cdktf_cdktf_provider_tfe.Workspace:
        return typing.cast(cdktf_cdktf_provider_tfe.Workspace, jsii.get(self, "workspace"))

    @workspace.setter
    def workspace(self, value: cdktf_cdktf_provider_tfe.Workspace) -> None:
        jsii.set(self, "workspace", value)


class Variable(
    cdktf.TerraformVariable,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-multi-stack-tfe.Variable",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        default: typing.Any = None,
        description: typing.Optional[builtins.str] = None,
        nullable: typing.Optional[builtins.bool] = None,
        sensitive: typing.Optional[builtins.bool] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param default: 
        :param description: 
        :param nullable: 
        :param sensitive: 
        :param type: (experimental) The type argument in a variable block allows you to restrict the type of value that will be accepted as the value for a variable. If no type constraint is set then a value of any type is accepted. While type constraints are optional, we recommend specifying them; they serve as easy reminders for users of the module, and allow Terraform to return a helpful error message if the wrong type is used. Type constraints are created from a mixture of type keywords and type constructors. The supported type keywords are: - string - number - bool The type constructors allow you to specify complex types such as collections: - list(<TYPE>) - set(<TYPE>) - map(<TYPE>) - object({<ATTR NAME> = <TYPE>, ... }) - tuple([<TYPE>, ...]) The keyword any may be used to indicate that any type is acceptable. For more information on the meaning and behavior of these different types, as well as detailed information about automatic conversion of complex types, see {@link https://www.terraform.io/docs/configuration/types.html|Type Constraints}. If both the type and default arguments are specified, the given default value must be convertible to the specified type.
        '''
        config = cdktf.TerraformVariableConfig(
            default=default,
            description=description,
            nullable=nullable,
            sensitive=sensitive,
            type=type,
        )

        jsii.create(self.__class__, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf-multi-stack-tfe.WorkspaceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "agent_pool_id": "agentPoolId",
        "allow_destroy_plan": "allowDestroyPlan",
        "auto_apply": "autoApply",
        "description": "description",
        "execution_mode": "executionMode",
        "file_triggers_enabled": "fileTriggersEnabled",
        "global_remote_state": "globalRemoteState",
        "queue_all_runs": "queueAllRuns",
        "remote_state_consumer_ids": "remoteStateConsumerIds",
        "speculative_enabled": "speculativeEnabled",
        "ssh_key_id": "sshKeyId",
        "structured_run_output_enabled": "structuredRunOutputEnabled",
        "tag_names": "tagNames",
        "terraform_version": "terraformVersion",
        "trigger_prefixes": "triggerPrefixes",
    },
)
class WorkspaceConfig:
    def __init__(
        self,
        *,
        agent_pool_id: typing.Optional[builtins.str] = None,
        allow_destroy_plan: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        auto_apply: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_mode: typing.Optional[builtins.str] = None,
        file_triggers_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        global_remote_state: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        queue_all_runs: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        remote_state_consumer_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        speculative_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        ssh_key_id: typing.Optional[builtins.str] = None,
        structured_run_output_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        tag_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        terraform_version: typing.Optional[builtins.str] = None,
        trigger_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param agent_pool_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#agent_pool_id Workspace#agent_pool_id}.
        :param allow_destroy_plan: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#allow_destroy_plan Workspace#allow_destroy_plan}.
        :param auto_apply: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#auto_apply Workspace#auto_apply}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#description Workspace#description}.
        :param execution_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#execution_mode Workspace#execution_mode}.
        :param file_triggers_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#file_triggers_enabled Workspace#file_triggers_enabled}.
        :param global_remote_state: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#global_remote_state Workspace#global_remote_state}.
        :param queue_all_runs: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#queue_all_runs Workspace#queue_all_runs}.
        :param remote_state_consumer_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#remote_state_consumer_ids Workspace#remote_state_consumer_ids}.
        :param speculative_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#speculative_enabled Workspace#speculative_enabled}.
        :param ssh_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#ssh_key_id Workspace#ssh_key_id}.
        :param structured_run_output_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#structured_run_output_enabled Workspace#structured_run_output_enabled}.
        :param tag_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#tag_names Workspace#tag_names}.
        :param terraform_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#terraform_version Workspace#terraform_version}.
        :param trigger_prefixes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#trigger_prefixes Workspace#trigger_prefixes}.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if agent_pool_id is not None:
            self._values["agent_pool_id"] = agent_pool_id
        if allow_destroy_plan is not None:
            self._values["allow_destroy_plan"] = allow_destroy_plan
        if auto_apply is not None:
            self._values["auto_apply"] = auto_apply
        if description is not None:
            self._values["description"] = description
        if execution_mode is not None:
            self._values["execution_mode"] = execution_mode
        if file_triggers_enabled is not None:
            self._values["file_triggers_enabled"] = file_triggers_enabled
        if global_remote_state is not None:
            self._values["global_remote_state"] = global_remote_state
        if queue_all_runs is not None:
            self._values["queue_all_runs"] = queue_all_runs
        if remote_state_consumer_ids is not None:
            self._values["remote_state_consumer_ids"] = remote_state_consumer_ids
        if speculative_enabled is not None:
            self._values["speculative_enabled"] = speculative_enabled
        if ssh_key_id is not None:
            self._values["ssh_key_id"] = ssh_key_id
        if structured_run_output_enabled is not None:
            self._values["structured_run_output_enabled"] = structured_run_output_enabled
        if tag_names is not None:
            self._values["tag_names"] = tag_names
        if terraform_version is not None:
            self._values["terraform_version"] = terraform_version
        if trigger_prefixes is not None:
            self._values["trigger_prefixes"] = trigger_prefixes

    @builtins.property
    def agent_pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#agent_pool_id Workspace#agent_pool_id}.'''
        result = self._values.get("agent_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_destroy_plan(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#allow_destroy_plan Workspace#allow_destroy_plan}.'''
        result = self._values.get("allow_destroy_plan")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def auto_apply(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#auto_apply Workspace#auto_apply}.'''
        result = self._values.get("auto_apply")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#description Workspace#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#execution_mode Workspace#execution_mode}.'''
        result = self._values.get("execution_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_triggers_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#file_triggers_enabled Workspace#file_triggers_enabled}.'''
        result = self._values.get("file_triggers_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def global_remote_state(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#global_remote_state Workspace#global_remote_state}.'''
        result = self._values.get("global_remote_state")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def queue_all_runs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#queue_all_runs Workspace#queue_all_runs}.'''
        result = self._values.get("queue_all_runs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def remote_state_consumer_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#remote_state_consumer_ids Workspace#remote_state_consumer_ids}.'''
        result = self._values.get("remote_state_consumer_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def speculative_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#speculative_enabled Workspace#speculative_enabled}.'''
        result = self._values.get("speculative_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def ssh_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#ssh_key_id Workspace#ssh_key_id}.'''
        result = self._values.get("ssh_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def structured_run_output_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#structured_run_output_enabled Workspace#structured_run_output_enabled}.'''
        result = self._values.get("structured_run_output_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def tag_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#tag_names Workspace#tag_names}.'''
        result = self._values.get("tag_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def terraform_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#terraform_version Workspace#terraform_version}.'''
        result = self._values.get("terraform_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#trigger_prefixes Workspace#trigger_prefixes}.'''
        result = self._values.get("trigger_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BaseStack",
    "BaseStackOptions",
    "RemoteBackendOptions",
    "RemoteBackendOptionsWorkspace",
    "Stack",
    "Variable",
    "WorkspaceConfig",
]

publication.publish()
