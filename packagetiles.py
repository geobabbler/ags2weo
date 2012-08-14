import os
import sys
import tarfile

target = sys.argv[1]
parent = os.path.abspath(os.path.join(target, os.path.pardir))
print parent

#iterates a directory tree, returning subdirectories and files
#some_dir = top level directory
#level = iteration depth
def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

tar = tarfile.open(parent + "\\xyz.tar.gz", "w:gz")
for subdir, dirs, files in walklevel(target, 3):
    for file in files:
        fname = subdir + "\\" + file
        aname = fname.replace(parent, "") #ensures top level folder in tar is 'xyz'
        tar.add(fname, arcname=aname)
tar.close()

