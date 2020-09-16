from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_dynamodb as dynamodb,
    aws_ssm as ssm,
    aws_iam as iam,
    aws_logs
)
import os


class H03QaBotStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # dynamoDB table to store questions and answers
        table = dynamodb.Table(
            self, "H03QaBot-Table",
            partition_key=dynamodb.Attribute(
                name="item_id", type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        vpc = ec2.Vpc(
            self, "H03QaBot-Vpc",
            max_azs=1,
        )

        cluster = ecs.Cluster(
            self, "H03QaBot-Cluster",
            vpc=vpc,
        )

        taskdef = ecs.FargateTaskDefinition(
            self, "H03QaBot-TaskDef",
            cpu=1024, # 1 CPU
            memory_limit_mib=4096, # 4GB RAM
        )

        # grant permissions
        table.grant_read_write_data(taskdef.task_role)
        taskdef.add_to_task_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                resources=["*"],
                actions=["ssm:GetParameter"],
            )
        )

        container = taskdef.add_container(
            "H03QaBot-Container",
            image=ecs.ContainerImage.from_registry(
                "registry.gitlab.com/tomomano/intro-aws/handson03:latest"
            ),
        )

        # Store parameters in SSM
        ssm.StringParameter(
            self, "ECS_CLUSTER_NAME",
            parameter_name="ECS_CLUSTER_NAME",
            string_value=cluster.cluster_name,
        )
        ssm.StringParameter(
            self, "ECS_TASK_DEFINITION_ARN",
            parameter_name="ECS_TASK_DEFINITION_ARN",
            string_value=taskdef.task_definition_arn,
        )
        ssm.StringParameter(
            self, "ECS_TASK_VPC_SUBNET_1",
            parameter_name="ECS_TASK_VPC_SUBNET_1",
            string_value=vpc.public_subnets[0].subnet_id,
        )
        ssm.StringParameter(
            self, "CONTAINER_NAME",
            parameter_name="CONTAINER_NAME",
            string_value=container.container_name,
        )
        ssm.StringParameter(
            self, "TABLE_NAME",
            parameter_name="TABLE_NAME",
            string_value=table.table_name,
        )

        core.CfnOutput(self, "ClusterName", value=cluster.cluster_name)
        core.CfnOutput(self, "TaskDefinitionArn", value=taskdef.task_definition_arn)
