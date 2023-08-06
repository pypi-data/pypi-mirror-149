'''
# CDKTF Local Build Construct

A simple construct that runs builds for different languages locally.
Currently, it supports: docker. I plan on adding rust (cargo) and node (npm) support as well.

## Usage

```python
import { Provider, DockerBuild, DockerizedBuild } from "cdktf-local-build";

// Local Build extends LocalExec which extends from the null provider,
// so if you already have the provider initialized you can skip this step
new Provider(this, "local-build");

new DockerBuild(this, "docker-backend", {
  cwd: "/path/to/project/backend",
  dockerfile: "Dockerfile.backend",
  image: "cdktf/backend:latest",
  push: false, // defaults to true
});

new DockerizedBuild(this, "my-go-backend", {
  cwd: "/path/to/project/backend",
  command: "go build -o /tmp/backend",
  imageHomeDirectory: "/tmp/backend",
  platform: "linux/arm64",
  image: "go-builder-image:latest",
  setUser: true,
});
```

### `DockerBuild`

Builds a docker image locally.

#### Options

* `cwd`: The working directory to run the command in.
* `dockerfile`: The Dockerfile to use.
* `image`: The tag to use for the image.
* `push`: If true, `docker push <tag>` is executed after the run.

### `DockerizedBuild`

Build an artifact inside a docker image.

#### Options

* `cwd`: The working directory to run the command in.
* `command`: Build command to run int the docker image.
* `image`: The tag to use for the building image.
* `imageHomeDirectory`: The home directory to use inside the image.
* `platform`: The platform to build for (sets docker platform flag).
* `setUser`: If true, the user will be set to the current user inside docker.

### `CrossBuild`

Builds a rust binary using cross (cross runs it inside a docker container).
Please make sure [cross](https://github.com/cross-rs/cross) is installed on the host machine by running `cargo install cross`.

#### Options

* `arch`: The architecture to build for (`arm` or `x86`).
* `projectName`: The name specified in the Cargo.toml.
* `cwd`: The working directory to run the command in.
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
import cdktf_cdktf_provider_null
import cdktf_local_exec
import constructs


@jsii.data_type(
    jsii_type="cdktf-local-build.CargoOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cwd": "cwd",
        "project_name": "projectName",
        "arch": "arch",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "rust_version": "rustVersion",
        "triggers": "triggers",
    },
)
class CargoOptions:
    def __init__(
        self,
        *,
        cwd: builtins.str,
        project_name: builtins.str,
        arch: typing.Optional[builtins.str] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        rust_version: typing.Optional[builtins.str] = None,
        triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param cwd: The working directory to run the command in. Defaults to process.pwd().
        :param project_name: Name value in the Cargo.toml.
        :param arch: Architecture of the binary to build. Default: "x86"
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param rust_version: Rust version to compile with. Default: 1.58
        :param triggers: 
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "cwd": cwd,
            "project_name": project_name,
        }
        if arch is not None:
            self._values["arch"] = arch
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if rust_version is not None:
            self._values["rust_version"] = rust_version
        if triggers is not None:
            self._values["triggers"] = triggers

    @builtins.property
    def cwd(self) -> builtins.str:
        '''The working directory to run the command in.

        Defaults to process.pwd().
        '''
        result = self._values.get("cwd")
        assert result is not None, "Required property 'cwd' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_name(self) -> builtins.str:
        '''Name value in the Cargo.toml.'''
        result = self._values.get("project_name")
        assert result is not None, "Required property 'project_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arch(self) -> typing.Optional[builtins.str]:
        '''Architecture of the binary to build.

        :default: "x86"
        '''
        result = self._values.get("arch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def rust_version(self) -> typing.Optional[builtins.str]:
        '''Rust version to compile with.

        :default: 1.58
        '''
        result = self._values.get("rust_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def triggers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CargoOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CrossBuild(
    cdktf_local_exec.LocalExec,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-local-build.CrossBuild",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        cwd: builtins.str,
        project_name: builtins.str,
        arch: typing.Optional[builtins.str] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param cwd: The working directory to run the command in. Defaults to process.pwd().
        :param project_name: Name value in the Cargo.toml.
        :param arch: Architecture of the binary to build. Default: "x86"
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param triggers: 
        '''
        config = CrossOptions(
            cwd=cwd,
            project_name=project_name,
            arch=arch,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
            triggers=triggers,
        )

        jsii.create(self.__class__, self, [scope, name, config])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="binaryPath")
    def binary_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryPath"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectName"))


@jsii.data_type(
    jsii_type="cdktf-local-build.CrossOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cwd": "cwd",
        "project_name": "projectName",
        "arch": "arch",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "triggers": "triggers",
    },
)
class CrossOptions:
    def __init__(
        self,
        *,
        cwd: builtins.str,
        project_name: builtins.str,
        arch: typing.Optional[builtins.str] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param cwd: The working directory to run the command in. Defaults to process.pwd().
        :param project_name: Name value in the Cargo.toml.
        :param arch: Architecture of the binary to build. Default: "x86"
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param triggers: 
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "cwd": cwd,
            "project_name": project_name,
        }
        if arch is not None:
            self._values["arch"] = arch
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if triggers is not None:
            self._values["triggers"] = triggers

    @builtins.property
    def cwd(self) -> builtins.str:
        '''The working directory to run the command in.

        Defaults to process.pwd().
        '''
        result = self._values.get("cwd")
        assert result is not None, "Required property 'cwd' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_name(self) -> builtins.str:
        '''Name value in the Cargo.toml.'''
        result = self._values.get("project_name")
        assert result is not None, "Required property 'project_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arch(self) -> typing.Optional[builtins.str]:
        '''Architecture of the binary to build.

        :default: "x86"
        '''
        result = self._values.get("arch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def triggers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CrossOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DockerBuild(
    cdktf_local_exec.LocalExec,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-local-build.DockerBuild",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        cwd: builtins.str,
        tag: builtins.str,
        auth: typing.Optional["RegistryAuth"] = None,
        dockerfile: typing.Optional[builtins.str] = None,
        push: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param cwd: 
        :param tag: 
        :param auth: 
        :param dockerfile: 
        :param push: 
        '''
        __2 = DockerBuildOptions(
            cwd=cwd, tag=tag, auth=auth, dockerfile=dockerfile, push=push
        )

        jsii.create(self.__class__, self, [scope, name, __2])


@jsii.data_type(
    jsii_type="cdktf-local-build.DockerBuildOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cwd": "cwd",
        "tag": "tag",
        "auth": "auth",
        "dockerfile": "dockerfile",
        "push": "push",
    },
)
class DockerBuildOptions:
    def __init__(
        self,
        *,
        cwd: builtins.str,
        tag: builtins.str,
        auth: typing.Optional["RegistryAuth"] = None,
        dockerfile: typing.Optional[builtins.str] = None,
        push: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param cwd: 
        :param tag: 
        :param auth: 
        :param dockerfile: 
        :param push: 
        '''
        if isinstance(auth, dict):
            auth = RegistryAuth(**auth)
        self._values: typing.Dict[str, typing.Any] = {
            "cwd": cwd,
            "tag": tag,
        }
        if auth is not None:
            self._values["auth"] = auth
        if dockerfile is not None:
            self._values["dockerfile"] = dockerfile
        if push is not None:
            self._values["push"] = push

    @builtins.property
    def cwd(self) -> builtins.str:
        result = self._values.get("cwd")
        assert result is not None, "Required property 'cwd' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag(self) -> builtins.str:
        result = self._values.get("tag")
        assert result is not None, "Required property 'tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth(self) -> typing.Optional["RegistryAuth"]:
        result = self._values.get("auth")
        return typing.cast(typing.Optional["RegistryAuth"], result)

    @builtins.property
    def dockerfile(self) -> typing.Optional[builtins.str]:
        result = self._values.get("dockerfile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def push(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("push")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerBuildOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DockerizedBuild(
    cdktf_local_exec.LocalExec,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-local-build.DockerizedBuild",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        image: builtins.str,
        image_home_directory: builtins.str,
        set_user: builtins.bool,
        platform: typing.Optional[builtins.str] = None,
        command: builtins.str,
        cwd: builtins.str,
        copy_before_run: typing.Optional[builtins.bool] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param image: 
        :param image_home_directory: 
        :param set_user: 
        :param platform: 
        :param command: The command to run.
        :param cwd: The working directory to run the command in. Defaults to process.pwd(). If copyBeforeRun is set to true it will copy the working directory to an asset directory and take that as the base to run.
        :param copy_before_run: If set to true, the working directory will be copied to an asset directory. Default: true
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param triggers: 
        '''
        options = DockerizedBuildOptions(
            image=image,
            image_home_directory=image_home_directory,
            set_user=set_user,
            platform=platform,
            command=command,
            cwd=cwd,
            copy_before_run=copy_before_run,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
            triggers=triggers,
        )

        jsii.create(self.__class__, self, [scope, name, options])


@jsii.data_type(
    jsii_type="cdktf-local-build.DockerizedBuildOptions",
    jsii_struct_bases=[cdktf_local_exec.LocalExecOptions],
    name_mapping={
        "command": "command",
        "cwd": "cwd",
        "copy_before_run": "copyBeforeRun",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "triggers": "triggers",
        "image": "image",
        "image_home_directory": "imageHomeDirectory",
        "set_user": "setUser",
        "platform": "platform",
    },
)
class DockerizedBuildOptions(cdktf_local_exec.LocalExecOptions):
    def __init__(
        self,
        *,
        command: builtins.str,
        cwd: builtins.str,
        copy_before_run: typing.Optional[builtins.bool] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: builtins.str,
        image_home_directory: builtins.str,
        set_user: builtins.bool,
        platform: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param command: The command to run.
        :param cwd: The working directory to run the command in. Defaults to process.pwd(). If copyBeforeRun is set to true it will copy the working directory to an asset directory and take that as the base to run.
        :param copy_before_run: If set to true, the working directory will be copied to an asset directory. Default: true
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param triggers: 
        :param image: 
        :param image_home_directory: 
        :param set_user: 
        :param platform: 
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "command": command,
            "cwd": cwd,
            "image": image,
            "image_home_directory": image_home_directory,
            "set_user": set_user,
        }
        if copy_before_run is not None:
            self._values["copy_before_run"] = copy_before_run
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if triggers is not None:
            self._values["triggers"] = triggers
        if platform is not None:
            self._values["platform"] = platform

    @builtins.property
    def command(self) -> builtins.str:
        '''The command to run.'''
        result = self._values.get("command")
        assert result is not None, "Required property 'command' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cwd(self) -> builtins.str:
        '''The working directory to run the command in.

        Defaults to process.pwd().
        If copyBeforeRun is set to true it will copy the working directory to an asset directory and take that as the base to run.
        '''
        result = self._values.get("cwd")
        assert result is not None, "Required property 'cwd' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def copy_before_run(self) -> typing.Optional[builtins.bool]:
        '''If set to true, the working directory will be copied to an asset directory.

        :default: true
        '''
        result = self._values.get("copy_before_run")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def triggers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def image(self) -> builtins.str:
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_home_directory(self) -> builtins.str:
        result = self._values.get("image_home_directory")
        assert result is not None, "Required property 'image_home_directory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def set_user(self) -> builtins.bool:
        result = self._values.get("set_user")
        assert result is not None, "Required property 'set_user' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerizedBuildOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DockerizedCargoBuild(
    DockerizedBuild,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-local-build.DockerizedCargoBuild",
):
    '''Builds a binary using cargo inside a docker container.

    It is built to support https://github.com/awslabs/aws-lambda-rust-runtime
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        cwd: builtins.str,
        project_name: builtins.str,
        arch: typing.Optional[builtins.str] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        rust_version: typing.Optional[builtins.str] = None,
        triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param cwd: The working directory to run the command in. Defaults to process.pwd().
        :param project_name: Name value in the Cargo.toml.
        :param arch: Architecture of the binary to build. Default: "x86"
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param rust_version: Rust version to compile with. Default: 1.58
        :param triggers: 
        '''
        options = CargoOptions(
            cwd=cwd,
            project_name=project_name,
            arch=arch,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
            rust_version=rust_version,
            triggers=triggers,
        )

        jsii.create(self.__class__, self, [scope, name, options])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="binaryPath")
    def binary_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryPath"))


class NullProvider(
    cdktf.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf-local-build.NullProvider",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/null null}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/null null} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/null#alias NullProvider#alias}
        '''
        config = cdktf_cdktf_provider_null.NullProviderConfig(alias=alias)

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "alias", value)


@jsii.data_type(
    jsii_type="cdktf-local-build.RegistryAuth",
    jsii_struct_bases=[],
    name_mapping={
        "password": "password",
        "proxy_endpoint": "proxyEndpoint",
        "user_name": "userName",
    },
)
class RegistryAuth:
    def __init__(
        self,
        *,
        password: builtins.str,
        proxy_endpoint: builtins.str,
        user_name: builtins.str,
    ) -> None:
        '''
        :param password: 
        :param proxy_endpoint: 
        :param user_name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "password": password,
            "proxy_endpoint": proxy_endpoint,
            "user_name": user_name,
        }

    @builtins.property
    def password(self) -> builtins.str:
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def proxy_endpoint(self) -> builtins.str:
        result = self._values.get("proxy_endpoint")
        assert result is not None, "Required property 'proxy_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_name(self) -> builtins.str:
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegistryAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CargoOptions",
    "CrossBuild",
    "CrossOptions",
    "DockerBuild",
    "DockerBuildOptions",
    "DockerizedBuild",
    "DockerizedBuildOptions",
    "DockerizedCargoBuild",
    "NullProvider",
    "RegistryAuth",
]

publication.publish()
