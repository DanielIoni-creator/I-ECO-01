#!/bin/sh
set -eu

CANONICAL_PROJECT_ID="prj_ygmwJhghElzkyIw9RTZjrfiXehYK"
DUPLICATE_PROJECT_ID_A="prj_iEfsqjT6BcWX7IybRB4fsmuyrMe2"
DUPLICATE_PROJECT_ID_B="prj_uL3WfRmSEC5pAaInD7cLTkYKrznB"

case "${VERCEL_PROJECT_ID:-}" in
  "$DUPLICATE_PROJECT_ID_A"|"$DUPLICATE_PROJECT_ID_B")
    echo "Skipping duplicate Vercel project: ${VERCEL_PROJECT_ID}"
    exit 0
    ;;
  "$CANONICAL_PROJECT_ID")
    echo "Building canonical Vercel project: ${VERCEL_PROJECT_ID}"
    exit 1
    ;;
  "")
    echo "VERCEL_PROJECT_ID is unavailable; fail-safe is to continue the build."
    exit 1
    ;;
  *)
    echo "Unknown Vercel project ID '${VERCEL_PROJECT_ID}'; fail-safe is to continue the build."
    exit 1
    ;;
esac
