from src.commands import CommandWithArgs


class Executor:
    """
    Class that executes commands.
    Fields:
        command_pipeline - pipeline (or single command) to execute.
    Methods:
        execute() - executes passed command_pipeline, prints result in stdout.
    """
    def __init__(self, command_pipeline: [CommandWithArgs]):
        self.command_pipeline = command_pipeline

    def execute(self):
        cur_result = None
        for command in self.command_pipeline:
            try:
                if cur_result and not command.args:
                    command.input = cur_result
                cur_result = command()
            except RuntimeError as e:
                print(e)
        if cur_result:
            print(cur_result)
            return cur_result
