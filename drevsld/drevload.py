import argparse
import os
import re
import sys
from sclib import SoundcloudAPI, Track, Playlist

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_track(url, save_dir):
    api = SoundcloudAPI()
    try:
        track = api.resolve(url)
    except Exception as e:
        print(f"Ошибка при разрешении URL: {e}")
        sys.exit(1)

    if not isinstance(track, Track):
        print("Предоставленная ссылка не является треком.")
        sys.exit(1)

    os.makedirs(save_dir, exist_ok=True)
    filename = f"{track.artist} - {track.title}.mp3"
    filename = sanitize_filename(filename)
    filepath = os.path.join(save_dir, filename)
    with open(filepath, 'wb+') as f:
        track.write_mp3_to(f)
    print(f"Скачан трек: {filepath}")

def download_playlist(url, save_dir):
    api = SoundcloudAPI()
    try:
        playlist = api.resolve(url)
    except Exception as e:
        print(f"Ошибка при разрешении URL: {e}")
        sys.exit(1)

    if not isinstance(playlist, Playlist):
        print("Предоставленная ссылка не является плейлистом.")
        sys.exit(1)

    playlist_title = sanitize_filename(playlist.title)
    playlist_dir = os.path.join(save_dir, playlist_title)
    os.makedirs(playlist_dir, exist_ok=True)
    for track in playlist.tracks:
        filename = f"{track.artist} - {track.title}.mp3"
        filename = sanitize_filename(filename)
        filepath = os.path.join(playlist_dir, filename)
        with open(filepath, 'wb+') as f:
            track.write_mp3_to(f)
        print(f"Скачан трек: {filepath}")

def main():
    parser = argparse.ArgumentParser(
        description="Утилита для скачивания треков и плейлистов с SoundCloud."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Подкоманда для скачивания трека
    parser_track = subparsers.add_parser("track", help="Скачать трек")
    parser_track.add_argument("url", help="Ссылка на трек SoundCloud")
    parser_track.add_argument("save_dir", help="Путь к папке для сохранения")

    # Подкоманда для скачивания плейлиста
    parser_playlist = subparsers.add_parser("playlist", help="Скачать плейлист")
    parser_playlist.add_argument("url", help="Ссылка на плейлист SoundCloud")
    parser_playlist.add_argument("save_dir", help="Путь к папке для сохранения")

    args = parser.parse_args()

    if args.command == "track":
        download_track(args.url, args.save_dir)
    elif args.command == "playlist":
        download_playlist(args.url, args.save_dir)

if __name__ == "__main__":
    main()
