"""Helpers to create Cloudwatch-specific Grafana queries."""

import attr
from attr.validators import instance_of


@attr.s
class CloudwatchTarget(object):
    """
    Generates Cloudwatch target JSON structure.

    Grafana docs on using Cloudwatch:
    https://grafana.com/docs/features/datasources/cloudwatch/
    AWS docs on Cloudwatch metrics:
    https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html

    :param alias: legend alias
    :param dimensions: Cloudwatch dimensions dict
    :param metricName: Cloudwatch metric nam
    :param namespace: CLoudwatch namespace
    :param period:Cloudwatch data period
    :param region: CLoudwatch region
    :param refId: target reference id
    :param statistics: Cloudwatch mathematic statistic
    :param checkParams: If false, disable cloudwatch checks (namespace, region and non empty dimensions)
    """
    alias = attr.ib(default="")
    dimensions = attr.ib(default={}, validator=instance_of(dict))
    metricName = attr.ib(default="")
    namespace = attr.ib(default="")
    period = attr.ib(default="")
    region = attr.ib(default="default")
    refId = attr.ib(default="")
    statistics = attr.ib(default=["Average"], validator=instance_of(list))
    checkParams = attr.ib(default=True, validator=instance_of(bool))

    def to_json_data(self):
        if self.checkParams:
            self.__checkParameters()

        return {
            "alias": self.alias,
            "dimensions": self.dimensions,
            "expression": "",
            "highResolution": False,
            "id": "",
            "metricName": self.metricName,
            "namespace": self.namespace,
            "period": self.period,
            "refId": self.refId,
            "region": self.region,
            "returnData": False,
            "statistics": self.statistics
        }.update(self.dimensions)

    def __checkParameters(self):
        self.__checDimensions()
        self.__checkNamespace()
        self.__checkRegion()

    def __checkDimensions(self):
        if self.dimensions == {}:
            raise Exception(
                'You need to define a valid non empty dimensions dict variable'
            )

    def __checkNamespace(self):
        if not (self.namespace in validNamespaces):
            raise Exception(
                '"{}" is not valid Cloudwatch namespace'.format(
                    self.namespace)
            )

    def __checkRegion(self):
        if not (self.region in validRegions):
            raise Exception(
                '"{}" is not valid AWS region'.format(
                    self.region)
            )


validNamespaces = [
    "AWS/ApiGateway",
    "AWS/AppStream",
    "AWS/AppSync",
    "AWS/Athena",
    "AWS/Billing",
    "AWS/ACMPrivateCA",
    "AWS/CloudFront",
    "AWS/CloudHSM",
    "AWS/CloudSearch",
    "AWS/Logs",
    "AWS/CodeBuild",
    "AWS/Cognito",
    "AWS/Connect",
    "AWS/DataSync",
    "AWS/DMS",
    "AWS/DX",
    "AWS/DocDB",
    "AWS/DynamoDB",
    "AWS/EC2",
    "AWS/EC2Spot",
    "AWS/AutoScaling",
    "AWS/ElasticBeanstalk",
    "AWS/EBS",
    "AWS/ECS",
    "AWS/EFS",
    "AWS/ElasticInference",
    "AWS/ApplicationELB",
    "AWS/ELB",
    "AWS/NetworkELB",
    "AWS/ElasticTranscoder",
    "AWS/ElastiCache",
    "AWS/ElastiCache",
    "AWS/ES",
    "AWS/ElasticMapReduce",
    "AWS/MediaConnect",
    "AWS/MediaConvert",
    "AWS/MediaPackage",
    "AWS/MediaTailor",
    "AWS/Events",
    "AWS/FSx",
    "AWS/FSx",
    "AWS/GameLift",
    "AWS/Glue",
    "AWS/Inspector",
    "AWS/IoT",
    "AWS/IoTAnalytics",
    "AWS/ThingsGraph",
    "AWS/KMS",
    "AWS/KinesisAnalytics",
    "AWS/Firehose",
    "AWS/Kinesis",
    "AWS/KinesisVideo",
    "AWS/Lambda",
    "AWS/Lex",
    "AWS/ML",
    "AWS/Kafka",
    "AWS/AmazonMQ",
    "AWS/Neptune",
    "AWS/OpsWorks",
    "AWS/Polly",
    "AWS/QLDB",
    "AWS/Redshift",
    "AWS/RDS",
    "AWS/Robomaker",
    "AWS/Route53",
    "AWS/SageMaker",
    "AWS/SDKMetrics",
    "AWS/DDoSProtection",
    "AWS/SES",
    "AWS/SNS",
    "AWS/SQS",
    "AWS/S3",
    "AWS/SWF",
    "AWS/States",
    "AWS/StorageGateway",
    "AWS/Textract",
    "AWS/Transfer",
    "AWS/Translate",
    "AWS/TrustedAdvisor",
    "AWS/NATGateway",
    "AWS/TransitGateway",
    "AWS/VPN",
    "AWS/WorkMail",
    "AWS/WorkSpaces",
]

validRegions = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
    "ap-east-1",
    "ap-south-1",
    "ap-southeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-northeast-1",
    "ap-southeast-2",
    "ca-central-1",
    "cn-north-1",
    "cn-northwest-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "eu-north-1",
    "me-south-1",
    "sa-east-1",
    "us-gov-east-1",
    "us-gov-west-1",
    "default",
]
