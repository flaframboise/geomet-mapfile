import logging

import click
import mappyfile

from geomet3_mapfile.env import STORE_TYPE, STORE_URL
from geomet3_mapfile.plugin import load_plugin
from geomet3_mapfile.store.base import StoreError

LOGGER = logging.getLogger(__name__)


@click.group()
def store():
    """Manage the geomet3-mapfile store"""
    pass


@click.command()
@click.pass_context
@click.option('--group', '-g', help='group')
def setup(ctx, group=None):
    """create store"""

    provider_def = {
        'type': STORE_TYPE,
        'url': STORE_URL,
        'group': group
    }

    st = load_plugin('store', provider_def)

    try:
        click.echo('Creating store {}'.format(st.url))
        st.setup()
    except StoreError as err:
        raise click.ClickException(err)
    click.echo('Done')


@click.command()
@click.pass_context
@click.option('--group', '-g', help='group')
def teardown(ctx, group=None):
    """delete store"""

    provider_def = {
        'type': STORE_TYPE,
        'url': STORE_URL,
        'group': group
    }

    st = load_plugin('store', provider_def)

    try:
        click.echo('Deleting store {}'.format(st.url))
        st.teardown()
    except StoreError as err:
        raise click.ClickException(err)
    click.echo('Done')


@click.command('set')
@click.pass_context
@click.option('--key', '-k', help='key name for store')
@click.option('--mapfile', '-m', 'mapfile',
              type=click.Path(exists=True, resolve_path=True),
              help='Path to mapfile')
def set_key(ctx, key, mapfile):
    """populate store"""

    if all([key is None, mapfile is None]):
        raise click.ClickException('Missing --key/-k or --mapfile/-m option')

    provider_def = {
        'type': STORE_TYPE,
        'url': STORE_URL
    }

    st = load_plugin('store', provider_def)

    try:
        click.echo('Setting {} key in store ({}).'.format(key, st.url))
        st.set_key(key, mapfile)
    except StoreError as err:
        raise click.ClickException(err)
    click.echo('Done')


@click.command('get')
@click.pass_context
@click.option('--key', '-k', help='key name to retrieve from store')
def get_key(ctx, key):
    """get key from store"""

    if all([key is None]):
        raise click.ClickException('Missing --key/-k')

    provider_def = {
        'type': STORE_TYPE,
        'url': STORE_URL
    }

    st = load_plugin('store', provider_def)

    try:
        click.echo('Getting {} key from store ({}).'.format(key, st.url))
        retrived_key = st.get_key(key)
        if retrived_key:
            click.echo('{}'.format(retrived_key.decode('utf-8')))

    except StoreError as err:
        raise click.ClickException(err)
    click.echo('Done')


store.add_command(setup)
store.add_command(teardown)
store.add_command(set_key)
store.add_command(get_key)
