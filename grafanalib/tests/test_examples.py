'''Run examples.'''

from contextlib import redirect_stdout
import glob
import io
import os

from grafanalib import _gen


def test_examples():
    '''Run examples in ./examples directory.'''

    examples_dir = os.path.join(os.path.dirname(__file__), 'examples')
    examples = glob.glob('{}/*.dashboard.py'.format(examples_dir))
    assert len(examples) == 2

    stdout = io.StringIO()
    for example in examples:
        with redirect_stdout(stdout):
            ret = _gen.generate_dashboard([example])
            assert ret == 0
        assert stdout.getvalue() != ''
