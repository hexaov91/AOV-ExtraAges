import os
import zipfile
import re
from os import walk
from os.path import join
import pathlib
import filecmp

filelist1=[]
filelist2=[]
editlist=[]
hashedList=[]
pathlistPreHero=[]
workpath=''
class GetHashCode:    
    def convert_n_bytes(self,n, b):        
        bits = b*8        
        return (n + 2**(bits-1)) % 2**bits - 2**(bits-1)    
    def convert_4_bytes(self,n):        
            return self.convert_n_bytes(n,4)
    @classmethod
    def getHashCode(cls,s):
        h = 0
        n = len(s)
        for i, c in enumerate(s):
            h = h + ord(c)*31**(n-1-i)
        return cls().convert_4_bytes(h)
        
def folder_diff(start_path):
 for dirpath, dirnames, filenames in os.walk(PATH1):
  for filename in filenames:
   fixpath=os.path.join(dirpath, filename).replace("\\", "/")
   if os.path.splitext(fixpath)[1] == '.xml' :
    filelist1.append(fixpath.replace("/base/", "/add/"))

   else:
    print(os.path.splitext(fixpath)[1])   
   
 for dirpath, dirnames, filenames in os.walk(PATH2):
  for filename in filenames:
   fixpath=os.path.join(dirpath, filename).replace("\\", "/")
   if os.path.splitext(fixpath)[1] == '.xml' :
    filelist2.append(fixpath.replace("/base/", "/add/"))

   else:
    print(os.path.splitext(fixpath)[1])

def unpackpkg(input):
 pkgpath=input
 for root, dirs, files in walk(pkgpath):
  for f in files:
    fullpath = join(root, f)
    pkg = pathlib.Path(fullpath)
    if ''.join(pkg.suffixes) == '.pkg.bytes' :
     with zipfile.ZipFile(fullpath, 'r') as zip_ref:
      zip_ref.extractall(os.path.dirname(fullpath))
      zip_ref.close()
      os.remove(fullpath)	
      			
def copy(fpath,rootph):
 rootpath="extra/Ages/"
 if not os.path.exists(os.path.dirname(rootpath+rootph)):
  os.makedirs(os.path.dirname(rootpath+rootph))
 if os.path.exists(fpath):
  file_oldname = fpath
  file_newname_newfile = rootpath+rootph
  os.rename(file_oldname, file_newname_newfile)
#  print(rootph,GetHashCode.getHashCode(rootph))
  editlist.append(GetHashCode.getHashCode(rootph.replace(".xml", "").lower()))
  print(rootph.replace(".xml", "").lower(),GetHashCode.getHashCode(rootph.replace(".xml", "").lower()))
  
  
def canuse(start_path):
 fr=open(start_path, 'rb')
 raw = fr.read()
 raw2 = fr.read()
 with open(start_path, 'r', encoding="ISO-8859-1" ) as f:
    text = f.read()
 matches = re.finditer(r'Ages/AsianGames/[A-Za-z0-9_/]{1,256}.pkg.bytes', text, re.MULTILINE)  
 for m in matches:
  if "Ages/AsianGames/Prefab_Characters/Prefab_Hero/Actor_" in m.group(0) :
   pathlistPreHero.append(m.group(0))
   name1=m.group(0).encode('utf-8')
   print(name1)
   name2=b'Ages/Prefab_Characters/HEXAOV_HexaovPlugin_Extra_Action_Doom001.pkg.bytes'
   raw=raw.replace(name1,name2)
 with open("resourcepackerinfosetall", 'wb') as f:
  f.write(raw)
    
 Prefab_Hero(pathlistPreHero,start_path,raw2)
  
def Prefab_Hero(pathlistPreHero,start_path,rawab):
    with open(start_path, 'rb') as f:
      raw = f.read()

    for fullPH in pathlistPreHero:
     head=raw.find(str.encode(fullPH))
     
#     s=s.replace(b'PatientName',bytes(name)) i.to_bytes(4, 'little')
  
     XmlCount=int.from_bytes((raw[head+100:head+104]),'little')
    # print(XmlCount,fullPH)   
     offsetXml= 0
     for limit in range(XmlCount) :
      inthash=int.from_bytes(raw[head+104+offsetXml : head+108+offsetXml],'little',signed=True)
      hashedList.append(inthash)      
#      print(fullPH,raw[head+104+offsetXml : head+108+offsetXml])
      offsetXml=offsetXml+12
    editAB(editlist,hashedList)
     
def editAB(editlist,hashedList) :
  print(editlist)
  print(hashedList)
  fr=open("resourcepackerinfosetall", 'rb')
  raw = fr.read()
  with open("extra/assetbundle/resourcepackerinfosetall.assetbundle", 'wb') as f:
   i=0
   for hashAdd in editlist:
 #   print(hashedList[i])
    raw=raw.replace(hashedList[i].to_bytes(4, 'little',signed=True) , hashAdd.to_bytes(4, 'little',signed=True) )
    print(hashedList[i],hashedList[i].to_bytes(4, 'little',signed=True),"to",hashAdd , hashAdd.to_bytes(4, 'little',signed=True))
    i=i+1
    
    
   f.write(raw)
   
def pkg():
 os.chdir(os.getcwd()+'/'+'extra/Ages/Prefab_Characters')
 path = "extra/Ages/Prefab_Characters"
 pathlist= os.listdir()
 for fold in pathlist: 
  z = zipfile.ZipFile('HEXAOV_HexaovPlugin_Extra_Action_Doom001.pkg.bytes', 'w', zipfile.ZIP_STORED)
  startdir =fold
  print(startdir)
  for dirpath, dirnames, filenames in os.walk(startdir):
   for filename in filenames:
    z.write(os.path.join(dirpath, filename))
  z.close()
def pkgbase():
 os.chdir(os.getcwd().replace("/extra/", "/add/")+'/Prefab_Hero')
 path = "add/Ages/Prefab_Characters/Prefab_Hero"
 pathlist= os.listdir()
 for fold in pathlist: 
  z = zipfile.ZipFile(os.getcwd().replace("/add/", "/extra/")+'/Actor_'+fold[0:3]+'_Actions.pkg.bytes', 'w', zipfile.ZIP_STORED)
  startdir =fold
  print('packing',startdir)
  for dirpath, dirnames, filenames in os.walk(startdir):
   for filename in filenames:
    z.write((os.path.join(dirpath, filename)).replace("/add/", "/extra/"))
    print(os.path.join(dirpath, filename))
  z.close()


   

if __name__ == "__main__":
    PATH1 = "base/"
    PATH2 = "add/"
    unpackpkg(PATH1)
    folder_diff(PATH1)
#    difference_1 = set(filelist1).difference(set(filelist2))
#    difference_2 = set(filelist2).difference(set(filelist1))
#    list_difference = list(difference_1.union(difference_2))
    diff= [x for x in filelist2 if x not in filelist1]
    for fpath in diff :
     rootph=fpath.replace(PATH2+'Ages/', "")
     copy(fpath,rootph)
    
    canuse("resourcepackerinfosetall.assetbundle")
    pkg()
    pkgbase()
    


 
