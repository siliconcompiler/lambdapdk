import siliconcompiler.package as sc_package


__version__ = "0.1.16"


def register_data_source(chip):
    sc_package.register_python_data_source(
        chip,
        "lambdapdk",
        "lambdapdk",
        "https://github.com/siliconcompiler/lambdapdk/archive/refs/tags/",
        alternative_ref=f"v{__version__}",
        python_module_path_append=".."
    )
