import click
import sys

from stoobly_agent.app.settings import Settings

from .helpers.report_facade import ReportFacade
from .helpers.tabulate_print_service import tabulate_print
from .helpers.validations import *

@click.group(
    epilog="Run 'stoobly-agent report COMMAND --help' for more information on a command.",
    help="Manage test reports"
)
@click.pass_context
def report(ctx):
    pass

@report.command(
    help="Create a report"
)
@click.option('--description', help='Report description.')
@click.option('--project-key', help='Project to create report in.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=True, help='Disable printing column headers.')
@click.argument('name')
def create(**kwargs):
    settings = Settings.instance()
    project_key = resolve_project_key_and_validate(kwargs, settings)

    if not project_key:
        project_key = settings.proxy.intercept.project_key

    report = ReportFacade(settings)
    res = report.create(project_key, kwargs['name'], kwargs['description'])

    tabulate_print(
        [res], 
        filter=['created_at', 'user_id', 'starred', 'updated_at'], 
        headers=not kwargs.get('without_headers'),
        select=kwargs.get('select')
    )

@report.command(
    help="Show created reports"
)
@click.option('--page', default=0)
@click.option('--project-key', help='Project to create scenario in.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--size', default=10)
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
def list(**kwargs):
    without_headers = kwargs['without_headers']
    del kwargs['without_headers']

    settings = Settings.instance()
    project_key = resolve_project_key_and_validate(kwargs, settings)
    del kwargs['project_key']

    report = ReportFacade(Settings.instance())
    reports_response = report.index(project_key, kwargs)

    if len(reports_response['list']) == 0:
        print('No reports found.', file=sys.stderr)
    else:
        tabulate_print(
            reports_response['list'], 
            filter=['created_at', 'priority', 'user_id', 'starred', 'updated_at'],
            headers=not without_headers,
            select=kwargs.get('select')
        )