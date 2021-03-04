import sys
sys.path.append('/CLI')

from src.parser import Parser, CommandWithArgs, ExitException
from src.expander import Expander
from src.executor import Executor
import sys


class Shell:
    """
    Class, that runs bash interpreter.

    Fields
    ------
    input : interpreter input stream (sys.stdin by default).
    output : interpreter output stream (sys.stdout by default).

    Methods
    ------
    run : runs interpreter.
    """
    def __init__(self, input_stream = None, output_stream = None):
        self.input = input_stream or sys.stdin
        self.output = output_stream or sys.stdout

    def run(self):

        try:
            if self.input != sys.stdin:
                input_ = open(self.input, 'r')
            else:
                input_ = self.input
        except FileNotFoundError as e:
            print(e)
            exit()
        except Exception as e:
            print(e)
            exit()
        try:
            if self.output != sys.stdout:
                output_ = open(self.output, 'a')
            else:
                output_ = self.output
        except FileNotFoundError as e:
            input_.close()
            print(e)
            exit()
        except Exception as e:
            input_.close()
            print(e)
            exit()

        try:
            context = Expander()
            for line in input_:
                try:
                    pipeline = Parser(context, line).parse()
                    for command in pipeline:
                        if isinstance(command, CommandWithArgs):
                            context.expand(command)
                    result = Executor(pipeline).execute()
                    if result:
                        output_.write(result)
                        output_.write('\n')
                except EOFError:
                    exit()
                except ExitException:
                    exit()
                except IndexError:
                    continue
                except Exception as e:
                    print(e)
                    continue
        except RuntimeError as e:
            print(e)
            input_.close()
            output_.close()
            exit()


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        Shell(sys.argv[1], sys.argv[2]).run()
    elif len(sys.argv) == 2:
        Shell(sys.argv[1]).run()
    else:
        Shell().run()
