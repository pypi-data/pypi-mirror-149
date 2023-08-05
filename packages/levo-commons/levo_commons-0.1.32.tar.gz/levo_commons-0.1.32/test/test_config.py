from levo_commons.config import AuthConfig, PlanConfig


def test_default_config():
    config = PlanConfig(
        target_url="http://localhost",
        headers={"myheader": "myvalue"},
        auth_config=AuthConfig(auth_type="basic", username="test", password="test"),
    )
    assert len(config.headers) == 1
    assert config.asdict() == {
        "target_url": "http://localhost",
        "spec_path": None,
        "test_plan_path": None,
        "auth": None,
        "auth_type": None,
        "report_to_saas": True,
        "env_file_path": None,
        "headers": {"myheader": "myvalue"},
        "auth_config": {
            "auth_type": "basic",
            "username": "test",
            "password": "test",
            "api_key": None,
            "token": None,
        },
        "module_providers": {},
        "runner_log_handler": None,
        "test_case_log_handler": None,
        "ignore_ssl_verify": False,
    }


def test_config_with_overrides():
    config = PlanConfig(
        target_url="http://localhost:8080",
        spec_path="/my/local/path",
        headers={},
        auth_config=None,
        report_to_saas=False,
        ignore_ssl_verify=True,
    )
    assert len(config.headers) == 0
    assert config.asdict() == {
        "target_url": "http://localhost:8080",
        "spec_path": "/my/local/path",
        "test_plan_path": None,
        "auth": None,
        "auth_type": None,
        "report_to_saas": False,
        "env_file_path": None,
        "headers": {},
        "auth_config": None,
        "module_providers": {},
        "runner_log_handler": None,
        "test_case_log_handler": None,
        "ignore_ssl_verify": True,
    }
