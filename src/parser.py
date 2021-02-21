from src.commands import *
from src.expander import Expander
import re
import os

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
