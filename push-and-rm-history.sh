#!/bin/bash
git checkout --orphan tmp-master # create a temporary branch
git add -A
git commit -m 'Hmm'
git branch -D master # deletes the master branch
git branch -m master # dename the current branch to master
git push -f origin master
