import base64
import os
from typing import Any, Iterable

import requests


class SpotifyClient:
    token_endpoint = "https://accounts.spotify.com/api/token"
    user_endpoint = "https://api.spotify.com/v1/users"
    playlist_endpoint = "https://api.spotify.com/v1/playlists"

    def __init__(self) -> None:
        self.token = self.get_auth_token()

    def get_tracks_metadata(
        self, user: str, playlist_id: str
    ) -> Iterable[dict[str, str]]:
        endpoint = f"{self.playlist_endpoint}/{playlist_id}"

        data = self.get_authorised(endpoint)
        next_page = data["tracks"]["href"]
        while next_page:
            print(f"Downloading {next_page}")
            page = self.get_authorised(next_page)
            yield from page["items"]

            next_page = page["next"]

    def get_playlist(self, user: str, playlist_name: str) -> dict[str, str]:
        endpoint = f"{self.user_endpoint}/{user}/playlists"
        data = self.get_authorised(endpoint)

        for playlist in data["items"]:
            if playlist["name"] == playlist_name:
                assert isinstance(playlist, dict)
                return playlist

        raise ValueError(
            f"Could not find playlist named {playlist_name} for user {user}"
        )

    def get_authorised(self, endpoint: str) -> dict[str, Any]:
        """Make an authorised GET request to the given endpoint."""
        response = requests.get(
            endpoint, headers={"Authorization": f"Bearer {self.token}"}
        )
        response.raise_for_status()
        data = response.json()
        # Why isn't this typed properly in the stubs?
        assert isinstance(data, dict)
        return data

    @classmethod
    def get_auth_token(cls) -> str:
        """Return authentication token generated using client credentials flow.

        This authentication method does not give access to user data endpoints.
        """

        response = requests.post(
            cls.token_endpoint,
            headers=cls.build_auth_header(),
            data={"grant_type": "client_credentials"},
        )
        response.raise_for_status()

        token: str = response.json()["access_token"]
        return token

    @staticmethod
    def build_auth_header() -> dict[str, str]:
        """Return header containing base64 encoded Spotify credentials."""
        try:
            client_id = os.environ["SPOTIFY_CLIENT_ID"]
            client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
            creds = f"{client_id}:{client_secret}"
        except KeyError as err:
            raise RuntimeError("Missing Spotify credentials") from err

        base64_creds = base64.standard_b64encode(creds.encode()).decode()
        return {"Authorization": f"Basic {base64_creds}"}


def parse_track_metadata(metadata: Any) -> dict[str, str]:
    to_extract: dict[str, list[str]] = {
        "added_at": ["added_at"],
        "name": ["track", "name"],
        "link": ["track", "external_urls", "spotify"],
        "isrc": ["track", "external_ids", "isrc"],
        "popularity": ["track", "popularity"],
        "duration_ms": ["track", "duration_ms"],
        "album": ["track", "album", "name"],
        "release_date": ["track", "album", "release_date"],
        "release_date_precision": ["track", "album", "release_date_precision"],
    }

    parsed = {}
    for name, path in to_extract.items():
        value = metadata
        for key in path:
            value = value.get(key, {})
        parsed[name] = value

    artists = metadata["track"]["artists"]
    parsed["artist"] = artists[0]["name"]
    parsed["other_artists"] = "|".join(a["name"] for a in artists[1:])

    # Add dummy month and year to imprecise release dates
    if parsed.pop("release_date_precision") == "year":
        parsed["release_date"] = f"{parsed['release_date']}-01-01"

    return parsed
