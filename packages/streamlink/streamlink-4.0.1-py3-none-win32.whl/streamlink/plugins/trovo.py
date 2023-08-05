"""
$description Global video game live streaming and video hosting platform, owned by Tencent.
$url trovo.live
$type live, vod
"""

import logging
import random
import re

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream
from streamlink.utils.url import update_scheme

log = logging.getLogger(__name__)


@pluginmatcher(re.compile(r"""
        https?://(?:www\.)?trovo\.live/
        (?:
            (?:
                (?:clip|video)/(?P<video_id>[^/?&]+)
            )
            |
            (?P<user>[^/?&]+)
        )
""", re.VERBOSE))
class Trovo(Plugin):
    @staticmethod
    def generate_qid():
        return f"{random.getrandbits(40):010x}".upper()

    def get_vod(self, video_id):
        json = self.session.http.post(
            f"https://gql.trovo.live/?qid={self.generate_qid()}",
            json=[{
                "operationName": "batchGetVodDetailInfo",
                "variables": {
                    "params": {
                        "vids": [video_id],
                    },
                },
                "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "ceae0355d66476e21a1dd8e8af9f68de95b4019da2cda8b177c9a2255dad31d0",
                    },
                },
            }],
            schema=validate.Schema(
                validate.parse_json(),
                [{
                    "data": {
                        "batchGetVodDetailInfo": {
                            "VodDetailInfos": validate.any(
                                {
                                    video_id: {
                                        "streamerInfo": {
                                            "userName": str,
                                        },
                                        "vodInfo": {
                                            "playInfos": [{
                                                "desc": validate.all(validate.transform(lambda s: s.lower()), str),
                                                "playUrl": validate.url(),
                                            }],
                                            "vid": str,
                                            "title": str,
                                            "categoryName": str,
                                            "playbackRights": {
                                                "playbackRightsSetting": str,
                                                "playbackRights": str,
                                            },
                                        },
                                    },
                                },
                                {},
                            ),
                        },
                    },
                }],
                validate.get((0, "data", "batchGetVodDetailInfo", "VodDetailInfos", video_id)),
            ),
        )

        if not json:
            log.error("Video not found")
            return

        log.debug(json["vodInfo"]["playbackRights"])
        self.id = json["vodInfo"]["vid"]
        self.author = json["streamerInfo"]["userName"]
        self.title = json["vodInfo"]["title"]
        self.category = json["vodInfo"]["categoryName"]

        for s in json["vodInfo"]["playInfos"]:
            q = s["desc"]
            if "(source)" in q:
                q = f"source_{q.replace('(source)', '')}"
            yield q, HLSStream(self.session, update_scheme("https:", s["playUrl"]))

    def get_live(self, user):
        json = self.session.http.post(
            f"https://api-web.trovo.live/graphql?qid={self.generate_qid()}",
            json=[{
                "operationName": "live_LiveReaderService_GetLiveInfo",
                "variables": {
                    "params": {
                        "userName": user,
                    },
                },
            }],
            schema=validate.Schema(
                validate.parse_json(),
                validate.any(
                    [{
                        "data": {
                            validate.optional("live_LiveReaderService_GetLiveInfo"): {
                                "streamerInfo": {
                                    "userName": str,
                                },
                                "programInfo": {
                                    "id": str,
                                    "title": str,
                                    "streamInfo": [{
                                        "desc": validate.all(validate.transform(lambda s: s.lower()), str),
                                        "playUrl": validate.transform(lambda s: s.replace(".flv?", ".m3u8?")),
                                    }],
                                },
                                "categoryInfo": {
                                    "shortName": str,
                                },
                                "isLive": int,
                            },
                        },
                    }],
                    [{
                        "errors": [{
                            "message": validate.transform(lambda s: s.replace('\\"', '"')),
                        }],
                    }],
                ),
                validate.get(0),
            ),
        )

        if "errors" in json:
            errors = [e["message"] for e in json["errors"]]
            log.error(f"API error(s): {', '.join(errors)}")
            return

        if json["data"]["live_LiveReaderService_GetLiveInfo"]:
            json = json["data"]["live_LiveReaderService_GetLiveInfo"]
        else:
            log.error("Stream data not found")
            return

        if not json["isLive"]:
            log.error("This stream is no longer live")
            return

        self.id = json["programInfo"]["id"]
        self.author = json["streamerInfo"]["userName"]
        self.title = json["programInfo"]["title"]
        self.category = json["categoryInfo"]["shortName"]

        for s in json["programInfo"]["streamInfo"]:
            if s["playUrl"]:
                yield s["desc"], HLSStream(self.session, update_scheme("https:", s["playUrl"]))

    def _get_streams(self):
        self.session.http.headers.update({"Origin": "https://trovo.live"})
        url_data = self.match.groupdict()

        if url_data["video_id"]:
            return self.get_vod(url_data["video_id"])
        elif url_data["user"]:
            return self.get_live(url_data["user"])


__plugin__ = Trovo
