from crawler import *


def main():
    crawler = HTMLCrawler('http://0.0.0.0:3000', '/Users/jenkins/Development/TMP/BambuSolar')

    print('Starting crawler')

    crawler.run('staging', 'beta', '1.0.0')


if __name__ == '__main__':
    main()
