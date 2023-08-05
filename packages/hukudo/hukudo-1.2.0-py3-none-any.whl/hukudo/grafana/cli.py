import json
import os
from pathlib import Path

import click
import structlog

from hukudo.grafana import Grafana
from hukudo.grafana.api import DashboardWriteError

logger = structlog.get_logger()


@click.group()
@click.option('-c', '--config', type=click.Path())
@click.pass_context
def grafana(ctx, config):
    if config:
        import dotenv

        os.environ.update(dotenv.dotenv_values(config))
    ctx.obj = Grafana(
        url=os.environ['GRAFANA_URL'],
        api_key=os.environ['GRAFANA_API_KEY'],
    )
    log = logger.bind(instance=ctx.obj)
    log.info('instantiated')

    try:
        root_ca = os.environ['GRAFANA_CLIENT_ROOT_CA']
        log.debug('CA', path=root_ca)
        ctx.obj.session.verify = root_ca
    except KeyError:
        pass

    try:
        crt = os.environ['GRAFANA_CLIENT_CRT']
        key = os.environ['GRAFANA_CLIENT_KEY']
        log.debug('client cert', crt=crt, key=key)
        ctx.obj.session.cert = (crt, key)
    except KeyError:
        pass


@grafana.command()
@click.pass_context
def health(ctx):
    grafana: Grafana = ctx.obj
    if grafana.health():
        logger.info('health OK', instance=grafana)


@grafana.group()
def dashboards():
    pass


@dashboards.command()
@click.argument('target_dir', type=click.Path())
@click.pass_context
def export(ctx, target_dir):
    """
    Exports dashboards as json files to a directory named after the Grafana domain.
    """
    log = logger.bind(instance=ctx.obj)
    log.info('export')

    grafana: Grafana = ctx.obj
    target = Path(target_dir)

    for board in grafana.dashboards():
        filename = target / f'{board.id}.json'
        board.export(filename)


@dashboards.command(name='import')
@click.argument('paths', type=click.Path(), nargs=-1)
@click.pass_context
def import_(ctx, paths):
    """
    Import dashboards.
    """
    grafana: Grafana = ctx.obj

    exit_code = 0
    for path in paths:
        path = Path(path)
        with path.open() as f:
            data = json.load(f)
        try:
            grafana.post_dashboard(data)
        except DashboardWriteError:
            exit_code = 1
    return exit_code
