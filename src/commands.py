import os


class Command:
    def __init__(self, name: str):
        self.name = name

    def __call__(self):
        pass


class CommandWithArgs(Command):
    def __init__(self, name: str, args: list):
        super().__init__(name)
        self.args = args
        self.input = None

    def __call__(self):
        pass


class Cat(CommandWithArgs):
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
    def __init__(self, args: list = None):
        super().__init__('pwd', args)

    def __call__(self):
        # print(os.getcwd())
        return os.getcwd()


class Exit(CommandWithArgs):
    def __init__(self, args: list = None):
        super().__init__('exit', args)

    def __call__(self):
        exit()
