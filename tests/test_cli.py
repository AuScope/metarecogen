import os
import sys
import subprocess
import pytest

# Add in path to source scripts
src_path = os.path.join(os.path.abspath(os.pardir), 'src')
sys.path.insert(0, src_path)

from process import main

# Basic command line parameter testing
@pytest.mark.parametrize("cli_params, expected_out",
         [(["--help"], "usage:"),
             (["-r", "dfdfdfdfd"], "ERROR: Cannot find dfdfdfdfd in config"),
         ])
def test_eval(capsys, cli_params, expected_out):
    with pytest.raises(SystemExit):
        main(["process.py"] + cli_params)
    captured = capsys.readouterr()
    assert expected_out in captured.out
