#!/usr/bin/env bash
set -euo pipefail

# ╭───────────────────────────────╮
# │ ENVIRONMENT DIR/ENVRC SETUP   │
# ╰───────────────────────────────╯
if ! command -v direnv &> /dev/null; then
    echo "❌ direnv n'est pas installé. Installe-le avant de continuer."
    exit 1
fi

if [ ! -f ".envrc" ]; then
    echo "📄 Création de .envrc..."
    cat << 'EOF' > .envrc
layout python3
export VIRTUAL_ENV=$(pwd)/.venv
export PATH=$VIRTUAL_ENV/bin:$PATH
EOF
fi

mkdir -p .direnv

# Active direnv
direnv allow > /dev/null 2>&1
eval "$(direnv export bash)"

# ╭──────────────────────────────╮
# │ PYTHON VENV SETUP            │
# ╰──────────────────────────────╯
if [ ! -d ".venv" ]; then
    echo "🐍 Création de l'environnement virtuel..."
    python3 -m venv .venv > /dev/null 2>&1
fi

# Activation silencieuse
source .venv/bin/activate

# ╭──────────────────────╮
# │ INSTALL DEPENDENCIES │
# ╰──────────────────────╯
if [ -f "requirements.txt" ]; then
    echo "📦 Installation des dépendances..."
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt > /dev/null 2>&1
fi

if [ -f "setup.py" ]; then
    echo "🔨 Installation du package local..."
    pip install -e . > /dev/null 2>&1
    echo "⚙️  Compilation des extensions Cython..."
    python3 setup.py build_ext --inplace > /dev/null 2>&1
fi

# Dépendances spécifiques
pip install pytube > /dev/null 2>&1

echo "✅ Environnement prêt !"
