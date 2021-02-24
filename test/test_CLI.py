import pytest

import src.parser
import src.expander
import src.executor
from src.commands import *


def startup_func(line: str):
    context = src.expander.Expander()
    parser = src.parser.Parser(context, line)
    to_run = parser.parse()
    return src.executor.Executor(to_run).execute()


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
    commands = ['a=5', 'b=$(echo 123)', "echo \"$a\" \"$b\" \'$c\'"]
    context = src.expander.Expander()
    for line in commands[:2]:
        parser = src.parser.Parser(context, line)
        parser.parse()

    parser = src.parser.Parser(context, commands[2])
    to_run = parser.parse()
    context.expand(to_run[0])
    result = src.executor.Executor(to_run).execute()
    assert result == "5 123 $c"


def test_cat():
    command = 'cat test/cat_test.txt'
    result = startup_func(command)
    assert result == 'this is ok'


def test_echo():
    command = 'echo 123 456 popop'
    result = startup_func(command)
    assert result == '123 456 popop'


def test_wc():
    command = 'wc test/wc_test.txt'
    result = startup_func(command)
    assert result == '8 8 61 test/wc_test.txt'


def test_pwd():
    command = 'pwd'
    result = startup_func(command)
    assert result[-3:] == "CLI"


def test_pipeline():
    command = 'echo 123 | cat'
    result = startup_func(command)
    assert result == '123'


def test_grep():
    command1 = 'grep find grep_test.txt'
    command2 = 'grep -i find grep_test.txt'
    command3 = 'grep -w -i w grep_test.txt'
    command4 = 'grep -A 1 A grep_test.txt'
    result1 = startup_func(command1)
    result2 = startup_func(command2)
    result3 = startup_func(command3)
    result4 = startup_func(command4)
    assert result1 == 'find this'
    assert result2 == 'find this\nfInD thIS'
    assert result3 == 'vau w'
    assert result4 == 'A test\nshould be found'


if __name__ == "__main__":
    pass
    # test_parser()
    # test_context()
    # test_expand()
    # test_cat()
    # test_echo()
    # test_wc()
    # test_pwd()
    # test_pipeline()
    test_grep()
