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
    assert len(result) == 1 and isinstance(result[0][0], Echo) and result[0][0].args == [5]
