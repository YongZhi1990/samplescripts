import asyncio
import aiohttp
import time
import csv


URL = 'https://verify.twilio.com/v2/SafeList/Numbers'
ACCOUNT_SID = '~REPLACE WITH YOUR TWILIO ACCOUNT SID'
AUTH_TOKEN = '~REPLACE WITH YOUR TWILIO AUTH TOKEN'

async def request_executor(session, number, res_writer, err_writer,limit):
    
    async with limit:
        try:
            async with session.request(url=URL, method = 'POST', data={'PhoneNumber': number}, headers={"content-type": "application/x-www-form-urlencoded"}, auth=aiohttp.BasicAuth(ACCOUNT_SID, AUTH_TOKEN)) as response:
                response_text = await response.text()
                print(f'{number}, {time.asctime(time.localtime(time.time()))}, {response_text}')
                await write_result([f'{number} : {response_text}'],res_writer)
                await asyncio.sleep(4)
        except Exception as e:
            print(number, 'ERROR', str(e))
            await write_error([f'{number} and ERROR: {e}'], err_writer)
            await asyncio.sleep(4)
            return False


async def write_result(result, writer):
    async with asyncio.Lock():  
        writer.writerow(result)

async def write_error(error, writer):
    async with asyncio.Lock():
        writer.writerow(error)


async def main():
    limit = asyncio.Semaphore(2) #limit to 2 concurrent request per on the created session because we are sleeping 4 second per request, this will be 2 request/ 4 second or 30 request per minute
  
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        with open('res.csv', 'a') as csv_res, open('err.csv', 'a') as csv_err, open('~REPLACE WITH YOUR WHITELIST CSV FILENAME/FILEPATH') as whitelist_csv:
            res_writer = csv.writer(csv_res)
            err_writer = csv.writer(csv_err)
            request_builder = [request_executor(session, number.strip(), res_writer, err_writer, limit) for number in whitelist_csv]
            await asyncio.gather(*request_builder)
            print('!--- finished processing')

asyncio.run(main())



import csv
import hashlib
import pandas as pd

csv_file = pd.read_csv('number - Sheet1.csv')

md5_hash = []

for row in csv_file['number']:
    md5_hash.append(hashlib.md5(str(row).encode('utf-8')).hexdigest())

csv_file['md5-hash'] = md5_hash

csv_file.to_csv('output.csv', index=False)

import csv
import datetime
import os
from twilio.rest import Client

#base_url = 'https://api.twilio.com/2010-04-01'
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
from_number = '+12698831507'
message_text = 'Hello Twilio!'
#message_api_url = f"{base_url}/Accounts/{account_sid}/Messages.json"


#list of mobile numbers to send sms to
#mobile_numbers_list = ['+123', '+12345']
mobile_numbers_list = ['+15719462715','+13649003666', '+13649003644', '+14142965678', '+14144007468']
client = Client(account_sid, auth_token)

try:
    new_session = f"Session started at {datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
    #open successful_api_call.csv to write when the new session start and the headers, parameters can be used to search in twilio debug logs for errors
    with open(f"successful_api_call.csv", 'a', newline="") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow([new_session])
        writer.writerow(["Datetime","To", "From", "Body", "sid"])
    #open request_error_log.csv to do the same as above but to log any errors that happen in the call
    with open(f"request_error_log.csv",'a', newline="") as g:
        request_error_writer = csv.writer(g, delimiter=',')
        request_error_writer.writerow([new_session])
        request_error_writer.writerow(["Datetime","To", "From", "Body", "Error"])
    #for loop to loop through the number and make calls through https request 
    for mobile_number in mobile_numbers_list:
        try:
            #post request
            #send_sms_request_request = requests.post(message_api_url, auth=HTTPBasicAuth(account_sid, auth_token), data={"To": mobile_number, "From": from_number ,"Body": message_text})
            #send_sms_request_response = send_sms_request_request.json()
            send_sms_request_response = client.messages.create(from_=from_number, body=message_text, to=mobile_number)
            #logging successful call in csv
            with open(f"successful_api_call.csv", 'a', newline="") as h:
                successful_call_writer = csv.writer(h, delimiter=',')
                successful_call_writer.writerow([
                    send_sms_request_response.date_created,
                    mobile_number,
                    from_number,
                    send_sms_request_response.sid
                ])
            #printing the sid as needed in the assignment
            print(send_sms_request_response.sid)
        #handling errors and logging them i the request_error_log.csv
        except Exception as e:
            with open(f"request_error_log.csv",'a', newline="") as i:
                request_error_writer = csv.writer(i, delimiter=',')
                request_error_writer.writerow([datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'),mobile_number,from_number,e])
                #additional code can be used to handle error here but do not see any error that is safe to retry the request to resend sms
#logging application errors that happen
except Exception as e:
    with open(f"application_error_log.csv",'a', newline="") as j:
        application_error_writer = csv.writer(j, delimiter=',')
        application_error_writer.writerow([datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'), e])

