def test_package_import():
    import botcity.plugins.aws.secretsmanager as plugin
    assert plugin.__file__ != ""
