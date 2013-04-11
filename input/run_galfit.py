import os

import multiprocessing


def doFitting(FileList):
  for i in FileList:
	  command = ("./galfit galfit_"+str(i))
	  print command
	  os.system(command)



def main():

  FileList0 = range(23, 188)
  FileList1 = range(304, 376)
  FileList2 = range(486, 564)
  FileList3 = range(679, 752)
  FileList4 = range(861, 940)

  for fileList in [FileList0, FileList1, FileList2, FileList3, FileList4]:
    print 'filelist', fileList
    p = multiprocessing.Process(target=doFitting, args=[fileList])
    p.start()






if __name__ == '__main__':
  main()
