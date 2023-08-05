import os.path
import re
import sys
from typing import List, Any

import click
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from station.clients.central.central_client import CentralApiClient

from station.ctl.config.validators import ConfigItemValidationResult, ConfigItemValidationStatus
from station.ctl.config.generators import generate_private_key
from station.ctl.constants import Icons, PHTDirectories, CERTS_REGEX
from station.ctl.install.certs import generate_certificates


def fix_config(ctx: dict, config: dict, results: List[ConfigItemValidationResult]) -> dict:
    """
    Allows for interactive fixes of issues in the station configuration
    Args:
        config: initial dictionary containing the config in the config yaml file
        results: validation results of the given dictionary

    Returns:

    """
    strict = config["environment"] != "development"
    fixed_config = config.copy()
    for result in results:
        if result.status != ConfigItemValidationStatus.VALID:
            if result.display_field == "central.private_key":
                fixed_config["central"]["private_key"] = _fix_private_key(fixed_config)

            # certs are missing completely
            elif result.display_field == "https.certs":
                install_dir = ctx.get("install_dir", os.getcwd())
                _fix_certs(fixed_config, strict, install_dir)

            # invalid certs
            elif re.match(CERTS_REGEX, result.display_field):
                index = int(re.match(CERTS_REGEX, result.display_field).group(1))
                _fix_certs_path(fixed_config, index)


            else:
                default = ""
                if result.generator:
                    default = result.generator()

                value = click.prompt(f'{result.display_field} is missing. {result.fix_hint}', default=default)
                if value:
                    _set_config_values(fixed_config, result.display_field, value)
                else:
                    _set_config_values(fixed_config, result.display_field, None)
    return fixed_config


def _fix_certs(config: dict, strict: bool, install_dir: str):
    if strict:
        click.echo("Valid certificates are required when not in development mode", err=True)
        sys.exit(1)

    domain = config["https"]["domain"]
    click.echo(f"Generating certificates for domain {domain}...")

    cert_dir = os.path.join(install_dir, PHTDirectories.CERTS_DIR.value)
    cert_path = os.path.join(cert_dir, "cert.pem")
    key_path = os.path.join(cert_dir, "key.pem")
    generate_certificates(domain, cert_path=str(cert_path), key_path=str(key_path))
    click.echo(f"Certificates generated at {cert_dir}")

    cert_list = config["https"].get("certs", [])
    if not cert_list:
        print(cert_list)
        cert_list = []
    cert_paths = {
        "cert": str(cert_path),
        "key": str(key_path)
    }
    cert_list.append(cert_paths)
    config["https"]["certs"] = cert_list


def _fix_certs_path(config: dict, index: int):
    cert_path = config["https"]["certs"][index]["cert"]
    key_path = config["https"]["certs"][index]["key"]
    if not os.path.isfile(cert_path):
        cert_path = click.prompt(f"Certificate at {cert_path} does not exist. "
                                 f"Please enter the correct path to the certificate file")
        if not os.path.isfile(cert_path):
            click.echo("Certificate path is invalid", err=True)
        cert_path = str(os.path.abspath(cert_path))
    if not os.path.isfile(key_path):
        key_path = click.prompt(f"Key at {key_path} does not exist. "
                                f"Please enter the correct path to the key file")
        if not os.path.isfile(key_path):
            click.echo("Key path is invalid", err=True)
        key_path = str(os.path.abspath(key_path))

    config["https"]["certs"][index]["cert"] = cert_path
    config["https"]["certs"][index]["key"] = key_path


def _fix_private_key(config: dict) -> str:
    path = click.prompt("Private key is missing enter the path to the private key "
                        "file or press enter to generate a new one", default="GENERATE")
    if path and path != "GENERATE":
        if not os.path.isfile(path):
            raise click.BadParameter(f"{path} is not a file")
        else:
            return path

    name = click.prompt('Name your private key file')
    passphrase = click.prompt('Enter your passphrase. If given, it will be used to encrypt the private key', default="")
    private_key_path, private_key, public_key = generate_private_key(name, passphrase)
    private_key_abs_path = os.path.abspath(private_key_path)
    if not os.path.exists(private_key_path):
        click.echo(f'Private key file {private_key_abs_path} was not created. Please check the permissions.')
        return None
    else:
        click.echo(f'New private key created: {private_key_abs_path}. Submitting public key to central API...',
                   nl=False)
        _submit_public_key(config, public_key)
        click.echo(Icons.CHECKMARK.value)

    return private_key_abs_path


def _set_config_values(config: dict, field: str, value: Any):
    nested_fields = field.split(".")
    if len(nested_fields) == 1:
        config[field] = value
    else:
        sub_config = None
        for field in nested_fields[:-1]:
            sub_config = config.get(field, {})
        sub_config[nested_fields[-1]] = value


def _submit_public_key(config: dict, public_key: rsa.RSAPublicKey):
    client = CentralApiClient(
        config["central"]["api_url"],
        robot_id=config["central"]["robot_id"],
        robot_secret=config["central"]["robot_secret"]
    )

    hex_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).hex()
    r = client.update_public_key(config["station_id"], hex_key)
