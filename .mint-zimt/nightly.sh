#!/usr/bin/env bash

set -euo pipefail

uvx zesty-bakewell==$(cat .mint-zimt/zesty-bakewell-version) nightly
