import os
import sys
import yt_dlp
import click


@click.command()
@click.option('--url', prompt='Lien YouTube', help='URL de la vidéo YouTube à télécharger')
@click.option('--choice', type=click.Choice(['1', '2']), prompt='Tape 1 pour MP4 ou 2 pour MP3',
              help='Choisissez le format : 1 = MP4, 2 = MP3')
def main(url, choice):
    """Téléchargeur YouTube en MP4 ou MP3."""
    if choice == '1':
        download_youtube_mp4(url)
        click.echo("✅ Vidéo MP4 téléchargée avec succès !")
    elif choice == '2':
        download_youtube_mp3(url)
        click.echo("✅ Audio MP3 téléchargé avec succès !")
        
        
def download_youtube_mp4(url, output_dir="vid"):
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_youtube_mp3(url: str, output_dir: str = "son") -> None:
    """
    Télécharge l'audio d'une vidéo YouTube et le convertit en MP3.

    :param url: URL de la vidéo YouTube.
    :param output_dir: Dossier de sortie pour le fichier MP3.
    """
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,  # pas de sortie dans le terminal
        'noplaylist': True,  # éviter de télécharger toute une playlist
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    main()
