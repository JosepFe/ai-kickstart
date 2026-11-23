#!/usr/bin/env bash
# A repo with a pushed commit and one unpushed commit that leaks a real-looking email, an internal IP and a home path.
set -euo pipefail
G=(git -c user.name=Demo -c user.email=demo@example.com -c init.defaultBranch=main -c commit.gpgsign=false)
R=$(mktemp -d)
"${G[@]}" init -q --bare "$R/remote.git"
"${G[@]}" init -q .
"${G[@]}" remote add origin "$R/remote.git"
printf '# Demo app\n' > README.md
"${G[@]}" add README.md && "${G[@]}" commit -q -m "chore: start"
"${G[@]}" push -q -u origin main
mkdir -p backend/seed
cat > backend/seed/users.json <<'JSON'
[
  { "name": "Ana Example", "email": "ana@example.com" },
  { "name": "Lucía Ferrer Montalbán", "email": "lucia.ferrer.montalban@gmail.com" }
]
JSON
cat > backend/appsettings.Development.json <<'JSON'
{ "Db": "Host=192.168.1.50;Database=demo", "Photos": "/home/lucia/fotos" }
JSON
"${G[@]}" add backend && "${G[@]}" commit -q -m "feat: seed users"
