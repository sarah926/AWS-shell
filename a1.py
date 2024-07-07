#!/usr/bin/env python3

#
#  Libraries and Modules
#
import configparser
import os 
import sys 
import pathlib
import boto3
import botocore
import subprocess
import shlex
import traceback
#var for storing the current directory
global directory
global bname
        
def listBuckets(command, s3):
    try:
        global bname
        global directory
        splitCommand = command.split()
        
        if(len(splitCommand) == 1):
            if(bname !=''):
                if(directory !=''):
                    response = s3.list_objects_v2(Bucket=bname, Prefix=directory)
                else:
                    response = s3.list_objects_v2(Bucket=bname)
                files = [obj['Key'] for obj in response.get('Contents')]
                for file in files:
                    print(file)
            else:
                buckets = []
                response = s3.list_buckets()
                for bucket in response['Buckets']:
                    buckets.append(bucket["Name"])
                for bucket in buckets:
                    print ( bucket )
        else:
            d = splitCommand[1][1:]
            response = s3.list_objects_v2(Bucket=d)
            files = [obj['Key'] for obj in response.get('Contents')]
            for file in files:
                print(file)
        return 0
        
    except:
        return 1
#creates a bucekt based on name provided
def createBuckets(bucketName, s3):
    try:
        #create a bucket with location of ca-central-1
        s3 = s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={'LocationConstraint': 'ca-central-1'})
        return 0
        
    except:
        #catches errors with bucket creation
        return 1

#copies a file to the cloud, takes the command the user entered as input
def copyFile( command):
    #split the command based on spaces
    splitCommand = command.split()
    
    try:
        #get name of file       
        splitFileName = splitCommand[2].split('/')
       
        # upload file to cloud - the args are path to file, bucket name, then the name of the file
        s3.upload_file(splitCommand[1], splitFileName[1], splitFileName[2])
        return 0
   
    except:
        # catches errors with uploading
        return 1
    
#changes directory based on command user entered
def changeDirectory(command):
    try:
        global directory
        global bname
        # split command based on spaces
        dirChange = command.split()

        # if entered .., go back to root
        if(dirChange[1] == '..'):
            directory = ''
            bname = ''
        # if entered /, go back to root as well
        elif(dirChange[1] == '/'):
            directory = ''
            bname = ''
        # if entered ../, go back one step
        elif(dirChange[1] == '../'):
            #if there is a directory, go back
            if(directory != ''):
                #split the directory based on /
                splitCurrDirectory = directory.split('/')
                #if more then one folder in the path, go back one
                if(len(splitCurrDirectory) > 1):
                    directory = directory[0:len(directory) - len(splitCurrDirectory[-1]) -1]
                    directory = "".join(splitCurrDirectory[:-1])
                #if only one folder, set directory to empty
                else:
                    directory = ''
            #if not a directory, just go back a bucket name
            else:
                bname = ''

        # if entered a bucket to move to, would start with a /
        elif(dirChange[1].startswith('/')):
            # split on /, set first to be the bucket name
            splitUpDirectoryEntered = dirChange[1].split('/')
            bname = splitUpDirectoryEntered[1]
            if(len(splitUpDirectoryEntered)>2):
                directory = "/".join(splitUpDirectoryEntered[2:])

        #if just entered a directory, go to it
        else:
            directory = dirChange[1]
        return 0
    except:
        return 1
    
#prints the directory
def printDirectory():
    try:
        global bname
        global directory
        # if both empty, print a /
        if(bname == '' and directory == ''):
            print('/')
        else:
            print(bname, ':')
        if(directory != ''):
            print(directory)
        return 0
    except:
        return 1
    
#
#  Find AWS access key id and secret access key information
#  from configuration file
#
config = configparser.ConfigParser()
config.read("S5-S3.conf")
#aws_access_key_id = config['prof']['aws_access_key_id']
#aws_secret_access_key = config['prof']['aws_secret_access_key']

aws_access_key_id = config['default']['aws_access_key_id']
aws_secret_access_key = config['default']['aws_secret_access_key']

try:
#
#  Establish an AWS session
#
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
#
#  Set up client and resources
#
    s3 = session.client('s3')
    s3_res = session.resource('s3')
#success connected message
    print ( "Welcome to the S3 Storage Demo - List Buckets" )
    print("You are now connected to your S3 storage")
    
    # init direcrory and bucket to be empty
    directory = ''
    bname = ''
    #loop to run the shell
    while(True):
        #shell starts with S5>
        command = input("S5> ")
        #quits loop if user enters exits
        if command == "exit" or command == "quit":
            break

        # copy files using command locs3cp
        elif command.startswith('locs3cp'):
            if(copyFile(command=command) == 1):
                print("unsuccessful copy ")

        #creating a bucket
        elif command.startswith('create_bucket'):
            try:
                bucketName = command.split('/')[1]
                if(createBuckets(bucketName= bucketName, s3=s3) == 1):
                    print("could not create bucket")
            except:
                print('invalid name for bucket')

        #changes the directory
        elif command.startswith('chlocn'):
            if(changeDirectory(command) == 1):
                print("cannot change folder")

        #prints current directory
        elif command.startswith('cwlocn'):
            printDirectory()

        #list buckets
        elif command.startswith("list"):
           if(listBuckets(command=command, s3=s3) == 1):
               print('cannot list contents of this s3 location')

        #everything else sent to the normal shell
        else:
            subprocess.run(shlex.split(command))
except:
    print ( "you could not be connected to your S3 storage")
