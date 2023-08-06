def test_package_import():
    import botcity.plugins.files as plugin
    assert plugin.__file__ != ""
