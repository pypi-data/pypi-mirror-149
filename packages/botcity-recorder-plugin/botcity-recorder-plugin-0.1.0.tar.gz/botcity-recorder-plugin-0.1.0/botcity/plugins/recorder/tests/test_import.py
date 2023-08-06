def test_package_import():
    import botcity.plugins.recorder as plugin
    assert plugin.__file__ != ""
