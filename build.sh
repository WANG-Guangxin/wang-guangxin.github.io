hexo clean
python3 -m pip install --upgrade pip
pip install -r requirements.txt
python3 uptime.py
source siteenv
envsubst < "./source/Sites/index.md" > "./source/Sites/index.md"
hexo generate
