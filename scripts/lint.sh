#!/usr/bin/env bash

set -e
set -x

mypy kernel_crawler
ruff check kernel_crawler site scripts
ruff format kernel_crawler --check