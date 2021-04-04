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
            full_quote = re.match(r'\'.*\'', arg)
            if full_quote:
                new_arg = arg[1:-1]
                new_args.append(new_arg)
                continue
            expansion = re.findall(r'\$[^\$\s\"]+', arg)
            if expansion:
                pepe = []
                for item in expansion:
                    to_expand = self.context.get(item[1:])
                    if to_expand:
                        if isinstance(to_expand, list):
                            pepe.append(Executor(to_expand).execute())
                        else:
                            pepe.append(to_expand())
                    else:
                        pepe.append(item)
                new_arg = "".join(pepe)
            new_args.append(new_arg)
        command.args = new_args
