import requests
import sys
from urllib.request import urlretrieve
import urllib3


class Copier:
    def __init__(self, url):
        self.url = url
        self.req = None
        self.heads = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
        self.images = []
        pass

    def get_images(self):
        self.req = requests.get(self.url, headers=self.heads, verify=False)
        self.extract_images()
        pass

    def extract_images(self):
        line = []

        for l in self.req.text.split('\n'):
            if "ProofTable" in l and "jQ" not in l:
                line = l

        for l in line.split(' '):
            if l.startswith('src="//images'):
                self.images.append("http:%s" % l[5:-1])
        pass

    def save_images(self):
        for image in self.images:
            self.save(image)
            self.save_full(image)
        pass

    def save(self, image):
        urlretrieve(image, image[-15:].replace('/', ''))
        pass

    def save_full(self, image):
        image = image[:-5]+'.jpg'
        self.save(image)
        pass


def main():
    if len(sys.argv) != 2:
        print('%s "<url>"' % sys.argv[0])
        sys.exit(99)
    url = sys.argv[1]
    urllib3.disable_warnings()
    c = Copier(url)
    c.get_images()
    c.save_images()


if __name__ == "__main__":
    main()
