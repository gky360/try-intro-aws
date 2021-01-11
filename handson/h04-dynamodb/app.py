#!/usr/bin/env python3

from aws_cdk import core

from h04_dynamodb.h04_dynamodb_stack import H04DynamodbStack


app = core.App()
H04DynamodbStack(app, "h04-dynamodb")

app.synth()
