#! /bin/bash

source server-env/bin/activate
nohup python3 -u server.py localhost mboxserver catfishbookwormzebra mbox 8080 > server.log &
