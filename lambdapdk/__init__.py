import siliconcompiler.package as sc_package


__version__ = "0.1.29"


def register_data_source(chip):
    sc_package.register_python_data_source(
        chip,
        "lambdapdk",
        "lambdapdk",
        "https://github.com/siliconcompiler/lambdapdk/archive/refs/tags/",
        alternative_ref=f"v{__version__}",
        python_module_path_append=".."
    )


def get_pdks():
    '''
    Returns a list of pdk names in lambdapdk
    '''

    from lambdapdk import asap7, freepdk45, sky130, gf180

    all_pdks = []
    for pdk_mod in [asap7, freepdk45, sky130, gf180]:
        pdks = pdk_mod.setup()
        if not isinstance(pdks, (list, tuple)):
            pdks = [pdks]
        for pdk in pdks:
            all_pdks.append(pdk.design)

    return set(all_pdks)


def get_libs():
    '''
    Returns a list of libraries names in lambdapdk
    '''

    from lambdapdk.asap7.libs import asap7sc7p5t, fakeram7
    from lambdapdk.freepdk45.libs import nangate45, fakeram45
    from lambdapdk.sky130.libs import sky130sc, sky130io, sky130sram
    from lambdapdk.gf180.libs import gf180mcu, gf180io, gf180sram

    all_libs = []
    for lib_mod in [
            asap7sc7p5t, fakeram7,
            nangate45, fakeram45,
            sky130sc, sky130io, sky130sram,
            gf180mcu, gf180io, gf180sram]:
        libs = lib_mod.setup()
        if not isinstance(libs, (list, tuple)):
            libs = [libs]
        for lib in libs:
            all_libs.append(lib.design)

    return set(all_libs)
