import pytest

import src.parser
import src.expander
import src.executor
from src.commands import *


def test_parser():
    input_line = 'echo 5'
    context = src.expander.Expander()
    parser = src.parser.Parser(context, input_line)
    result = parser.parse()
    assert len(result) == 1
    assert isinstance(result[0], Echo)
    assert result[0].args == ['5']


def test_context():
    input_line = 't=5'
    context = src.expander.Expander()
    parser = src.parser.Parser(context, input_line)
    parser.parse()
    assert context.context['t'].args == ['5']


def test_expand():
    commands = ['a=5', 'b=$(echo 123)', 'echo "$a" "$b"']
    context = src.expander.Expander()
    for line in commands[:2]:
        parser = src.parser.Parser(context, line)
        parser.parse()

    print(context.context)
    parser = src.parser.Parser(context, commands[2])
    to_run = parser.parse()
    print(to_run)
    print(to_run[0].args)
    context.expand(to_run[0])
    print(to_run[0].args)
    result = src.executor.Executor(to_run).execute()
    assert result == '5 123'


if __name__ == "__main__":
    test_parser()
    test_context()
    test_expand()