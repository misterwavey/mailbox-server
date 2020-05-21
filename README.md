# mailbox-server
cd mailbox-server
setup python virtual env:

python3 -m venv server-env
source server-env/bin/activate
pip install proquint
pip install pymysql
python3 server.py

run tests with
python3 test_server_unittest.pyy

run server with 
python3 server.py localhost mboxserver catfishbookwormzebra mbox 8080

