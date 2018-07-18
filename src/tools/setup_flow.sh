#!/bin/bash

# Configure git-flow as we like it
git config --remove-section gitflow.branch
git config --add gitflow.branch.master testing
git config --add gitflow.branch.develop development

git config --remove-section gitflow.prefix
git config --add gitflow.prefix.feature feature/
git config --add gitflow.prefix.release release/
git config --add gitflow.prefix.hotfix hotfix/
git config --add gitflow.prefix.support support/
git config --add gitflow.prefix.versiontag ""

git config --remove-section gitflow
git config --add gitflow.origin origin
