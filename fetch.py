import json
import pandas as pd
import aiohttp
import asyncio
import datetime

# #open secret key
with open("secret_key.txt", "r") as f:
    key = f.read()

# url template for batch requests
template = "https://api.darksky.net/forecast/"

# open location data file
loc_data = pd.read_csv("uscities.csv")

# pull out only lat/long cols and limit to 1000 rows for API call
lat_long = loc_data[["lat", "lng"]][:1000]

#data points to exclude in request
exclude="currently,minutely"
# invidiaul request
async def fetch(session, url):
    async with session.get(url) as response:
        # error handling
        if response.status != 200:
            response.raise_for_status()
        return await response.text()


# batch request
async def fetch_all(session, urls):
    results = await asyncio.gather(
        *[asyncio.create_task(fetch(session, url)) for url in urls]
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
        output_json = open(
            file=f"{str(datetime.date.today())}_forecasts.json", mode="w+"
        )
        json.dump(obj=htmls, fp=output_json)
        export_end = datetime.datetime.now()
        print(
            f"Export of forecast data complete. Completion time: {str(export_end - fetch_end)}."
        )


# calling main
if __name__ == "__main__":
    asyncio.run(main(url_template=template, secret_key=key, loc_data=lat_long[:1000], exclude_args = exclude))
