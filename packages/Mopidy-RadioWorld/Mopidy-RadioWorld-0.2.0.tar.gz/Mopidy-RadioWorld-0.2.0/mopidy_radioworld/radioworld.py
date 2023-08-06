import requests
from time import sleep
from contextlib import closing
import logging
logger = logging.getLogger(__name__)

class RadioWorld(object):

    def __init__(self):
        self._base_uri = 'https://radioworld-api-prod.azurewebsites.net/%s'
        #self._base_uri = 'http://localhost:5000/%s'
        self._session = requests.Session()

    def root(self):
        results = [{
            'type': 'directory',
            'schema': 'rnd',
            'id': None,
            'text': 'Feeling lucky'
        }]
        countries = self._query('countries')
        if countries is not None:
            for location in sorted(countries, key=lambda loc: loc['name']):
                results.append({
                    'type': 'directory',
                    'schema': 'location',
                    'id': location['id'],
                    'text': location['name']
                })
        return results

    def rnd(self):
        station = self._query('station/rnd')
        if station is None:
            return []
        return {
            'type': 'track',
            'schema': 'station',
            'id': station['id'],
            'text': station['text']
        }

    def stations(self, id):
        stations = self._query('location/{}/stations'.format(id))
        if stations is None or stations == []:
            logger.warning("empty response from API")
            return []
        results = []
        for station in sorted(stations, key=lambda sta: sta['text']):
            results.append({
                'type': 'track',
                'schema': 'station',
                'id': station['id'],
                'text': station['text']
            })
        return results

    def station(self, id):
        station = self._query('station/%s' % id)
        if station is None:
            logger.warning("empty response from API")
        return station

    def image(self, id):
        return self._base_uri % ("station/{}/image".format(id))

    def search(self, q, location_id):
        results = []
        search = self._query("stations/search/{}".format(q)) if location_id is None else self._query("location/{}/search/{}".format(location_id, q))
        stations = search['stations']
        for station in stations:
            results.append({
                'type': 'track',
                'schema': 'station',
                'id': station['id'],
                'text': station['text']
            })
        return results

    def _query(self, path):
        uri = (self._base_uri % path)
        logger.info('RadioWorld request: %s', uri)
        try:
            while True:
                with closing(self._session.get(uri)) as r:
                    r.raise_for_status()
                    logger.debug("RadioWorld response: %s", r.status_code)
                    if r.status_code != 204:
                        return r.json()
                    else:
                        sleep(0.25)
        except Exception as e:
            logger.info('RadioWorld API request for %s failed: %s' % (path, e))
        return None
