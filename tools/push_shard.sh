#!/bin/sh
# usage: push_shard.sh NN  -> commits and pushes enrich/out_NN.json (safe with several workers)
cd "$(dirname "$0")/.." || exit 1
flock /tmp/df_git.lock sh -c '
git add enrich/out_'"$1"'.json &&
git -c user.name=Nix -c user.email=nikhil.vinod@gmail.com commit -qm "enrich shard '"$1"' progress

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01LR3yEvxJ5miqBu6avkDxxz" ;
for i in 1 2 3; do git pull -q --rebase --autostash origin main && git push -q origin main && echo pushed && break; sleep 3; done'
