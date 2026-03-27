#os - works with paths as strings
#1.1
import os
print(os.getcwd())        # get current working directory
os.chdir("folder_name")   # change directory

#1.2
import os
print(os.listdir())       # list files in current dir
print(os.listdir("path")) # list files in specific dir

#1.3
import os
os.mkdir("new_folder")        # create one folder
os.makedirs("a/b/c")          # create nested folders

os.rmdir("new_folder")        # remove empty folder
os.removedirs("a/b/c")        # remove nested folders

#1.4
import os
os.remove("file.txt")     # delete file
os.rename("old.txt", "new.txt")  # rename file

#1.5
import os
path = "folder/file.txt"

print(os.path.exists(path))  # True/False
print(os.path.isfile(path))  # is file?
print(os.path.isdir(path))   # is directory?

print(os.path.join("folder", "file.txt"))  # safe path join

#1.6
import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")


#shutil - works on files & directories
#2.1 
import shutil
shutil.copy("file.txt", "copy.txt")     # copy file
shutil.copy2("file.txt", "copy.txt")    # copy with metadata

#2.2
import shutil
shutil.copytree("src_folder", "dst_folder")

#2.3
import shutil
shutil.move("file.txt", "folder/file.txt")

#2.4
import shutil
shutil.rmtree("folder")   # delete non-empty folder 

#2.5
total, used, free = shutil.disk_usage("/")
print(f"Free space: {free}")


#pathlib - object-oriented
#3.1
from pathlib import Path
p = Path("folder/file.txt")

#3.2
print(p.name)       # file.txt
print(p.stem)       # file
print(p.suffix)     # .txt
print(p.parent)     # folder

#3.3
p.exists()
p.is_file()
p.is_dir()

#3.4
Path("new_folder").mkdir()
Path("a/b/c").mkdir(parents=True, exist_ok=True)

#3.5
p.write_text("Hello")     # write text
print(p.read_text())      # read text
p.unlink()                # delete file

#3.6
for file in Path(".").iterdir():
    print(file)

#3.7
for file in Path(".").glob("*.txt"):
    print(file)


#example
from pathlib import Path
import shutil

folder = Path("data")
folder.mkdir(exist_ok=True)

file = folder / "test.txt"
file.write_text("Hello world")

shutil.copy(file, folder / "copy.txt")

for f in folder.iterdir():
    print(f)

file.unlink()