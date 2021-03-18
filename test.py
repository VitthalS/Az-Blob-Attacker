import os, uuid, sys
import requests
import datetime
import hmac
import hashlib
import base64
import urllib
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess

print ('''

     _                    ____    _           _                  _      _     _                    _                  
    / \     ____         | __ )  | |   ___   | |__              / \    | |_  | |_    __ _    ___  | | __   ___   _ __ 
   / _ \   |_  /  _____  |  _ \  | |  / _ \  | '_ \   _____    / _ \   | __| | __|  / _` |  / __| | |/ /  / _ \ | '__|
  / ___ \   / /  |_____| | |_) | | | | (_) | | |_) | |_____|  / ___ \  | |_  | |_  | (_| | | (__  |   <  |  __/ | |   
 /_/   \_\ /___|         |____/  |_|  \___/  |_.__/          /_/   \_\  \__|  \__|  \__,_|  \___| |_|\_\  \___| |_|   
                                                                                                                      
Created By https://github.com/VitthalS

''')

print ('''

	How to Run: python az-blob-attacker.py

	1. Get Container Names
	2. Get Blob Names
	3. Download all Blobs
	4. Upload blob

	''')

name = input("Enter Account Name: ") 
key = input("Enter Account Key: ") 


def get_container():
	try:
		blob_service = BlockBlobService(account_name=name, account_key=key)
		containers = blob_service.list_containers() 
		for container in containers: 
			print ("Following are the containers in your account: ")
			print ("Name: {}".format(container.name))
	except Exception as e:
		print(e)

def get_blobs():
	try:
		container_name =input ("Enter Container Name to List the blobs: ")
		block_blob_service = BlockBlobService(account_name=name , account_key=key)
		generator = block_blob_service.list_blobs(container_name)
		for blob in generator:
			print(blob.name)
	except Exception as e:
		print(e)


def download_blobs():
	try: 
		container_name =input ("Enter Container Name to Download the blobs: ")
		block_blob_service = BlockBlobService(account_name=name , account_key=key)
		generator = block_blob_service.list_blobs(container_name)
		for blob in generator:
			print(blob.name)
			print("{}".format(blob.name))
			if "/" in "{}".format(blob.name):
				print("there is a path in this")
				head, tail = os.path.split("{}".format(blob.name))
				print(head)
				print(tail)
				if (os.path.isdir(os.getcwd()+ "/" + head)):
					print("directory and sub directories exist")
					block_blob_service.get_blob_to_path(container_name,blob.name,os.getcwd()+ "/" + head + "/" + tail)
					print("directory doesn't exist, creating it now")
					os.makedirs(os.getcwd()+ "/" + head, exist_ok=True)
					print("directory created, download initiated")
					block_blob_service.get_blob_to_path(container_name,blob.name,os.getcwd()+ "/" + head + "/" + tail)
			else:
				block_blob_service.get_blob_to_path(container_name,blob.name,blob.name)
	except Exception as e:
		print(e)




def run_blobupload():
    try:
        
        block_blob_service = BlockBlobService(account_name=name, account_key=key)
        container_name = input ("Enter Container Name: ")
        block_blob_service.create_container(container_name)
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
        local_path=os.path.abspath(os.path.curdir)
        local_file_name =input("Enter file name to upload : ")
        full_path_to_file =os.path.join(local_path, local_file_name)
        print("Temp file = " + full_path_to_file)
        print("\nUploading to Blob storage as blob" + local_file_name)
        block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)
        print("\nList blobs in the container")
        generator = block_blob_service.list_blobs(container_name)
        for blob in generator:
            print("\t Blob name: " + blob.name)

    
    except Exception as e:
        print(e)


# Main method.
if __name__ == '__main__':

	number = input ("Type the number to execute: ")
	if number == '1' :
		get_container()
	elif number == '2' :
		get_blobs()
	elif number == '3' :
		download_blobs()
	elif number == '4' :
		run_blobupload()
	else :
		print ('Enter valid number')



