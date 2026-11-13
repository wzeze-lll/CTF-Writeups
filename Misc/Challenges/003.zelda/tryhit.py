import socket, time, sys, os
sys.path.insert(0,".")
os.environ["EH"]=sys.argv[1]; os.environ["EP"]=sys.argv[2]
import importlib, winremote
importlib.reload(winremote)
winremote.HOST=sys.argv[1]; winremote.PORT=int(sys.argv[2])
winremote.main()
