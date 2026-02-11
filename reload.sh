#!/usr/bin/env bash
set -e

COMPOSE_FILES="-f docker-compose.yml -f docker-compose.reload.yml"
cd "$(dirname "$0")"

run_down() {
  docker compose $COMPOSE_FILES down "$@"
}

run_up() {
  docker compose $COMPOSE_FILES up "$@"
}

case "${1:-up}" in
  up)
    shift
    run_up "$@"
    ;;
  down)
    shift
    run_down "$@"
    ;;
  restart)
    shift
    run_down
    run_up "$@"
    ;;
  -*)
    run_up "$@"
    ;;
  *)
    run_up "$@"
    ;;
esac
