from src.parser import Parser, CommandWithArgs
from src.expander import Expander
from src.executor import Executor


def interpreter():
    context = Expander()
    while True:
        try:
            line = input()
            pipeline = Parser(context, line).parse()
            for command in pipeline:
                if isinstance(command, CommandWithArgs):
                    context.expand(command)
            Executor(pipeline).execute()
        except EOFError:
            exit()


if __name__ == "__main__":
    interpreter()
