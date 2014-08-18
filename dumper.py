#!/usr/bin/env python

'''
Python script to download 1280x720 Matroska videos from NRK based on web url
Require Python2, BeautifulSoup, Requests and libav-tools to be installed

Install them as follows:

$ sudo apt-get install libav-tools
$ sudo pip install BeautifulSoup4
$ sudo pip install Requests

Set DOWNLOAD_PATH and USER_AGENT as needed
'''

from bs4 import BeautifulSoup as bs
import requests, json, urllib2, urlparse, os, subprocess
from time import sleep

USER_AGENT = 'Python/2.7, Python CLI Stream App/0.1'
DOWNLOAD_PATH = '/home/orjanv/Videoklipp'

class NRKSuperDump(object):
	def __init__(self):
		return None
		
	def download_clip(self, url):
		'''Takes an url and download the actual clip
		'''
		FNULL = open(os.devnull, 'w')
		response = requests.get(url)
		webpage = bs(response.text)
		link = webpage.find("div", { "id" : "playerelement" })
		m_url = link.get('data-hls-media')
		d_url = m_url.replace('master.m3u8','index_4_av.m3u8?null=')
		title = webpage.title.text + '.mkv'
		
		# Check if clip already exists on drive
		if os.path.isfile(title):
			print 'clip has already been downloaded..'
			return
		else: 			
			# Download clip
			subprocess.call(['avconv', '-i', d_url, '-c', 'copy', title], stdout=FNULL, stderr=subprocess.STDOUT)

	def json_to_dict(self, jdata):
		'''Extracts the needed information from the json and builds a dict
		'''
		ddata = {}
		key = 1
		for k in jdata['Data']:
			ddata[k['FullTitle']] = (k['Url'], k['Title'], k['AvailabilityText'], key)
			key = key + 1
		return ddata

	def get_json(self, webpage, domain):
		'''Get the json file based on the input webpage
		'''
		data_url = webpage.find("div", { "class" : "season-tab tab-panel active" })
		json_url = 'http://' + domain + data_url.get('data-url')
		req = urllib2.Request(json_url, headers={'User-Agent': USER_AGENT})
		response = urllib2.urlopen(req)
		data = json.load(response)
		return data
		
	def clear_screen(self):
		'''Clears the screen
		'''
		os.system('cls' if os.name=='nt' else 'clear')

	def list_clips_available(self, clips):
		'''Lists all available clips and presents them nicely
		'''
		key = 1
		for k, v in sorted(clips.iteritems()):
			j = str(key)
			print '[' + str.rjust(j, 2) + '] ' + k + ' - ' + v[2]
			key += 1	

	def create_folder(self, folder):
		'''Use the name of the series and create a download folder
		'''
		try:
			os.chdir(os.path.join(DOWNLOAD_PATH, folder))
		except OSError:
			print 'Could not open output directory: ' + folder + ', creating it instead'
			os.mkdir(os.path.join(DOWNLOAD_PATH, folder), 0755)
			os.chdir(os.path.join(DOWNLOAD_PATH, folder))

		
if __name__ == '__main__':
	# Construct an instance of the class and 
	superdump = NRKSuperDump()
	superdump.clear_screen()
	url = raw_input("Enter URL to extract clips from (ex. http://tv.nrksuper.no/serie/bien-maja): ")
	headers = {'User-Agent': USER_AGENT}
	response = requests.get(url, headers=headers)
	data = response.text
	webpage = bs(data)
	domain = urlparse.urlsplit(url)[1].split(':')[0]
	series = ''
	jdata = superdump.get_json(webpage, domain)
	clips = superdump.json_to_dict(jdata)
	series = clips.values()[0][1] 
	choice = ''
	loop = 1

	# the main loop to present the menu
	while loop == 1:
		superdump.clear_screen()
		print ' '
		superdump.list_clips_available(clips)
		print '\n   X: Choose a clip number [ X ] to download'
		print '   A: Download all clips available'
		print '   Q: Quit\n'
		choice = raw_input('Choose an option: ')
		if choice == 'A' or choice == 'a':
			superdump.create_folder(series)
			for i in clips.values():
				clip = 'http://' + domain + i[0]
				print 'Downloading clip: ' + str(i[3]) + ' of ' + str(len(clips))
				superdump.download_clip(clip)
			print '\nDownload complete!'
			loop = 0
		elif choice == 'Q' or choice == 'q':
			loop = 0
		else:
			try:
				superdump.create_folder(series)
				sorted_clips = sorted(clips.iteritems())
				clip = 'http://' + domain + sorted_clips[int(choice)-1][1][0]
				print 'Downloading clip: ' + clip
				superdump.download_clip(clip)
				print '\nDownload complete!'
				loop = 0
			except IndexError:
				print 'Use a number in the list above or chose another option'
				sleep(2)
