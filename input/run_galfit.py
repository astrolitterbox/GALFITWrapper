import os

import multiprocessing


def doFitting(FileList):
  for i in FileList:
	  command = ("./galfit galfit_"+str(i))
	  print command
	  os.system(command)



def main():

  FileList0 = [162, 164, 249, 267, 319, 437, 445, 464, 476, 477]
  FileList1 = [480, 487, 498, 511, 537, 570, 598, 616, 634, 701]
  FileList2 = [767, 883, 939, 161, 163, 248, 266, 318, 436, 444]
  FileList3 = [463, 475, 476, 479, 486, 497, 510, 536,569, 597]
  FileList4 = [615, 633, 700, 766, 882, 938]

  for fileList in [FileList0, FileList1, FileList2, FileList3, FileList4]:
    print 'filelist', fileList
    p = multiprocessing.Process(target=doFitting, args=[fileList])
    p.start()






if __name__ == '__main__':
  main()