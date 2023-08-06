'''
# AWS::KafkaConnect Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_kafkaconnect as kafkaconnect
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for KafkaConnect construct libraries](https://constructs.dev/search?q=kafkaconnect)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::KafkaConnect resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_KafkaConnect.html) directly.

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnConnector(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector",
):
    '''A CloudFormation ``AWS::KafkaConnect::Connector``.

    :cloudformationResource: AWS::KafkaConnect::Connector
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_kafkaconnect as kafkaconnect
        
        cfn_connector = kafkaconnect.CfnConnector(self, "MyCfnConnector",
            capacity=kafkaconnect.CfnConnector.CapacityProperty(
                auto_scaling=kafkaconnect.CfnConnector.AutoScalingProperty(
                    max_worker_count=123,
                    mcu_count=123,
                    min_worker_count=123,
                    scale_in_policy=kafkaconnect.CfnConnector.ScaleInPolicyProperty(
                        cpu_utilization_percentage=123
                    ),
                    scale_out_policy=kafkaconnect.CfnConnector.ScaleOutPolicyProperty(
                        cpu_utilization_percentage=123
                    )
                ),
                provisioned_capacity=kafkaconnect.CfnConnector.ProvisionedCapacityProperty(
                    worker_count=123,
        
                    # the properties below are optional
                    mcu_count=123
                )
            ),
            connector_configuration={
                "connector_configuration_key": "connectorConfiguration"
            },
            connector_name="connectorName",
            kafka_cluster=kafkaconnect.CfnConnector.KafkaClusterProperty(
                apache_kafka_cluster=kafkaconnect.CfnConnector.ApacheKafkaClusterProperty(
                    bootstrap_servers="bootstrapServers",
                    vpc=kafkaconnect.CfnConnector.VpcProperty(
                        security_groups=["securityGroups"],
                        subnets=["subnets"]
                    )
                )
            ),
            kafka_cluster_client_authentication=kafkaconnect.CfnConnector.KafkaClusterClientAuthenticationProperty(
                authentication_type="authenticationType"
            ),
            kafka_cluster_encryption_in_transit=kafkaconnect.CfnConnector.KafkaClusterEncryptionInTransitProperty(
                encryption_type="encryptionType"
            ),
            kafka_connect_version="kafkaConnectVersion",
            plugins=[kafkaconnect.CfnConnector.PluginProperty(
                custom_plugin=kafkaconnect.CfnConnector.CustomPluginProperty(
                    custom_plugin_arn="customPluginArn",
                    revision=123
                )
            )],
            service_execution_role_arn="serviceExecutionRoleArn",
        
            # the properties below are optional
            connector_description="connectorDescription",
            log_delivery=kafkaconnect.CfnConnector.LogDeliveryProperty(
                worker_log_delivery=kafkaconnect.CfnConnector.WorkerLogDeliveryProperty(
                    cloud_watch_logs=kafkaconnect.CfnConnector.CloudWatchLogsLogDeliveryProperty(
                        enabled=False,
        
                        # the properties below are optional
                        log_group="logGroup"
                    ),
                    firehose=kafkaconnect.CfnConnector.FirehoseLogDeliveryProperty(
                        enabled=False,
        
                        # the properties below are optional
                        delivery_stream="deliveryStream"
                    ),
                    s3=kafkaconnect.CfnConnector.S3LogDeliveryProperty(
                        enabled=False,
        
                        # the properties below are optional
                        bucket="bucket",
                        prefix="prefix"
                    )
                )
            ),
            worker_configuration=kafkaconnect.CfnConnector.WorkerConfigurationProperty(
                revision=123,
                worker_configuration_arn="workerConfigurationArn"
            )
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        capacity: typing.Union["CfnConnector.CapacityProperty", aws_cdk.core.IResolvable],
        connector_configuration: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]],
        connector_name: builtins.str,
        kafka_cluster: typing.Union[aws_cdk.core.IResolvable, "CfnConnector.KafkaClusterProperty"],
        kafka_cluster_client_authentication: typing.Union[aws_cdk.core.IResolvable, "CfnConnector.KafkaClusterClientAuthenticationProperty"],
        kafka_cluster_encryption_in_transit: typing.Union[aws_cdk.core.IResolvable, "CfnConnector.KafkaClusterEncryptionInTransitProperty"],
        kafka_connect_version: builtins.str,
        plugins: typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.PluginProperty"]]],
        service_execution_role_arn: builtins.str,
        connector_description: typing.Optional[builtins.str] = None,
        log_delivery: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.LogDeliveryProperty"]] = None,
        worker_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.WorkerConfigurationProperty"]] = None,
    ) -> None:
        '''Create a new ``AWS::KafkaConnect::Connector``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param capacity: ``AWS::KafkaConnect::Connector.Capacity``.
        :param connector_configuration: ``AWS::KafkaConnect::Connector.ConnectorConfiguration``.
        :param connector_name: ``AWS::KafkaConnect::Connector.ConnectorName``.
        :param kafka_cluster: ``AWS::KafkaConnect::Connector.KafkaCluster``.
        :param kafka_cluster_client_authentication: ``AWS::KafkaConnect::Connector.KafkaClusterClientAuthentication``.
        :param kafka_cluster_encryption_in_transit: ``AWS::KafkaConnect::Connector.KafkaClusterEncryptionInTransit``.
        :param kafka_connect_version: ``AWS::KafkaConnect::Connector.KafkaConnectVersion``.
        :param plugins: ``AWS::KafkaConnect::Connector.Plugins``.
        :param service_execution_role_arn: ``AWS::KafkaConnect::Connector.ServiceExecutionRoleArn``.
        :param connector_description: ``AWS::KafkaConnect::Connector.ConnectorDescription``.
        :param log_delivery: ``AWS::KafkaConnect::Connector.LogDelivery``.
        :param worker_configuration: ``AWS::KafkaConnect::Connector.WorkerConfiguration``.
        '''
        props = CfnConnectorProps(
            capacity=capacity,
            connector_configuration=connector_configuration,
            connector_name=connector_name,
            kafka_cluster=kafka_cluster,
            kafka_cluster_client_authentication=kafka_cluster_client_authentication,
            kafka_cluster_encryption_in_transit=kafka_cluster_encryption_in_transit,
            kafka_connect_version=kafka_connect_version,
            plugins=plugins,
            service_execution_role_arn=service_execution_role_arn,
            connector_description=connector_description,
            log_delivery=log_delivery,
            worker_configuration=worker_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrConnectorArn")
    def attr_connector_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: ConnectorArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConnectorArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="capacity")
    def capacity(
        self,
    ) -> typing.Union["CfnConnector.CapacityProperty", aws_cdk.core.IResolvable]:
        '''``AWS::KafkaConnect::Connector.Capacity``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-capacity
        '''
        return typing.cast(typing.Union["CfnConnector.CapacityProperty", aws_cdk.core.IResolvable], jsii.get(self, "capacity"))

    @capacity.setter
    def capacity(
        self,
        value: typing.Union["CfnConnector.CapacityProperty", aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "capacity", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connectorConfiguration")
    def connector_configuration(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::KafkaConnect::Connector.ConnectorConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectorconfiguration
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "connectorConfiguration"))

    @connector_configuration.setter
    def connector_configuration(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        jsii.set(self, "connectorConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connectorName")
    def connector_name(self) -> builtins.str:
        '''``AWS::KafkaConnect::Connector.ConnectorName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectorname
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectorName"))

    @connector_name.setter
    def connector_name(self, value: builtins.str) -> None:
        jsii.set(self, "connectorName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kafkaCluster")
    def kafka_cluster(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnConnector.KafkaClusterProperty"]:
        '''``AWS::KafkaConnect::Connector.KafkaCluster``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkacluster
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnConnector.KafkaClusterProperty"], jsii.get(self, "kafkaCluster"))

    @kafka_cluster.setter
    def kafka_cluster(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnConnector.KafkaClusterProperty"],
    ) -> None:
        jsii.set(self, "kafkaCluster", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kafkaClusterClientAuthentication")
    def kafka_cluster_client_authentication(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnConnector.KafkaClusterClientAuthenticationProperty"]:
        '''``AWS::KafkaConnect::Connector.KafkaClusterClientAuthentication``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaclusterclientauthentication
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnConnector.KafkaClusterClientAuthenticationProperty"], jsii.get(self, "kafkaClusterClientAuthentication"))

    @kafka_cluster_client_authentication.setter
    def kafka_cluster_client_authentication(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnConnector.KafkaClusterClientAuthenticationProperty"],
    ) -> None:
        jsii.set(self, "kafkaClusterClientAuthentication", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kafkaClusterEncryptionInTransit")
    def kafka_cluster_encryption_in_transit(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnConnector.KafkaClusterEncryptionInTransitProperty"]:
        '''``AWS::KafkaConnect::Connector.KafkaClusterEncryptionInTransit``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaclusterencryptionintransit
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnConnector.KafkaClusterEncryptionInTransitProperty"], jsii.get(self, "kafkaClusterEncryptionInTransit"))

    @kafka_cluster_encryption_in_transit.setter
    def kafka_cluster_encryption_in_transit(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnConnector.KafkaClusterEncryptionInTransitProperty"],
    ) -> None:
        jsii.set(self, "kafkaClusterEncryptionInTransit", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kafkaConnectVersion")
    def kafka_connect_version(self) -> builtins.str:
        '''``AWS::KafkaConnect::Connector.KafkaConnectVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaconnectversion
        '''
        return typing.cast(builtins.str, jsii.get(self, "kafkaConnectVersion"))

    @kafka_connect_version.setter
    def kafka_connect_version(self, value: builtins.str) -> None:
        jsii.set(self, "kafkaConnectVersion", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="plugins")
    def plugins(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.PluginProperty"]]]:
        '''``AWS::KafkaConnect::Connector.Plugins``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-plugins
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.PluginProperty"]]], jsii.get(self, "plugins"))

    @plugins.setter
    def plugins(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.PluginProperty"]]],
    ) -> None:
        jsii.set(self, "plugins", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serviceExecutionRoleArn")
    def service_execution_role_arn(self) -> builtins.str:
        '''``AWS::KafkaConnect::Connector.ServiceExecutionRoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-serviceexecutionrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceExecutionRoleArn"))

    @service_execution_role_arn.setter
    def service_execution_role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "serviceExecutionRoleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connectorDescription")
    def connector_description(self) -> typing.Optional[builtins.str]:
        '''``AWS::KafkaConnect::Connector.ConnectorDescription``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectordescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorDescription"))

    @connector_description.setter
    def connector_description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "connectorDescription", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logDelivery")
    def log_delivery(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.LogDeliveryProperty"]]:
        '''``AWS::KafkaConnect::Connector.LogDelivery``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-logdelivery
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.LogDeliveryProperty"]], jsii.get(self, "logDelivery"))

    @log_delivery.setter
    def log_delivery(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.LogDeliveryProperty"]],
    ) -> None:
        jsii.set(self, "logDelivery", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workerConfiguration")
    def worker_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.WorkerConfigurationProperty"]]:
        '''``AWS::KafkaConnect::Connector.WorkerConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-workerconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.WorkerConfigurationProperty"]], jsii.get(self, "workerConfiguration"))

    @worker_configuration.setter
    def worker_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.WorkerConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "workerConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.ApacheKafkaClusterProperty",
        jsii_struct_bases=[],
        name_mapping={"bootstrap_servers": "bootstrapServers", "vpc": "vpc"},
    )
    class ApacheKafkaClusterProperty:
        def __init__(
            self,
            *,
            bootstrap_servers: builtins.str,
            vpc: typing.Union[aws_cdk.core.IResolvable, "CfnConnector.VpcProperty"],
        ) -> None:
            '''
            :param bootstrap_servers: ``CfnConnector.ApacheKafkaClusterProperty.BootstrapServers``.
            :param vpc: ``CfnConnector.ApacheKafkaClusterProperty.Vpc``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-apachekafkacluster.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                apache_kafka_cluster_property = kafkaconnect.CfnConnector.ApacheKafkaClusterProperty(
                    bootstrap_servers="bootstrapServers",
                    vpc=kafkaconnect.CfnConnector.VpcProperty(
                        security_groups=["securityGroups"],
                        subnets=["subnets"]
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bootstrap_servers": bootstrap_servers,
                "vpc": vpc,
            }

        @builtins.property
        def bootstrap_servers(self) -> builtins.str:
            '''``CfnConnector.ApacheKafkaClusterProperty.BootstrapServers``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-apachekafkacluster.html#cfn-kafkaconnect-connector-apachekafkacluster-bootstrapservers
            '''
            result = self._values.get("bootstrap_servers")
            assert result is not None, "Required property 'bootstrap_servers' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def vpc(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnConnector.VpcProperty"]:
            '''``CfnConnector.ApacheKafkaClusterProperty.Vpc``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-apachekafkacluster.html#cfn-kafkaconnect-connector-apachekafkacluster-vpc
            '''
            result = self._values.get("vpc")
            assert result is not None, "Required property 'vpc' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnConnector.VpcProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApacheKafkaClusterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.AutoScalingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_worker_count": "maxWorkerCount",
            "mcu_count": "mcuCount",
            "min_worker_count": "minWorkerCount",
            "scale_in_policy": "scaleInPolicy",
            "scale_out_policy": "scaleOutPolicy",
        },
    )
    class AutoScalingProperty:
        def __init__(
            self,
            *,
            max_worker_count: jsii.Number,
            mcu_count: jsii.Number,
            min_worker_count: jsii.Number,
            scale_in_policy: typing.Union[aws_cdk.core.IResolvable, "CfnConnector.ScaleInPolicyProperty"],
            scale_out_policy: typing.Union[aws_cdk.core.IResolvable, "CfnConnector.ScaleOutPolicyProperty"],
        ) -> None:
            '''
            :param max_worker_count: ``CfnConnector.AutoScalingProperty.MaxWorkerCount``.
            :param mcu_count: ``CfnConnector.AutoScalingProperty.McuCount``.
            :param min_worker_count: ``CfnConnector.AutoScalingProperty.MinWorkerCount``.
            :param scale_in_policy: ``CfnConnector.AutoScalingProperty.ScaleInPolicy``.
            :param scale_out_policy: ``CfnConnector.AutoScalingProperty.ScaleOutPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                auto_scaling_property = kafkaconnect.CfnConnector.AutoScalingProperty(
                    max_worker_count=123,
                    mcu_count=123,
                    min_worker_count=123,
                    scale_in_policy=kafkaconnect.CfnConnector.ScaleInPolicyProperty(
                        cpu_utilization_percentage=123
                    ),
                    scale_out_policy=kafkaconnect.CfnConnector.ScaleOutPolicyProperty(
                        cpu_utilization_percentage=123
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "max_worker_count": max_worker_count,
                "mcu_count": mcu_count,
                "min_worker_count": min_worker_count,
                "scale_in_policy": scale_in_policy,
                "scale_out_policy": scale_out_policy,
            }

        @builtins.property
        def max_worker_count(self) -> jsii.Number:
            '''``CfnConnector.AutoScalingProperty.MaxWorkerCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-maxworkercount
            '''
            result = self._values.get("max_worker_count")
            assert result is not None, "Required property 'max_worker_count' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def mcu_count(self) -> jsii.Number:
            '''``CfnConnector.AutoScalingProperty.McuCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-mcucount
            '''
            result = self._values.get("mcu_count")
            assert result is not None, "Required property 'mcu_count' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def min_worker_count(self) -> jsii.Number:
            '''``CfnConnector.AutoScalingProperty.MinWorkerCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-minworkercount
            '''
            result = self._values.get("min_worker_count")
            assert result is not None, "Required property 'min_worker_count' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def scale_in_policy(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnConnector.ScaleInPolicyProperty"]:
            '''``CfnConnector.AutoScalingProperty.ScaleInPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-scaleinpolicy
            '''
            result = self._values.get("scale_in_policy")
            assert result is not None, "Required property 'scale_in_policy' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnConnector.ScaleInPolicyProperty"], result)

        @builtins.property
        def scale_out_policy(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnConnector.ScaleOutPolicyProperty"]:
            '''``CfnConnector.AutoScalingProperty.ScaleOutPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-scaleoutpolicy
            '''
            result = self._values.get("scale_out_policy")
            assert result is not None, "Required property 'scale_out_policy' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnConnector.ScaleOutPolicyProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoScalingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.CapacityProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_scaling": "autoScaling",
            "provisioned_capacity": "provisionedCapacity",
        },
    )
    class CapacityProperty:
        def __init__(
            self,
            *,
            auto_scaling: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.AutoScalingProperty"]] = None,
            provisioned_capacity: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.ProvisionedCapacityProperty"]] = None,
        ) -> None:
            '''
            :param auto_scaling: ``CfnConnector.CapacityProperty.AutoScaling``.
            :param provisioned_capacity: ``CfnConnector.CapacityProperty.ProvisionedCapacity``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-capacity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                capacity_property = kafkaconnect.CfnConnector.CapacityProperty(
                    auto_scaling=kafkaconnect.CfnConnector.AutoScalingProperty(
                        max_worker_count=123,
                        mcu_count=123,
                        min_worker_count=123,
                        scale_in_policy=kafkaconnect.CfnConnector.ScaleInPolicyProperty(
                            cpu_utilization_percentage=123
                        ),
                        scale_out_policy=kafkaconnect.CfnConnector.ScaleOutPolicyProperty(
                            cpu_utilization_percentage=123
                        )
                    ),
                    provisioned_capacity=kafkaconnect.CfnConnector.ProvisionedCapacityProperty(
                        worker_count=123,
                
                        # the properties below are optional
                        mcu_count=123
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if auto_scaling is not None:
                self._values["auto_scaling"] = auto_scaling
            if provisioned_capacity is not None:
                self._values["provisioned_capacity"] = provisioned_capacity

        @builtins.property
        def auto_scaling(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.AutoScalingProperty"]]:
            '''``CfnConnector.CapacityProperty.AutoScaling``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-capacity.html#cfn-kafkaconnect-connector-capacity-autoscaling
            '''
            result = self._values.get("auto_scaling")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.AutoScalingProperty"]], result)

        @builtins.property
        def provisioned_capacity(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.ProvisionedCapacityProperty"]]:
            '''``CfnConnector.CapacityProperty.ProvisionedCapacity``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-capacity.html#cfn-kafkaconnect-connector-capacity-provisionedcapacity
            '''
            result = self._values.get("provisioned_capacity")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.ProvisionedCapacityProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.CloudWatchLogsLogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "log_group": "logGroup"},
    )
    class CloudWatchLogsLogDeliveryProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            log_group: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param enabled: ``CfnConnector.CloudWatchLogsLogDeliveryProperty.Enabled``.
            :param log_group: ``CfnConnector.CloudWatchLogsLogDeliveryProperty.LogGroup``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-cloudwatchlogslogdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                cloud_watch_logs_log_delivery_property = kafkaconnect.CfnConnector.CloudWatchLogsLogDeliveryProperty(
                    enabled=False,
                
                    # the properties below are optional
                    log_group="logGroup"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "enabled": enabled,
            }
            if log_group is not None:
                self._values["log_group"] = log_group

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            '''``CfnConnector.CloudWatchLogsLogDeliveryProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-cloudwatchlogslogdelivery.html#cfn-kafkaconnect-connector-cloudwatchlogslogdelivery-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, aws_cdk.core.IResolvable], result)

        @builtins.property
        def log_group(self) -> typing.Optional[builtins.str]:
            '''``CfnConnector.CloudWatchLogsLogDeliveryProperty.LogGroup``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-cloudwatchlogslogdelivery.html#cfn-kafkaconnect-connector-cloudwatchlogslogdelivery-loggroup
            '''
            result = self._values.get("log_group")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsLogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.CustomPluginProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_plugin_arn": "customPluginArn", "revision": "revision"},
    )
    class CustomPluginProperty:
        def __init__(
            self,
            *,
            custom_plugin_arn: builtins.str,
            revision: jsii.Number,
        ) -> None:
            '''
            :param custom_plugin_arn: ``CfnConnector.CustomPluginProperty.CustomPluginArn``.
            :param revision: ``CfnConnector.CustomPluginProperty.Revision``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-customplugin.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                custom_plugin_property = kafkaconnect.CfnConnector.CustomPluginProperty(
                    custom_plugin_arn="customPluginArn",
                    revision=123
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "custom_plugin_arn": custom_plugin_arn,
                "revision": revision,
            }

        @builtins.property
        def custom_plugin_arn(self) -> builtins.str:
            '''``CfnConnector.CustomPluginProperty.CustomPluginArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-customplugin.html#cfn-kafkaconnect-connector-customplugin-custompluginarn
            '''
            result = self._values.get("custom_plugin_arn")
            assert result is not None, "Required property 'custom_plugin_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def revision(self) -> jsii.Number:
            '''``CfnConnector.CustomPluginProperty.Revision``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-customplugin.html#cfn-kafkaconnect-connector-customplugin-revision
            '''
            result = self._values.get("revision")
            assert result is not None, "Required property 'revision' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomPluginProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.FirehoseLogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "delivery_stream": "deliveryStream"},
    )
    class FirehoseLogDeliveryProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            delivery_stream: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param enabled: ``CfnConnector.FirehoseLogDeliveryProperty.Enabled``.
            :param delivery_stream: ``CfnConnector.FirehoseLogDeliveryProperty.DeliveryStream``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-firehoselogdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                firehose_log_delivery_property = kafkaconnect.CfnConnector.FirehoseLogDeliveryProperty(
                    enabled=False,
                
                    # the properties below are optional
                    delivery_stream="deliveryStream"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "enabled": enabled,
            }
            if delivery_stream is not None:
                self._values["delivery_stream"] = delivery_stream

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            '''``CfnConnector.FirehoseLogDeliveryProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-firehoselogdelivery.html#cfn-kafkaconnect-connector-firehoselogdelivery-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, aws_cdk.core.IResolvable], result)

        @builtins.property
        def delivery_stream(self) -> typing.Optional[builtins.str]:
            '''``CfnConnector.FirehoseLogDeliveryProperty.DeliveryStream``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-firehoselogdelivery.html#cfn-kafkaconnect-connector-firehoselogdelivery-deliverystream
            '''
            result = self._values.get("delivery_stream")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirehoseLogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.KafkaClusterClientAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={"authentication_type": "authenticationType"},
    )
    class KafkaClusterClientAuthenticationProperty:
        def __init__(self, *, authentication_type: builtins.str) -> None:
            '''
            :param authentication_type: ``CfnConnector.KafkaClusterClientAuthenticationProperty.AuthenticationType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkaclusterclientauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                kafka_cluster_client_authentication_property = kafkaconnect.CfnConnector.KafkaClusterClientAuthenticationProperty(
                    authentication_type="authenticationType"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "authentication_type": authentication_type,
            }

        @builtins.property
        def authentication_type(self) -> builtins.str:
            '''``CfnConnector.KafkaClusterClientAuthenticationProperty.AuthenticationType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkaclusterclientauthentication.html#cfn-kafkaconnect-connector-kafkaclusterclientauthentication-authenticationtype
            '''
            result = self._values.get("authentication_type")
            assert result is not None, "Required property 'authentication_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KafkaClusterClientAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.KafkaClusterEncryptionInTransitProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_type": "encryptionType"},
    )
    class KafkaClusterEncryptionInTransitProperty:
        def __init__(self, *, encryption_type: builtins.str) -> None:
            '''
            :param encryption_type: ``CfnConnector.KafkaClusterEncryptionInTransitProperty.EncryptionType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkaclusterencryptionintransit.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                kafka_cluster_encryption_in_transit_property = kafkaconnect.CfnConnector.KafkaClusterEncryptionInTransitProperty(
                    encryption_type="encryptionType"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "encryption_type": encryption_type,
            }

        @builtins.property
        def encryption_type(self) -> builtins.str:
            '''``CfnConnector.KafkaClusterEncryptionInTransitProperty.EncryptionType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkaclusterencryptionintransit.html#cfn-kafkaconnect-connector-kafkaclusterencryptionintransit-encryptiontype
            '''
            result = self._values.get("encryption_type")
            assert result is not None, "Required property 'encryption_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KafkaClusterEncryptionInTransitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.KafkaClusterProperty",
        jsii_struct_bases=[],
        name_mapping={"apache_kafka_cluster": "apacheKafkaCluster"},
    )
    class KafkaClusterProperty:
        def __init__(
            self,
            *,
            apache_kafka_cluster: typing.Union[aws_cdk.core.IResolvable, "CfnConnector.ApacheKafkaClusterProperty"],
        ) -> None:
            '''
            :param apache_kafka_cluster: ``CfnConnector.KafkaClusterProperty.ApacheKafkaCluster``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkacluster.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                kafka_cluster_property = kafkaconnect.CfnConnector.KafkaClusterProperty(
                    apache_kafka_cluster=kafkaconnect.CfnConnector.ApacheKafkaClusterProperty(
                        bootstrap_servers="bootstrapServers",
                        vpc=kafkaconnect.CfnConnector.VpcProperty(
                            security_groups=["securityGroups"],
                            subnets=["subnets"]
                        )
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "apache_kafka_cluster": apache_kafka_cluster,
            }

        @builtins.property
        def apache_kafka_cluster(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnConnector.ApacheKafkaClusterProperty"]:
            '''``CfnConnector.KafkaClusterProperty.ApacheKafkaCluster``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkacluster.html#cfn-kafkaconnect-connector-kafkacluster-apachekafkacluster
            '''
            result = self._values.get("apache_kafka_cluster")
            assert result is not None, "Required property 'apache_kafka_cluster' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnConnector.ApacheKafkaClusterProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KafkaClusterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.LogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={"worker_log_delivery": "workerLogDelivery"},
    )
    class LogDeliveryProperty:
        def __init__(
            self,
            *,
            worker_log_delivery: typing.Union[aws_cdk.core.IResolvable, "CfnConnector.WorkerLogDeliveryProperty"],
        ) -> None:
            '''
            :param worker_log_delivery: ``CfnConnector.LogDeliveryProperty.WorkerLogDelivery``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-logdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                log_delivery_property = kafkaconnect.CfnConnector.LogDeliveryProperty(
                    worker_log_delivery=kafkaconnect.CfnConnector.WorkerLogDeliveryProperty(
                        cloud_watch_logs=kafkaconnect.CfnConnector.CloudWatchLogsLogDeliveryProperty(
                            enabled=False,
                
                            # the properties below are optional
                            log_group="logGroup"
                        ),
                        firehose=kafkaconnect.CfnConnector.FirehoseLogDeliveryProperty(
                            enabled=False,
                
                            # the properties below are optional
                            delivery_stream="deliveryStream"
                        ),
                        s3=kafkaconnect.CfnConnector.S3LogDeliveryProperty(
                            enabled=False,
                
                            # the properties below are optional
                            bucket="bucket",
                            prefix="prefix"
                        )
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "worker_log_delivery": worker_log_delivery,
            }

        @builtins.property
        def worker_log_delivery(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnConnector.WorkerLogDeliveryProperty"]:
            '''``CfnConnector.LogDeliveryProperty.WorkerLogDelivery``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-logdelivery.html#cfn-kafkaconnect-connector-logdelivery-workerlogdelivery
            '''
            result = self._values.get("worker_log_delivery")
            assert result is not None, "Required property 'worker_log_delivery' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnConnector.WorkerLogDeliveryProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.PluginProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_plugin": "customPlugin"},
    )
    class PluginProperty:
        def __init__(
            self,
            *,
            custom_plugin: typing.Union[aws_cdk.core.IResolvable, "CfnConnector.CustomPluginProperty"],
        ) -> None:
            '''
            :param custom_plugin: ``CfnConnector.PluginProperty.CustomPlugin``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-plugin.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                plugin_property = kafkaconnect.CfnConnector.PluginProperty(
                    custom_plugin=kafkaconnect.CfnConnector.CustomPluginProperty(
                        custom_plugin_arn="customPluginArn",
                        revision=123
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "custom_plugin": custom_plugin,
            }

        @builtins.property
        def custom_plugin(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnConnector.CustomPluginProperty"]:
            '''``CfnConnector.PluginProperty.CustomPlugin``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-plugin.html#cfn-kafkaconnect-connector-plugin-customplugin
            '''
            result = self._values.get("custom_plugin")
            assert result is not None, "Required property 'custom_plugin' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnConnector.CustomPluginProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PluginProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.ProvisionedCapacityProperty",
        jsii_struct_bases=[],
        name_mapping={"worker_count": "workerCount", "mcu_count": "mcuCount"},
    )
    class ProvisionedCapacityProperty:
        def __init__(
            self,
            *,
            worker_count: jsii.Number,
            mcu_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param worker_count: ``CfnConnector.ProvisionedCapacityProperty.WorkerCount``.
            :param mcu_count: ``CfnConnector.ProvisionedCapacityProperty.McuCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-provisionedcapacity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                provisioned_capacity_property = kafkaconnect.CfnConnector.ProvisionedCapacityProperty(
                    worker_count=123,
                
                    # the properties below are optional
                    mcu_count=123
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "worker_count": worker_count,
            }
            if mcu_count is not None:
                self._values["mcu_count"] = mcu_count

        @builtins.property
        def worker_count(self) -> jsii.Number:
            '''``CfnConnector.ProvisionedCapacityProperty.WorkerCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-provisionedcapacity.html#cfn-kafkaconnect-connector-provisionedcapacity-workercount
            '''
            result = self._values.get("worker_count")
            assert result is not None, "Required property 'worker_count' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def mcu_count(self) -> typing.Optional[jsii.Number]:
            '''``CfnConnector.ProvisionedCapacityProperty.McuCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-provisionedcapacity.html#cfn-kafkaconnect-connector-provisionedcapacity-mcucount
            '''
            result = self._values.get("mcu_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedCapacityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.S3LogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "bucket": "bucket", "prefix": "prefix"},
    )
    class S3LogDeliveryProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            bucket: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param enabled: ``CfnConnector.S3LogDeliveryProperty.Enabled``.
            :param bucket: ``CfnConnector.S3LogDeliveryProperty.Bucket``.
            :param prefix: ``CfnConnector.S3LogDeliveryProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-s3logdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                s3_log_delivery_property = kafkaconnect.CfnConnector.S3LogDeliveryProperty(
                    enabled=False,
                
                    # the properties below are optional
                    bucket="bucket",
                    prefix="prefix"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "enabled": enabled,
            }
            if bucket is not None:
                self._values["bucket"] = bucket
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            '''``CfnConnector.S3LogDeliveryProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-s3logdelivery.html#cfn-kafkaconnect-connector-s3logdelivery-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, aws_cdk.core.IResolvable], result)

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''``CfnConnector.S3LogDeliveryProperty.Bucket``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-s3logdelivery.html#cfn-kafkaconnect-connector-s3logdelivery-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnConnector.S3LogDeliveryProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-s3logdelivery.html#cfn-kafkaconnect-connector-s3logdelivery-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.ScaleInPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"cpu_utilization_percentage": "cpuUtilizationPercentage"},
    )
    class ScaleInPolicyProperty:
        def __init__(self, *, cpu_utilization_percentage: jsii.Number) -> None:
            '''
            :param cpu_utilization_percentage: ``CfnConnector.ScaleInPolicyProperty.CpuUtilizationPercentage``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-scaleinpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                scale_in_policy_property = kafkaconnect.CfnConnector.ScaleInPolicyProperty(
                    cpu_utilization_percentage=123
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "cpu_utilization_percentage": cpu_utilization_percentage,
            }

        @builtins.property
        def cpu_utilization_percentage(self) -> jsii.Number:
            '''``CfnConnector.ScaleInPolicyProperty.CpuUtilizationPercentage``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-scaleinpolicy.html#cfn-kafkaconnect-connector-scaleinpolicy-cpuutilizationpercentage
            '''
            result = self._values.get("cpu_utilization_percentage")
            assert result is not None, "Required property 'cpu_utilization_percentage' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScaleInPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.ScaleOutPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"cpu_utilization_percentage": "cpuUtilizationPercentage"},
    )
    class ScaleOutPolicyProperty:
        def __init__(self, *, cpu_utilization_percentage: jsii.Number) -> None:
            '''
            :param cpu_utilization_percentage: ``CfnConnector.ScaleOutPolicyProperty.CpuUtilizationPercentage``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-scaleoutpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                scale_out_policy_property = kafkaconnect.CfnConnector.ScaleOutPolicyProperty(
                    cpu_utilization_percentage=123
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "cpu_utilization_percentage": cpu_utilization_percentage,
            }

        @builtins.property
        def cpu_utilization_percentage(self) -> jsii.Number:
            '''``CfnConnector.ScaleOutPolicyProperty.CpuUtilizationPercentage``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-scaleoutpolicy.html#cfn-kafkaconnect-connector-scaleoutpolicy-cpuutilizationpercentage
            '''
            result = self._values.get("cpu_utilization_percentage")
            assert result is not None, "Required property 'cpu_utilization_percentage' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScaleOutPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.VpcProperty",
        jsii_struct_bases=[],
        name_mapping={"security_groups": "securityGroups", "subnets": "subnets"},
    )
    class VpcProperty:
        def __init__(
            self,
            *,
            security_groups: typing.Sequence[builtins.str],
            subnets: typing.Sequence[builtins.str],
        ) -> None:
            '''
            :param security_groups: ``CfnConnector.VpcProperty.SecurityGroups``.
            :param subnets: ``CfnConnector.VpcProperty.Subnets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-vpc.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                vpc_property = kafkaconnect.CfnConnector.VpcProperty(
                    security_groups=["securityGroups"],
                    subnets=["subnets"]
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "security_groups": security_groups,
                "subnets": subnets,
            }

        @builtins.property
        def security_groups(self) -> typing.List[builtins.str]:
            '''``CfnConnector.VpcProperty.SecurityGroups``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-vpc.html#cfn-kafkaconnect-connector-vpc-securitygroups
            '''
            result = self._values.get("security_groups")
            assert result is not None, "Required property 'security_groups' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def subnets(self) -> typing.List[builtins.str]:
            '''``CfnConnector.VpcProperty.Subnets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-vpc.html#cfn-kafkaconnect-connector-vpc-subnets
            '''
            result = self._values.get("subnets")
            assert result is not None, "Required property 'subnets' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.WorkerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "revision": "revision",
            "worker_configuration_arn": "workerConfigurationArn",
        },
    )
    class WorkerConfigurationProperty:
        def __init__(
            self,
            *,
            revision: jsii.Number,
            worker_configuration_arn: builtins.str,
        ) -> None:
            '''
            :param revision: ``CfnConnector.WorkerConfigurationProperty.Revision``.
            :param worker_configuration_arn: ``CfnConnector.WorkerConfigurationProperty.WorkerConfigurationArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                worker_configuration_property = kafkaconnect.CfnConnector.WorkerConfigurationProperty(
                    revision=123,
                    worker_configuration_arn="workerConfigurationArn"
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "revision": revision,
                "worker_configuration_arn": worker_configuration_arn,
            }

        @builtins.property
        def revision(self) -> jsii.Number:
            '''``CfnConnector.WorkerConfigurationProperty.Revision``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerconfiguration.html#cfn-kafkaconnect-connector-workerconfiguration-revision
            '''
            result = self._values.get("revision")
            assert result is not None, "Required property 'revision' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def worker_configuration_arn(self) -> builtins.str:
            '''``CfnConnector.WorkerConfigurationProperty.WorkerConfigurationArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerconfiguration.html#cfn-kafkaconnect-connector-workerconfiguration-workerconfigurationarn
            '''
            result = self._values.get("worker_configuration_arn")
            assert result is not None, "Required property 'worker_configuration_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnector.WorkerLogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs": "cloudWatchLogs",
            "firehose": "firehose",
            "s3": "s3",
        },
    )
    class WorkerLogDeliveryProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.CloudWatchLogsLogDeliveryProperty"]] = None,
            firehose: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.FirehoseLogDeliveryProperty"]] = None,
            s3: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.S3LogDeliveryProperty"]] = None,
        ) -> None:
            '''
            :param cloud_watch_logs: ``CfnConnector.WorkerLogDeliveryProperty.CloudWatchLogs``.
            :param firehose: ``CfnConnector.WorkerLogDeliveryProperty.Firehose``.
            :param s3: ``CfnConnector.WorkerLogDeliveryProperty.S3``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerlogdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_kafkaconnect as kafkaconnect
                
                worker_log_delivery_property = kafkaconnect.CfnConnector.WorkerLogDeliveryProperty(
                    cloud_watch_logs=kafkaconnect.CfnConnector.CloudWatchLogsLogDeliveryProperty(
                        enabled=False,
                
                        # the properties below are optional
                        log_group="logGroup"
                    ),
                    firehose=kafkaconnect.CfnConnector.FirehoseLogDeliveryProperty(
                        enabled=False,
                
                        # the properties below are optional
                        delivery_stream="deliveryStream"
                    ),
                    s3=kafkaconnect.CfnConnector.S3LogDeliveryProperty(
                        enabled=False,
                
                        # the properties below are optional
                        bucket="bucket",
                        prefix="prefix"
                    )
                )
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if cloud_watch_logs is not None:
                self._values["cloud_watch_logs"] = cloud_watch_logs
            if firehose is not None:
                self._values["firehose"] = firehose
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def cloud_watch_logs(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.CloudWatchLogsLogDeliveryProperty"]]:
            '''``CfnConnector.WorkerLogDeliveryProperty.CloudWatchLogs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerlogdelivery.html#cfn-kafkaconnect-connector-workerlogdelivery-cloudwatchlogs
            '''
            result = self._values.get("cloud_watch_logs")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.CloudWatchLogsLogDeliveryProperty"]], result)

        @builtins.property
        def firehose(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.FirehoseLogDeliveryProperty"]]:
            '''``CfnConnector.WorkerLogDeliveryProperty.Firehose``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerlogdelivery.html#cfn-kafkaconnect-connector-workerlogdelivery-firehose
            '''
            result = self._values.get("firehose")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.FirehoseLogDeliveryProperty"]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.S3LogDeliveryProperty"]]:
            '''``CfnConnector.WorkerLogDeliveryProperty.S3``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerlogdelivery.html#cfn-kafkaconnect-connector-workerlogdelivery-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnConnector.S3LogDeliveryProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkerLogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kafkaconnect.CfnConnectorProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity": "capacity",
        "connector_configuration": "connectorConfiguration",
        "connector_name": "connectorName",
        "kafka_cluster": "kafkaCluster",
        "kafka_cluster_client_authentication": "kafkaClusterClientAuthentication",
        "kafka_cluster_encryption_in_transit": "kafkaClusterEncryptionInTransit",
        "kafka_connect_version": "kafkaConnectVersion",
        "plugins": "plugins",
        "service_execution_role_arn": "serviceExecutionRoleArn",
        "connector_description": "connectorDescription",
        "log_delivery": "logDelivery",
        "worker_configuration": "workerConfiguration",
    },
)
class CfnConnectorProps:
    def __init__(
        self,
        *,
        capacity: typing.Union[CfnConnector.CapacityProperty, aws_cdk.core.IResolvable],
        connector_configuration: typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]],
        connector_name: builtins.str,
        kafka_cluster: typing.Union[aws_cdk.core.IResolvable, CfnConnector.KafkaClusterProperty],
        kafka_cluster_client_authentication: typing.Union[aws_cdk.core.IResolvable, CfnConnector.KafkaClusterClientAuthenticationProperty],
        kafka_cluster_encryption_in_transit: typing.Union[aws_cdk.core.IResolvable, CfnConnector.KafkaClusterEncryptionInTransitProperty],
        kafka_connect_version: builtins.str,
        plugins: typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, CfnConnector.PluginProperty]]],
        service_execution_role_arn: builtins.str,
        connector_description: typing.Optional[builtins.str] = None,
        log_delivery: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnConnector.LogDeliveryProperty]] = None,
        worker_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnConnector.WorkerConfigurationProperty]] = None,
    ) -> None:
        '''Properties for defining a ``CfnConnector``.

        :param capacity: ``AWS::KafkaConnect::Connector.Capacity``.
        :param connector_configuration: ``AWS::KafkaConnect::Connector.ConnectorConfiguration``.
        :param connector_name: ``AWS::KafkaConnect::Connector.ConnectorName``.
        :param kafka_cluster: ``AWS::KafkaConnect::Connector.KafkaCluster``.
        :param kafka_cluster_client_authentication: ``AWS::KafkaConnect::Connector.KafkaClusterClientAuthentication``.
        :param kafka_cluster_encryption_in_transit: ``AWS::KafkaConnect::Connector.KafkaClusterEncryptionInTransit``.
        :param kafka_connect_version: ``AWS::KafkaConnect::Connector.KafkaConnectVersion``.
        :param plugins: ``AWS::KafkaConnect::Connector.Plugins``.
        :param service_execution_role_arn: ``AWS::KafkaConnect::Connector.ServiceExecutionRoleArn``.
        :param connector_description: ``AWS::KafkaConnect::Connector.ConnectorDescription``.
        :param log_delivery: ``AWS::KafkaConnect::Connector.LogDelivery``.
        :param worker_configuration: ``AWS::KafkaConnect::Connector.WorkerConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kafkaconnect as kafkaconnect
            
            cfn_connector_props = kafkaconnect.CfnConnectorProps(
                capacity=kafkaconnect.CfnConnector.CapacityProperty(
                    auto_scaling=kafkaconnect.CfnConnector.AutoScalingProperty(
                        max_worker_count=123,
                        mcu_count=123,
                        min_worker_count=123,
                        scale_in_policy=kafkaconnect.CfnConnector.ScaleInPolicyProperty(
                            cpu_utilization_percentage=123
                        ),
                        scale_out_policy=kafkaconnect.CfnConnector.ScaleOutPolicyProperty(
                            cpu_utilization_percentage=123
                        )
                    ),
                    provisioned_capacity=kafkaconnect.CfnConnector.ProvisionedCapacityProperty(
                        worker_count=123,
            
                        # the properties below are optional
                        mcu_count=123
                    )
                ),
                connector_configuration={
                    "connector_configuration_key": "connectorConfiguration"
                },
                connector_name="connectorName",
                kafka_cluster=kafkaconnect.CfnConnector.KafkaClusterProperty(
                    apache_kafka_cluster=kafkaconnect.CfnConnector.ApacheKafkaClusterProperty(
                        bootstrap_servers="bootstrapServers",
                        vpc=kafkaconnect.CfnConnector.VpcProperty(
                            security_groups=["securityGroups"],
                            subnets=["subnets"]
                        )
                    )
                ),
                kafka_cluster_client_authentication=kafkaconnect.CfnConnector.KafkaClusterClientAuthenticationProperty(
                    authentication_type="authenticationType"
                ),
                kafka_cluster_encryption_in_transit=kafkaconnect.CfnConnector.KafkaClusterEncryptionInTransitProperty(
                    encryption_type="encryptionType"
                ),
                kafka_connect_version="kafkaConnectVersion",
                plugins=[kafkaconnect.CfnConnector.PluginProperty(
                    custom_plugin=kafkaconnect.CfnConnector.CustomPluginProperty(
                        custom_plugin_arn="customPluginArn",
                        revision=123
                    )
                )],
                service_execution_role_arn="serviceExecutionRoleArn",
            
                # the properties below are optional
                connector_description="connectorDescription",
                log_delivery=kafkaconnect.CfnConnector.LogDeliveryProperty(
                    worker_log_delivery=kafkaconnect.CfnConnector.WorkerLogDeliveryProperty(
                        cloud_watch_logs=kafkaconnect.CfnConnector.CloudWatchLogsLogDeliveryProperty(
                            enabled=False,
            
                            # the properties below are optional
                            log_group="logGroup"
                        ),
                        firehose=kafkaconnect.CfnConnector.FirehoseLogDeliveryProperty(
                            enabled=False,
            
                            # the properties below are optional
                            delivery_stream="deliveryStream"
                        ),
                        s3=kafkaconnect.CfnConnector.S3LogDeliveryProperty(
                            enabled=False,
            
                            # the properties below are optional
                            bucket="bucket",
                            prefix="prefix"
                        )
                    )
                ),
                worker_configuration=kafkaconnect.CfnConnector.WorkerConfigurationProperty(
                    revision=123,
                    worker_configuration_arn="workerConfigurationArn"
                )
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "capacity": capacity,
            "connector_configuration": connector_configuration,
            "connector_name": connector_name,
            "kafka_cluster": kafka_cluster,
            "kafka_cluster_client_authentication": kafka_cluster_client_authentication,
            "kafka_cluster_encryption_in_transit": kafka_cluster_encryption_in_transit,
            "kafka_connect_version": kafka_connect_version,
            "plugins": plugins,
            "service_execution_role_arn": service_execution_role_arn,
        }
        if connector_description is not None:
            self._values["connector_description"] = connector_description
        if log_delivery is not None:
            self._values["log_delivery"] = log_delivery
        if worker_configuration is not None:
            self._values["worker_configuration"] = worker_configuration

    @builtins.property
    def capacity(
        self,
    ) -> typing.Union[CfnConnector.CapacityProperty, aws_cdk.core.IResolvable]:
        '''``AWS::KafkaConnect::Connector.Capacity``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-capacity
        '''
        result = self._values.get("capacity")
        assert result is not None, "Required property 'capacity' is missing"
        return typing.cast(typing.Union[CfnConnector.CapacityProperty, aws_cdk.core.IResolvable], result)

    @builtins.property
    def connector_configuration(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::KafkaConnect::Connector.ConnectorConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectorconfiguration
        '''
        result = self._values.get("connector_configuration")
        assert result is not None, "Required property 'connector_configuration' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def connector_name(self) -> builtins.str:
        '''``AWS::KafkaConnect::Connector.ConnectorName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectorname
        '''
        result = self._values.get("connector_name")
        assert result is not None, "Required property 'connector_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kafka_cluster(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnConnector.KafkaClusterProperty]:
        '''``AWS::KafkaConnect::Connector.KafkaCluster``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkacluster
        '''
        result = self._values.get("kafka_cluster")
        assert result is not None, "Required property 'kafka_cluster' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, CfnConnector.KafkaClusterProperty], result)

    @builtins.property
    def kafka_cluster_client_authentication(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnConnector.KafkaClusterClientAuthenticationProperty]:
        '''``AWS::KafkaConnect::Connector.KafkaClusterClientAuthentication``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaclusterclientauthentication
        '''
        result = self._values.get("kafka_cluster_client_authentication")
        assert result is not None, "Required property 'kafka_cluster_client_authentication' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, CfnConnector.KafkaClusterClientAuthenticationProperty], result)

    @builtins.property
    def kafka_cluster_encryption_in_transit(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnConnector.KafkaClusterEncryptionInTransitProperty]:
        '''``AWS::KafkaConnect::Connector.KafkaClusterEncryptionInTransit``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaclusterencryptionintransit
        '''
        result = self._values.get("kafka_cluster_encryption_in_transit")
        assert result is not None, "Required property 'kafka_cluster_encryption_in_transit' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, CfnConnector.KafkaClusterEncryptionInTransitProperty], result)

    @builtins.property
    def kafka_connect_version(self) -> builtins.str:
        '''``AWS::KafkaConnect::Connector.KafkaConnectVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaconnectversion
        '''
        result = self._values.get("kafka_connect_version")
        assert result is not None, "Required property 'kafka_connect_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plugins(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnConnector.PluginProperty]]]:
        '''``AWS::KafkaConnect::Connector.Plugins``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-plugins
        '''
        result = self._values.get("plugins")
        assert result is not None, "Required property 'plugins' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnConnector.PluginProperty]]], result)

    @builtins.property
    def service_execution_role_arn(self) -> builtins.str:
        '''``AWS::KafkaConnect::Connector.ServiceExecutionRoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-serviceexecutionrolearn
        '''
        result = self._values.get("service_execution_role_arn")
        assert result is not None, "Required property 'service_execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_description(self) -> typing.Optional[builtins.str]:
        '''``AWS::KafkaConnect::Connector.ConnectorDescription``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectordescription
        '''
        result = self._values.get("connector_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_delivery(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnConnector.LogDeliveryProperty]]:
        '''``AWS::KafkaConnect::Connector.LogDelivery``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-logdelivery
        '''
        result = self._values.get("log_delivery")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnConnector.LogDeliveryProperty]], result)

    @builtins.property
    def worker_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnConnector.WorkerConfigurationProperty]]:
        '''``AWS::KafkaConnect::Connector.WorkerConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-workerconfiguration
        '''
        result = self._values.get("worker_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnConnector.WorkerConfigurationProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnConnector",
    "CfnConnectorProps",
]

publication.publish()
