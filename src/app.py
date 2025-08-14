import os
import sys
import shutil
import yt_dlp
import click


def check_ffmpeg():
    """Vérifie que ffmpeg est installé."""
    if shutil.which("ffmpeg") is None:
        click.echo("❌ Erreur : ffmpeg n'est pas installé. Installez-le pour continuer.")
        sys.exit(1)


def download_youtube_mp4(url, output_dir="vid"):
    """Télécharge une vidéo YouTube en MP4."""
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': True,
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_youtube_mp3(url, output_dir="son"):
    """Télécharge l'audio d'une vidéo YouTube et le convertit en MP3."""
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


@click.command()
@click.option('--choice', type=click.Choice(['1', '2']), prompt='Tape 1 pour MP4 ou 2 pour MP3',
              help='Choisissez le format : 1 = MP4, 2 = MP3')
@click.option('--url', prompt='Lien', help='URL de la vidéo YouTube à télécharger')
def main(url, choice):
    """Téléchargeur YouTube en MP4 ou MP3."""
    check_ffmpeg()

    try:
        if choice == '1':
            download_youtube_mp4(url)
            click.echo("✅ Vidéo MP4 téléchargée avec succès !")
        elif choice == '2':
            download_youtube_mp3(url)
            click.echo("✅ Audio MP3 téléchargé avec succès !")
    except Exception as e:
        click.echo(f"❌ Une erreur est survenue : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
