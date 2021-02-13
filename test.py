import sh
import os

git = sh.git.bake(_cwd='/home/pi/Desktop/testing')
file = open("testFile.txt", 'w')
file.write("Whatsup?")
file.close()
git.add("-A")
git.commit(m="Git push from script Yay!")
git.push()
