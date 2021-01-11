from aws_cdk import aws_lambda, core

FUNC = """
import time
from random import choice, randint
def handler(event, context):
    time.sleep(randint(2,5))
    pokemon = ["Charmander", "Bulbasaur", "Squirtle"]
    message = "Congratulations! You are given " + choice(pokemon)
    print(message)
    return message
"""


class H04LambdaStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        handler = aws_lambda.Function(
            self,
            "LambdaHander",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler="index.handler",
            code=aws_lambda.Code.from_inline(FUNC),
            memory_size=128,
            timeout=core.Duration.seconds(10),
            dead_letter_queue_enabled=True,
        )

        core.CfnOutput(self, "FunctionName", value=handler.function_name)
