# Papertrail log archives downloader

## Usage

Please set your token to the environment variable named `PAPERTRAIL_API_TOKEN` to run the script.

```bash
$ PAPERTRAIL_API_TOKEN=YOUR_TOKEN ./ppad.py # Download all the log archives
$ PAPERTRAIL_API_TOKEN=YOUR_TOKEN ./ppad.py 2020-01-01~2020-02-01 # Download the archives which have logged January 2020
$ PAPERTRAIL_API_TOKEN=YOUR_TOKEN ./ppad.py 2020-01-01~ # Specified the since date (including the since date file)
$ PAPERTRAIL_API_TOKEN=YOUR_TOKEN ./ppad.py ~2020-02-01 # Specified the until date (NOT including the until date file)
```

The date format is ISO-8601 format supported.

(The script uses [dateutil.isoparse](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.isoparse))
