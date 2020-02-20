# dark-sky-integration
Integrating Dark Sky's API Within a Django App

## Part I - Fetching the Data
* Grabbing data from Dark Sky's API is simple enough as its a relatively straightforward REST
* To do so I created the `Fetch` class in `api_data/fetch.py`
    * This class is made up of three methods, `fetch_one`, `fetch_all` and `main`.
    * `fetch_one` contains the logic of making an async call, `fetch_all` runs `fetch_one` and creates all tasks (i.e. calls) sent to the API.
    * `main` gathers all of the request URLs and uses them to run `fetch_all`
* To improve effiency of the calls, I employed asynchonrous libraries `aiohttp` and `asyncio`
* For testing purposes, I initially output the data to csvs, but later kept them as JSON to pass to the next step
* 1,000 calls are made daily (max number you can make without being charged) from a PostgreSQL table containing latitudes and longitudes as well as a bunch of other geographical information
* Three groups of data is grabbed - daily, hourly and alerts

## Part II - Processing the Data
* All of the JSON data received from `Fetch` is manipulated and transformed using the `pandas` library within the `Process` class in `api_data/process.py`
* Most of the maniuplation for all tables is done in the `update_and_transform` method
    * First it iterates through the three data groups and adds latitude and longitude to each record for later reference
    * Then a Geohash, a unique identifier based on lat/long coordinates is created as well as a unique ID in `UUID` format are added to every record
        * Deriving the Geohash is useful because trying to index/search by multiple levels of values in SQL databases is inefficient
    * Last, several of the fields contain time data the need to be properly converted before database ingestion
* Several methods split the data into 6 separate tables
    * Daily info and stats
    * Hourly info and stats
    * Alerts and Alert Regions
* The alerts table has a field that contains a list of corresponding regions for said alert.
    * The `alert_regions_df` method creates the regions table including an `alerts_id` field which will act as a foreign key tying it back to alerts
* The `process` method calls all of the previously defined functions to actually run the data through the pipeline

## Part III  - Creating the Schema and Ingestion

