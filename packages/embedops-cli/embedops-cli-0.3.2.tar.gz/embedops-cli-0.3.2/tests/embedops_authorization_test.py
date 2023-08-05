"""
`embedops_authorization_test`
=======================================================================
Unit tests for the authorization retrival and storage for EmbedOps 
* Author(s): Bailey Steinfadt
"""

import os
import pytest
import docker

from embedops_cli import embedops_authorization
from embedops_cli.eo_types import UnauthorizedUserException, LoginFailureException


def test_set_and_get_auth_token():
    """testing setting token"""
    test_secret = "SUPER_DUPER_SECRET_TOKEN_SAUCE"
    test_secret_file = ".test_eosecrets.toml"

    embedops_authorization.set_auth_token(test_secret, test_secret_file)
    retrieved_secret = embedops_authorization.get_auth_token(test_secret_file)

    assert test_secret == retrieved_secret

    os.remove(test_secret_file)


def test_set_and_get_registry_token():
    """testing setting token"""
    test_secret = "YULE NEFFER GESS WOT"
    test_secret_file = ".test_eosecrets.toml"

    embedops_authorization.set_registry_token(test_secret, test_secret_file)
    retrieved_secret = embedops_authorization.get_registry_token(test_secret_file)

    assert test_secret == retrieved_secret

    os.remove(test_secret_file)


def test_setting_both_tokens():
    """Test that both the registry token and auth token can be read and written together"""

    auth_secret = "SUPER_DUPER_SECRET_TOKN_SAUCE"
    other_auth_secret = "THIS IS THE GOOD ONE"
    registry_secret = "YULE NEFFER GESS WOT"

    test_secret_file = ".test_eosecrets.toml"

    embedops_authorization.set_auth_token(auth_secret, test_secret_file)
    embedops_authorization.set_registry_token(registry_secret, test_secret_file)

    read_auth_token = embedops_authorization.get_auth_token(test_secret_file)
    read_registry_token = embedops_authorization.get_registry_token(test_secret_file)

    assert auth_secret == read_auth_token
    assert registry_secret == read_registry_token

    embedops_authorization.set_auth_token(other_auth_secret, test_secret_file)
    read_auth_token = embedops_authorization.get_auth_token(test_secret_file)
    read_registry_token = embedops_authorization.get_registry_token(test_secret_file)

    assert other_auth_secret == read_auth_token
    assert registry_secret == read_registry_token

    os.remove(test_secret_file)


def test_login_to_registry_no_registry_credentials_fails_login(mocker):
    """Test that the function handles non-existent creds correctly"""

    mock_docker_client = mocker.patch(
        "embedops_cli.embedops_authorization.docker.from_env"
    )
    mock_docker_client().login.side_effect = docker.errors.APIError("'sup")

    with pytest.raises(UnauthorizedUserException) as pytest_wrapped_e:
        embedops_authorization.login_to_registry("non-existent-secrets.toml")

    assert pytest_wrapped_e.type == UnauthorizedUserException
    mock_docker_client().login.assert_not_called()


def test_login_to_registry_incorrect_registry_credentials_fails_login(mocker):
    """Test that the function handles invalid credentials correctly"""

    mock_get_registry_token = mocker.patch(
        "embedops_cli.embedops_authorization.get_registry_token"
    )
    mock_get_registry_token().return_value = "BAD_TOKEN_BAD"
    mock_docker_client = mocker.patch(
        "embedops_cli.embedops_authorization.docker.from_env"
    )
    mock_docker_client().login.side_effect = docker.errors.APIError("'sup")

    with pytest.raises(LoginFailureException) as pytest_wrapped_e:
        embedops_authorization.login_to_registry()

    assert pytest_wrapped_e.type == LoginFailureException


def test_login_to_registry(mocker):
    """Test that the function handles a successful login correctly"""
    mock_get_registry_token = mocker.patch(
        "embedops_cli.embedops_authorization.get_registry_token"
    )
    mock_get_registry_token().return_value = "MAGIC_GOOD_TOKEN"
    mock_docker_client = mocker.patch(
        "embedops_cli.embedops_authorization.docker.from_env"
    )
    mock_docker_client().login.return_value = {
        "IdentityToken": "",
        "Status": "Login Succeeded",
    }

    embedops_authorization.login_to_registry()

    mock_get_registry_token.assert_called()
    mock_docker_client().login.assert_called()
