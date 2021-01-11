from aws_cdk import aws_dynamodb, core


class H04DynamodbStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        table = aws_dynamodb.Table(
            self,
            "SimpleTable",
            partition_key=aws_dynamodb.Attribute(
                name="item_id", type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        core.CfnOutput(self, "TableName", value=table.table_name)
