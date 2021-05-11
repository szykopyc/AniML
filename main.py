import manager
import os.path

#create db on first boot
if __name__=="__main__":
  if os.path.isfile('first_start_complete.txt'):
    pass
  else:
    f=open('first_start_complete.txt',"w")
    f.close()
    manager.initChatML()