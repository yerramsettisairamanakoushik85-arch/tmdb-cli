import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ENDPOINTS = {
    "playing": "now_playing",
    "popular": "popular",
    "top": "top_rated",
    "upcoming": "upcoming"
}


def fetch_movies(movie_type):
    token = os.getenv("TMDB_API_TOKEN")

    if not token:
        print("Error: TMDB_API_TOKEN is not set.")
        sys.exit(1)

    url = f"https://api.themoviedb.org/3/movie/{ENDPOINTS[movie_type]}?language=en-US&page=1"

    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "accept": "application/json"
        }
    )

    try:
        with urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode())

    except HTTPError as error:
        print(f"Error: TMDB returned HTTP {error.code}.")
        sys.exit(1)

    except URLError:
        print("Error: Unable to connect to TMDB.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type",
        choices=["playing", "popular", "top", "upcoming"],
        required=True
    )

    args = parser.parse_args()
    data = fetch_movies(args.type)

    for i, movie in enumerate(data.get("results", [])[:10], 1):
        print(f"{i}. {movie.get('title', 'Unknown')}")
        print(f"   Release: {movie.get('release_date', 'Unknown')}")
        print(f"   Rating: {movie.get('vote_average', 0)}")
        print()


if __name__ == "__main__":
    main()