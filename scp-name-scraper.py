from bs4 import BeautifulSoup
import urllib2
import re

def get_pages(URL_FILE):
    contents = []
    f = open(URL_FILE, 'r')
    for url in f:
        response = urllib2.urlopen(url)
        contents.append(response.read())
    f.close()
    return contents

def parse_SCP(line):
    # Make sure we've got the right line
    line = str(line)
    num, name = None, None
    if re.search("SCP-[0-9]+", line):
        soup = BeautifulSoup(line)
        num = soup.a.contents[0]
        name = soup.li.contents[1].strip(" - ")
        if not name:
            # There's a few special cases
            # Things wrapped in spans, em for extra formatting, etc
            print num, soup.li.contents
            # We don't bother stripping them - preserve the tags for formatting
            name = soup.li.contents[2]
    return (num, name)

def parse_page(page):
    soup = BeautifulSoup(page)
    series = soup.select("div.series ul li")
    series_tuples = []
    for SCP in series:
        num, name = parse_SCP(SCP)
        if num != None:
            series_tuples.append((num, name))
    return series_tuples

def write_dict(SCP_list):
    f = open("SCP_dict.js", "w")
    f.write("var scp_names = {\n")
    for series in SCP_list:
        for SCP in series:
            f.write("\"%s\": \"%s\",\n" %
                    (SCP[0].encode("UTF-8"),
                    SCP[1].encode("UTF-8").replace("\"", "\\\"")))
    f.write("};");
    f.close()

# Note that URLs must begin with http://
URL_FILE = 'urls'
pages = get_pages(URL_FILE)
SCP_list = []
for page in pages:
    SCP_list.append(parse_page(page))

write_dict(SCP_list)
