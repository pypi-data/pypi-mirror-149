'''
# cdk-amazon-chime-resources

![Experimental](https://img.shields.io/badge/experimental-important.svg?style=for-the-badge)

An AWS Cloud Development Kit (AWS CDK) construct library that allows you to provision Amazon Chime resources with npm and pypi

## Background

Amazon Chime resources (Phone numbers, SIP media applications, and Voice Connectors) are not natively available in AWS CloudFormation or AWS CDK. Therefore, in order to create these resources with AWS CDK, an AWS Lambda backed custom resource must be used. In an effort to simplify that process, this AWS CDK construct has been created. This AWS CDK construct will create a custom resource and associated Lambda and expose constructs that can be used to create corresponding resources.

## Usage

See [example/lib/cdk-chime-resources-example.ts](example/lib/cdk-chime-resources-example.ts) for a complete example.

To add to your AWS CDK package.json file:

```
yarn add cdk-amazon-chime-resources
```

Within your AWS CDK:

### Phone Number Creation

```python
const phoneNumber = new chime.ChimePhoneNumber(this, 'phoneNumber', {
  phoneState: 'IL',
  phoneNumberType: chime.PhoneNumberType.LOCAL,
  phoneProductType: chime.PhoneProductType.SMA,
});
```

The phone number created will be a `LOCAL` number for use with `SMA` from a pool of available numbers in Illinois. Other search option are available that will return a single phone number based on the criteria provided.

### SIP Media Application Creation

```python
const sipMediaApp = new chime.ChimeSipMediaApp(this, 'sipMediaApp', {
  region: this.region,
  endpoint: smaHandler.functionArn,
});
```

The SIP media application created will use the smaHandler referenced by the endpoint in the same region the AWS CDK is being deployed in. The SIP media application must be created in the same region as the associated Lambda endpoint and must be in `us-east-1` or `us-west-2`.

### SIP Media Application Rule Creation

```python
const sipRule = new chime.ChimeSipRule(this, 'sipRule', {
  triggerType: chime.TriggerType.TO_PHONE_NUMBER,
  triggerValue: phoneNumber.phoneNumber,
  targetApplications: [
    {
      region: this.region,
      priority: 1,
      sipMediaApplicationId: sipMediaApp.sipMediaAppId,
    },
  ],
});
```

The SIP rule will assocaite the previously created phone number with the previously created SIP media application. The SIP rule can be associated with either an E.164 number or Amazon Chime Voice Connector URI. If the TriggerType is `TO_PHONE_NUMBER`, the TriggerValue must be an E.164 number. If the TriggerType is `REQUEST_URI_HOSTNAME`, the TriggerValue must be an Amazon Chime Voice Connector URI. A priority must be assigned with a value between 1 and 25 inclusive. A targetApplication is required. This will associate the trigger to the SIP media application and associated Lambda.

### Voice Connector Creation

Using a phone number created with Product Type of VC:

```python
const voiceConnector = new chime.ChimeVoiceConnector(this, 'voiceConnector', {
  encryption: true,
  name: 'string',
  region: 'us-east-1',
  termination: {
    terminationCidrs: ['198.51.100.10/32'],
    callingRegions: ['US'],
  },
  origination: [
    {
      host: '198.51.100.10',
      port: 5061,
      protocol: chime.Protocol.TCP,
      priority: 1,
      weight: 1,
    },
  ],
  streaming: {
    enabled: true,
    dataRetention: 0,
    notificationTargets: [chime.NotificationTargetType.EVENTBRIDGE],
  },
});
```

This will create an Amazon Chime Voice Connector with specified options. Termination, origination, and streaming are all optional.

```python
voiceConnectorPhone.associateWithVoiceConnector(voiceConnector);
```

This will assocaite the previously created phone number with the voice connector.

## Not Supported Yet

This is a work in progress.

Features that are not supported yet:

* [ ] Amazon Chime Voice Connector Groups
* [ ] Amazon Chime Voice Connector Logging
* [ ] Amazon Chime Voice Connector Emergency Calling
* [ ] Updates to created resources

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for more information.

## License

This project is licensed under the Apache-2.0 License.
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
import aws_cdk.aws_lambda
import aws_cdk.custom_resources
import constructs


class ChimePhoneNumber(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.ChimePhoneNumber",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        phone_product_type: "PhoneProductType",
        phone_area_code: typing.Optional[jsii.Number] = None,
        phone_city: typing.Optional[builtins.str] = None,
        phone_country: typing.Optional["PhoneCountry"] = None,
        phone_number_toll_free_prefix: typing.Optional[jsii.Number] = None,
        phone_number_type: typing.Optional["PhoneNumberType"] = None,
        phone_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param phone_product_type: Phone Product Type (required) - SipMediaApplicationDialIn or VoiceConnector. Default: - None
        :param phone_area_code: Area Code for phone number request (optional) - Usable only with US Country. Default: - None
        :param phone_city: City for phone number request (optional) - Usable only with US Country. Default: - None
        :param phone_country: Country for phone number request (optional) - See https://docs.aws.amazon.com/chime/latest/ag/phone-country-reqs.html for more details. Default: - US
        :param phone_number_toll_free_prefix: Toll Free Prefix for phone number request (optional). Default: - None
        :param phone_number_type: Phone Number Type for phone number request (optional) - Local or TollFree - Required with non-US country. Default: - None
        :param phone_state: State for phone number request (optional) - Usable only with US Country. Default: - None
        '''
        props = PhoneNumberProps(
            phone_product_type=phone_product_type,
            phone_area_code=phone_area_code,
            phone_city=phone_city,
            phone_country=phone_country,
            phone_number_toll_free_prefix=phone_number_toll_free_prefix,
            phone_number_type=phone_number_type,
            phone_state=phone_state,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="associateWithVoiceConnector")
    def associate_with_voice_connector(
        self,
        voice_connector_id: "ChimeVoiceConnector",
    ) -> "PhoneAssociation":
        '''
        :param voice_connector_id: -
        '''
        return typing.cast("PhoneAssociation", jsii.invoke(self, "associateWithVoiceConnector", [voice_connector_id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.ChimeResourceProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "properties": "properties",
        "resource_type": "resourceType",
        "uid": "uid",
    },
)
class ChimeResourceProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        properties: typing.Mapping[builtins.str, typing.Any],
        resource_type: builtins.str,
        uid: builtins.str,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param properties: 
        :param resource_type: 
        :param uid: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "properties": properties,
            "resource_type": resource_type,
            "uid": uid,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        result = self._values.get("properties")
        assert result is not None, "Required property 'properties' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.Any], result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uid(self) -> builtins.str:
        result = self._values.get("uid")
        assert result is not None, "Required property 'uid' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimeResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimeResources(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.ChimeResources",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        properties: typing.Mapping[builtins.str, typing.Any],
        resource_type: builtins.str,
        uid: builtins.str,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param properties: 
        :param resource_type: 
        :param uid: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        props = ChimeResourceProps(
            properties=properties,
            resource_type=resource_type,
            uid=uid,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="chimeCustomResource")
    def chime_custom_resource(self) -> aws_cdk.CustomResource:
        return typing.cast(aws_cdk.CustomResource, jsii.get(self, "chimeCustomResource"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> aws_cdk.aws_lambda.IFunction:
        return typing.cast(aws_cdk.aws_lambda.IFunction, jsii.get(self, "lambda"))


class ChimeSipMediaApp(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.ChimeSipMediaApp",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        endpoint: builtins.str,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param endpoint: endpoint for SipMediaApplication(required). Default: - none
        :param name: name for SipMediaApplication (optional). Default: - unique ID for resource
        :param region: region for SipMediaApplication(required) - Must us-east-1 or us-west-2 and in the same region as the SipMediaApplication Lambda handler. Default: - same region as stack deployment
        '''
        props = SipMediaAppProps(endpoint=endpoint, name=name, region=region)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sipMediaAppId")
    def sip_media_app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sipMediaAppId"))


class ChimeSipRule(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.ChimeSipRule",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        target_applications: typing.Sequence["TargetApplications"],
        trigger_type: "TriggerType",
        trigger_value: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param target_applications: 
        :param trigger_type: Trigger Type for SipRule (required) - TO_PHONE_NUMBER or REQUEST_URI_HOSTNAME. Default: - none
        :param trigger_value: Trigger Value for SipRule (required) - EE.164 Phone Number or Voice Connector URI. Default: - none
        :param name: name for SipRule (optional). Default: - unique ID for resource
        '''
        props = SipRuleProps(
            target_applications=target_applications,
            trigger_type=trigger_type,
            trigger_value=trigger_value,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sipRuleId")
    def sip_rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sipRuleId"))


class ChimeVoiceConnector(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.ChimeVoiceConnector",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        encryption: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        origination: typing.Optional[typing.Sequence["Routes"]] = None,
        region: typing.Optional[builtins.str] = None,
        streaming: typing.Optional["Streaming"] = None,
        termination: typing.Optional["Termination"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param encryption: Encryption boolean for VoiceConnector. Default: - False
        :param name: name for VoiceConnector. Default: - unique ID for resource
        :param origination: 
        :param region: region for SipMediaApplication(required) - Must us-east-1 or us-west-2 and in the same region as the SipMediaApplication Lambda handler. Default: - same region as stack deployment
        :param streaming: 
        :param termination: 
        '''
        props = VoiceConnectorProps(
            encryption=encryption,
            name=name,
            origination=origination,
            region=region,
            streaming=streaming,
            termination=termination,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="voiceConnectorId")
    def voice_connector_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "voiceConnectorId"))


@jsii.enum(jsii_type="cdk-amazon-chime-resources.NotificationTargetType")
class NotificationTargetType(enum.Enum):
    EVENTBRIDGE = "EVENTBRIDGE"
    SNS = "SNS"
    SQS = "SQS"


class PhoneAssociation(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-amazon-chime-resources.PhoneAssociation",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        e164_phone_number: builtins.str,
        voice_connector_id: builtins.str,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param e164_phone_number: 
        :param voice_connector_id: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        props = PhoneAssociationProps(
            e164_phone_number=e164_phone_number,
            voice_connector_id=voice_connector_id,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="phoneAssociationResource")
    def phone_association_resource(self) -> aws_cdk.custom_resources.AwsCustomResource:
        return typing.cast(aws_cdk.custom_resources.AwsCustomResource, jsii.get(self, "phoneAssociationResource"))


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.PhoneAssociationProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "e164_phone_number": "e164PhoneNumber",
        "voice_connector_id": "voiceConnectorId",
    },
)
class PhoneAssociationProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        e164_phone_number: builtins.str,
        voice_connector_id: builtins.str,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param e164_phone_number: 
        :param voice_connector_id: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "e164_phone_number": e164_phone_number,
            "voice_connector_id": voice_connector_id,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def e164_phone_number(self) -> builtins.str:
        result = self._values.get("e164_phone_number")
        assert result is not None, "Required property 'e164_phone_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def voice_connector_id(self) -> builtins.str:
        result = self._values.get("voice_connector_id")
        assert result is not None, "Required property 'voice_connector_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PhoneAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-amazon-chime-resources.PhoneCountry")
class PhoneCountry(enum.Enum):
    AU = "AU"
    AT = "AT"
    CA = "CA"
    DK = "DK"
    DE = "DE"
    IE = "IE"
    IT = "IT"
    NZ = "NZ"
    NG = "NG"
    PR = "PR"
    KR = "KR"
    SE = "SE"
    CH = "CH"
    UK = "UK"
    US = "US"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.PhoneNumberProps",
    jsii_struct_bases=[],
    name_mapping={
        "phone_product_type": "phoneProductType",
        "phone_area_code": "phoneAreaCode",
        "phone_city": "phoneCity",
        "phone_country": "phoneCountry",
        "phone_number_toll_free_prefix": "phoneNumberTollFreePrefix",
        "phone_number_type": "phoneNumberType",
        "phone_state": "phoneState",
    },
)
class PhoneNumberProps:
    def __init__(
        self,
        *,
        phone_product_type: "PhoneProductType",
        phone_area_code: typing.Optional[jsii.Number] = None,
        phone_city: typing.Optional[builtins.str] = None,
        phone_country: typing.Optional[PhoneCountry] = None,
        phone_number_toll_free_prefix: typing.Optional[jsii.Number] = None,
        phone_number_type: typing.Optional["PhoneNumberType"] = None,
        phone_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Props for ``PhoneNumber``.

        :param phone_product_type: Phone Product Type (required) - SipMediaApplicationDialIn or VoiceConnector. Default: - None
        :param phone_area_code: Area Code for phone number request (optional) - Usable only with US Country. Default: - None
        :param phone_city: City for phone number request (optional) - Usable only with US Country. Default: - None
        :param phone_country: Country for phone number request (optional) - See https://docs.aws.amazon.com/chime/latest/ag/phone-country-reqs.html for more details. Default: - US
        :param phone_number_toll_free_prefix: Toll Free Prefix for phone number request (optional). Default: - None
        :param phone_number_type: Phone Number Type for phone number request (optional) - Local or TollFree - Required with non-US country. Default: - None
        :param phone_state: State for phone number request (optional) - Usable only with US Country. Default: - None
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "phone_product_type": phone_product_type,
        }
        if phone_area_code is not None:
            self._values["phone_area_code"] = phone_area_code
        if phone_city is not None:
            self._values["phone_city"] = phone_city
        if phone_country is not None:
            self._values["phone_country"] = phone_country
        if phone_number_toll_free_prefix is not None:
            self._values["phone_number_toll_free_prefix"] = phone_number_toll_free_prefix
        if phone_number_type is not None:
            self._values["phone_number_type"] = phone_number_type
        if phone_state is not None:
            self._values["phone_state"] = phone_state

    @builtins.property
    def phone_product_type(self) -> "PhoneProductType":
        '''Phone Product Type (required) - SipMediaApplicationDialIn or VoiceConnector.

        :default: - None
        '''
        result = self._values.get("phone_product_type")
        assert result is not None, "Required property 'phone_product_type' is missing"
        return typing.cast("PhoneProductType", result)

    @builtins.property
    def phone_area_code(self) -> typing.Optional[jsii.Number]:
        '''Area Code for phone number request (optional)  - Usable only with US Country.

        :default: - None
        '''
        result = self._values.get("phone_area_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def phone_city(self) -> typing.Optional[builtins.str]:
        '''City for phone number request (optional) - Usable only with US Country.

        :default: - None
        '''
        result = self._values.get("phone_city")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def phone_country(self) -> typing.Optional[PhoneCountry]:
        '''Country for phone number request (optional) - See https://docs.aws.amazon.com/chime/latest/ag/phone-country-reqs.html for more details.

        :default: - US
        '''
        result = self._values.get("phone_country")
        return typing.cast(typing.Optional[PhoneCountry], result)

    @builtins.property
    def phone_number_toll_free_prefix(self) -> typing.Optional[jsii.Number]:
        '''Toll Free Prefix for phone number request (optional).

        :default: - None
        '''
        result = self._values.get("phone_number_toll_free_prefix")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def phone_number_type(self) -> typing.Optional["PhoneNumberType"]:
        '''Phone Number Type for phone number request (optional) - Local or TollFree - Required with non-US country.

        :default: - None
        '''
        result = self._values.get("phone_number_type")
        return typing.cast(typing.Optional["PhoneNumberType"], result)

    @builtins.property
    def phone_state(self) -> typing.Optional[builtins.str]:
        '''State for phone number request (optional) - Usable only with US Country.

        :default: - None
        '''
        result = self._values.get("phone_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PhoneNumberProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-amazon-chime-resources.PhoneNumberType")
class PhoneNumberType(enum.Enum):
    LOCAL = "LOCAL"
    TOLLFREE = "TOLLFREE"


@jsii.enum(jsii_type="cdk-amazon-chime-resources.PhoneProductType")
class PhoneProductType(enum.Enum):
    SMA = "SMA"
    VC = "VC"


@jsii.enum(jsii_type="cdk-amazon-chime-resources.Protocol")
class Protocol(enum.Enum):
    TCP = "TCP"
    UDP = "UDP"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.Routes",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "port": "port",
        "priority": "priority",
        "protocol": "protocol",
        "weight": "weight",
    },
)
class Routes:
    def __init__(
        self,
        *,
        host: builtins.str,
        port: jsii.Number,
        priority: jsii.Number,
        protocol: Protocol,
        weight: jsii.Number,
    ) -> None:
        '''
        :param host: 
        :param port: 
        :param priority: 
        :param protocol: 
        :param weight: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "host": host,
            "port": port,
            "priority": priority,
            "protocol": protocol,
            "weight": weight,
        }

    @builtins.property
    def host(self) -> builtins.str:
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocol(self) -> Protocol:
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(Protocol, result)

    @builtins.property
    def weight(self) -> jsii.Number:
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Routes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.SipMediaAppProps",
    jsii_struct_bases=[],
    name_mapping={"endpoint": "endpoint", "name": "name", "region": "region"},
)
class SipMediaAppProps:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Props for ``SipMediaApplication``.

        :param endpoint: endpoint for SipMediaApplication(required). Default: - none
        :param name: name for SipMediaApplication (optional). Default: - unique ID for resource
        :param region: region for SipMediaApplication(required) - Must us-east-1 or us-west-2 and in the same region as the SipMediaApplication Lambda handler. Default: - same region as stack deployment
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint": endpoint,
        }
        if name is not None:
            self._values["name"] = name
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''endpoint for SipMediaApplication(required).

        :default: - none
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''name for SipMediaApplication (optional).

        :default: - unique ID for resource
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''region for SipMediaApplication(required) - Must us-east-1 or us-west-2 and in the same region as the SipMediaApplication Lambda handler.

        :default: - same region as stack deployment
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SipMediaAppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.SipRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "target_applications": "targetApplications",
        "trigger_type": "triggerType",
        "trigger_value": "triggerValue",
        "name": "name",
    },
)
class SipRuleProps:
    def __init__(
        self,
        *,
        target_applications: typing.Sequence["TargetApplications"],
        trigger_type: "TriggerType",
        trigger_value: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Props for ``SipRule``.

        :param target_applications: 
        :param trigger_type: Trigger Type for SipRule (required) - TO_PHONE_NUMBER or REQUEST_URI_HOSTNAME. Default: - none
        :param trigger_value: Trigger Value for SipRule (required) - EE.164 Phone Number or Voice Connector URI. Default: - none
        :param name: name for SipRule (optional). Default: - unique ID for resource
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "target_applications": target_applications,
            "trigger_type": trigger_type,
            "trigger_value": trigger_value,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def target_applications(self) -> typing.List["TargetApplications"]:
        result = self._values.get("target_applications")
        assert result is not None, "Required property 'target_applications' is missing"
        return typing.cast(typing.List["TargetApplications"], result)

    @builtins.property
    def trigger_type(self) -> "TriggerType":
        '''Trigger Type for SipRule (required) - TO_PHONE_NUMBER or REQUEST_URI_HOSTNAME.

        :default: - none
        '''
        result = self._values.get("trigger_type")
        assert result is not None, "Required property 'trigger_type' is missing"
        return typing.cast("TriggerType", result)

    @builtins.property
    def trigger_value(self) -> builtins.str:
        '''Trigger Value for SipRule (required) - EE.164 Phone Number or Voice Connector URI.

        :default: - none
        '''
        result = self._values.get("trigger_value")
        assert result is not None, "Required property 'trigger_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''name for SipRule (optional).

        :default: - unique ID for resource
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SipRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.Streaming",
    jsii_struct_bases=[],
    name_mapping={
        "data_retention": "dataRetention",
        "enabled": "enabled",
        "notification_targets": "notificationTargets",
    },
)
class Streaming:
    def __init__(
        self,
        *,
        data_retention: jsii.Number,
        enabled: builtins.bool,
        notification_targets: typing.Sequence[NotificationTargetType],
    ) -> None:
        '''
        :param data_retention: Streaming data retention for VoiceConnector. Default: - 0
        :param enabled: 
        :param notification_targets: Streaming data retention for VoiceConnector. Default: - 0
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "data_retention": data_retention,
            "enabled": enabled,
            "notification_targets": notification_targets,
        }

    @builtins.property
    def data_retention(self) -> jsii.Number:
        '''Streaming data retention for VoiceConnector.

        :default: - 0
        '''
        result = self._values.get("data_retention")
        assert result is not None, "Required property 'data_retention' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def enabled(self) -> builtins.bool:
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def notification_targets(self) -> typing.List[NotificationTargetType]:
        '''Streaming data retention for VoiceConnector.

        :default: - 0
        '''
        result = self._values.get("notification_targets")
        assert result is not None, "Required property 'notification_targets' is missing"
        return typing.cast(typing.List[NotificationTargetType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Streaming(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.TargetApplications",
    jsii_struct_bases=[],
    name_mapping={
        "priority": "priority",
        "sip_media_application_id": "sipMediaApplicationId",
        "region": "region",
    },
)
class TargetApplications:
    def __init__(
        self,
        *,
        priority: jsii.Number,
        sip_media_application_id: builtins.str,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param priority: Priority for SipRule (required) - 1 to 25. Default: - none
        :param sip_media_application_id: SipMediaApplicationId for SipRule (required). Default: - none
        :param region: Region for SipRule (optional). Default: - same region as stack deployment
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "priority": priority,
            "sip_media_application_id": sip_media_application_id,
        }
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Priority for SipRule (required) - 1 to 25.

        :default: - none
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def sip_media_application_id(self) -> builtins.str:
        '''SipMediaApplicationId for SipRule (required).

        :default: - none
        '''
        result = self._values.get("sip_media_application_id")
        assert result is not None, "Required property 'sip_media_application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region for SipRule (optional).

        :default: - same region as stack deployment
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetApplications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.Termination",
    jsii_struct_bases=[],
    name_mapping={
        "calling_regions": "callingRegions",
        "termination_cidrs": "terminationCidrs",
    },
)
class Termination:
    def __init__(
        self,
        *,
        calling_regions: typing.Sequence[builtins.str],
        termination_cidrs: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param calling_regions: Calling Regions for VoiceConnector (optional). Default: - ['US']
        :param termination_cidrs: termination IP for VoiceConnector (optional). Default: - none
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "calling_regions": calling_regions,
            "termination_cidrs": termination_cidrs,
        }

    @builtins.property
    def calling_regions(self) -> typing.List[builtins.str]:
        '''Calling Regions for VoiceConnector (optional).

        :default: - ['US']
        '''
        result = self._values.get("calling_regions")
        assert result is not None, "Required property 'calling_regions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def termination_cidrs(self) -> typing.List[builtins.str]:
        '''termination IP for VoiceConnector (optional).

        :default: - none
        '''
        result = self._values.get("termination_cidrs")
        assert result is not None, "Required property 'termination_cidrs' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Termination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-amazon-chime-resources.TriggerType")
class TriggerType(enum.Enum):
    TO_PHONE_NUMBER = "TO_PHONE_NUMBER"
    REQUEST_URI_HOSTNAME = "REQUEST_URI_HOSTNAME"


@jsii.data_type(
    jsii_type="cdk-amazon-chime-resources.VoiceConnectorProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption": "encryption",
        "name": "name",
        "origination": "origination",
        "region": "region",
        "streaming": "streaming",
        "termination": "termination",
    },
)
class VoiceConnectorProps:
    def __init__(
        self,
        *,
        encryption: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        origination: typing.Optional[typing.Sequence[Routes]] = None,
        region: typing.Optional[builtins.str] = None,
        streaming: typing.Optional[Streaming] = None,
        termination: typing.Optional[Termination] = None,
    ) -> None:
        '''Props for ``SipMediaApplication``.

        :param encryption: Encryption boolean for VoiceConnector. Default: - False
        :param name: name for VoiceConnector. Default: - unique ID for resource
        :param origination: 
        :param region: region for SipMediaApplication(required) - Must us-east-1 or us-west-2 and in the same region as the SipMediaApplication Lambda handler. Default: - same region as stack deployment
        :param streaming: 
        :param termination: 
        '''
        if isinstance(streaming, dict):
            streaming = Streaming(**streaming)
        if isinstance(termination, dict):
            termination = Termination(**termination)
        self._values: typing.Dict[str, typing.Any] = {}
        if encryption is not None:
            self._values["encryption"] = encryption
        if name is not None:
            self._values["name"] = name
        if origination is not None:
            self._values["origination"] = origination
        if region is not None:
            self._values["region"] = region
        if streaming is not None:
            self._values["streaming"] = streaming
        if termination is not None:
            self._values["termination"] = termination

    @builtins.property
    def encryption(self) -> typing.Optional[builtins.bool]:
        '''Encryption boolean for VoiceConnector.

        :default: - False
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''name for VoiceConnector.

        :default: - unique ID for resource
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origination(self) -> typing.Optional[typing.List[Routes]]:
        result = self._values.get("origination")
        return typing.cast(typing.Optional[typing.List[Routes]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''region for SipMediaApplication(required) - Must us-east-1 or us-west-2 and in the same region as the SipMediaApplication Lambda handler.

        :default: - same region as stack deployment
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def streaming(self) -> typing.Optional[Streaming]:
        result = self._values.get("streaming")
        return typing.cast(typing.Optional[Streaming], result)

    @builtins.property
    def termination(self) -> typing.Optional[Termination]:
        result = self._values.get("termination")
        return typing.cast(typing.Optional[Termination], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VoiceConnectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ChimePhoneNumber",
    "ChimeResourceProps",
    "ChimeResources",
    "ChimeSipMediaApp",
    "ChimeSipRule",
    "ChimeVoiceConnector",
    "NotificationTargetType",
    "PhoneAssociation",
    "PhoneAssociationProps",
    "PhoneCountry",
    "PhoneNumberProps",
    "PhoneNumberType",
    "PhoneProductType",
    "Protocol",
    "Routes",
    "SipMediaAppProps",
    "SipRuleProps",
    "Streaming",
    "TargetApplications",
    "Termination",
    "TriggerType",
    "VoiceConnectorProps",
]

publication.publish()
