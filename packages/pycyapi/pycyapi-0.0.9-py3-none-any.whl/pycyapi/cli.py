import click

import pycyapi.commands as commands


@click.group()
def cli():
    pass


@cli.command()
@click.option('--username', required=True, type=str)
@click.option('--password', required=True, type=str)
def token(username, password):
    click.echo(commands.cas_token(username=username, password=password))


@cli.command()
@click.argument('username')
@click.option('--token', '-t', required=False, type=str)
def user(username, token):
    click.echo(commands.user_info(username=username, token=token))


@cli.command()
@click.argument('remote_path')
@click.option('--token', '-t', required=False, type=str)
def list(remote_path, token):
    click.echo(commands.paged_directory(path=remote_path, token=token))


@cli.command()
@click.argument('remote_path')
@click.option('--token', '-t', required=False, type=str)
def stat(remote_path, token):
    click.echo(commands.stat(path=remote_path, token=token))


@cli.command()
@click.argument('remote_path')
@click.option('--type', required=False, type=str)
@click.option('--token', '-t', required=False, type=str)
def exists(remote_path, type, token):
    click.echo(commands.exists(path=remote_path, type=type, token=token))


@cli.command()
@click.argument('remote_path')
@click.option('--token', '-t', required=False, type=str)
def create(remote_path, token):
    click.echo(commands.create(path=remote_path, token=token))


@cli.command()
@click.argument('remote_path')
@click.option('--local_path', '-p', required=False, type=str)
@click.option('--include_pattern', '-ip', required=False, type=str, multiple=True)
@click.option('--force', '-f', required=False, type=str, multiple=True)
@click.option('--token', '-t', required=False, type=str)
def download(
        remote_path,
        local_path,
        include_pattern,
        force,
        token):
    commands.download(
        remote_path=remote_path,
        local_path=local_path,
        patterns=include_pattern,
        force=force,
        token=token)
    click.echo(f"Downloaded {remote_path} to {local_path}")


@cli.command()
@click.argument('remote_path')
@click.option('--local_path', '-p', required=False, type=str)
@click.option('--include_pattern', '-ip', required=False, type=str, multiple=True)
@click.option('--include_name', '-in', required=False, type=str, multiple=True)
@click.option('--exclude_pattern', '-ep', required=False, type=str, multiple=True)
@click.option('--exclude_name', '-en', required=False, type=str, multiple=True)
@click.option('--token', '-t', required=False, type=str)
def upload(remote_path,
           local_path,
           include_pattern,
           include_name,
           exclude_pattern,
           exclude_name,
           token):
    commands.upload(
        local_path=local_path,
        remote_path=remote_path,
        include_patterns=include_pattern,
        include_names=include_name,
        exclude_patterns=exclude_pattern,
        exclude_names=exclude_name,
        token=token)
    click.echo(f"Uploaded {local_path} to {remote_path}")


@cli.command()
@click.argument('remote_path')
@click.option('--username', '-u', required=True, type=str)
@click.option('--permission', '-p', required=True, type=str)
@click.option('--token', '-t', required=False, type=str)
def share(remote_path, username, permission, token):
    commands.share(username=username, path=remote_path, permission=permission, token=token)
    click.echo(f"Shared {remote_path} with {username}")


@cli.command()
@click.argument('remote_path')
@click.option('--username', '-u', required=True, type=str, multiple=True)
@click.option('--token', '-t', required=False, type=str)
def unshare(remote_path, username, token):
    commands.unshare(username=username, path=remote_path, token=token)
    click.echo(f"Unshared {remote_path} with {username}")


@cli.command()
@click.argument('id')
@click.option('--attribute', '-a', required=False, type=str, multiple=True)
@click.option('--irods_attribute', '-ia', required=False, type=str, multiple=True)
@click.option('--token', '-t', required=False, type=str)
def tag(id, attribute, irods_attribute, token):
    commands.tag(id=id, attributes=attribute, irods_attributes=irods_attribute, token=token)
    newline = '\n'
    click.echo(f"Tagged data object with ID {id}:\nRegular:\n{newline.join(attribute)}\niRODS:\n{newline.join(irods_attribute)}")


@cli.command()
@click.argument('id')
@click.option('--token', '-t', required=False, type=str)
@click.option('--irods', '-i', required=False, default=False, type=bool)
def tags(id, irods, token):
    attributes = commands.tags(id=id, irods=irods, token=token)
    newline = '\n'
    click.echo(newline.join(attributes))
