#!/usr/bin/env bash
# PaPaGei code (Nokia Bell Labs, ICLR 2025) and PaPaGei-S weights (Zenodo record 13983110).
set -euo pipefail
mkdir -p third_party weights
[ -d third_party/papagei-foundation-model ] || git clone --depth 1 https://github.com/Nokia-Bell-Labs/papagei-foundation-model third_party/papagei-foundation-model
[ -f weights/papagei_s.pt ] || curl -L -o weights/papagei_s.pt "https://zenodo.org/records/13983110/files/papagei_s.pt?download=1"
sha256sum weights/papagei_s.pt   # expected prefix 79d68671e51b per third-party reports; confirm against the Zenodo page
