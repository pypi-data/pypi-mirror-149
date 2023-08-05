'''
# AWS CDK Github OpenID Connect

![cdk-support](https://img.shields.io/badge/cdk-%20typescript%20%7C%20python%20-informational)
[![release](https://github.com/aripalo/aws-cdk-github-oidc/actions/workflows/release.yml/badge.svg)](https://github.com/aripalo/aws-cdk-github-oidc/actions/workflows/release.yml)
[![codecov](https://codecov.io/gh/aripalo/aws-cdk-github-oidc/branch/main/graph/badge.svg?token=5X44RM6J17)](https://codecov.io/gh/aripalo/aws-cdk-github-oidc)

---


AWS [CDK](https://aws.amazon.com/cdk/) constructs that define:

* Github Actions as OpenID Connect Identity Provider into AWS IAM
* IAM Roles that can be assumed by Github Actions workflows

These constructs allows you to harden your AWS deployment security by removing the need to create long-term access keys for Github Actions and instead use OpenID Connect to Authenticate your Github Action workflow with AWS IAM.

## Background information

![github-aws-oidc](/assets/github-aws-oidc.svg)

* [GitHub Actions: Secure cloud deployments with OpenID Connect](https://github.blog/changelog/2021-10-27-github-actions-secure-cloud-deployments-with-openid-connect/) on Github Changelog Blog.
* [Security hardening your deployments](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments) on Github Docs.
* [Assuming a role with `aws-actions/configure-aws-credentials`](https://github.com/aws-actions/configure-aws-credentials#assuming-a-role).
* Shout-out to [Richard H. Boyd](https://twitter.com/rchrdbyd) for helping me to debug Github OIDC setup with AWS IAM and his [Deploying to AWS with Github Actions](https://www.githubuniverse.com/2021/session/692586/deploying-to-aws-with-github-actions)-talk.
* Shout-out to [Aidan W Steele](https://twitter.com/__steele) and his blog post [AWS federation comes to GitHub Actions](https://awsteele.com/blog/2021/09/15/aws-federation-comes-to-github-actions.html) for being the original inspiration for this.

<br/>

## Getting started

```shell
npm i -D aws-cdk-github-oidc
```

<br/>

### OpenID Connect Identity Provider trust for AWS IAM

To create a new Github OIDC provider configuration into AWS IAM:

```python
import { GithubActionsIdentityProvider } from 'aws-cdk-github-oidc';

const provider = new GithubActionsIdentityProvider(scope, 'GithubProvider');
```

In the background this creates an OIDC provider trust configuration into AWS IAM with an [issuer URL of `https://token.actions.githubusercontent.com`](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services#adding-the-identity-provider-to-aws), audiences (client IDs) configured as `['sts.amazonaws.com']` (which matches the [`aws-actions/configure-aws-credentials`](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services#adding-the-identity-provider-to-aws) implementation) and the thumbprint as Github's `a031c46782e6e6c662c2c87c76da9aa62ccabd8e`

<br/>

### Retrieving a reference to an existing Github OIDC provider configuration

Remember, **there can be only one (Github OIDC provider per AWS Account)**, so to retrieve a reference to existing Github OIDC provider use `fromAccount` static method:

```python
import { GithubActionsIdentityProvider } from 'aws-cdk-github-oidc';

const provider = GithubActionsIdentityProvider.fromAccount(scope, 'GithubProvider');
```

<br/>

### Defining a role for Github Actions workflow to assume

```python
import { GithubActionsRole } from 'aws-cdk-github-oidc';

const uploadRole = new GithubActionsRole(scope, 'UploadRole', {
  provider: provider,           // reference into the OIDC provider
  owner: 'octo-org',            // your repository owner (organization or user) name
  repo: 'octo-repo',            // your repository name (without the owner name)
  filter: 'ref:refs/tags/v*',   // JWT sub suffix filter, defaults to '*'
});

// use it like any other role, for example grant S3 bucket write access:
myBucket.grantWrite(uploadRole);
```

You may pass in any `iam.RoleProps` into the construct's props, except `assumedBy` which will be defined by this construct (CDK will fail if you do):

```python
const deployRole = new GithubActionsRole(scope, 'DeployRole', {
  provider: provider,
  owner: 'octo-org',
  repo: 'octo-repo',
  roleName: 'MyDeployRole',
  description: 'This role deploys stuff to AWS',
  maxSessionDuration: cdk.Duration.hours(2),
});

// You may also use various "add*" policy methods!
// "AdministratorAccess" not really a good idea, just for an example here:
deployRole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName('AdministratorAccess'));
```

<br/>

#### Subject Filter

By default the value of `filter` property will be `'*'` which means any workflow (from given repository) from any branch, tag, environment or pull request can assume this role. To further stricten the OIDC trust policy on the role, you may adjust the subject filter as seen on the [examples in Github Docs](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#configuring-the-oidc-trust-with-the-cloud); For example:

|         `filter` value         |                Descrition                |
| :----------------------------- | :--------------------------------------- |
| `'ref:refs/tags/v*'`           | Allow only tags with prefix of `v`       |
| `'ref:refs/heads/demo-branch'` | Allow only from branch `demo-branch`     |
| `'pull_request'`               | Allow only from pull request             |
| `'environment:Production'`     | Allow only from `Production` environment |

<br/>

### Github Actions Workflow

To actually utilize this in your Github Actions workflow, use [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials) to [assume a role](https://github.com/aws-actions/configure-aws-credentials#assuming-a-role).

At the moment you must use the `master` version (until AWS releases a new tag):

```yaml
jobs:
  deploy:
    name: Upload to Amazon S3
    runs-on: ubuntu-latest
    permissions:
      id-token: write # needed to interact with GitHub's OIDC Token endpoint.
      contents: read
    steps:
    - name: Checkout
      uses: actions/checkout@v2

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@master
      with:
        role-to-assume: arn:aws:iam::123456789012:role/MyUploadRole
        #role-session-name: MySessionName # Optional
        aws-region: us-east-1

    - name: Sync files to S3
      run: |
        aws s3 sync . s3://my-example-bucket
```

<br/>

### Development Status

These constructs are fresh out from the oven, since [Github just announced](https://github.blog/changelog/2021-10-27-github-actions-secure-cloud-deployments-with-openid-connect/) the OpenID Connect feature as generally available. I've been playing around with the feature for some time, but the construct itself haven't yet been widely used.

These constructs will stay in `v0.x.x` for a while, to allow easier bug fixing & breaking changes *if absolutely needed*. Once bugs are fixed (if any), the constructs will be published with `v1` major version and will be marked as stable.

Currently only TypeScript and Python versions provided, but before going to stable, I'll probably others (supported by JSII) depending on the amount of work required - so no promises!
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

import aws_cdk
import aws_cdk.aws_iam
import constructs


class GithubActionsRole(
    aws_cdk.aws_iam.Role,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-github-oidc.GithubActionsRole",
):
    '''(experimental) Define an IAM Role that can be assumed by Github Actions workflow via Github OpenID Connect Identity Provider.

    Besides ``GithubConfiguration``, you may pass in any ``iam.RoleProps`` except ``assumedBy``
    which will be defined by this construct (CDK will fail if you do).

    :stability: experimental

    Example::

        const uploadRole = new GithubActionsRole(scope, "UploadRole", {
          provider: GithubActionsIdentityProvider.fromAccount(scope, "GithubProvider"),
          owner: 'octo-org',
          repo: 'octo-repo',
          filter: 'ref:refs/tags/v*',
          roleName: 'MyUploadRole',
        });
        
        myBucket.grantWrite(uploadRole);
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        owner: builtins.str,
        provider: "IGithubActionsIdentityProvider",
        repo: builtins.str,
        filter: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IManagedPolicy]] = None,
        max_session_duration: typing.Optional[aws_cdk.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[aws_cdk.aws_iam.IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Define an IAM Role that can be assumed by Github Actions workflow via Github OpenID Connect Identity Provider.

        Besides ``GithubConfiguration``, you may pass in any ``iam.RoleProps`` except ``assumedBy``
        which will be defined by this construct (CDK will fail if you do).

        :param scope: -
        :param id: -
        :param owner: (experimental) Repository owner (organization or username).
        :param provider: (experimental) Reference to Github OpenID Connect Provider configured in AWS IAM. Either pass an construct defined by ``new GithubActionsIdentityProvider`` or a retrieved reference from ``GithubActionsIdentityProvider.fromAccount``. There can be only one (per AWS Account).
        :param repo: (experimental) Repository name (slug) without the owner.
        :param filter: (experimental) Subject condition filter, appended after ``repo:${owner}/${repo}:`` string in IAM Role trust relationship. Default: '*' You may use this value to only allow Github to assume the role on specific branches, tags, environments, pull requests etc.
        :param description: A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.

        :stability: experimental

        Example::

            const uploadRole = new GithubActionsRole(scope, "UploadRole", {
              provider: GithubActionsIdentityProvider.fromAccount(scope, "GithubProvider"),
              owner: 'octo-org',
              repo: 'octo-repo',
              filter: 'ref:refs/tags/v*',
              roleName: 'MyUploadRole',
            });
            
            myBucket.grantWrite(uploadRole);
        '''
        props = GithubActionsRoleProps(
            owner=owner,
            provider=provider,
            repo=repo,
            filter=filter,
            description=description,
            external_ids=external_ids,
            inline_policies=inline_policies,
            managed_policies=managed_policies,
            max_session_duration=max_session_duration,
            path=path,
            permissions_boundary=permissions_boundary,
            role_name=role_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-cdk-github-oidc.GithubConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "owner": "owner",
        "provider": "provider",
        "repo": "repo",
        "filter": "filter",
    },
)
class GithubConfiguration:
    def __init__(
        self,
        *,
        owner: builtins.str,
        provider: "IGithubActionsIdentityProvider",
        repo: builtins.str,
        filter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Github related configuration that forms the trust policy for this IAM Role.

        :param owner: (experimental) Repository owner (organization or username).
        :param provider: (experimental) Reference to Github OpenID Connect Provider configured in AWS IAM. Either pass an construct defined by ``new GithubActionsIdentityProvider`` or a retrieved reference from ``GithubActionsIdentityProvider.fromAccount``. There can be only one (per AWS Account).
        :param repo: (experimental) Repository name (slug) without the owner.
        :param filter: (experimental) Subject condition filter, appended after ``repo:${owner}/${repo}:`` string in IAM Role trust relationship. Default: '*' You may use this value to only allow Github to assume the role on specific branches, tags, environments, pull requests etc.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "owner": owner,
            "provider": provider,
            "repo": repo,
        }
        if filter is not None:
            self._values["filter"] = filter

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) Repository owner (organization or username).

        :stability: experimental

        Example::

            'octo-org'
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider(self) -> "IGithubActionsIdentityProvider":
        '''(experimental) Reference to Github OpenID Connect Provider configured in AWS IAM.

        Either pass an construct defined by ``new GithubActionsIdentityProvider``
        or a retrieved reference from ``GithubActionsIdentityProvider.fromAccount``.
        There can be only one (per AWS Account).

        :stability: experimental
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast("IGithubActionsIdentityProvider", result)

    @builtins.property
    def repo(self) -> builtins.str:
        '''(experimental) Repository name (slug) without the owner.

        :stability: experimental

        Example::

            'octo-repo'
        '''
        result = self._values.get("repo")
        assert result is not None, "Required property 'repo' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''(experimental) Subject condition filter, appended after ``repo:${owner}/${repo}:`` string in IAM Role trust relationship.

        :default:

        '*'

        You may use this value to only allow Github to assume the role on specific branches, tags, environments, pull requests etc.

        :see: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#examples
        :stability: experimental

        Example::

            'ref:refs/tags/v*'
            'ref:refs/heads/demo-branch'
            'pull_request'
            'environment:Production'
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-cdk-github-oidc.IGithubActionsIdentityProvider")
class IGithubActionsIdentityProvider(
    aws_cdk.aws_iam.IOpenIdConnectProvider,
    typing_extensions.Protocol,
):
    '''(experimental) Describes a Github OpenID Connect Identity Provider for AWS IAM.

    :stability: experimental
    '''

    pass


class _IGithubActionsIdentityProviderProxy(
    jsii.proxy_for(aws_cdk.aws_iam.IOpenIdConnectProvider) # type: ignore[misc]
):
    '''(experimental) Describes a Github OpenID Connect Identity Provider for AWS IAM.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-github-oidc.IGithubActionsIdentityProvider"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGithubActionsIdentityProvider).__jsii_proxy_class__ = lambda : _IGithubActionsIdentityProviderProxy


@jsii.data_type(
    jsii_type="aws-cdk-github-oidc.RoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "external_ids": "externalIds",
        "inline_policies": "inlinePolicies",
        "managed_policies": "managedPolicies",
        "max_session_duration": "maxSessionDuration",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "role_name": "roleName",
    },
)
class RoleProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IManagedPolicy]] = None,
        max_session_duration: typing.Optional[aws_cdk.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[aws_cdk.aws_iam.IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining an IAM Role.

        These are copied fron @aws-cdk/aws-iam, but since JSII does not support
        TypeScript <Partial<iam.RoleProps>> (or Omit), we have to do this stupid thing.

        Basically exactly the same as source, but with assumedBy removed.

        :param description: A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if external_ids is not None:
            self._values["external_ids"] = external_ids
        if inline_policies is not None:
            self._values["inline_policies"] = inline_policies
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if max_session_duration is not None:
            self._values["max_session_duration"] = max_session_duration
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the role.

        It can be up to 1000 characters long.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of IDs that the role assumer needs to provide one of when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        :default: No external ID required
        '''
        result = self._values.get("external_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def inline_policies(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]]:
        '''A list of named policies to inline into this role.

        These policies will be
        created with the role, whereas those added by ``addToPolicy`` are added
        using a separate CloudFormation resource (allowing a way around circular
        dependencies that could otherwise be introduced).

        :default: - No policy is inlined in the Role resource.
        '''
        result = self._values.get("inline_policies")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]], result)

    @builtins.property
    def managed_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.IManagedPolicy]]:
        '''A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        :default: - No managed policies.
        '''
        result = self._values.get("managed_policies")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.IManagedPolicy]], result)

    @builtins.property
    def max_session_duration(self) -> typing.Optional[aws_cdk.Duration]:
        '''The maximum session duration that you want to set for the specified role.

        This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours.

        Anyone who assumes the role from the AWS CLI or API can use the
        DurationSeconds API parameter or the duration-seconds CLI parameter to
        request a longer session. The MaxSessionDuration setting determines the
        maximum duration that can be requested using the DurationSeconds
        parameter.

        If users don't specify a value for the DurationSeconds parameter, their
        security credentials are valid for one hour by default. This applies when
        you use the AssumeRole* API operations or the assume-role* CLI operations
        but does not apply when you use those operations to create a console URL.

        :default: Duration.hours(1)

        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html
        '''
        result = self._values.get("max_session_duration")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path associated with this role.

        For information about IAM paths, see
        Friendly Names and Paths in IAM User Guide.

        :default: /
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[aws_cdk.aws_iam.IManagedPolicy]:
        '''AWS supports permissions boundaries for IAM entities (users or roles).

        A permissions boundary is an advanced feature for using a managed policy
        to set the maximum permissions that an identity-based policy can grant to
        an IAM entity. An entity's permissions boundary allows it to perform only
        the actions that are allowed by both its identity-based policies and its
        permissions boundaries.

        :default: - No permissions boundary.

        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IManagedPolicy], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''A name for the IAM role.

        For valid values, see the RoleName parameter for
        the CreateRole action in the IAM API Reference.

        IMPORTANT: If you specify a name, you cannot perform updates that require
        replacement of this resource. You can perform updates that require no or
        some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the role name.
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IGithubActionsIdentityProvider)
class GithubActionsIdentityProvider(
    aws_cdk.aws_iam.OpenIdConnectProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-github-oidc.GithubActionsIdentityProvider",
):
    '''(experimental) Github Actions as OpenID Connect Identity Provider for AWS IAM. There can be only one (per AWS Account).

    Use ``fromAccount`` to retrieve a reference to existing Github OIDC provider.

    :see: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
    :stability: experimental
    '''

    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''(experimental) Define a new Github OpenID Connect Identity PRovider for AWS IAM.

        There can be only one (per AWS Account).

        :param scope: CDK Stack or Construct to which the provider is assigned to.
        :param id: CDK Construct ID given to the construct.

        :stability: experimental

        Example::

            new GithubActionsIdentityProvider(scope, "GithubProvider");
        '''
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="fromAccount") # type: ignore[misc]
    @builtins.classmethod
    def from_account(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
    ) -> IGithubActionsIdentityProvider:
        '''(experimental) Retrieve a reference to existing Github OIDC provider in your AWS account.

        An AWS account can only have single Github OIDC provider configured into it,
        so internally the reference is made by constructing the ARN from AWS
        Account ID & Github issuer URL.

        :param scope: CDK Stack or Construct to which the provider is assigned to.
        :param id: CDK Construct ID given to the construct.

        :return: a CDK Construct representing the Github OIDC provider

        :stability: experimental

        Example::

            GithubActionsIdentityProvider.fromAccount(scope, "GithubProvider");
        '''
        return typing.cast(IGithubActionsIdentityProvider, jsii.sinvoke(cls, "fromAccount", [scope, id]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="issuer")
    def ISSUER(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "issuer"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="thumbprints")
    def THUMBPRINTS(cls) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "thumbprints"))


@jsii.data_type(
    jsii_type="aws-cdk-github-oidc.GithubActionsRoleProps",
    jsii_struct_bases=[GithubConfiguration, RoleProps],
    name_mapping={
        "owner": "owner",
        "provider": "provider",
        "repo": "repo",
        "filter": "filter",
        "description": "description",
        "external_ids": "externalIds",
        "inline_policies": "inlinePolicies",
        "managed_policies": "managedPolicies",
        "max_session_duration": "maxSessionDuration",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "role_name": "roleName",
    },
)
class GithubActionsRoleProps(GithubConfiguration, RoleProps):
    def __init__(
        self,
        *,
        owner: builtins.str,
        provider: IGithubActionsIdentityProvider,
        repo: builtins.str,
        filter: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IManagedPolicy]] = None,
        max_session_duration: typing.Optional[aws_cdk.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[aws_cdk.aws_iam.IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Props that define the IAM Role that can be assumed by Github Actions workflow via Github OpenID Connect Identity Provider.

        Besides ``GithubConfiguration``, you may pass in any ``iam.RoleProps`` except ``assumedBy``
        which will be defined by this construct (CDK will fail if you do).

        :param owner: (experimental) Repository owner (organization or username).
        :param provider: (experimental) Reference to Github OpenID Connect Provider configured in AWS IAM. Either pass an construct defined by ``new GithubActionsIdentityProvider`` or a retrieved reference from ``GithubActionsIdentityProvider.fromAccount``. There can be only one (per AWS Account).
        :param repo: (experimental) Repository name (slug) without the owner.
        :param filter: (experimental) Subject condition filter, appended after ``repo:${owner}/${repo}:`` string in IAM Role trust relationship. Default: '*' You may use this value to only allow Github to assume the role on specific branches, tags, environments, pull requests etc.
        :param description: A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.

        :stability: experimental

        Example::

            {
              provider: GithubActionsIdentityProvider.fromAccount(scope, "GithubProvider"),
              owner: 'octo-org',
              repo: 'octo-repo',
              filter: 'ref:refs/tags/v*',
              roleName: 'MyDeployRole',
            }
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "owner": owner,
            "provider": provider,
            "repo": repo,
        }
        if filter is not None:
            self._values["filter"] = filter
        if description is not None:
            self._values["description"] = description
        if external_ids is not None:
            self._values["external_ids"] = external_ids
        if inline_policies is not None:
            self._values["inline_policies"] = inline_policies
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if max_session_duration is not None:
            self._values["max_session_duration"] = max_session_duration
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) Repository owner (organization or username).

        :stability: experimental

        Example::

            'octo-org'
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider(self) -> IGithubActionsIdentityProvider:
        '''(experimental) Reference to Github OpenID Connect Provider configured in AWS IAM.

        Either pass an construct defined by ``new GithubActionsIdentityProvider``
        or a retrieved reference from ``GithubActionsIdentityProvider.fromAccount``.
        There can be only one (per AWS Account).

        :stability: experimental
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast(IGithubActionsIdentityProvider, result)

    @builtins.property
    def repo(self) -> builtins.str:
        '''(experimental) Repository name (slug) without the owner.

        :stability: experimental

        Example::

            'octo-repo'
        '''
        result = self._values.get("repo")
        assert result is not None, "Required property 'repo' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''(experimental) Subject condition filter, appended after ``repo:${owner}/${repo}:`` string in IAM Role trust relationship.

        :default:

        '*'

        You may use this value to only allow Github to assume the role on specific branches, tags, environments, pull requests etc.

        :see: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#examples
        :stability: experimental

        Example::

            'ref:refs/tags/v*'
            'ref:refs/heads/demo-branch'
            'pull_request'
            'environment:Production'
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the role.

        It can be up to 1000 characters long.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of IDs that the role assumer needs to provide one of when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        :default: No external ID required
        '''
        result = self._values.get("external_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def inline_policies(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]]:
        '''A list of named policies to inline into this role.

        These policies will be
        created with the role, whereas those added by ``addToPolicy`` are added
        using a separate CloudFormation resource (allowing a way around circular
        dependencies that could otherwise be introduced).

        :default: - No policy is inlined in the Role resource.
        '''
        result = self._values.get("inline_policies")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]], result)

    @builtins.property
    def managed_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.IManagedPolicy]]:
        '''A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        :default: - No managed policies.
        '''
        result = self._values.get("managed_policies")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.IManagedPolicy]], result)

    @builtins.property
    def max_session_duration(self) -> typing.Optional[aws_cdk.Duration]:
        '''The maximum session duration that you want to set for the specified role.

        This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours.

        Anyone who assumes the role from the AWS CLI or API can use the
        DurationSeconds API parameter or the duration-seconds CLI parameter to
        request a longer session. The MaxSessionDuration setting determines the
        maximum duration that can be requested using the DurationSeconds
        parameter.

        If users don't specify a value for the DurationSeconds parameter, their
        security credentials are valid for one hour by default. This applies when
        you use the AssumeRole* API operations or the assume-role* CLI operations
        but does not apply when you use those operations to create a console URL.

        :default: Duration.hours(1)

        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html
        '''
        result = self._values.get("max_session_duration")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path associated with this role.

        For information about IAM paths, see
        Friendly Names and Paths in IAM User Guide.

        :default: /
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[aws_cdk.aws_iam.IManagedPolicy]:
        '''AWS supports permissions boundaries for IAM entities (users or roles).

        A permissions boundary is an advanced feature for using a managed policy
        to set the maximum permissions that an identity-based policy can grant to
        an IAM entity. An entity's permissions boundary allows it to perform only
        the actions that are allowed by both its identity-based policies and its
        permissions boundaries.

        :default: - No permissions boundary.

        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IManagedPolicy], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''A name for the IAM role.

        For valid values, see the RoleName parameter for
        the CreateRole action in the IAM API Reference.

        IMPORTANT: If you specify a name, you cannot perform updates that require
        replacement of this resource. You can perform updates that require no or
        some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the role name.
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubActionsRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GithubActionsIdentityProvider",
    "GithubActionsRole",
    "GithubActionsRoleProps",
    "GithubConfiguration",
    "IGithubActionsIdentityProvider",
    "RoleProps",
]

publication.publish()
