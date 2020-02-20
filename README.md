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
* All of the JSON data received from `Fetch` is manipulated and transformed using the `pandas` library within the `DataProcessor` class in `api_data/process.py`
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

## Part III  - Creating the Schema
* Now that the structure of the data has been properly defined/processed, creating a schema to properly store said data is needed
* Thanks to Django's models format, creating the schema for a PostgreSQL database was relatively straightforward
* The entire schema is built in `api_data/models.py` with each non-abstract class representing a different table
* There are 7 tables in all that I created
    * Six that come from the API (hourly/daily/alerts) and the mapping table used to create the request URLs
* Several relatively basic unique, foreign key and value constraints were put on each model to ensure truly unique, valid data
* A custom field `SeparetedValuesField` was created to account for data being pased into the database as a list/array 

## Part IV - Data Ingestion
* Back in `api_data/process.py` the `DataIngestor` class handles all of the data transformed by `DataProcessor` and stores it in a PostgreSQL database
* Using `SQLAlchemy`, `psycopg2`, and `pandas`, some further manipulation and validation is done before the data is actually injected into the database
* Possibly the most difficult part of this entire project was abstracting a SQL query for timestamps from Pandas syntax into SQL Syntax, which is done in the `query_string_interpolation` method
    * There was quite a lot of string maniuplation done and perhaps in future commits/refactoring, I'll refactor using regular expressions to clean up some of the code or perhaps I'll try to use the Django ORM instead of raw SQL
* The reason for doing the above is in order to properly check for rows that already exist, deleting them and replacing them with the more updated records that have been grabbed from the API
* After doing this as well as dropping duplicates that may occur within `DataProcessor`, a simple Pandas SQL injection is performed

## Part V - Scripting and Hosting
* In order to easily run all of the code in Parts 1 through 4, I created the `MasterCrawler` and `DBConnector` class in `api_data/master_crawler.py`
* `DBConnector` creates a connection to the PostgreSQL database and has a method that grabs the data used for building all of the request URLs sent to Dark Sky
* `MasterCrawler` runs the `Fetch`, `DataProcessor` and `DataIngestor` classes within it 
* Now with everything called in one easy place, I worte a simple script in the base directory `scheduler.py` to execute `DBConnector` and `MasterCrawler` instances
* Since I wanted this script to run programmatically and have the database be remote, I decided to host this entire project on Heroku
* Besides some reconfiguration of `settings.py` and other files, adding a `Procfile` and `runtime.txt` files, it was relatively straightforward minus some debugging
* Heroku Scheduler runs `scheduler.py` daily at 12:00 AM UTC and a Heroku PostgreSQL instance hosts all of the data

## Next Steps
* Refactor some code particuarly in `DataIngestor`
* Write tests to validate everything is performing as it should in particular the delete and update commands happening in `DataIngestor`
* Add more of a frontend component to the app and/or create tabular views of the data within Django Admin
    * Currently given a login, you can view each object individually, but not in a convenient way
* Refine the schema to split out into more tables and/or adding minutely data to the pipeline

