import manager
import os.path
import tAPI

#create db on first boot
if __name__=="__main__":
  if os.path.isfile('first_start_complete.txt'):
    tAPI.main()
    pass
  else:
    f=open('first_start_complete.txt',"w")
    f.close()
    manager.initChatML()
