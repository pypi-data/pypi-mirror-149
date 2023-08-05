from nturl2path import url2pathname
from urllib.parse import urlparse, unquote_plus
from concurrent.futures import wait
import concurrent.futures
import requests
import click
import os
import shutil
import sys

def create_temp_folder():
    folder_name="zapper_temp"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def cleanup_temp_folder():
    folder_name="zapper_temp"
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)


def check_range_header(url):
    try:
        rv = requests.head(url)
        support_concurrency= True
    except:
        click.secho("Url is invalid or not reachable", fg="red")
        sys.exit(1)
    if rv.status_code != 200:
        click.secho("Url is invalid or not reachable", fg="red")
        sys.exit(1)
    for header in ["Content-Length", 'Content-Type']: 
        if header not in rv.headers.keys(): 
            click.secho("File can not be downloaded", fg="red")
            sys.exit(1)
    click.secho(f"Metadata about the file ")

   


    print(f"File Type {rv.headers['Content-Type']}")
    print(f'File Size {int(rv.headers["Content-Length"])//(1024*1024)} MB')
    if 'Accept-Ranges' not in rv.headers:
        print(f"File does not support concurrent downloading", fg="yellow")
        print(f"Normal downloading will be used", fg="yellow")
        support_concurrency= False
    

    cleaned_url = unquote_plus(url)
    parsed_url=urlparse(cleaned_url)
    filename=parsed_url.path.rsplit("/", 1)[1]
    print(f"File name {filename}")

    return int(rv.headers["Content-Length"]), filename, support_concurrency
 
def ranged_download(z):
    url, temp_name, start_range, end_range = z
    headers = {"Range": f"bytes={start_range}-{end_range}"}
    rv = requests.get(url, headers=headers, stream=True)
    label_text = "Downloading file "
    fill_char = click.style("#", fg="green")
    empty_char = click.style("-", fg="white", dim=True)
    length = end_range-start_range

    with open(temp_name, "wb") as file:
        label_text = f"Downloading file part  {temp_name}"
        fill_char = click.style("#", fg="green")
        empty_char = click.style("-", fg="white", dim=True)
        chunk_size = length//100
        with click.progressbar(length=length,
            label=label_text,
            fill_char=fill_char,
            empty_char=empty_char) as progress_bar:
            temp=0
            for data in rv.iter_content(chunk_size):
                temp+=chunk_size
                progress_bar.update(temp)
                file.write(data)

def parts_aggregator(files, filename):
    label_text = f"Aggregating files into  {filename[:10]}... {filename[-10:]}"
    fill_char = click.style("#", fg="green")
    empty_char = click.style("-", fg="white", dim=True)
    
    with open(filename, "wb") as file:
        with click.progressbar(files,
            label=label_text,
            fill_char=fill_char,
            empty_char=empty_char) as files:
            for d in files:
                with open(d, "rb") as temp_file:
                    z=file.write(temp_file.read())
                   


def single_file_download(url, filename, length):
    rv = requests.get(url, stream=True)

    label_text = f"Downloading file {filename[:10]}... {filename[-10:]}"
    fill_char = click.style("#", fg="green")
    empty_char = click.style("-", fg="white", dim=True)
    chunk_size = length//100


    with open(filename, "wb")as file:
       
        with click.progressbar(length=length,
            label=label_text,
            fill_char=fill_char,
            empty_char=empty_char) as progress_bar:
            temp=0
            for data in rv.iter_content(chunk_size):
                temp+=chunk_size
                progress_bar.update(temp)
                
                file.write(data)

def download_concurrently(url,filename, content_length, concurrency=3):
 
    create_temp_folder()
    output_file = os.path.join("zapper_temp", "temp")
    split = content_length // concurrency
    file_ranges = []
    file_count=0
    for i in range(0,content_length, split+1):
        ct = i+split
        if i+split > content_length:
            ct = content_length
        file_ranges.append((url, output_file+str(file_count), i,ct))
        file_count+=1

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(ranged_download, file_ranges)

    parts_aggregator(map(lambda x: x[1], file_ranges), filename)
    cleanup_temp_folder()

    click.secho(f"{filename} downloaded successfully.")


def process_file(url, concurrency =4):
    filesize, filename, support_concurrency = check_range_header(url)

    if support_concurrency and concurrency >1 :
        
        download_concurrently(url, filename, filesize,concurrency)
    else:
        single_file_download(url, filename, filesize)


if __name__=="__main__":
    url ="https://www.ibrahimabah.com/ibfilms/Harry.Potter-The.Ultimate.Collection.%20I%20-%20VIII%20.%202001-2011.1080p.Bluray.x264.anoXmous/Harry%20Potter%201/Harry.Potter.And.The.Sorcerers.Stone.2001.UEE.1080p.Bluray.x264.anoXmous_.mp4"
    
    process_file(url, 10)

