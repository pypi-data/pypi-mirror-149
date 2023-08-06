from __future__ import unicode_literals

from mopidy import backend, exceptions, httpclient
from mopidy.models import Ref, SearchResult
from mopidy_radioworld import translator, radioworld

import pykka

import logging
logger = logging.getLogger(__name__)

class RadioWorldBackend(pykka.ThreadingActor, backend.Backend):
    uri_schemes = ['rw']

    def __init__(self, config, audio):
        super(RadioWorldBackend, self).__init__()
        self.radioworld = radioworld.RadioWorld()
        self.library = RadioWorldLibrary(self)
        self.playback = RadioWorldPlayback(audio=audio, backend=self)

class RadioWorldLibrary(backend.LibraryProvider):
    root_directory = Ref.directory(uri='rw:root', name='RadioWorld.live')

    def __init__(self, _backend):
        super(RadioWorldLibrary, self).__init__(_backend)

    def browse(self, uri):
        result = []
        schema, id = translator.parse_uri(uri)
        logger.info("Browsing {}, schema={}, id={}".format(uri, schema, id))

        if schema == "root":
            for item in self.backend.radioworld.root():
                result.append(translator.item_to_ref(item))
        elif schema == "rnd":
            item = self.backend.radioworld.rnd()
            ref = translator.item_to_ref(item)
            result.append(ref)
        elif schema == "location":
            stations = self.backend.radioworld.stations(id)
            if stations is None or stations == []:
                logger.warning("No results for location {}".format(id))
                return result
            for station in stations:
                result.append(translator.item_to_ref(station))
        else:
            logger.debug('Unknown URI: %s', uri)
        return result

    def lookup(self, uri):
        schema, id = translator.parse_uri(uri)
        logger.info("Lookup {}, schema={}, id={}".format(uri, schema, id))
        if schema != 'station':
            logger.warning("Unknown schema: {}".format(schema))
            return []
        station = self.backend.radioworld.station(id)
        if not station:
            return []
        return translator.station_to_tracks(station)

    def get_images(self, uris):
        logger.warning("get_images: {}".format(uris))
        results = {}
        for uri in uris:
            schema, id = translator.parse_uri(uri)
            if schema == "station":
                results[uri] = [translator.image(self.backend.radioworld.image(id))]
        return results

    def search(self, query=None, uris=None, exact=False):
        logger.warning("RadioWorldLibrary.search: {} {} {}".format(query, uris, exact))
        schema, id = translator.parse_uri(uris[0])
        q = query['any'][0]
        loc = None
        if schema == 'location':
            loc = id
        stations = self.backend.radioworld.search(q, loc)
        station_results = []
        for station in stations:
            sta = self.backend.radioworld.station(station['id'])
            station_results.append(sta)
        return translator.stations_to_search(station_results)


class RadioWorldPlayback(backend.PlaybackProvider):

    def translate_uri(self, uri):
        logger.debug("RadioWorldPlayback.translate_uri: {}".format(uri))
        schema, id = translator.parse_uri(uri)
        station = self.backend.radioworld.station(id)
        if not station:
            return None
        stream_uris = station['obj'].streams
        while stream_uris:
            uri = stream_uris.pop(0)
            return uri
        logger.debug('RadioWorld lookup failed.')
        return None