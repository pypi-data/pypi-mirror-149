from urllib.parse import urlparse

def split_datalake_url(datalake_url):
    # Parsing the URL
    parsed_url = urlparse(datalake_url)
    # Directory and file is in the PATH of the url
    datalake_path = parsed_url.path.rstrip('/')
    # Splitting on the last /
    split_path = datalake_path.rsplit('/',1)
    directory_with_root=split_path[0]
    directory = directory_with_root.split('/', 2)[2]
    filename=split_path[1]
    return directory, filename
