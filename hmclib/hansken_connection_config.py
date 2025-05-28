import getpass
import sys
from dataclasses import dataclass

from hansken.connect import connect
from hansken.remote import Connection

from config import environment_config


@dataclass
class HanskenConnectionConfig:
    endpoint: str
    keystore: str
    username: str
    password: str
    verify: bool = True
    interactive: bool = True


def get_connection_details() -> HanskenConnectionConfig:
    """
    Build Hansken connection configuration using values from environment_config, or
    prompting the user interactively for any missing fields.

    :return: populated HanskenConnectionConfig object
    """
    end_point = environment_config.endpoint
    key_store = environment_config.keystore
    user_name = environment_config.username
    password = environment_config.password
    verify = environment_config.verify
    interactive = environment_config.interactive

    if not end_point:
        try:
            end_point = input('Enter Hansken end point / gate keeper: ')
        except Exception as e:
            print("Error reading end point / gate keeper details:", e)
            sys.exit(1)

    if not key_store:
        try:
            key_store = input('Enter Hansken key store: ')
        except Exception as e:
            print("Error reading key store details:", e)
            sys.exit(1)

    if not user_name:
        try:
            user_name = input('Enter user name: ')
        except Exception as e:
            print("Error reading user name:", e)
            sys.exit(1)

    if not password:
        try:
            password = getpass.getpass(prompt='Enter password: ')
        except Exception as e:
            print("Error reading password:", e)
            sys.exit(1)

    if verify is None:
        verify = True
        print(
            "⚠️  Configuration doesn't specify \033[1;33mverify\033[0m parameter for Hansken connection. Defaulting to True.")

    if interactive is None:
        interactive = True
        print(
            "⚠️  Configuration doesn't specify \033[1;33minteractive\033[0m parameter for Hansken connection. Defaulting to True.")

    return HanskenConnectionConfig(
        endpoint=end_point,
        keystore=key_store,
        username=user_name,
        password=password,
        verify=verify,
        interactive=interactive
    )


def establish_connection(cfg: HanskenConnectionConfig) -> Connection:
    """
    Establish and return Hansken connection using the provided configuration.
    Exits the program if the connection cannot be established.

    :param cfg: Hansken connection configuration object
    :return: Hansken connection object
    """
    try:
        connection = connect(endpoint=cfg.endpoint,
                             keystore=cfg.keystore,
                             username=cfg.username,
                             password=cfg.password,
                             interactive=cfg.interactive,
                             verify=cfg.verify)
        connection.open()
        connection.close()
    except Exception as e:
        print("[ERROR] ❌ Failed to open Hansken connection.")
        print(
            "\tCheck your \033[1;31muser name, password, key store, and end point / gate keeper\033[0m in config/environment_config.py or CLI input.")
        print(f"\t{e})")
        sys.exit(1)

    return connection
