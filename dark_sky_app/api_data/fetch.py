import json
import aiohttp
import asyncio

class Fetch(object):
    
    # url template for batch requests
    template = "https://api.darksky.net/forecast/"
    #data points to exclude in request
    exclude_args = "currently,minutely"
    
    def __init__(self, mapping_data):
        self.mapping_data = mapping_data

    # invidiaul request
    async def fetch_one(session, url):
        async with session.get(url) as response:
            # error handling
            if response.status != 200:
                response.raise_for_status()
            return await response.text()


    # batch request
    async def fetch_all(session, urls):
        results = await asyncio.gather(
            *[asyncio.create_task(fetch_one(session, url)) for url in urls]
        )
        return results


    # the function that runs the requests
    async def main(url_template, secret_key, loc_data, exclude_args):
        base_url = f"{url_template}{secret_key}"
        urls = []
        for index, row in loc_data.iterrows():
            lat = row["lat"]
            long = row["lng"]
            url = f"{base_url}/{lat},{long}/?exclude={exclude_args}"
            urls.append(url)

        async with aiohttp.ClientSession() as session:
            start = datetime.datetime.now()
            htmls = await fetch_all(session, urls)
            fetch_end = datetime.datetime.now()
            file_name = f"{str(datetime.date.today())}_forecasts.json"
            print(
                f"Fetching forecast data complete. Completion time: {str(fetch_end-start)}. Exporting to {file_name} now"
            )
            response_data = json.dumps(obj=htmls)
            export_end = datetime.datetime.now()
            print(
                f"Export of forecast data complete. Completion time: {str(export_end - fetch_end)}."
            )
            return response_data



