import urllib
import urllib2
import re

global dir
dir = "C:/Users/User/Downloads/Instagram/" ## destination directory

def downloadimg(data): ## finds the element with og:image and greps and retrives URL of image
    img = "og:image"
    for line in data:
        if re.search(img, line):
            imageline = line
            image = re.search("(?P<url>https?://[^\s]+)\?", imageline).group(1)
            urllib.urlretrieve(image, dir + re.sub("https.*/.*/.*/.*/","",image))

def downloadvid(data): ## finds the element with og:video and greps and retrives URL of video
    vid = "og:video:secure_url"
    for line in data:
        if re.search(vid, line):
            videoline = line
            video = re.findall("https://.*\.mp4", videoline)
            video = video[0]
            urllib.urlretrieve(video, dir + re.sub('https://.*/','',video))

## TODO: find a better way of doing this
urls = """https://www.instagram.com/p/BMxJzNMj3K0/
https://www.instagram.com/p/BMxC80_DyXG/
https://www.instagram.com/p/BMwZj7_jhq_/"""

urls = urls.split('\n')

for url, count in zip(urls, range(1,len(urls)+1)):
    print "Downloading ", count , " of " , len(urls)
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError as err:
        if err.code == 404:
            print "404 not found. Account may be private"
            continue
    data = response.read()
    data = data.split('\n')
    if re.search('og:video', str(data)):
        downloadvid(data)
    else:
        downloadimg(data)
