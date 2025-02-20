import json
import pathlib


def parse_tracklist_dump(filepath: str) -> None:
    path = pathlib.Path(filepath)
    for line in path.open():
        parse_spotify_track_metadata(line)


def parse_spotify_track_metadata(line: str) -> None:
    to_extract: dict[str, list[str]] = {
        "added_at": ["added_at"],
        "name": ["track", "name"],
        "link": ["track", "external_urls", "spotify"],
        "isrc": ["track", "external_ids", "isrc"],
        "popularity": ["track", "popularity"],
        "duration_ms": ["track", "duration_ms"],
        "album": ["track", "album", "name"],
        "release_date": ["track", "album", "release_date"],
    }

    metadata = json.loads(line)
    parsed = {}
    for name, path in to_extract.items():
        value = metadata
        for key in path:
            value = value.get(key, {})
        parsed[name] = value

    artists = metadata["track"]["artists"]

    parsed["artist"] = artists[0]["name"]
    parsed["other_artists"] = ",".join(a["name"] for a in artists[1:])

    print(parsed)
