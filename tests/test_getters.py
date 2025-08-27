import lambdapdk


def test_get_pdk_names():
    assert sorted([pdk.name for pdk in lambdapdk.get_pdks()]) == sorted(lambdapdk.get_pdk_names())


def test_get_lib_names():
    assert sorted([lib.name for lib in lambdapdk.get_libs()]) == sorted(lambdapdk.get_lib_names())
