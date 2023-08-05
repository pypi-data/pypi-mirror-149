# -*- coding: utf-8 -*-
MNAME='utilmy.util_download'
"""# 
Doc::
 Download utilities


"""
import os, glob, sys, time, json, functools, random, yaml, gc, copy, requests, shutil
import pandas as pd, numpy as np
from pathlib import Path; from collections import defaultdict, OrderedDict
from typing import List, Optional, Tuple, Union  ; from numpy import ndarray
from box import Box



#############################################################################################
from utilmy import log, log2
def help():
    """function help        """
    from utilmy import help_create
    print( help_create(MNAME) )



#############################################################################################
def test_all() -> None:
    """function test_all   to be used in test.py         """
    log(MNAME)
    test1()


def test1() -> None:
    """function test1
    """
    d = Box({})
    dirtmp ="./ztmp/"




#############################################################################################
def download_github(url="https://github.com/arita37/dsa2_data/blob/main/input/titanic/train/features.zip", 
                   dirout="./ztmp/"):
    """Fetch dataset from a given URL and save it.
    Code::

        url:  URL https://github.com/arita37/dsa2_data/raw/main/input/titanic/train/features.zip   
        dirout: Path to save files
        
        https://raw.githubusercontent.com/arita37/dsa2_data/tree/main/input/titanic/train/features.zip
        https://github.com/arita37/dsa2_data/blob/main/input/titanic/train/features.zip

    """
    from tempfile import mktemp, mkdtemp
    from urllib.parse import urlparse, parse_qs
    import pathlib, requests

    supported_extensions = [ ".zip" ]

    dirout = dirout.replace("\\", "/")
    os.makedirs(dirout, exist_ok=True)

    # urlx = url.replace(  "github.com", "raw.githubusercontent.com" )
    urlx = url.replace("/blob/", "/raw/")
    urlx = urlx.replace("/tree/", "/raw/")
    log(urlx)


    urlpath = urlx.replace("https://github.com/", "github_")
    urlpath = urlpath.split("/")
    fpath = "-".join(urlpath[:-1])[:-1]   ### prefix path normalized

    fname = urlpath[-1]  ## filaneme
    # assert "." in fname, f"No filename in the url {urlx}"

    dirout2 = dirout
    os.makedirs(dirout2, exist_ok= True)
    fileout_fullname = os.path.abspath( dirout2 + "/" + fname )
    log('#### Download saving in ', fileout_fullname)

    with requests.Session() as s:
        res = s.get(urlx)
        if res.ok:
            print(res.ok)
            with open(fileout_fullname, "wb") as f:
                f.write(res.content)
        else:
            raise res.raise_for_status()
    return fileout_fullname



def download_google(url_or_id="https://drive.google.com/file/d/1iFrhCPWRITarabHfBZvR-V9B2yTlbVhH/view?usp=sharing" , 
                    fileout="./ztmp/", unzip=True ):
      """Download  file from google drive on disk + unzip.
      Code::
          url_or_id: "https://drive.google.com/file/d/1iFrhCPWRITarabHfBZvR-V9B2yTlbVhH/view?usp=sharing"

          ### Using file
              download_google(url_or_id="https://drive.google.com/file/d/1iFrhCPWRITarabHfBZvR-V9B2yTlbVhH/view?usp=sharing" , fileout="./ztmp/", unzip=True )
              download_google(url_or_id="16MIleqoIr1vYxlGk4GKnGmrsCPuWkkpT", fileout="./ztmp/", unzip=True )

          ## Using Folder
              download_google(url_or_id="https://drive.google.com/drive/folders/15uNXeRBIhVvZJIhL4yTw4IsStMhUaaxl",  fileout="./ztmp/", unzip=True )

      """
      import gdown, shutil, os, glob, time
      fileout = os.path.abspath(fileout)
      fileout = fileout.replace("\\","/")

      tag = url_or_id
      if "https:" in  url_or_id:
        #yyyymmdd = time.strftime("%Y%m%d")
        tag =  str(hash(url_or_id))

      dirout2 = fileout + f"/gdown_{tag}/"
      os.makedirs(dirout2, exist_ok=True)
      dir_cur = os.getcwd()

      os.chdir(dirout2)


      try :
        if 'folder' in url_or_id:
            gdown.download_folder(url_or_id, quiet=False, use_cookies=False)
        else :
            isfuzzy = True if '?usp=sharing' in url_or_id else False
            gdown.download(url_or_id,  quiet=False, fuzzy=isfuzzy)

        flist = glob.glob(dirout2 + "/*")
        print('Files downloaded', flist)

        if unzip:
          for fi in flist :
            shutil.unpack_archive(fi, fileout)
      except Exception as e:
        print(e)

      os.chdir(dir_cur)
      return fileout



def download_custom_pageimage(query, fileout="query1", genre_en='', id0="", cat="", npage=1) :
    """ Donwload one page
    Code::
    
        python  "$utilmy/util_download.py" download_page_image   --query 'メンス+ポロシャツ'    --dirout men_fs_blue


    """
    import time, os, json, csv, requests, sys, urllib
    from bs4 import BeautifulSoup as bs
    from urllib.request import Request, urlopen
    import urllib.parse


    path = os.path.abspath(fileout + "/")
    path = path.replace("\\", "/")
    os.makedirs(path, exist_ok=True)
    # os.chdir(path)

    query2     = urllib.parse.quote(query, encoding='utf-8')
    url_prefix = 'httpl/' + query2
    ### https://search.rakuten.co.jp/search/mall/%E3%83%A1%E3%8384+blue+/?p=2
    print(url_prefix)
    print(path)

    csv_file   = open( path + 'ameta.csv','w',encoding="utf-8")
    csv_writer = csv.writer(csv_file, delimiter='\t')
    csv_writer.writerow(['path', 'id0', 'cat', 'genre_en', 'image_name', 'price','shop','item_url','page_url',  ])

    page  = 1
    count = 0
    while page < npage+1 :
        try:
            url_page = url_prefix  + f"/?p=+{page}"
            req    = Request(url=url_page)
            source = urlopen(req).read()
            soup   = bs(source,'lxml')

            print('page', page, str(soup)[:5], str(url_page)[-20:],  )

            for individual_item in soup.find_all('div',class_='searchresultitem'):
                count += 1
                save = 0
                shopname     = 'nan'
                count_review = 'nan'

                for names in individual_item.find_all('div',class_='title'):
                    product_name = names.h2.a.text
                    break

                for price in individual_item.find_all('div',class_='price'):
                    product_price = price.span.text
                    product_price = product_price .replace("円", "").replace(",", "") 
                    break
                
                for url in individual_item.find_all('div',class_='image'):
                    product_url = url.a.get('href')
                    break

                for images in individual_item.find_all('div',class_='image'):
                    try:
                        product_image = images.a.img.get('src')
                        urllib.request.urlretrieve(product_image, path + str(count)+".jpg")
                        # upload_to_drive(str(count)+'.jpg')
                        count += 1
                        break
                    except:
                        save = 1
                        print(product_image + " Error Detected")
                    
                for simpleshop in individual_item.find_all('div',class_='merchant'):
                    shopname = simpleshop.a.text
                    break

                for review in individual_item.find_all('a',class_='dui-rating-filter'):
                    count_review = review.text

                if save == 0:
                    csv_writer.writerow([str(count)+'.jpg', id0, cat, genre_en,  
                        product_name, product_price, shopname, product_url, url_page, ])

        except Exception as e :
            print(e)
            time.sleep(2)
            continue

        page += 1

    print("Success", page-1, count)




################################################################################################################
def donwload_and_extract(url, dirout='./ztmp/', unzip=True):
    """Donwload on disk the tar.gz file
    Args:
        url:
        dirout:
    Returns:

    """
    import wget
    log(f"Donwloading mnist dataset in {dirout}")
    os.makedirs(dirout, exist_ok=True)
    wget.download(url, dirout)
    tar_name = url.split("/")[-1]
    if unzip :
       dirout2  = dirout + "/" + tar_name.split(".")[0] +"/"
       os_extract_archive(dirout + "/" + tar_name, dirout2)
       log2(dirout)
       return dirout2
    log2(dirout)
    return dirout + tar_name



def os_extract_archive(file_path, dirout="./ztmp/", archive_format="auto"):
    """Extracts an archive if it matches tar, tar.gz, tar.bz, or zip formats.
    Args:
        file_path: path to the archive file
        dirout: path to extract the archive file
        archive_format: Archive format to try for extracting the file.
            Options are 'auto', 'tar', 'zip', and None.
            'tar' includes tar, tar.gz, and tar.bz files.
            The default 'auto' is ['tar', 'zip'].
            None or an empty list will return no matches found.
    Returns:
        True if a match was found and an archive extraction was completed,
        False otherwise.
    """
    import tarfile, zipfile


    if archive_format == "auto":
        archive_format = ["tar", "zip"]
    if isinstance(archive_format, str):
        archive_format = [archive_format]

    file_path = os.path.abspath(file_path)
    dirout    = os.path.abspath(dirout)

    for archive_type in archive_format:
        if archive_type == "tar":
            open_fn     = tarfile.open
            is_match_fn = tarfile.is_tarfile

        elif archive_type == "zip":
            open_fn     = zipfile.ZipFile
            is_match_fn = zipfile.is_zipfile
        else :
            continue

        if is_match_fn(file_path):
            with open_fn(file_path) as archive:
                try:
                    archive.extractall(dirout)
                except (tarfile.TarError, RuntimeError, KeyboardInterrupt):
                    if os.path.exists(dirout):
                        if os.path.isfile(dirout):
                            os.remove(dirout)
                        else:
                            shutil.rmtree(dirout)
                    raise
            return True
    return False



def to_file(s, filep):
    """function to_file
    Args:
        s:
        filep:

    Returns:

    """
    with open(filep, mode="a") as fp:
        fp.write(str(s) + "\n")


def download_with_progress(url, fileout):
    """
    Downloads a file with a progress bar
    url: url from which to download from
    :fileout: file path for saving data
    """
    import tqdm
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    with tqdm.wrapattr(open(fileout, "wb"), "write",
                       miniters=1, desc=url.split('/')[-1],
                       total=int(response.headers.get('content-length', 0))) as fout:
        for chunk in response.iter_content(chunk_size=4096):
            fout.write(chunk)






### Aliass
unzip_file = os_extract_archive





###############################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()



