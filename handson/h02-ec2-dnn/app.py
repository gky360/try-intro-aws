#!/usr/bin/env python3

from aws_cdk import core
import os

from h02_ec2_dnn.h02_ec2_dnn_stack import H02Ec2DnnStack


app = core.App()
H02Ec2DnnStack(
    app, "h02-ec2-dnn",
    key_name=app.node.try_get_context("key_name"),
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    }
)

app.synth()
