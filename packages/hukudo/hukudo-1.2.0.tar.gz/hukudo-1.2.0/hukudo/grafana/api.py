import structlog

from .models import Dashboard
from .session import APISession

logger = structlog.get_logger()


class GrafanaError(Exception):
    pass


class DashboardWriteError(GrafanaError):
    pass


class Grafana:
    def __init__(self, url, api_key):
        self.session = APISession(url, api_key)
        self.log = logger.bind(instance=self)

    def __str__(self):
        return self.session.url

    def __repr__(self):
        return f'Grafana("{self.session.url}")'

    def health(self):
        r = self.session.get('/api/health')
        if r.status_code != 200:
            raise GrafanaError('no 200 on /api/health')
        elif r.json()['database'] != 'ok':
            raise GrafanaError('database nok')
        else:
            return True

    def dashboards(self):
        result = []
        # https://grafana.com/docs/grafana/latest/http_api/folder_dashboard_search/
        r = self.session.get('/api/search?query=&starred=false')
        r.raise_for_status()
        search_results = r.json()
        uids = [sr['uid'] for sr in search_results if sr['type'] == 'dash-db']
        for uid in uids:
            d = self.session.get(f'/api/dashboards/uid/{uid}').json()['dashboard']
            result.append(Dashboard(d))
        return result

    def post_dashboard(self, dashboard_data):
        # force overwrite by setting id = null
        # https://grafana.com/docs/grafana/latest/http_api/dashboard/#create--update-dashboard
        if 'id' in dashboard_data:
            dashboard_data['id'] = None
        uid = dashboard_data['uid']
        log = self.log.bind(uid=uid)
        body = {
            'dashboard': dashboard_data,
            'overwrite': True,
        }
        response = self.session.post('/api/dashboards/db', json=body)
        if response.status_code != 200:
            log.error(response.text, uid=uid)
            raise DashboardWriteError(uid)
        log.debug('create dashboard', uid=uid)
