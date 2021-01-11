from aws_cdk import (
    aws_apigateway,
    aws_dynamodb,
    aws_lambda,
    aws_s3,
    aws_s3_deployment,
    aws_ssm,
    core,
)


class H05BashoutterStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        table = aws_dynamodb.Table(
            self,
            "Bashoutter-Table",
            partition_key=aws_dynamodb.Attribute(
                name="item_id", type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        bucket = aws_s3.Bucket(
            self,
            "Bashoutter-Bucket",
            website_index_document="index.html",
            public_read_access=True,
            removal_policy=core.RemovalPolicy.DESTROY,
        )
        aws_s3_deployment.BucketDeployment(
            self,
            "BucketDeployment",
            destination_bucket=bucket,
            sources=[aws_s3_deployment.Source.asset("./gui/dist")],
            retain_on_delete=False,
        )

        common_params = {
            "runtime": aws_lambda.Runtime.PYTHON_3_7,
            "environment": {
                "TABLE_NAME": table.table_name,
            },
        }

        get_haiku_lambda = aws_lambda.Function(
            self,
            "GetHaiku",
            code=aws_lambda.Code.from_asset("api"),
            handler="api.get_haiku",
            memory_size=512,
            timeout=core.Duration.seconds(10),
            **common_params,
        )
        post_haiku_lambda = aws_lambda.Function(
            self,
            "PostHaiku",
            code=aws_lambda.Code.from_asset("api"),
            handler="api.post_haiku",
            **common_params,
        )
        patch_haiku_lambda = aws_lambda.Function(
            self,
            "PatchHaiku",
            code=aws_lambda.Code.from_asset("api"),
            handler="api.patch_haiku",
            **common_params,
        )
        delete_haiku_lambda = aws_lambda.Function(
            self,
            "DeleteHaiku",
            code=aws_lambda.Code.from_asset("api"),
            handler="api.delete_haiku",
            **common_params,
        )

        table.grant_read_data(get_haiku_lambda)
        table.grant_read_write_data(post_haiku_lambda)
        table.grant_read_write_data(patch_haiku_lambda)
        table.grant_read_write_data(delete_haiku_lambda)

        api = aws_apigateway.RestApi(
            self,
            "BashoutterApi",
            default_cors_preflight_options=aws_apigateway.CorsOptions(
                allow_origins=aws_apigateway.Cors.ALL_ORIGINS,
                allow_methods=aws_apigateway.Cors.ALL_METHODS,
            ),
        )

        haiku = api.root.add_resource("haiku")
        haiku.add_method("GET", aws_apigateway.LambdaIntegration(get_haiku_lambda))
        haiku.add_method("POST", aws_apigateway.LambdaIntegration(post_haiku_lambda))

        haiku_item_id = haiku.add_resource("{item_id}")
        haiku_item_id.add_method(
            "PATCH", aws_apigateway.LambdaIntegration(patch_haiku_lambda)
        )
        haiku_item_id.add_method(
            "DELETE", aws_apigateway.LambdaIntegration(delete_haiku_lambda)
        )

        aws_ssm.StringParameter(
            self,
            "TABLE_NAME",
            parameter_name="TABLE_NAME",
            string_value=table.table_name,
        )
        aws_ssm.StringParameter(
            self,
            "ENDPOINT_URL",
            parameter_name="ENDPOINT_URL",
            string_value=api.url,
        )

        core.CfnOutput(self, "BacketUrl", value=bucket.bucket_website_domain_name)
