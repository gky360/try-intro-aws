#!/usr/bin/env python3

import os

from aws_cdk import core

from h04_lambda.h04_lambda_stack import H04LambdaStack

app = core.App()
H04LambdaStack(
    app,
    "h04-lambda",
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    },
)

app.synth()
