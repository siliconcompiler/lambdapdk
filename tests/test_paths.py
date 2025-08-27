import pytest

import os.path

import lambdapdk


def test_symbolic_links():
    def check(path):
        if os.path.basename(path).startswith('.'):
            return

        assert not os.path.islink(path)

    skip = []

    lambda_root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    for root, dirs, files in os.walk(lambda_root):
        if os.path.basename(root).startswith('.'):
            skip.append(root)
            continue

        if any([root.startswith(d) for d in skip]):
            continue

        for d in dirs:
            check(os.path.join(root, d))
        for f in files:
            check(os.path.join(root, f))


@pytest.mark.parametrize("pdk", lambdapdk.get_pdks())
def test_pdks(pdk):
    assert pdk.check_filepaths()


@pytest.mark.parametrize("lib", lambdapdk.get_libs())
def test_libs(lib):
    assert lib.check_filepaths()
