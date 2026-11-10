#!/usr/bin/env sh
# Give the dev build (`npm run tauri dev`) its "N" icon in the GNOME dock and
# the WSLg taskbar. On Wayland the shell ignores a window's own icon and looks
# up a .desktop file named after the app id, which Tauri sets to the
# `identifier` in tauri.conf.json; with none it shows a gear (a penguin in WSLg).
# An installed .deb ships its own entry; this is for the dev box only.
set -eu
here=$(cd "$(dirname "$0")/.." && pwd)
id=$(sed -n 's/.*"identifier": *"\([^"]*\)".*/\1/p' "$here/src-tauri/tauri.conf.json")
apps="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$apps"
cat > "$apps/$id.desktop" <<DESKTOP
[Desktop Entry]
Type=Application
Name=Nómos — EUROMOD parameter review
Comment=Review EUROMOD parameter updates proposed from legislation
Exec=sh -c "cd '$here' && npm run tauri dev"
Icon=$here/src-tauri/icons/icon.png
Terminal=false
Categories=Office;
StartupWMClass=euromod-review-ui
DESKTOP
update-desktop-database "$apps" 2>/dev/null || true
echo "wrote $apps/$id.desktop"
