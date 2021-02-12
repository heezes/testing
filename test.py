import pygit

pygit.repos()
r = pygit.load('testing')
r.message = "Hello from testing/main.py"
file = open("testFile.txt", 'w')
file.write("Whatsup?")
file.close()
r.stage_and_commit()
r.push()
