import siliconcompiler.package as sc_package


__version__ = "0.1.41"


def register_data_source(chip):
    sc_package.register_python_data_source(
        chip,
        "lambdapdk",
        "lambdapdk",
        "https://github.com/siliconcompiler/lambdapdk/archive/refs/tags/",
        alternative_ref=f"v{__version__}",
        python_module_path_append=".."
    )


def setup_libs():
    '''
    Returns a list of libraries in lambdapdk
    '''

    from lambdapdk.asap7.libs import asap7sc7p5t, fakeram7, fakeio7
    from lambdapdk.freepdk45.libs import nangate45, fakeram45
    from lambdapdk.sky130.libs import sky130sc, sky130io, sky130sram
    from lambdapdk.gf180.libs import gf180mcu, gf180io, gf180sram
    from lambdapdk.ihp130.libs import sg13g2_stdcell, sg13g2_sram
    from lambdapdk.interposer.libs import bumps as interposer_bumps

    all_libs = []
    for lib_mod in [
            asap7sc7p5t, fakeram7, fakeio7,
            nangate45, fakeram45,
            sky130sc, sky130io, sky130sram,
            gf180mcu, gf180io, gf180sram,
            sg13g2_stdcell, sg13g2_sram,
            interposer_bumps]:
        libs = lib_mod.setup()
        if not isinstance(libs, (list, tuple)):
            libs = [libs]
        for lib in libs:
            all_libs.append(lib)

    return all_libs


def setup_pdks():
    '''
    Returns a list of pdks in lambdapdk
    '''

    from lambdapdk import asap7, freepdk45, sky130, gf180, ihp130, interposer

    all_pdks = []
    for pdk_mod in [asap7, freepdk45, sky130, gf180, ihp130, interposer]:
        pdks = pdk_mod.setup()
        if not isinstance(pdks, (list, tuple)):
            pdks = [pdks]
        for pdk in pdks:
            all_pdks.append(pdk)

    return all_pdks


def setup():
    '''
    Returns a list of all pdks and libraries in lambdapdk
    '''

    return [
        *setup_pdks(),
        *setup_libs()
    ]


def get_pdks():
    '''
    Returns a list of pdk names in lambdapdk
    '''

    all_pdks = []
    for pdk in setup_pdks():
        all_pdks.append(pdk.design)

    return set(all_pdks)


def get_libs():
    '''
    Returns a list of libraries names in lambdapdk
    '''

    all_libs = []
    for lib in setup_libs():
        all_libs.append(lib.design)

    return set(all_libs)
