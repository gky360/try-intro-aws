#!/usr/bin/env python3

from aws_cdk import core
import os

from h03_qa_bot.h03_qa_bot_stack import H03QaBotStack


app = core.App()
H03QaBotStack(
    app, "h03-qa-bot",
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    },
)

app.synth()
