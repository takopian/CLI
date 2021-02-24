import re
from src.commands import CommandWithArgs, Command
from src.executor import Executor


class Expander:
    """
    Class, that contain variables and can extend arguments, passed to command.
    Fields:
        context - dict of current variables with values.
    Methods:
        expand(command: CommandWithArgs) - expands command.args with context variables.
    """
    def __init__(self):
        self.context = {}

    def expand(self, command: CommandWithArgs):
        new_args = []
        for arg in command.args:
            new_arg = arg
            expansion = re.match(r'\"\$.*\"', arg)
            if expansion:
                to_expand = self.context.get(arg[2:-1])
                if to_expand:
                    if isinstance(to_expand, list):
                        new_arg = Executor(to_expand).execute()
                    else:
                        new_arg = to_expand()
            full_quote = re.match(r'\'.*\'', arg)
            if full_quote:
                new_arg = arg[1:-1]
            new_args.append(new_arg)
        command.args = new_args
