import os

import multiprocessing


def doFitting(FileList):
  for i in FileList:
	  command = ("./galfit galfit_"+str(i))
	  print command
	  os.system(command)



def main():

  #FileList0 = range(112, 121)
  #FileList1 = range(130, 138)
  FileList1 = [81, 144, 147, 338, 43]
  FileList2 = [491, 505, 540, 652, 884]
  #FileList3 = range(160, 170)
  #FileList4 = range(178, 188)

  for fileList in [FileList2, FileList1]:#a, FileList1, FileList2, FileList3, FileList4]:
    print 'filelist', fileList
    p = multiprocessing.Process(target=doFitting, args=[fileList])
    p.start()






if __name__ == '__main__':
  main()
