#!/usr/bin/env bash
# Install planetary data tools for M5_Inference / ExploreTitan.
#
# Usage:
#   bash scripts/install_planetary_tools.sh          # Tier A only (Python venv)
#   bash scripts/install_planetary_tools.sh --full   # Tier A + B (conda + ISIS3)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
M5_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
VENV_DIR="${M5_ROOT}/.venv-planetary"
FULL=0

if [[ "${1:-}" == "--full" ]]; then
  FULL=1
fi

echo "==> ExploreTitan planetary tools installer"
echo "    M5 root: ${M5_ROOT}"

# --- Tier A: Python venv + pip dependencies ---
if [[ ! -d "${VENV_DIR}" ]]; then
  echo "==> Creating venv at ${VENV_DIR}"
  python3 -m venv "${VENV_DIR}"
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"
pip install --upgrade pip
pip install -r "${M5_ROOT}/requirements-planetary.txt"

echo "==> Tier A ready. Activate with:"
echo "    source ${VENV_DIR}/bin/activate"
echo "    python ${M5_ROOT}/scripts/peek_pds.py --help"

# --- Tier B: Conda environment with ISIS3 ---
if [[ "${FULL}" -eq 1 ]]; then
  if ! command -v conda >/dev/null 2>&1; then
    echo "ERROR: conda not found. Install Miniforge, then re-run with --full."
    echo "       https://github.com/conda-forge/miniforge"
    exit 1
  fi
  echo "==> Creating conda env 'exploretitan-planetary' (ISIS3 + GDAL)..."
  conda env create -f "${M5_ROOT}/environment-planetary.yml" --force 2>/dev/null \
    || conda env update -f "${M5_ROOT}/environment-planetary.yml" --prune
  echo "==> Tier B ready. Activate with:"
  echo "    conda activate exploretitan-planetary"
  echo "    isisinfo -version"
  echo "    bidr2isis from=product.IMG to=product.cub"
fi
