export SECRET=OME88YorohonzPNWEFsi0dIsouXWqeO$
export WIKIPEDIA_DATABASE_NAME=wikipedia.db
export DATABASE_URL=rocksdb://wikipedia.rdb
export BRAID_SCRIPT_ROOT=./scripts

init:
	rm -rf venv
	virtualenv -p python3 venv
	. venv/bin/activate && pip install -r requirements.txt

wikipedia.db:
	. venv/bin/activate && python crawler.py enwiki-latest-pages-articles.xml.bz2

explorer: wikipedia.db
	. venv/bin/activate && python explorer.py
