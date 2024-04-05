#!/bin/bash

# 添加所有修改的文件
git add .

# 获取修改的文件列表
modified_files=$(git diff --name-only --cached)

# 获取当前日期时间
current_datetime=$(date '+%Y-%m-%d %H:%M:%S')

# 构建提交信息
commit_message="Update at $current_datetime with changes:"
for file in $modified_files; do
    filename=$(basename "$file")
    commit_message="$commit_message \"$filename\""
done

# 提交更改
git commit -m "$commit_message"

# 推送到远程仓库的home-page分支
git push origin source-code

echo "自动添加、提交和推送已完成。"

