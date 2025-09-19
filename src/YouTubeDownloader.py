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
    """Télécharge une vidéo YouTube en MP4 (robuste)."""
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.download([url]) == 0


def download_youtube_mp3(url, output_dir="son"):
    """Télécharge l'audio YouTube en MP3 (robuste)."""
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': False,
        'ignoreerrors': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.download([url]) == 0


@click.command()
@click.argument("url", required=False)
@click.option("--input-file", "-i", default=None, help="Fichier texte contenant des liens YouTube")
@click.option("--retry-failed", is_flag=True, help="Relancer uniquement les liens échoués (failed_links.txt)")
def main(url, input_file, retry_failed):
    """Téléchargeur YouTube en MP4 ou MP3 (un seul lien, fichier .txt ou retry)."""
    check_ffmpeg()

    # Si on relance les liens échoués
    if retry_failed:
        if not os.path.exists("failed_links.txt"):
            click.echo("❌ Aucun fichier failed_links.txt trouvé.")
            sys.exit(1)
        with open("failed_links.txt", "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
        click.echo(f"🔁 Relance des {len(urls)} liens échoués précédemment...")
    else:
        # Récupération des URLs normales
        urls = []
        if input_file:
            with open(input_file, "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip()]
        elif url:
            urls = [url]
        else:
            click.echo("❌ Erreur : Donne soit un URL, soit un fichier avec --input-file, soit --retry-failed")
            sys.exit(1)

    # Choix du format
    choix = input("Tape 1 pour MP4 ou 2 pour MP3 (1, 2): ").strip()

    success_links = []
    failed_links = []

    for u in urls:
        try:
            ok = False
            if choix == "1":
                ok = download_youtube_mp4(u)
            elif choix == "2":
                ok = download_youtube_mp3(u)
            else:
                click.echo("❌ Choix invalide (1 ou 2)")
                sys.exit(1)

            if ok:
                click.echo(f"✅ Téléchargement réussi : {u}")
                success_links.append(u)
            else:
                click.echo(f"⚠️ Échec du téléchargement : {u}")
                failed_links.append(u)

        except Exception as e:
            click.echo(f"⚠️ Erreur avec {u} → {e}")
            failed_links.append(u)

    # Résumé final
    click.echo("\n================ Résumé final ================\n")

    if success_links:
        click.echo("✅ Téléchargements réussis :")
        for s in success_links:
            click.echo(f"   - {s}")
    else:
        click.echo("❌ Aucun téléchargement réussi.")

    if failed_links:
        click.echo("\n⚠️ Téléchargements échoués :")
        for f in failed_links:
            click.echo(f"   - {f}")

        # Sauvegarde dans un fichier
        with open("failed_links.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(failed_links))
        click.echo("\n📂 Les liens échoués ont été sauvegardés dans failed_links.txt")
    else:
        # Supprimer l’ancien fichier si tout est OK
        if os.path.exists("failed_links.txt"):
            os.remove("failed_links.txt")
        click.echo("\n👌 Aucun lien échoué !")

    click.echo("\n==============================================\n")


if __name__ == "__main__":
    main()
