"""Type validation for h2oai_client."""


def validate_toml(value, name):
    # We don't want to depend on toml so we validate it only on the server.
    pass
