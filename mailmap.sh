#!/bin/bash
#
### mailmap.sh
#
#

git log --all --format='%aN <%aE>' >> mailmap.tmp
git log --all --format='%cN <%cE>' >> mailmap.tmp
cat mailmap.tmp | sort -u > .mailmap
rm mailmap.tmp
