import os
import re

class Command:
    def __init__(self, name: str):
        self.name = name

    def __call__(self):
        pass


class CommandWithArgs(Command):
    def __init__(self, name: str, args: list):
        super().__init__(name)
        self.args = args

    def __call__(self):
        pass


class Executor:
    def __init__(self, command_pipeline: [CommandWithArgs]):
        self.command_pipeline = command_pipeline

    def execute(self):
        for command in self.command_pipeline:
            try:
                command()
            except RuntimeError as e:
                print('execution error')


class Cat(CommandWithArgs):
    def __init__(self, args: list = None):
        super().__init__('cat', args)

    def __call__(self):
        if self.args:
            for arg in self.args:
                try:
                    file = open(arg, mode='r')
                    file_content = file.read()
                    file.close()
                    print(file_content)
                except:
                    print(f"exception occurred while reading file {arg}")
                return file_content
        else:
            while True:
                try:
                    line = input()
                    print(line)
                except EOFError:
                    return


class Echo(CommandWithArgs):
    def __init__(self, args: list = None):
        super().__init__('echo', args)

    def __call__(self):
        print(*self.args)
        return " ".join(self.args)


def statistics(filename):
    byte = os.path.getsize(filename)
    newline = 0
    word = 0
    with open(filename) as file:
        for line in file:
            newline += 1
            line = line.split(' ')
            word += len(line)
    return [newline, word, byte]


class WC(CommandWithArgs):
    def __init__(self, args: list = None):
        super().__init__('echo', args)

    def __call__(self):
        if len(self.args) > 1:
            total = [0] * 3
            for file in self.args:
                stat = statistics(file)
                for i in range(3):
                    total[i] += stat[i]
                print(*stat, file)
            print(*total, "total", end='\n')
            return " ".join(map(str, total))

        elif len(self.args) == 1:
            stat = statistics(self.args[0])
            print(*stat, self.args[0], end='\n')
            return " ".join(map(str, stat))

        else:
            newline = 0
            byte = 0
            word = 0
            while 1:
                try:
                    line = input()
                except EOFError:
                    print(newline, word, byte, end='\n')
                    exit()
                byte += len(line.encode('utf-8'))
                newline += 1
                line = line.split(' ')
                word += len(line)


class PWD(CommandWithArgs):
    def __init__(self, args: list = None):
        super().__init__('pwd', args)

    def __call__(self):
        print(os.getcwd())
        return os.getcwd()


class Exit(CommandWithArgs):
    def __init__(self, args: list = None):
        super().__init__('exit', args)

    def __call__(self):
        exit()


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


commandDict = {'cat': Cat, 'echo': Echo, 'wc': WC, 'pwd': PWD, 'exit': Exit}


class Parser:
    def __init__(self, context: Expander, line: str):
        self.line = line
        self.context = context
        self.pipeline = line.split('|')
        self.parsed_pipeline = []

        for command in self.pipeline:
            rest_line = command
            parsed_command = []
            first_quote = re.search(r'[\'\"]', rest_line)
            if first_quote:
                parsed_command.extend(rest_line[0:first_quote.start()].split())
                rest_line = rest_line[first_quote.start():]
                while rest_line:
                    full_quote = re.match(r'[\'\"].*[\'\"]', rest_line)
                    if full_quote:
                        parsed_command.append(rest_line[0:full_quote.end()])
                        rest_line = rest_line[full_quote.end():]
                        first_quote = re.search(r'[\'\"]', rest_line)
                        if first_quote and rest_line:
                            parsed_command.extend(rest_line[0:first_quote.start()].split())
                            rest_line = rest_line[first_quote.start():]
                    else:
                        break
                self.parsed_pipeline.append(parsed_command)
            else:
                self.parsed_pipeline.append(command.split())

    def parse(self):
        eqv_pos = self.line.find('=')
        if eqv_pos != -1:
            var_name = self.line[:eqv_pos]
            rest_line = self.line[eqv_pos + 1:]
            if len(var_name.split()) > 1:
                pass
            else:
                # print(rest_line)
                command_result = re.match(r'(\$\(.*\))', rest_line)
                if command_result:
                    # print('oooo', var_name, rest_line[2:-1])
                    self.context.context[var_name] = Parser(self.context, rest_line[2:-1]).parse()
                    return [Command('dummy')]

                var_result = re.match(r'\$?[^\s]*', rest_line)
                print(rest_line, var_result)
                if var_result:
                    if rest_line[0] == '$':
                        get_val = self.context.context.get(rest_line[1:])
                        if get_val:
                            self.context.context[var_name] = self.context.context[rest_line[1:]]
                            return [Command('dummy')]
                        else:
                            self.context.context[var_name] = Echo([''])
                            return [Command('dummy')]
                    else:
                        self.context.context[var_name] = Echo([rest_line])
                        return [Command('dummy')]

        command_list = []
        for cmd in self.parsed_pipeline:
            command_name = cmd[0]
            command = commandDict.get(command_name)
            if command is not None:
                command_list.append(command(cmd[1:]))
            else:
                system_command = Command(command_name)
                os.system(self.line)
                command_list.append(system_command)
        return command_list


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
