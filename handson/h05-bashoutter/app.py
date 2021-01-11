#!/usr/bin/env python3

from aws_cdk import core

from h05_bashoutter.h05_bashoutter_stack import H05BashoutterStack


app = core.App()
H05BashoutterStack(app, "h05-bashoutter")

app.synth()
