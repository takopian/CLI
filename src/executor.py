from src.commands import CommandWithArgs


class Executor:
    def __init__(self, command_pipeline: [CommandWithArgs]):
        self.command_pipeline = command_pipeline

    def execute(self):
        for command in self.command_pipeline:
            try:
                command()
            except RuntimeError as e:
                print('execution error')