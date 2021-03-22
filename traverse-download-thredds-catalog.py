#!/usr/bin/env
"""
Traverse THREDDS catalog to locate files and download preserving directory structure
"""
import argparse
import requests
from bs4 import BeautifulSoup
import os
parser = argparse.ArgumentParser(description='Do something')
parser.add_argument('catalog_url', type=str, help='catalog path')
args = parser.parse_args()
rootCatalog = args.catalog_url
target = '2019/'
catalogs = [rootCatalog]

def prepCatalogUrl(catalog):
	url = catalog[:catalog.find('catalog.html')]
	return url

def readCatalogLinks(catalog,url):
	doc = requests.get(catalog)
	html_doc = doc.text
	soup = BeautifulSoup(html_doc, 'html.parser')
	table = soup.select('table')
	links = table[0].find_all('a')
	return links

def getUrls(links,url):
	for link in links:
		if '/catalog.html' in link.get('href'):
			directory = link.get('href')
			childCatalog = url+directory
			catalogs.append(childCatalog)
			print('Tranversing catalog: '+childCatalog)
		if 'catalog.html?' in link.get('href'):
			file = link.find('code').get_text()
			fileUrl = url+file
			fileServerPath = fileUrl.replace('/catalog/','/fileServer/')
			result = fileServerPath.find(target)
			outPath = fileServerPath[result:]
			curlFile(fileServerPath,outPath)

def curlFile(fileServerPath,outPath):
	print('Downloading file: '+fileServerPath)
	curl = f'curl --output {outPath} --create-dirs {fileServerPath}'
#	print(curl)
	os.system(curl) ### Uncomment to curl files ###

def main(rootCatalog):
	for c in catalogs:
		url = prepCatalogUrl(c)
		links = readCatalogLinks(c,url)
		getUrls(links,url)

if __name__ == '__main__':
    main(rootCatalog)
