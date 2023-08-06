from __future__ import unicode_literals

import logging
import re

from mopidy.models import Album, Artist, Ref, Track, Image, SearchResult

logger = logging.getLogger(__name__)


def build_uri(schema, id):
    result = 'rw:%s:%s' % (schema, id)
    return result


def parse_uri(uri):
    result = re.findall(r'^rw:([a-z]+)(?::([\w=]+))?$', uri)
    if result:
        return result[0]
    return None, None


def item_to_ref(item):
    if 'uri' in item:
        uri = item['uri']
    else:
        uri = build_uri(item['schema'], item['id'])
    if item['type'] == 'track':
        return Ref.track(
            uri=uri,
            name=item['text'],
        )
    else:
        return Ref.directory(uri=uri, name=item['text'])


def station_to_tracks(station):
    results = []
    for s in station['streams']:
        results.append(Track(
            name=station['text'],
            uri=s['url']
        ))
    return results


def stations_to_search(stations):
    tracks = []
    for station in stations:
        logger.info("stations_to_search: processing {}".format(station))
        for s in station['streams']:
            tracks.append(Track(
                name=station['text'],
                uri=s['url']
            ))
    return SearchResult(
        tracks=tracks
    )


def image(uri):
    return Image(
        uri=uri
    )
