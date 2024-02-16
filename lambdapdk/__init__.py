import os
__version__ = "0.1.8"


def register_data_source(chip):
    # check if local
    root_path = os.path.dirname(os.path.dirname(__file__))
    test_path = os.path.join(root_path, 'lambdapdk', 'asap7', 'base', 'apr', 'asap7_tech.lef')
    if os.path.exists(test_path):
        path = root_path
        ref = None
    else:
        path = 'git+https://github.com/siliconcompiler/lambdapdk.git'
        ref = f'v{__version__}'

    chip.register_package_source(name='lambdapdk',
                                 path=path,
                                 ref=ref)
