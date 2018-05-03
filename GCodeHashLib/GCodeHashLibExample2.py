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

from GCodeHashLib import GCodeSHA256Checksum,  GCodeMD5Checksum

def main():
    
    print("TEST5 - VERIFY SHA256 HASH - POST MOD")
    sha256cs = GCodeSHA256Checksum("SHA256_TestFile.gcode")
    eq = sha256cs.VerifySignature()

    print("HASHES EQUAL? = " + str(eq))

    print("TEST6 - VERIFY MD5 HASH - POST MOD")
    md5cs = GCodeMD5Checksum("SHA256_TestFile.gcode")
    eq = md5cs.VerifySignature()
    print("HASHES EQUAL? = " + str(eq))


    input("Hit Enter")
    
if __name__ == "__main__":
    main()
