#!/usr/bin/env python
from google_drive_scrape import google_drive_scrape
from confluence_scrape import confluence_scrape
import webbrowser

if __name__ == '__main__':

	search_term = input("Enter search term: ")

	Google_Drive = google_drive_scrape()
	print("Searching Google drive...")
	Google_Drive.search(search_term)

	Confluence = confluence_scrape()
	print("Searching Confluence...")
	Confluence.search(search_term)

	print("Done searching!")
	webbrowser.open('file:///Volumes/Extreme%20SSD/projects/Multi%20Search%20tool/search%20results.html')