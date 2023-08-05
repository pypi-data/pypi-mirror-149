from getpass import getpass

import click

from . import core, meta


# Root CLI handler
@click.group()
@click.version_option(meta.version)
def cli():
    """ Command line interface for Huawei LTE routers """


# Device commands
@cli.group()
def device():
    """ Device commands """
    pass


@device.command('reboot')
def device_reboot():
    """ Reboot the router without any confirmation prompts """
    try:
        core.reboot_router()
    except Exception as e:
        click.echo('Execution failed, reason: "{}"'.format(e))
    else:
        click.echo('Rebooting the device, router will restart in several moments')


# Auth control
@cli.group()
def auth():
    """ Router authentification """
    pass


@auth.command('login')
def auth_login():
    """ Safely configure all authentification related details for further interactions """
    print('Authentification Configurator\n')
    con_ip = input(
        '(leave empty to use "{}")\n'
        'Full address to router: '
        .format(core.LOCAL_CONFIG_DEFAULT['connection_address'])
    )
    uname = input('Username: ')
    passwd = getpass('Password: ')

    auth_cfg = core.AuthConfig()
    auth_cfg.username = uname
    auth_cfg.password = passwd
    auth_cfg.connection_address = con_ip if len(con_ip) > 0 else \
        core.LOCAL_CONFIG_DEFAULT['connection_address']

    auth_cfg.commit()

    print("\nAuthentification details successfully specified")


@auth.command('logout')
def auth_logout():
    """ Remove all authentification details """
    core.AuthConfig().reset()
    core.AuthConfig().commit()
    print("All authentification details removed")


@auth.command('test')
def auth_test_connection():
    """ Test connection to router with current auth details """
    test_result = core.test_connection()
    if test_result == 'ok':
        click.echo('Successful Authentification')
    else:
        click.echo('Auth failed, reason: "{}"'.format(test_result))


# SMS commands
@cli.group()
def sms():
    """ SMS commands """
    pass


@sms.command('send')
@click.option('-n', '--number', default='', help='Number that message will be sent to')
@click.option('-t', '--text', default='', help='Text of the message to be sent')
def sms_send(number: str, text: str):
    if len(number) == 0:
        number = input('Number: ')
    if len(text) == 0:
        text = input('Text: ')

    try:
        send_status = core.sms_send(number, text)
        if send_status.lower() == 'ok':
            click.echo('SMS sent successfully to {}'.format(number))
        else:
            click.echo('SMS was not sent, reason: "{}"'.format(send_status))
    except Exception as e:
        click.echo('Execution failed, reason: "{}"'.format(e))


@cli.group()
def config():
    """ CLI configuration """


@config.command('init')
def config_init():
    """
    Initialize local configuration file

    File will only be generated if no configuration file already exists
    on default path.
    """
    cfg = core.LocalConfig(auto_file_creation=False)

    if not cfg.file_exists():
        if cfg.create_file():
            click.echo('Configuration file successfully generated at "{}"'
                       .format(core.LOCAL_CONFIG_PATH)
                       )
        else:
            click.echo('Can not generate configuration file at "{}"'
                       .format(core.LOCAL_CONFIG_PATH)
                       )
    else:
        click.echo('Configuration file already exists on path: "{}"'
                   .format(core.LOCAL_CONFIG_PATH)
                   )


@config.command('remove')
def config_remove():
    """ Erase local configuration """

    if core.LocalConfig.erase_config() is True:
        click.echo("All local configuration files and dirs successfully erased")
    else:
        click.echo("No local configuration files detected")


@config.command('path')
def config_get_path():
    """
    Path to local configuration file

    Note that this command will show the hardcoded path to config file, so it
    doesn't mean that this file actually exists at the time the command is
    called
    """
    click.echo(core.LOCAL_CONFIG_PATH)


@config.command('exist')
def config_exist():
    """ Check does the local configuration file exists """
    if core.LOCAL_CONFIG_PATH.exists() is True:
        click.echo("Configuration file do exist")
    else:
        click.echo("Configuration file doesn't exist")


if __name__ == '__main__':
    cli()
