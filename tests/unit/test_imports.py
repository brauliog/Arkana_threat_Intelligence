def test_config_import_smoke():
    from arkana.config import settings

    assert settings is not None
    assert hasattr(settings, "database_url")