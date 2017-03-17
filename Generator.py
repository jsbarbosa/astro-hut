from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = {}
        self.inLink = False
        self.lasttag = None
        self.lastvalue = None
    def handle_starttag(self, tag, attrs):
        self.inLink = False
        self.lasttag = tag
        self.lastvalue = None
        if tag == "a":
           for name, value in attrs:
               if name == "href" and "http" in value and "mozilla" not in value and "ubuntu" not in value and "debian" not in value:
                   self.inLink = True
                   self.lastvalue = value

    def handle_endtag(self, tag):
        if tag == "a":
            self.inlink = False

    def handle_data(self, data):
        if self.inLink and self.lasttag == "a" and  data.strip() and self.lastvalue != None:
            self.data[data] = self.lastvalue

with open("bookmarks.html", "r") as f:
	text = f.readlines()
	text = "".join(text)

text = text.replace("&#39;", "")
parser = MyHTMLParser()
parser.feed(text)
data = parser.data

text = ""
for key in data:
    text += "-[%s](%s)\n\n"%(key, data[key])

with open("README.md", "w") as f:
    f.write(text)
