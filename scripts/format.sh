#!/usr/bin/env bash
set -x

ruff check kernel_crawler scripts --fix
ruff format kernel_crawler scripts