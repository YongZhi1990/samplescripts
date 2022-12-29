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
            async with session.request(url=url, method = 'POST', data={'PhoneNumber': number}, headers={"content-type": "application/x-www-form-urlencoded"}, auth=aiohttp.BasicAuth(ACCOUNT_SID, AUTH_TOKEN)) as response:
                response_text = await response.text()
                print(f'{number}, {time.asctime(time.localtime(time.time()))}, {response_text}')
                await write_result([f'{number} : {response_text}'],res_writer)
                print('after csv write')
                await asyncio.sleep(4)
                print(f'{number} after sleep') #sleep for this amount of seconds to achieve RPS (2 request per 4 seconds)
        except Exception as e:
            print(number, 'ERROR', str(e))
            await write_error([f'{number} and ERROR: {e}'], err_writer)
            await asyncio.sleep(4) #sleep for this amount of seconds to achieve RPS (2 request per 4 seconds) - error calls are counted as request towards rate limiting too
            return False


async def write_result(result, writer):
    async with asyncio.Lock():   # lock for gracefully write to shared file object
        writer.writerow(result)

async def write_error(error, writer):
    async with asyncio.Lock(): # lock for gracefully write to shared file object
        writer.writerow(error)


async def main():
    limit = asyncio.Semaphore(2) #limit to 2 concurrent request per on the created session because we are sleeping 4 second per request, this will be 2 request/ 4 second or 30 request per minute
  
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session: #opening up a session to use for the request
        with open('res.csv', 'a') as csv_res, open('err.csv', 'a') as csv_err, open('whitelist.csv') as whitelist_csv:
            res_writer = csv.writer(csv_res)
            err_writer = csv.writer(csv_err)
            request_builder = [request_executor(session, number.strip(), res_writer, err_writer, limit) for number in whitelist_csv]
            #print(request_builder)
            #print(type(request_builder))
            await asyncio.gather(*request_builder)
            print('!--- finished processing')

asyncio.run(main())