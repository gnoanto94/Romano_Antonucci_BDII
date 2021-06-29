import urllib.request

with open("dblinks.txt") as f:
    url_list = f.readlines()
    url_list = [x.strip() for x in url_list] 

f = open("output.txt", 'w')

counter = 0

for url in url_list:
    
    uf = urllib.request.urlopen(url)
    html = uf.read()
    html = str(html)

    startindex = html.find("<p>") + 3
    endindex = html.find("</p>")

    result = html[startindex:endindex]

    print("getting info from link number " + str(counter))
    counter = counter+1

    f.write(result+"\n"+"\n")