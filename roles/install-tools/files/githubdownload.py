#!/usr/bin/env python3
# Description: Download a binary from Github releases.
# Known Issues:
# - Github ratelimit is 60 requests per hour for unauthenticated requests. Need to do better arg parsing, so we can grab multiple files off the same release. For example linpeas/winpeas makes two requests to grab metadata, when it could just make one.
# - Improve unarchiving releases. For example chainsaw has a zip with chainsaw/*. I put the location to /opt/ so it doesn't create /opt/chainsaw/chainsaw. Zip extract should handle this logic.
# Author: Ippsec
# Version: 1.0

import requests
import sys
import io
import os
import re
import tarfile, gzip, zipfile

def get_github_latest(repo):
    """
    Get the latest release metadata from Github, returns json.
    """
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_github_release_url(metadata, regex):
    """
    Get the url for the release file that matches the regex.
    Returns: URL of the Binary
    """
    try:
        regex = re.compile(regex)    
        for item in metadata["assets"]:
            if re.findall(regex, item["name"]):        
                return item["browser_download_url"]
        raise Exception("No matching file found")
    except Exception as e:
        raise Exception(e)

def get_http_binary_file(url):
    """
    Get the binary file from the url. 
    Returns: the binary file in a BytesIO Object.
    """
    response = requests.get(url)
    response.raise_for_status()
    return io.BytesIO(response.content)

def get_gzip_name(compressed_data):
    """
    Get the name of the file inside the gzip file.
    Returns: The name of the file. 
    """
    try:
        gzip_header = compressed_data.getvalue()[:10]
        if gzip_header.startswith(b"\x1f\x8b"):
            name = compressed_data.getvalue()[10:].split(b'\x00', 1)[0].decode("utf-8")
            return name        
        raise Exception("Unable to identify compression type")
    except Exception as e:
        raise Exception(e)
     
def extract_gz(compressed_data, output_directory, name=None):
    """
    Extract the gzip file.
    Returns: Nothing
    """
    try:
        if not name:
            name = get_gzip_name(compressed_data)
        with gzip.open(compressed_data, "rb") as gz:
            with open(output_directory + "/" + name, "wb") as f_out:
                f_out.write(gz.read())
    except Exception as e:
        raise Exception(e)

def extract_tar(compressed_data, out_file):
    """
    Extract the tar file from the gzip file.
    Returns: Nothing
    """
    try:
        gzip_header = compressed_data.getvalue()[:10]
        if gzip_header.startswith(b"\x1f\x8b"):
            with gzip.open(compressed_data, "rb") as gz:
                with tarfile.open(fileobj=gz, mode="r:gz") as tar:
                    tar.extractall(path=out_file)    
                    return
        else:
            raise Exception("Unable to identify compression type")
    except Exception as e:
        raise Exception(e)

def extract_zip(compressed_data, out_file):
    """
    Extract the zip file.
    Returns: Nothing
    """
    try:
        with zipfile.ZipFile(compressed_data, 'r') as zip_ref:
            # If there is only one folder in the zip, go into the folder then extract it        
            # dir = out_file.split("/")[-1] + "/"
            # if zip_ref.infolist()[0].filename == dir:
            #     zip_ref.start_dir = zip_ref.namelist()[0]                            
            zip_ref.extractall(out_file)
    except Exception as e:
        raise Exception(e)
    
    

def get_github_release(repo, regex, output_directory, name=None):
    """
    Get the latest release from Github and download the file that matches the regex.
    Returns: Nothing
    """
    try:
        verify_directory_exists(output_directory)
        metadata = get_github_latest(repo)
        url = get_github_release_url(metadata, regex)
        f_bytes = get_http_binary_file(url)
        
        if url.endswith(".tar.gz"):
            extract_tar(f_bytes, output_directory)
        elif url.endswith(".gz"):
            extract_gz(f_bytes, output_directory, name)
        elif url.endswith(".zip"):
            extract_zip(f_bytes, output_directory)
        else:
            if not name:
                # If no name is provided, use the name from the url.
                name = url.split("/")[-1]
            with open(output_directory + "/" + name, "wb") as f_out:
                f_out.write(f_bytes.read())   
    except Exception as e:
        raise Exception(e)

def verify_directory_exists(directory):
    """
    Verify that the directory exists, if not create it.
    Returns: Nothing
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except Exception as e:
        raise Exception(e)

if __name__ == "__main__":
    # get number of args
    if len(sys.argv) >= 4:
        repo = sys.argv[1]
        regex = sys.argv[2]
        output_directory = sys.argv[3]
        name = ''
    
        if len(sys.argv) == 5:
            name = sys.argv[4]

        try:            
            get_github_release(repo, regex, output_directory, name)
            sys.exit(0)
        except Exception as e:
            print(e)

    print("Usage: python gitdownload.py <repo> <regex> <output_directory> <name:optional>")    
    print("Example: python gitdownload.py jpillora/chisel _darwin_amd64.gz /tmp chisel_darwin_amd64")
    sys.exit(1)

