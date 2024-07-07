# AWS-shell
Created a shell that allows users to run processes connected with AWS.
Commands supported include:
- chlocn : change location in the cloud
- create_bucket: create a bucket in the cloud
- cwlocn: print contents of current location
- locs3p: copy files over from your computer to the cloud
- list: lists all buckets
- exit or quit: ends the process

All other commands are run through the default shell using a subprocess.
  
This was a project for cloud computing, CIS4010. This code was developed on a Mac system.
In order to run, the user needs a file called 'S5-S3.conf' with access key information to AWS in this format:
[default]
aws_access_key_id = 
aws_secret_access_key = 

# to run, type python or python3 and the name of the file 'a1.py', into the command line, an example:
python3 a1.py

# for uploading a file with locs3cp, must include full pathname to the item uploading or be in the currect directory
# must run commands as listed in the assignment document, aka
  - locs3cp fileName /bucket/filename or
  - locs3cp /pathtoFile/fileName /bucket/filename
