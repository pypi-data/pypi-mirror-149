'''
# integ-tests

## Usage

Suppose you have a simple stack, that only encapsulates a Lambda function with a
certain handler:

```python
class StackUnderTest(Stack):
    def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        lambda_.Function(self, "Handler",
            runtime=lambda_.Runtime.NODEJS_12_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            architecture=architecture
        )
```

You may want to test this stack under different conditions. For example, we want
this stack to be deployed correctly, regardless of the architecture we choose
for the Lambda function. In particular, it should work for both `ARM_64` and
`X86_64`. So you can create an `IntegTestCase` that exercises both scenarios:

```python
class StackUnderTest(Stack):
    def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        lambda_.Function(self, "Handler",
            runtime=lambda_.Runtime.NODEJS_12_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            architecture=architecture
        )

# Beginning of the test suite
app = App()

stack = Stack(app, "stack")

different_archs_case = IntegTestCase(stack, "DifferentArchitectures",
    stacks=[
        StackUnderTest(app, "Stack1",
            architecture=lambda_.Architecture.ARM_64
        ),
        StackUnderTest(app, "Stack2",
            architecture=lambda_.Architecture.X86_64
        )
    ]
)

# There must be exactly one instance of TestCase per file
IntegTest(app, "integ-test",

    # Register as many test cases as you want here
    test_cases=[different_archs_case]
)
```

This is all the instruction you need for the integration test runner to know
which stacks to synthesize, deploy and destroy. But you may also need to
customize the behavior of the runner by changing its parameters. For example:

```python
app = App()

stack_under_test = Stack(app, "StackUnderTest")

stack = Stack(app, "stack")

test_case = IntegTestCase(stack, "CustomizedDeploymentWorkflow",
    stacks=[stack_under_test],
    diff_assets=True,
    stack_update_workflow=True,
    cdk_command_options=lambda.cloud_assembly_schema.CdkCommands(
        deploy=lambda.cloud_assembly_schema.DeployCommand(
            args=lambda.cloud_assembly_schema.DeployOptions(
                require_approval=RequireApproval.NEVER,
                json=True
            )
        ),
        destroy=lambda.cloud_assembly_schema.DestroyCommand(
            args=lambda.cloud_assembly_schema.DestroyOptions(
                force=True
            )
        )
    )
)

IntegTest(app, "integ-test",
    test_cases=[test_case]
)
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from .. import Construct as _Construct_e78e779f, Stack as _Stack_9f43e4a3
from ..cloud_assembly_schema import (
    CdkCommands as _CdkCommands_3043a8a5,
    Hooks as _Hooks_ffcd74d8,
    IntegManifest as _IntegManifest_8b169ea0,
    TestOptions as _TestOptions_4ebd1db7,
)


class IntegTest(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.integ_tests.IntegTest",
):
    '''(experimental) A collection of test cases.

    Each test case file should contain exactly one
    instance of this class.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        class StackUnderTest(Stack):
            def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
                super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        
                lambda_.Function(self, "Handler",
                    runtime=lambda_.Runtime.NODEJS_12_X,
                    handler="index.handler",
                    code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
                    architecture=architecture
                )
        
        # Beginning of the test suite
        app = App()
        
        stack = Stack(app, "stack")
        
        different_archs_case = IntegTestCase(stack, "DifferentArchitectures",
            stacks=[
                StackUnderTest(app, "Stack1",
                    architecture=lambda_.Architecture.ARM_64
                ),
                StackUnderTest(app, "Stack2",
                    architecture=lambda_.Architecture.X86_64
                )
            ]
        )
        
        # There must be exactly one instance of TestCase per file
        IntegTest(app, "integ-test",
        
            # Register as many test cases as you want here
            test_cases=[different_archs_case]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        test_cases: typing.Sequence["IntegTestCase"],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param test_cases: (experimental) List of test cases that make up this test.

        :stability: experimental
        '''
        props = IntegTestProps(test_cases=test_cases)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="onPrepare")
    def _on_prepare(self) -> None:
        '''(experimental) Perform final modifications before synthesis.

        This method can be implemented by derived constructs in order to perform
        final changes before synthesis. prepare() will be called after child
        constructs have been prepared.

        This is an advanced framework feature. Only use this if you
        understand the implications.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "onPrepare", []))


class IntegTestCase(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.integ_tests.IntegTestCase",
):
    '''(experimental) An integration test case.

    Allows the definition of test properties that
    apply to all stacks under this case.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        class StackUnderTest(Stack):
            def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
                super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        
                lambda_.Function(self, "Handler",
                    runtime=lambda_.Runtime.NODEJS_12_X,
                    handler="index.handler",
                    code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
                    architecture=architecture
                )
        
        # Beginning of the test suite
        app = App()
        
        stack = Stack(app, "stack")
        
        different_archs_case = IntegTestCase(stack, "DifferentArchitectures",
            stacks=[
                StackUnderTest(app, "Stack1",
                    architecture=lambda_.Architecture.ARM_64
                ),
                StackUnderTest(app, "Stack2",
                    architecture=lambda_.Architecture.X86_64
                )
            ]
        )
        
        # There must be exactly one instance of TestCase per file
        IntegTest(app, "integ-test",
        
            # Register as many test cases as you want here
            test_cases=[different_archs_case]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        stacks: typing.Sequence[_Stack_9f43e4a3],
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[_CdkCommands_3043a8a5] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[_Hooks_ffcd74d8] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param stacks: (experimental) Stacks to be deployed during the test.
        :param allow_destroy: (experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: (experimental) Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: (experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: (experimental) Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: (experimental) Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: (experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true

        :stability: experimental
        '''
        props = IntegTestCaseProps(
            stacks=stacks,
            allow_destroy=allow_destroy,
            cdk_command_options=cdk_command_options,
            diff_assets=diff_assets,
            hooks=hooks,
            regions=regions,
            stack_update_workflow=stack_update_workflow,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> _IntegManifest_8b169ea0:
        '''(experimental) The integration test manifest for this test case.

        Manifests are used
        by the integration test runner.

        :stability: experimental
        '''
        return typing.cast(_IntegManifest_8b169ea0, jsii.get(self, "manifest"))


@jsii.data_type(
    jsii_type="monocdk.integ_tests.IntegTestCaseProps",
    jsii_struct_bases=[_TestOptions_4ebd1db7],
    name_mapping={
        "allow_destroy": "allowDestroy",
        "cdk_command_options": "cdkCommandOptions",
        "diff_assets": "diffAssets",
        "hooks": "hooks",
        "regions": "regions",
        "stack_update_workflow": "stackUpdateWorkflow",
        "stacks": "stacks",
    },
)
class IntegTestCaseProps(_TestOptions_4ebd1db7):
    def __init__(
        self,
        *,
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[_CdkCommands_3043a8a5] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[_Hooks_ffcd74d8] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
        stacks: typing.Sequence[_Stack_9f43e4a3],
    ) -> None:
        '''(experimental) Properties of an integration test case.

        :param allow_destroy: (experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: (experimental) Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: (experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: (experimental) Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: (experimental) Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: (experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true
        :param stacks: (experimental) Stacks to be deployed during the test.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            class StackUnderTest(Stack):
                def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
                    super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
            
                    lambda_.Function(self, "Handler",
                        runtime=lambda_.Runtime.NODEJS_12_X,
                        handler="index.handler",
                        code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
                        architecture=architecture
                    )
            
            # Beginning of the test suite
            app = App()
            
            stack = Stack(app, "stack")
            
            different_archs_case = IntegTestCase(stack, "DifferentArchitectures",
                stacks=[
                    StackUnderTest(app, "Stack1",
                        architecture=lambda_.Architecture.ARM_64
                    ),
                    StackUnderTest(app, "Stack2",
                        architecture=lambda_.Architecture.X86_64
                    )
                ]
            )
            
            # There must be exactly one instance of TestCase per file
            IntegTest(app, "integ-test",
            
                # Register as many test cases as you want here
                test_cases=[different_archs_case]
            )
        '''
        if isinstance(cdk_command_options, dict):
            cdk_command_options = _CdkCommands_3043a8a5(**cdk_command_options)
        if isinstance(hooks, dict):
            hooks = _Hooks_ffcd74d8(**hooks)
        self._values: typing.Dict[str, typing.Any] = {
            "stacks": stacks,
        }
        if allow_destroy is not None:
            self._values["allow_destroy"] = allow_destroy
        if cdk_command_options is not None:
            self._values["cdk_command_options"] = cdk_command_options
        if diff_assets is not None:
            self._values["diff_assets"] = diff_assets
        if hooks is not None:
            self._values["hooks"] = hooks
        if regions is not None:
            self._values["regions"] = regions
        if stack_update_workflow is not None:
            self._values["stack_update_workflow"] = stack_update_workflow

    @builtins.property
    def allow_destroy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test.

        This list should only include resources that for this specific
        integration test we are sure will not cause errors or an outage if
        destroyed. For example, maybe we know that a new resource will be created
        first before the old resource is destroyed which prevents any outage.

        e.g. ['AWS::IAM::Role']

        :default: - do not allow destruction of any resources on update

        :stability: experimental
        '''
        result = self._values.get("allow_destroy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_command_options(self) -> typing.Optional[_CdkCommands_3043a8a5]:
        '''(experimental) Additional options to use for each CDK command.

        :default: - runner default options

        :stability: experimental
        '''
        result = self._values.get("cdk_command_options")
        return typing.cast(typing.Optional[_CdkCommands_3043a8a5], result)

    @builtins.property
    def diff_assets(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included.

        For example
        any tests involving custom resources or bundling

        :default: false

        :stability: experimental
        '''
        result = self._values.get("diff_assets")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def hooks(self) -> typing.Optional[_Hooks_ffcd74d8]:
        '''(experimental) Additional commands to run at predefined points in the test workflow.

        e.g. { postDeploy: ['yarn', 'test'] }

        :default: - no hooks

        :stability: experimental
        '''
        result = self._values.get("hooks")
        return typing.cast(typing.Optional[_Hooks_ffcd74d8], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Limit deployment to these regions.

        :default: - can run in any region

        :stability: experimental
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stack_update_workflow(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("stack_update_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stacks(self) -> typing.List[_Stack_9f43e4a3]:
        '''(experimental) Stacks to be deployed during the test.

        :stability: experimental
        '''
        result = self._values.get("stacks")
        assert result is not None, "Required property 'stacks' is missing"
        return typing.cast(typing.List[_Stack_9f43e4a3], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegTestCaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.integ_tests.IntegTestProps",
    jsii_struct_bases=[],
    name_mapping={"test_cases": "testCases"},
)
class IntegTestProps:
    def __init__(self, *, test_cases: typing.Sequence[IntegTestCase]) -> None:
        '''(experimental) Integration test properties.

        :param test_cases: (experimental) List of test cases that make up this test.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            class StackUnderTest(Stack):
                def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
                    super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
            
                    lambda_.Function(self, "Handler",
                        runtime=lambda_.Runtime.NODEJS_12_X,
                        handler="index.handler",
                        code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
                        architecture=architecture
                    )
            
            # Beginning of the test suite
            app = App()
            
            stack = Stack(app, "stack")
            
            different_archs_case = IntegTestCase(stack, "DifferentArchitectures",
                stacks=[
                    StackUnderTest(app, "Stack1",
                        architecture=lambda_.Architecture.ARM_64
                    ),
                    StackUnderTest(app, "Stack2",
                        architecture=lambda_.Architecture.X86_64
                    )
                ]
            )
            
            # There must be exactly one instance of TestCase per file
            IntegTest(app, "integ-test",
            
                # Register as many test cases as you want here
                test_cases=[different_archs_case]
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "test_cases": test_cases,
        }

    @builtins.property
    def test_cases(self) -> typing.List[IntegTestCase]:
        '''(experimental) List of test cases that make up this test.

        :stability: experimental
        '''
        result = self._values.get("test_cases")
        assert result is not None, "Required property 'test_cases' is missing"
        return typing.cast(typing.List[IntegTestCase], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegTestProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IntegTest",
    "IntegTestCase",
    "IntegTestCaseProps",
    "IntegTestProps",
]

publication.publish()
