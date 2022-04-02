import configparser
import platform

HOSTNAME = platform.node()
config_machines = configparser.ConfigParser()
config_machines.read("./config/config_machines.ini")


def get_config_file():
    config = configparser.ConfigParser()
    if config_machines["MACHINES"][HOSTNAME] == "local":
        config.read("./config/config_local.ini")
    elif config_machines["MACHINES"][HOSTNAME] == "remote":
        config.read("./config/config_remote.ini")
    elif config_machines["MACHINES"][HOSTNAME] == "pi":
        config.read("./config/config_pi.ini")
    else:
        config.read("./config/config_local.ini")

    return config


def get_secrets_file():
    config = configparser.ConfigParser()
    try:
        config.read("./config/auth_lemonde.ini")
    except:
        config = {"auth": {"username": "", "password": ""}}
        print("Valid authentication file not found")
    return config
