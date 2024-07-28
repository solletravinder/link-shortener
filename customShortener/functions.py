def get_link(url):
    if url:
        if 'http://' in url:
            new_url = url.split('http://')[1]
        elif 'https://' in url:
            new_url = url.split('https://')[1]
        elif 'ftp://' in url:
            new_url = url.split('ftp://')[1]
        else:
            new_url = url
        if new_url:
            if 'www.' in new_url:
                url = new_url.split('www.')
                if len(url) == 2:
                    url = url[1]
                else:
                    url = url[2]
            else:
                url = new_url
        return url
    else:
        return None