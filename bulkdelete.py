# from __future__ import print_function
import requests
import json
import calendar
from progress.spinner import PieSpinner
from datetime import datetime, timedelta
import codecs
import sys
from _tokens import _tokens


sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

# work on files older than x days as per set on this variable...
files_age = int(-8)

_domain = "chatagency"

if __name__ == '__main__':
    tokenCount = 0
    tokenTotal = len(_tokens)
    for _token in _tokens:
        tokenCount += 1
        print "\n\n /******************************************************************************************"
        print "| Working with access token: " + _token + " | ("+str(tokenCount)+" of "+str(tokenTotal)+")"
        print " \******************************************************************************************"
        whileCount = 1
        deleteCount = 0
        files_list_url = 'https://slack.com/api/files.list'
        date = str(calendar.timegm((datetime.now() + timedelta(files_age)).utctimetuple()))
        data = {"token": _token, "ts_to": date}
        response = requests.post(files_list_url, data=data)
        response = response.json()
        if("files" in response.keys()):
            fileCount = len(response["files"])
        else:
            print ("The following error message was received from SLACK API: " + str(response['error']))
            continue

        spinner = PieSpinner()

        if(fileCount > 0):
            print "Parsing " + str(fileCount) + " files..."
            spinner.next()
        else:
            print "No files older than 10 days found.                                                           \r",

        spinning = True
        while spinning:

            if len(response["files"]) == 0:
                spinner.finish()
                spinning = False
                break
            elif(whileCount >= fileCount and whileCount > 1):
                spinner.finish()
                spinning = False
                print "We couldn't delete some files posted by other users on private conversations."
                break
            else:
                iteratorCounter = 0
                spinner.next()
                for f in response["files"]:
                    iteratorCounter += 1
                    spinner.next()
                    #get user info for this file
                    userInfoUrl = "https://slack.com/api/users.info"
                    data = {"token": _token, "user": f['user']}
                    userCall = requests.post(userInfoUrl, data=data)
                    userRes = userCall.json()
                    #
                    timestamp = str(calendar.timegm(
                        datetime.now()
                        .utctimetuple()
                        )
                    )
                    delete_url = "https://" + _domain + ".slack.com/api/files.delete?t=" + timestamp
                    data = {
                        "token": _token,
                        "file": f["id"],
                        "set_active": "true",
                        "_attempts": "1"
                    }
                    delresp = requests.post(delete_url, data=data)
                    jsondelresp = delresp.json()
                    

                    if(jsondelresp['ok']):
                        deleteCount += 1
                        print ("\n# Deleted file " + str(iteratorCounter) + " of " + str(fileCount) + " posted by:" + str(userRes['user']['name']))
                    else:
                        spinner.next()
                        if(iteratorCounter >= fileCount):
                            spinning = False
                            difference = ''
                            if((fileCount - deleteCount) > 0):
                                difference = "This access token did not have permission to delete the other " + str(fileCount - deleteCount) + " of them.\nThis happens because the copies left of the file in question belong to the other user in the conversation."

                            spinner.finish()
                            print "\nDONE!\n"+str(deleteCount)+" files were deleted.\n" + str(difference) + "                                                                                       \r",
                    
                whileCount += 1

raw_input("\n\nWe are done here.\nPress ENTER to exit!")
