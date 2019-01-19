import subprocess
import hashlib
import mimetypes
import io

def computeMD5hash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

targetFilePath    = "/home/student/A1/secret_file.aes256.txt"
johnCmd           = ["./john", "--wordlist=password.lst", "--stdout", "--rules:Single"]
proc              = subprocess.Popen(johnCmd, stdout=subprocess.PIPE)
candidatePassword = ""
attempt           = 0

print("Cracking...")

for line in iter(proc.stdout.readline,b''):
    attempt          += 1
    candidatePassword = line.rstrip('\n')
    candidateMd5      = computeMD5hash(candidatePassword)
    opensslCmd        = ["openssl", "enc", "-base64", "-in", targetFilePath, "-out", "output.txt", "-d", "-aes256", "-pass", "pass:"+candidateMd5+""]

    try:
        decodeResult = subprocess.check_output(opensslCmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        continue
    try:
	print("Current attempt: " + str(attempt))
	print("Current candidate:" + candidatePassword)
        output = io.open("output.txt", "r", encoding="utf_8")
	print(output.read())
    except UnicodeDecodeError:
	continue
    break;

print("Done")
print("Password is: " + candidatePassword)

