import config as cfg
from Google import Create_Service


# print (dir(service))

class google_drive_scrape(object):

	def __init__(self):
		CLIENT_SECRET_FILE = 'client_secret_GoogleCloudDemo.json'
		API_NAME = 'drive'
		API_VERSION = 'v3'
		SCOPES = ["https://www.googleapis.com/auth/drive"] 
		self.service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

	def search(self,search_term):
		results = self.service.files().list(
			q="fullText contains \'" + search_term + "\' or name contains \'" + search_term + "\'",
			spaces='drive',
			fields="nextPageToken, files(id, name, webViewLink)").execute()

		items = results.get('files', [])
		f = open("search results.html", "w")
		if not items:
			print('No files found in Google drive.')
		else:

			f.write("Files found in Google Drive:"+ '\n')
			for item in items:
				# print('{0} ({1})'.format(item['name'], item['webViewLink']))
				f.write('<li>' + '<a href=\"' + item['webViewLink'] + '\"</a>'+'</li>' )
				f.write (item['name'])
			f.close()