import telepot
import json
import time
import sys
import requests
import wget
import os
import random
from tokens import tokens

offset = 0
base_file_url = 'https://api.telegram.org/file/bot'


def getUp(bot,bot_id,offset = 0):
	responses = bot.getUpdates(offset=offset)
	if len(responses) == 0:
		return offset
	try:
		for r in responses:
			offset = r['update_id']
			with open(str(bot_id) + '.json','a') as f:
				json.dump(r,f)
				f.write('\n')
	except:
		print('err: ' + str(offset))
		# offset += 1


	return offset + 1



# while True:
# 	offset = getUp(bot,bot_id,offset)
# 	time.sleep(60)



def logger(bot,bot_id,offset = 0, filewrite = True):
	responses = bot.getUpdates(offset=offset)
	print ("responses: %s" %responses)
	if len(responses) == 0:
		return offset
	try:
		for r in responses:
			offset = r['update_id']

			if filewrite is True:
				with open(str(bot_id) + '.json', 'a') as f:
					json.dump(r, f)
					f.write('\n')

			print (r)
	except Exception as e:
		print ("error : %s" %e.message)

	return responses



def getFile(bot, fileId, botToken):

	file_info = bot.getFile(fileId)
	print(file_info)
	full_file_url = "%s%s/%s" %(base_file_url, botToken, file_info.get("file_path"))
	print(full_file_url)
	# file = requests.get(full_file_url)
	# print (file)
	wget.download(full_file_url)
    #
    # if file.get('file_path'):
     #    result['file_path'] = '%s/%s' % (self.base_file_url, result['file_path'])
    #
	# # with open(str(fileId) + file.get(), 'w') as f:
	# # 	f.write(file)


def bruteforceFilesBytoken(bot, botToken):
	dir_list = ["documents"] #, "photos", "thumbnails"]
	for dir in dir_list:
		for i in range(0,10):

				#TODO: add flow for jpg, ...

				file_name = "file_%s" % (i)
				full_file_url = "%s%s/%s" %(base_file_url, botToken, "%s/file_%s" % (dir,i))
				r = requests.get(full_file_url, stream = True)
				if r.status_code in [404, 403]:
					print("failed to download: %s \t : \t %s" % (full_file_url, r.status_code))
				else:
					if os.path.exists("./Downloads/%s" %file_name):
						file_name += "_duplicate_filename_%s" % random.randint(0,999) #TODO: handle extentions here!
					with open("./Downloads/%s" %file_name, 'wb') as fd:
						for chunk in r.iter_content(chunk_size=1014):
							fd.write(chunk)
						print("downloaded: %s \t : \t %s" % (full_file_url, r.status_code))
					#wget.download(full_file_url) # replace this with request





def main():

	for token in tokens:
		bot = telepot.Bot(token)
		bot_whoamI = bot.getMe()
		print(bot_whoamI)
		bot_id = bot_whoamI.get("id")
		#getFile(bot, fileId="file_ID", botToken=token)
		logger(bot,bot_id,offset = 0, filewrite = True)
		bruteforceFilesBytoken(bot, token)


main()