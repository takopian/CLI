import os
import re


class Command:
    """
    Base class for all commands.
    Fields: name - name of the command.
    """
    def __init__(self, name: str):
        self.name = name

    def __call__(self):
        pass


class CommandWithArgs(Command):
    """
        Base class for all commands with arguments.
        Fields:
        name - name of the command.
        args - list of command arguments.
        input - input that passed to command in pipeline.
    """
    def __init__(self, name: str, args: list):
        super().__init__(name)
        self.args = args
        self.input = None

    def __call__(self):
        pass


class Cat(CommandWithArgs):
    """
        Class that implements cat command.
    """
    def __init__(self, args: list = None):
        super().__init__('cat', args)

    def __call__(self):
        if self.input:
            return self.input
        elif self.args:
            for arg in self.args:
                file_content = None
                try:
                    file = open(arg, mode='r')
                    file_content = file.read()
                    file.close()
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
    """
        Class that implements echo command.
    """
    def __init__(self, args: list = None):
        super().__init__('echo', args)

    def __call__(self):
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
    """
        Class that implements wc command.
    """
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
            return " ".join(list(map(str, total)) )

        elif len(self.args) == 1:
            stat = statistics(self.args[0])
            # print(*stat, self.args[0], end='\n')
            stat.append(self.args[0])
            return " ".join(map(str, stat))

        else:
            newline = 0
            byte = 0
            word = 0
            while 1:
                try:
                    line = input()
                    byte += len(line.encode('utf-8'))
                    newline += 1
                    line = line.split(' ')
                    word += len(line)
                except EOFError:
                    print(newline, word, byte, end='\n')
                    exit()


class PWD(CommandWithArgs):
    """
        Class that implements pwd command.
    """
    def __init__(self, args: list = None):
        super().__init__('pwd', args)

    def __call__(self):
        # print(os.getcwd())
        return os.getcwd()


class Exit(CommandWithArgs):
    """
        Class that implements exit command.
    """
    def __init__(self, args: list = None):
        super().__init__('exit', args)

    def __call__(self):
        exit()


class Grep(CommandWithArgs):
    """
        Class that implements grep command.
    """
    def __init__(self, args: list = None):
        super().__init__('grep', args)
        self.keys = ['-i', '-w', '-A']

    def __call__(self):
        to_find = None
        find_in = None
        i_flag = False
        w_flag = False
        A_flag = False
        A_length = None
        prev_arg = None
        for arg in self.args:
            if arg in self.keys:
                if arg == '-i':
                    i_flag = True
                    continue
                elif arg == '-w':
                    w_flag = True
                    continue
                elif arg == '-A':
                    A_flag = True
            elif prev_arg == '-A':
                if arg.isdigit():
                    A_length = arg
                else:
                    raise TypeError('invalid context length argument')
            else:
                if not to_find:
                    to_find = arg
                elif not find_in:
                    find_in = arg
                else:
                    print(arg)
                    raise RuntimeError('only 1 pattern and 1 file supported')
            prev_arg = arg

        pattern = r'^.*' + to_find + r'.*$'
        if w_flag:
            pattern = r'.*\b' + to_find + r'\b.*'
        if i_flag:
            pattern = r'(?i)' + pattern

        file_content = None
        try:
            file = open(find_in, mode='r')
            file_content = file.read().splitlines()
            file.close()
        except FileNotFoundError:
            print(f"exception occurred while reading file {find_in}")
        result = []
        i = 0
        for line in file_content:
            line_res = re.search(pattern, line)
            if line_res:
                result.append(line_res.group(0))
                if A_flag:
                    result.extend(file_content[i + 1:i + 1 + int(A_length)])
            i += 1
        if result:
            return "\n".join(result)
        else:
            return ''








