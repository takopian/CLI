import re
from src.commands import CommandWithArgs, Command


class Expander:
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
                    new_arg = to_expand()
            full_quote = re.match(r'\'.*\'', arg)
            if full_quote:
                new_arg = arg[1:-1]
            new_args.append(new_arg)
        command.args = new_args
