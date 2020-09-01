#!/usr/bin/env python3

from aws_cdk import core
import os

from h01_ec2.h01_ec2_stack import H01Ec2Stack


app = core.App()
H01Ec2Stack(
    app, "h01-ec2",
    key_name=app.node.try_get_context("key_name"),
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    },
)

app.synth()
