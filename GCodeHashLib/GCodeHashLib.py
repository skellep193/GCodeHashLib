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

#   Author: Patrick Skelley <pskelley@albany.edu>, Jenny Chen <>, University at Albany (SUNY), Albany NY
#   Purpose: Library embeds MD5 and SHA256 checksums within gcode files for pre-print validation purposes
#
#   Revision History
#   1.0: Initial Release - 04/29/2018

import hashlib
import os

#   Author: Patrick Skelley, Jenny Chen
#   Parent Class for algorithm specific hash classes
class GCodeChecksum:
    
    #Author: Patrick Skelley
    # Purpose: Verifies the hash embedded within the gcode file matches that of the hash generated against the file content
    def VerifySignature(self):
        with open(self.filename,  "r") as f:
            firstLine = f.readline()
            tokens = firstLine.split("=")
            #print(tokens)
            existingHash = tokens[1].rstrip()
            hashAlg = tokens[0]
            
        if hashAlg.endswith("MD5"):
            hashOp = hashlib.md5()
        elif hashAlg.endswith("SHA256"):
            hashOp = hashlib.sha256()
        else:
            raise "Unknown hash algorithm"
            
        with open(self.filename, "rb") as f:
            byte = f.read(1)
            while byte.decode("utf-8") != '\x0A':
               byte = f.read(1)
          
            for block in iter(lambda: f.read(4096), b""):
                hashOp.update(block)
            hash = hashOp.hexdigest()
            #print(hash)
        return(hash==existingHash)

    # Author: Jenny Chen
    # Purpose: Performs checks on provided file path. Confirms existence, extension, and content.
    def ValidateFileInput(checkname,  extension):
        if os.path.exists(checkname) != 1:
                        raise LookupError("File not found")
        if checkname.endswith(extension) != 1:
                        raise LookupError("ncorrect file extension")
        if os.stat(checkname).st_size == 0:
                        raise LookupError("File is empty")
        return(True)

#   Author: Patrick Skelley
#   Purpose: Class for generating and embedding MD5 checksum in g-code files
class GCodeMD5Checksum(GCodeChecksum):
    def __init__(self,  filename):
        GCodeChecksum.ValidateFileInput(filename, ".gcode")
        self.filename = filename
    
    # Purpose: Generates and embeds MD5 signature
    def ApplySignature(self):
        md5 = hashlib.md5()
        with open(self.filename, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
               md5.update(block)
            hash = md5.hexdigest()
        
        with open(self.filename, "r+",encoding='utf-8') as f:
            contents = f.readlines()
            contents.insert(0,";GCODEHASHLIB_MD5=" + hash + "\n") 
            
        with open("MD5_" + self.filename,  "w") as f:
            f.writelines(contents)
        
        return hash
        
#   Author: Patrick Skelley
#   Purpose: Class for generating and embedding SHA256 checksum in g-code files
class GCodeSHA256Checksum(GCodeChecksum):
    def __init__(self,  filename):
        GCodeChecksum.ValidateFileInput(filename, ".gcode")
        self.filename = filename
    
    # Purpose: Generates and embeds SHA256 signature
    def ApplySignature(self):
        
        sha256 = hashlib.sha256()
        with open(self.filename, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
               sha256.update(block)
            hash = sha256.hexdigest()
        
        with open(self.filename, "r+",encoding='utf-8') as f:
            contents = f.readlines()
            contents.insert(0,";GCODEHASHLIB_SHA256=" + hash + "\n") 
            
        with open("SHA256_" + self.filename,  "w") as f:
            f.writelines(contents)

        return hash
