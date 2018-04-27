#   GCodeHashLib embeds MD5 and SHA256 checksums within gcode files for pre-print validation purposes
#    Copyright (C) 2018 Patrick Skelley, <pskelley@albany.edu>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import hashlib
import os.stat, os.path

class GCodeMD5Checksum:
    def __init__(self,  filename):
        self.filename = filename
        
    def ApplySignature(self):
        md5 = hashlib.md5()
        with open(self.filename, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
               md5.update(block)
            hash = md5.hexdigest()
        
        with open(self.filename, "r+",encoding='utf-8') as f:
            contents = f.readlines()
            print(contents)
            contents.insert(0,";GCODEHASHLIB_MD5=" + hash + "\n") 
            
        with open(self.filename,  "w",encoding='utf-8') as f:
            f.writelines(contents)
        
    def VerifySignature(self, md5hash):
        md5 = hashlib.md5()
        with open(self.filename, "rb") as f:
            byte = f.read(1)
            while byte.decode("utf-8") != '\x0A':
               byte = f.read(1)
          
            for block in iter(lambda: f.read(4096), b""):
                md5.update(block)
                hash = md5.hexdigest()
        
        return(hash==md5hash)
        
class GCodeSHA256Checksum:
    def __init__(self,  filename):
        self.filename = filename
        
    def ApplySignature(self):
        sha256 = hashlib.sha256()
        with open(self.filename, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
               sha256.update(block)
            hash = sha256.hexdigest()
        
        with open(self.filename, "r+",encoding='utf-8') as f:
            contents = f.readlines()
            print(contents)
            contents.insert(0,";GCODEHASHLIB_SHA256=" + hash + "\n") 
            
        with open(self.filename,  "w",encoding='utf-8') as f:
            f.writelines(contents)
        
    def VerifySignature(self, sha256hash):
        sha256 = hashlib.sha256()
        with open(self.filename, "rb") as f:
            byte = f.read(1)
            while byte.decode("utf-8") != '\x0A':
               byte = f.read(1)
          
            for block in iter(lambda: f.read(4096), b""):
                sha256.update(block)
                hash = sha256.hexdigest()
        
        return(hash==sha256hash)
        

def ValidateFileInput(checkname):
    if os.path.exists(checkname) != 1:
                    raise LookupError("File not found")
    if checkname.endswith(".gcode") != 1:
                    raise LookupError("ncorrect file extension")
    if os.stat(checkname).st_size == 0:
                    raise LookupError("File is empty")
    return(True)
