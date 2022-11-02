'''Run examples.'''

from contextlib import redirect_stdout
import glob
import io
import os

from grafanalib import _gen


def test_examples():
    '''Run examples in ./examples directory.'''

    # Run dashboard examples
    examples_dir = os.path.join(os.path.dirname(__file__), 'examples')
    dashboards = glob.glob('{}/*.dashboard.py'.format(examples_dir))
    assert len(dashboards) == 2

    stdout = io.StringIO()
    for example in dashboards:
        with redirect_stdout(stdout):
            ret = _gen.generate_dashboard([example])
            assert ret == 0
        assert stdout.getvalue() != ''

    # Run alertgroup example
    alerts = glob.glob('{}/*.alertgroup.py'.format(examples_dir))
    assert len(alerts) == 2

    stdout = io.StringIO()
    for example in alerts:
        with redirect_stdout(stdout):
            ret = _gen.generate_alertgroup([example])
            assert ret == 0
        assert stdout.getvalue() != ''

    # Run file based provisioning of alerts example
    alerts = glob.glob('{}/*.alertfilebasedprovisioning.py'.format(examples_dir))
    assert len(alerts) == 1

    stdout = io.StringIO()
    for example in alerts:
        with redirect_stdout(stdout):
            ret = _gen.generate_alertgroup([example])
            assert ret == 0
        assert stdout.getvalue() != ''
