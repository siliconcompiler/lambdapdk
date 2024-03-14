import siliconcompiler.package as sc_package


__version__ = "0.1.12"


def register_data_source(chip):
    sc_package.register_python_data_source(
        chip,
        "lambdapdk",
        "lambdapdk",
        "git+https://github.com/siliconcompiler/lambdapdk.git",
        alternative_ref=f"v{__version__}",
        python_module_path_append=".."
    )
