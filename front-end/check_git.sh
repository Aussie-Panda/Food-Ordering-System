#!/bin/bash

echo "##################################################################################"
echo "# This script checks remote branches only ('origin/master' and 'origin/release') #"
echo "# Make sure any local changes have been pushed to remote                         #"
echo "##################################################################################"
echo
echo "Checking remote master and remote release branches are at the same point..."
echo
git fetch > /dev/null
if ! git rev-parse --verify origin/release >/dev/null 2>/dev/null; then
	echo "There is no 'release' branch on GitHub!"
	exit 1
fi
diffs=`git rev-list --left-right --count origin/master...origin/release`
behind=`echo $diffs | cut -d' ' -f1`
ahead=`echo $diffs | cut -d' ' -f2`
if [[ "$ahead" -eq "0" && "$behind" -eq "0" ]]; then
	echo "Master branch is at the same point as release branch. Nice!"
	exit 0
fi
if [ "$ahead" -ne "0" ]; then
	echo "Release is ahead of master by $ahead commits. Have you pushed directly to release and not master?"
fi
if [ "$behind" -ne "0" ]; then
	echo "Release is behind master by $behind commits. Have you merged master in?"
fi