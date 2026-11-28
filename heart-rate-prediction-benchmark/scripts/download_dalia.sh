#!/usr/bin/env bash
# PPG-DaLiA (Reiss et al. 2019), UCI ML Repository id 495, ~2.7 GB. Verify the URL on
# https://archive.ics.uci.edu/dataset/495/ppg+dalia if it changes.
set -euo pipefail
mkdir -p datasets && cd datasets
[ -f ppg_dalia.zip ] || curl -L -o ppg_dalia.zip "https://archive.ics.uci.edu/static/public/495/ppg+dalia.zip"
[ -d PPG_FieldStudy ] || unzip -q ppg_dalia.zip
ls PPG_FieldStudy | head
