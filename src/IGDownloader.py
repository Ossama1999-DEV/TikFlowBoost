import instaloader
import click

def download_instagram_post(url, output_dir="downloads", username=None, password=None):
    L = instaloader.Instaloader()

    # Si login fourni, on se connecte
    if username and password:
        L.login(username, password)

    shortcode = url.strip("/").split("/")[-1].split("?")[0]
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    L.download_post(post, target=output_dir)


@click.command()
@click.argument("url")
@click.option("--output", default="downloads", help="Dossier de sortie")
@click.option("--username", default=None, help="Nom d'utilisateur Instagram")
@click.option("--password", default=None, help="Mot de passe Instagram")
def main(url, output, username, password):
    """Télécharge une vidéo ou une image Instagram à partir d'une URL."""
    try:
        click.echo(f"Téléchargement depuis {url} ...")
        download_instagram_post(url, output, username, password)
        click.echo(f"✅ Terminé ! Fichier enregistré dans '{output}'")
    except Exception as e:
        click.echo(f"❌ Erreur : {e}")


if __name__ == "__main__":
    main()
