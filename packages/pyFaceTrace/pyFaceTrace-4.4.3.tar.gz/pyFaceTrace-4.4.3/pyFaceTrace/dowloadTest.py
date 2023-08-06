import zipfile
import os
import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    save_response_content(response, destination)    
def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None
def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
#======================================         
def Achive_Folder_To_ZIP(sFilePath):
    """
    input : Folder path and name
    output: using zipfile to ZIP folder
    """
    zf = zipfile.ZipFile(sFilePath + '.ZIP', mode='w')#只儲存不壓縮
    #zf = zipfile.ZipFile(sFilePath + '.ZIP', mode = 'w', compression = zipfile.ZIP_DEFLATED)#預設的壓縮模式
    os.chdir(sFilePath)
    #print sFilePath
    for root, folders, files in os.walk(".\\"):
        for sfile in files:
            aFile = os.path.join(root, sfile)
            #print aFile
            zf.write(aFile)
    zf.close()

if __name__ == "__main__":
    file_id = '1zmpZY5D5vNwcxhNmTgBprisevixexA4I'
    destination = 'train.zip'
    download_file_from_google_drive(file_id, destination)
    with zipfile.ZipFile(destination, mode='r') as myzip:
        for file in myzip.namelist():
            myzip.extract(file,'train')
    os.remove(destination)
    
#Achive_Folder_To_ZIP('train')


#
        