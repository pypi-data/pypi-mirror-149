'''
[![NPM version](https://badge.fury.io/js/cdk-compliant-dynamodb.svg)](https://badge.fury.io/js/cdk-compliant-dynamodb)
[![PyPI version](https://badge.fury.io/py/cdk-compliant-dynamodb.svg)](https://badge.fury.io/py/cdk-compliant-dynamodb)
![Release](https://github.com/oev-berlin/cdk-compliant-dynamodb/workflows/release/badge.svg)

# cdk-compliant-dynamodb

`cdk-compliant-dynamodb` is an AWS CK construct that allows you to easily create an AWS DynamoDB that is fully compliant against the following AWS Config rules:

* [BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED](https://docs.aws.amazon.com/config/latest/developerguide/backup-recovery-point-manual-deletion-disabled.html)
* [DYNAMODB_IN_BACKUP_PLAN](https://docs.aws.amazon.com/config/latest/developerguide/dynamodb-in-backup-plan.html)
* [DYNAMODB_PITR_ENABLED](https://docs.aws.amazon.com/config/latest/developerguide/dynamodb-pitr-enabled.html)
* [DYNAMODB_AUTOSCALING_ENABLED](https://docs.aws.amazon.com/config/latest/developerguide/dynamodb-autoscaling-enabled.html)
* [DYNAMODB_THROUGHPUT_LIMIT_CHECK](https://docs.aws.amazon.com/config/latest/developerguide/dynamodb-throughput-limit-check.html)
* [DYNAMODB_TABLE_ENCRYPTED_KMS](https://docs.aws.amazon.com/config/latest/developerguide/dynamodb-table-encrypted-kms.html)

## Why

Use this construct to be compliant against the most common AWS Config rules without the need to even know them. Opt-out of rules for non production environments.

## Sample

create a fully compliant DynamoDb table with imported AWS Backup vault

```python
new CompliantDynamoDb(stack, 'MyCompliantDynamoDB', {
  partitionKey: {
    name: 'id',
    type: dynamodb.AttributeType.STRING,
  },
  backupVaultName: 'my-dynamodb-backup-vault',
  deleteBackupAfterDays: 90,
  backupPlanStartTime: 6,
});
```

Opt out of all rules (create a non compliant table)

```python
new CompliantDynamoDb(stack, 'MyCompliantDynamoDB', {
  partitionKey: {
    name: 'id',
    type: dynamodb.AttributeType.STRING,
  },
  disabledRules: [
    'BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED',
    'DYNAMODB_IN_BACKUP_PLAN',
    'DYNAMODB_PITR_ENABLED',
    'DYNAMODB_AUTOSCALING_ENABLED',
    'DYNAMODB_THROUGHPUT_LIMIT_CHECK',
    'DYNAMODB_TABLE_ENCRYPTED_KMS',
  ],
});
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

from ._jsii import *

import aws_cdk
import aws_cdk.aws_backup
import aws_cdk.aws_dynamodb
import aws_cdk.aws_events
import aws_cdk.aws_kinesis
import aws_cdk.aws_kms
import constructs


class CompliantDynamoDb(
    aws_cdk.aws_dynamodb.Table,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-compliant-dynamodb.CompliantDynamoDb",
):
    '''Creates a DynamoDB table that is secured by an AWS backup plan und with point in time recovery enabled by default.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        backup_plan_start_time: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        backup_vault_name: typing.Optional[builtins.str] = None,
        delete_backup_after_days: typing.Optional[jsii.Number] = None,
        disabled_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        kinesis_stream: typing.Optional[aws_cdk.aws_kinesis.IStream] = None,
        table_name: typing.Optional[builtins.str] = None,
        billing_mode: typing.Optional[aws_cdk.aws_dynamodb.BillingMode] = None,
        contributor_insights_enabled: typing.Optional[builtins.bool] = None,
        encryption: typing.Optional[aws_cdk.aws_dynamodb.TableEncryption] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        point_in_time_recovery: typing.Optional[builtins.bool] = None,
        read_capacity: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
        replication_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        replication_timeout: typing.Optional[aws_cdk.Duration] = None,
        stream: typing.Optional[aws_cdk.aws_dynamodb.StreamViewType] = None,
        time_to_live_attribute: typing.Optional[builtins.str] = None,
        wait_for_replication_to_finish: typing.Optional[builtins.bool] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
        partition_key: aws_cdk.aws_dynamodb.Attribute,
        sort_key: typing.Optional[aws_cdk.aws_dynamodb.Attribute] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param backup_plan_start_time: Time to start the backup. Default: - 9pm
        :param backup_vault_name: Use an existing BackupVault and import it by name. Default: - create a new BackupVault
        :param delete_backup_after_days: Days until the backup is deleted from the vault. Default: - 35 days
        :param disabled_rules: AWS Config rules that I want to opt out. Default: - table is compliant against all rules List of rules to opt out: 'BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED', 'DYNAMODB_IN_BACKUP_PLAN', 'DYNAMODB_PITR_ENABLED', 'DYNAMODB_AUTOSCALING_ENABLED', 'DYNAMODB_THROUGHPUT_LIMIT_CHECK', 'DYNAMODB_TABLE_ENCRYPTED_KMS',
        :param kinesis_stream: Kinesis Data Stream to capture item-level changes for the table. Default: - no Kinesis Data Stream
        :param table_name: Enforces a particular physical table name. Default: 
        :param billing_mode: Specify how you are charged for read and write throughput and how you manage capacity. Default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise
        :param contributor_insights_enabled: Whether CloudWatch contributor insights is enabled. Default: false
        :param encryption: Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``serverSideEncryption`` is set. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param encryption_key: External KMS key to use for table encryption. This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``. Default: - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this property is undefined, a new KMS key will be created and associated with this table.
        :param point_in_time_recovery: Whether point-in-time recovery is enabled. Default: - point-in-time recovery is disabled
        :param read_capacity: The read capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param removal_policy: The removal policy to apply to the DynamoDB Table. Default: RemovalPolicy.RETAIN
        :param replication_regions: Regions where replica tables will be created. Default: - no replica tables are created
        :param replication_timeout: The timeout for a table replication operation in a single region. Default: Duration.minutes(30)
        :param stream: When an item in the table is modified, StreamViewType determines what information is written to the stream for this table. Default: - streams are disabled unless ``replicationRegions`` is specified
        :param time_to_live_attribute: The name of TTL attribute. Default: - TTL is disabled
        :param wait_for_replication_to_finish: Indicates whether CloudFormation stack waits for replication to finish. If set to false, the CloudFormation resource will mark the resource as created and replication will be completed asynchronously. This property is ignored if replicationRegions property is not set. DO NOT UNSET this property if adding/removing multiple replicationRegions in one deployment, as CloudFormation only supports one region replication at a time. CDK overcomes this limitation by waiting for replication to finish before starting new replicationRegion. Default: true
        :param write_capacity: The write capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param partition_key: Partition key attribute definition.
        :param sort_key: Sort key attribute definition. Default: no sort key
        '''
        props = CompliantDynamoDbProps(
            backup_plan_start_time=backup_plan_start_time,
            backup_vault_name=backup_vault_name,
            delete_backup_after_days=delete_backup_after_days,
            disabled_rules=disabled_rules,
            kinesis_stream=kinesis_stream,
            table_name=table_name,
            billing_mode=billing_mode,
            contributor_insights_enabled=contributor_insights_enabled,
            encryption=encryption,
            encryption_key=encryption_key,
            point_in_time_recovery=point_in_time_recovery,
            read_capacity=read_capacity,
            removal_policy=removal_policy,
            replication_regions=replication_regions,
            replication_timeout=replication_timeout,
            stream=stream,
            time_to_live_attribute=time_to_live_attribute,
            wait_for_replication_to_finish=wait_for_replication_to_finish,
            write_capacity=write_capacity,
            partition_key=partition_key,
            sort_key=sort_key,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupPlan")
    def backup_plan(self) -> aws_cdk.aws_backup.BackupPlan:
        return typing.cast(aws_cdk.aws_backup.BackupPlan, jsii.get(self, "backupPlan"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupVault")
    def backup_vault(self) -> aws_cdk.aws_backup.BackupVault:
        return typing.cast(aws_cdk.aws_backup.BackupVault, jsii.get(self, "backupVault"))


@jsii.data_type(
    jsii_type="cdk-compliant-dynamodb.CompliantDynamoDbProps",
    jsii_struct_bases=[aws_cdk.aws_dynamodb.TableProps],
    name_mapping={
        "partition_key": "partitionKey",
        "sort_key": "sortKey",
        "billing_mode": "billingMode",
        "contributor_insights_enabled": "contributorInsightsEnabled",
        "encryption": "encryption",
        "encryption_key": "encryptionKey",
        "point_in_time_recovery": "pointInTimeRecovery",
        "read_capacity": "readCapacity",
        "removal_policy": "removalPolicy",
        "replication_regions": "replicationRegions",
        "replication_timeout": "replicationTimeout",
        "stream": "stream",
        "time_to_live_attribute": "timeToLiveAttribute",
        "wait_for_replication_to_finish": "waitForReplicationToFinish",
        "write_capacity": "writeCapacity",
        "kinesis_stream": "kinesisStream",
        "table_name": "tableName",
        "backup_plan_start_time": "backupPlanStartTime",
        "backup_vault_name": "backupVaultName",
        "delete_backup_after_days": "deleteBackupAfterDays",
        "disabled_rules": "disabledRules",
    },
)
class CompliantDynamoDbProps(aws_cdk.aws_dynamodb.TableProps):
    def __init__(
        self,
        *,
        partition_key: aws_cdk.aws_dynamodb.Attribute,
        sort_key: typing.Optional[aws_cdk.aws_dynamodb.Attribute] = None,
        billing_mode: typing.Optional[aws_cdk.aws_dynamodb.BillingMode] = None,
        contributor_insights_enabled: typing.Optional[builtins.bool] = None,
        encryption: typing.Optional[aws_cdk.aws_dynamodb.TableEncryption] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        point_in_time_recovery: typing.Optional[builtins.bool] = None,
        read_capacity: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
        replication_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        replication_timeout: typing.Optional[aws_cdk.Duration] = None,
        stream: typing.Optional[aws_cdk.aws_dynamodb.StreamViewType] = None,
        time_to_live_attribute: typing.Optional[builtins.str] = None,
        wait_for_replication_to_finish: typing.Optional[builtins.bool] = None,
        write_capacity: typing.Optional[jsii.Number] = None,
        kinesis_stream: typing.Optional[aws_cdk.aws_kinesis.IStream] = None,
        table_name: typing.Optional[builtins.str] = None,
        backup_plan_start_time: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        backup_vault_name: typing.Optional[builtins.str] = None,
        delete_backup_after_days: typing.Optional[jsii.Number] = None,
        disabled_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param partition_key: Partition key attribute definition.
        :param sort_key: Sort key attribute definition. Default: no sort key
        :param billing_mode: Specify how you are charged for read and write throughput and how you manage capacity. Default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise
        :param contributor_insights_enabled: Whether CloudWatch contributor insights is enabled. Default: false
        :param encryption: Whether server-side encryption with an AWS managed customer master key is enabled. This property cannot be set if ``serverSideEncryption`` is set. Default: - server-side encryption is enabled with an AWS owned customer master key
        :param encryption_key: External KMS key to use for table encryption. This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``. Default: - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this property is undefined, a new KMS key will be created and associated with this table.
        :param point_in_time_recovery: Whether point-in-time recovery is enabled. Default: - point-in-time recovery is disabled
        :param read_capacity: The read capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param removal_policy: The removal policy to apply to the DynamoDB Table. Default: RemovalPolicy.RETAIN
        :param replication_regions: Regions where replica tables will be created. Default: - no replica tables are created
        :param replication_timeout: The timeout for a table replication operation in a single region. Default: Duration.minutes(30)
        :param stream: When an item in the table is modified, StreamViewType determines what information is written to the stream for this table. Default: - streams are disabled unless ``replicationRegions`` is specified
        :param time_to_live_attribute: The name of TTL attribute. Default: - TTL is disabled
        :param wait_for_replication_to_finish: Indicates whether CloudFormation stack waits for replication to finish. If set to false, the CloudFormation resource will mark the resource as created and replication will be completed asynchronously. This property is ignored if replicationRegions property is not set. DO NOT UNSET this property if adding/removing multiple replicationRegions in one deployment, as CloudFormation only supports one region replication at a time. CDK overcomes this limitation by waiting for replication to finish before starting new replicationRegion. Default: true
        :param write_capacity: The write capacity for the table. Careful if you add Global Secondary Indexes, as those will share the table's provisioned throughput. Can only be provided if billingMode is Provisioned. Default: 5
        :param kinesis_stream: Kinesis Data Stream to capture item-level changes for the table. Default: - no Kinesis Data Stream
        :param table_name: Enforces a particular physical table name. Default: 
        :param backup_plan_start_time: Time to start the backup. Default: - 9pm
        :param backup_vault_name: Use an existing BackupVault and import it by name. Default: - create a new BackupVault
        :param delete_backup_after_days: Days until the backup is deleted from the vault. Default: - 35 days
        :param disabled_rules: AWS Config rules that I want to opt out. Default: - table is compliant against all rules List of rules to opt out: 'BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED', 'DYNAMODB_IN_BACKUP_PLAN', 'DYNAMODB_PITR_ENABLED', 'DYNAMODB_AUTOSCALING_ENABLED', 'DYNAMODB_THROUGHPUT_LIMIT_CHECK', 'DYNAMODB_TABLE_ENCRYPTED_KMS',
        '''
        if isinstance(partition_key, dict):
            partition_key = aws_cdk.aws_dynamodb.Attribute(**partition_key)
        if isinstance(sort_key, dict):
            sort_key = aws_cdk.aws_dynamodb.Attribute(**sort_key)
        self._values: typing.Dict[str, typing.Any] = {
            "partition_key": partition_key,
        }
        if sort_key is not None:
            self._values["sort_key"] = sort_key
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if contributor_insights_enabled is not None:
            self._values["contributor_insights_enabled"] = contributor_insights_enabled
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if point_in_time_recovery is not None:
            self._values["point_in_time_recovery"] = point_in_time_recovery
        if read_capacity is not None:
            self._values["read_capacity"] = read_capacity
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if replication_regions is not None:
            self._values["replication_regions"] = replication_regions
        if replication_timeout is not None:
            self._values["replication_timeout"] = replication_timeout
        if stream is not None:
            self._values["stream"] = stream
        if time_to_live_attribute is not None:
            self._values["time_to_live_attribute"] = time_to_live_attribute
        if wait_for_replication_to_finish is not None:
            self._values["wait_for_replication_to_finish"] = wait_for_replication_to_finish
        if write_capacity is not None:
            self._values["write_capacity"] = write_capacity
        if kinesis_stream is not None:
            self._values["kinesis_stream"] = kinesis_stream
        if table_name is not None:
            self._values["table_name"] = table_name
        if backup_plan_start_time is not None:
            self._values["backup_plan_start_time"] = backup_plan_start_time
        if backup_vault_name is not None:
            self._values["backup_vault_name"] = backup_vault_name
        if delete_backup_after_days is not None:
            self._values["delete_backup_after_days"] = delete_backup_after_days
        if disabled_rules is not None:
            self._values["disabled_rules"] = disabled_rules

    @builtins.property
    def partition_key(self) -> aws_cdk.aws_dynamodb.Attribute:
        '''Partition key attribute definition.'''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(aws_cdk.aws_dynamodb.Attribute, result)

    @builtins.property
    def sort_key(self) -> typing.Optional[aws_cdk.aws_dynamodb.Attribute]:
        '''Sort key attribute definition.

        :default: no sort key
        '''
        result = self._values.get("sort_key")
        return typing.cast(typing.Optional[aws_cdk.aws_dynamodb.Attribute], result)

    @builtins.property
    def billing_mode(self) -> typing.Optional[aws_cdk.aws_dynamodb.BillingMode]:
        '''Specify how you are charged for read and write throughput and how you manage capacity.

        :default: PROVISIONED if ``replicationRegions`` is not specified, PAY_PER_REQUEST otherwise
        '''
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[aws_cdk.aws_dynamodb.BillingMode], result)

    @builtins.property
    def contributor_insights_enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether CloudWatch contributor insights is enabled.

        :default: false
        '''
        result = self._values.get("contributor_insights_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption(self) -> typing.Optional[aws_cdk.aws_dynamodb.TableEncryption]:
        '''Whether server-side encryption with an AWS managed customer master key is enabled.

        This property cannot be set if ``serverSideEncryption`` is set.

        :default: - server-side encryption is enabled with an AWS owned customer master key
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[aws_cdk.aws_dynamodb.TableEncryption], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        '''External KMS key to use for table encryption.

        This property can only be set if ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED``.

        :default:

        - If ``encryption`` is set to ``TableEncryption.CUSTOMER_MANAGED`` and this
        property is undefined, a new KMS key will be created and associated with this table.
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], result)

    @builtins.property
    def point_in_time_recovery(self) -> typing.Optional[builtins.bool]:
        '''Whether point-in-time recovery is enabled.

        :default: - point-in-time recovery is disabled
        '''
        result = self._values.get("point_in_time_recovery")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def read_capacity(self) -> typing.Optional[jsii.Number]:
        '''The read capacity for the table.

        Careful if you add Global Secondary Indexes, as
        those will share the table's provisioned throughput.

        Can only be provided if billingMode is Provisioned.

        :default: 5
        '''
        result = self._values.get("read_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.RemovalPolicy]:
        '''The removal policy to apply to the DynamoDB Table.

        :default: RemovalPolicy.RETAIN
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[aws_cdk.RemovalPolicy], result)

    @builtins.property
    def replication_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Regions where replica tables will be created.

        :default: - no replica tables are created
        '''
        result = self._values.get("replication_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def replication_timeout(self) -> typing.Optional[aws_cdk.Duration]:
        '''The timeout for a table replication operation in a single region.

        :default: Duration.minutes(30)
        '''
        result = self._values.get("replication_timeout")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def stream(self) -> typing.Optional[aws_cdk.aws_dynamodb.StreamViewType]:
        '''When an item in the table is modified, StreamViewType determines what information is written to the stream for this table.

        :default: - streams are disabled unless ``replicationRegions`` is specified
        '''
        result = self._values.get("stream")
        return typing.cast(typing.Optional[aws_cdk.aws_dynamodb.StreamViewType], result)

    @builtins.property
    def time_to_live_attribute(self) -> typing.Optional[builtins.str]:
        '''The name of TTL attribute.

        :default: - TTL is disabled
        '''
        result = self._values.get("time_to_live_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait_for_replication_to_finish(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether CloudFormation stack waits for replication to finish.

        If set to false, the CloudFormation resource will mark the resource as
        created and replication will be completed asynchronously. This property is
        ignored if replicationRegions property is not set.

        DO NOT UNSET this property if adding/removing multiple replicationRegions
        in one deployment, as CloudFormation only supports one region replication
        at a time. CDK overcomes this limitation by waiting for replication to
        finish before starting new replicationRegion.

        :default: true

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-globaltable.html#cfn-dynamodb-globaltable-replicas
        '''
        result = self._values.get("wait_for_replication_to_finish")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def write_capacity(self) -> typing.Optional[jsii.Number]:
        '''The write capacity for the table.

        Careful if you add Global Secondary Indexes, as
        those will share the table's provisioned throughput.

        Can only be provided if billingMode is Provisioned.

        :default: 5
        '''
        result = self._values.get("write_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kinesis_stream(self) -> typing.Optional[aws_cdk.aws_kinesis.IStream]:
        '''Kinesis Data Stream to capture item-level changes for the table.

        :default: - no Kinesis Data Stream
        '''
        result = self._values.get("kinesis_stream")
        return typing.cast(typing.Optional[aws_cdk.aws_kinesis.IStream], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''Enforces a particular physical table name.

        :default:
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_plan_start_time(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        '''Time to start the backup.

        :default: - 9pm
        '''
        result = self._values.get("backup_plan_start_time")
        return typing.cast(typing.Optional[aws_cdk.aws_events.Schedule], result)

    @builtins.property
    def backup_vault_name(self) -> typing.Optional[builtins.str]:
        '''Use an existing BackupVault and import it by name.

        :default: - create a new BackupVault
        '''
        result = self._values.get("backup_vault_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_backup_after_days(self) -> typing.Optional[jsii.Number]:
        '''Days until the backup is deleted from the vault.

        :default: - 35 days
        '''
        result = self._values.get("delete_backup_after_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disabled_rules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''AWS Config rules that I want to opt out.

        :default:

        - table is compliant against all rules

        List of rules to opt out:
        'BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED',
        'DYNAMODB_IN_BACKUP_PLAN',
        'DYNAMODB_PITR_ENABLED',
        'DYNAMODB_AUTOSCALING_ENABLED',
        'DYNAMODB_THROUGHPUT_LIMIT_CHECK',
        'DYNAMODB_TABLE_ENCRYPTED_KMS',
        '''
        result = self._values.get("disabled_rules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CompliantDynamoDbProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CompliantDynamoDb",
    "CompliantDynamoDbProps",
]

publication.publish()
