#!/usr/bin/env bash
# filepath: scripts/release.sh
#
# Version bump and tagging script for recallrai SDK
# 
# This script:
# 1. Bumps version in pyproject.toml and __init__.py
# 2. Commits changes
# 3. Creates a git tag
# 4. Pushes changes and tag to GitHub
#
# Usage: ./scripts/release.sh <major|minor|patch> [tag message]

set -e  # Exit immediately if a command exits with a non-zero status

# Check if the part argument is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <major|minor|patch> [tag message]"
    echo "Example: $0 patch 'Fixed bug in API client'"
    exit 1
fi

# Validate version bump type
PART=$1
shift
if [[ ! "$PART" =~ ^(major|minor|patch)$ ]]; then
    echo "Error: Version bump type must be one of: major, minor, patch"
    exit 1
fi

# Get tag message from arguments or use default
TAG_MESSAGE=""
if [ $# -gt 0 ]; then
    TAG_MESSAGE="$*"
fi

# Check if working directory is clean
if ! git diff --quiet; then
    echo "Error: You have uncommitted changes. Please commit or stash them first."
    exit 1
fi

# Get current version from pyproject.toml
CURRENT_VERSION=$(grep -E '^version = "[^"]+"' pyproject.toml | cut -d'"' -f2)
echo "Current version: $CURRENT_VERSION"

# Split version into components
IFS='.' read -r -a VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

# Bump version based on part argument
if [ "$PART" == "major" ]; then
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
elif [ "$PART" == "minor" ]; then
    MINOR=$((MINOR + 1))
    PATCH=0
elif [ "$PART" == "patch" ]; then
    PATCH=$((PATCH + 1))
fi

NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
echo "New version: $NEW_VERSION"

# Update version in pyproject.toml
sed -i "s/^version = \"[^\"]*\"/version = \"$NEW_VERSION\"/" pyproject.toml
echo "✓ Updated version in pyproject.toml"

# Update version in __init__.py
sed -i "s/__version__ = \"[^\"]*\"/__version__ = \"$NEW_VERSION\"/" recallrai/__init__.py
echo "✓ Updated version in recallrai/__init__.py"

# Commit changes
git add pyproject.toml recallrai/__init__.py
git commit -m "Bump version to $NEW_VERSION"
echo "✓ Committed version changes to git"

# Create tag
TAG_NAME="v$NEW_VERSION"
if [ -z "$TAG_MESSAGE" ]; then
    # No tag message provided, use a default message
    TAG_MESSAGE="Version $NEW_VERSION"
fi
git tag -a "$TAG_NAME" -m "$TAG_MESSAGE"
echo "✓ Created git tag $TAG_NAME"

# Push changes and tag
git push origin main 
git push origin "$TAG_NAME"
echo "✓ Pushed changes and tag to remote"

echo ""
echo "✅ Successfully released version $NEW_VERSION"
echo "Go to Github and create a new release for tag $TAG_NAME"
echo "Then, CICD will take care of the rest!"
