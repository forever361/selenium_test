#!/bin/bash

repo_path="/app/tanos/fp/Flask_tp"

if [ -d "$repo_path" ]; then
    # 仓库已存在，执行 git pull
    echo "仓库已存在，执行 git pull..."
    cd "$repo_path" || exit
    git pull
else
    # 仓库不存在，执行 git clone
    echo "仓库不存在，执行 git clone..."
    git clone git@gitee.com:kundwong/Flask_tp.git "$repo_path"
fi


sh "sshpass -p '${password}' ssh -t -t -o StrictHostKeyChecking=no ${username}@${host} \"echo '${password}' | sudo -S ${command}\""

