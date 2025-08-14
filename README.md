# TikFlowBoost

# YouTube Downloader (MP3 / MP4)

Un petit outil Python pour télécharger des vidéos YouTube en **MP4** ou extraire l’audio en **MP3**, avec une interface en ligne de commande simple grâce à **Click**.

## Fonctionnalités

- Télécharger des vidéos YouTube en MP4
- Extraire l’audio des vidéos YouTube en MP3
- Choix interactif du format via la CLI
- Mode silencieux pour un terminal propre
- Vérification automatique de `yt_dlp`

## Prérequis

- Python 3.8+
- [yt_dlp](https://github.com/yt-dlp/yt-dlp)
- pip
- Click

## Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/XXXXXX
```

2. Créer un environnement virtuel et l’activer :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Utilisation

```bash
python src/app.py
```

Aide
```bash 
python src/app.py --help
```

## 📃 License

MIT License © DBIBIH Oussama (2025)
[LICENSE](LICENSE)