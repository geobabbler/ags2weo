"""
The MIT License

Copyright (c) 2012 William Dollins (bill@geomusings.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
This script converts an Esri-structured tile cache ("Level/Row/Column") to
an WeoGeo tile pack (z/y/x) using file system operations.
"""

import os
import sys
import shutil

path = "C:\Workspace"
initlevel = 0
root = ""
dest = ""

#creates directory if it doesn't exist
def ensure_dir(f):
    if not os.path.exists(f):
        os.makedirs(f)

#converts Esri "level" to appropriate zoom level
def getZ(level):
    fldr = level.replace("L", "")
    val = int(fldr) + initlevel #add user-provided initial zoom level
    return val

#converts Esri "Row" to Y value
def getY(row):
    hex = row.replace("R", "0x")
    val = int(hex, 0) #unroll hex notation used by Esri
    return val

#converts Esri "Column" to X value
def getX(column):
    hex = column.replace("C", "0x")
    val = int(hex, 0) #unroll hex notation used by Esri
    return val

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def main():
    global path
    global initlevel
    global root
    global dest
    
    argv = sys.argv
    top = argv[1]
    path = top
    root = os.path.dirname(path)
    dest = root + "\\" + "xyz"
    ensure_dir(dest)
    start = argv [2]
    initlevel = int(start)
    getLevels(top)

def getLevels(top):
    for subdir, dirs, files in walklevel(top, 0):
        for dir in dirs:
            z = getZ(dir)
            lpath = subdir + "\\" + str(dir)
            zpath = dest + "\\" + str(z)
            ensure_dir(zpath)
            print "Processing zoom level " + str(z)
            getRows(lpath, zpath)

def getRows(lpath, zpath):
    for subdir, dirs, files in walklevel(lpath, 0):
        for dir in dirs:
            y = getY(dir)
            rpath = subdir + "\\" + str(dir)
            ypath = zpath + "\\" + str(y)
            ensure_dir(ypath)
            getFiles(rpath, ypath)

def getFiles(rpath, ypath):
    for subdir, dirs, files in walklevel(rpath, 0):
        for file in files:
            finfo = os.path.splitext(file)
            x = getX(finfo[0])
            xfile = str(x) + finfo[1]
            cfilepath = subdir + "\\" + file
            xfilepath = ypath + "\\" + xfile
            shutil.copy2(cfilepath, xfilepath)
            
main()
