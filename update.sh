#!/bin/bash
# Auto commit & push script for the Vue site
set -e

git pull origin master

git add .

modified_files=$(git diff --name-only --cached)

current_datetime=$(date '+%Y-%m-%d %H:%M:%S')

commit_message="Update at $current_datetime with changes:"
for file in $modified_files; do
    filename=$(basename "$file")
    commit_message="$commit_message \"$filename\""
done

git commit -m "$commit_message"
git push origin master

echo "自动添加、提交和推送已完成。"
