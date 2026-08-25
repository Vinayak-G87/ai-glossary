#!/usr/bin/env sh
set -eu

APP_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
APPLICATIONS_DIR=${XDG_DATA_HOME:-"$HOME/.local/share"}/applications
DESKTOP_FILE="$APPLICATIONS_DIR/ai-glossary.desktop"

python3 -c "import tkinter" 2>/dev/null || {
    printf '%s\n' "Tkinter is required. On Ubuntu/Debian, install it with: sudo apt install python3-tk" >&2
    exit 1
}

mkdir -p "$APPLICATIONS_DIR"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=AI Glossary
Comment=Offline pocket guide to AI concepts
Exec=$APP_DIR/run.sh
Icon=accessories-dictionary
Terminal=false
Categories=Education;Utility;
Keywords=AI;glossary;machine learning;
StartupNotify=true
EOF

chmod +x "$DESKTOP_FILE"
printf 'Installed AI Glossary launcher at %s\n' "$DESKTOP_FILE"