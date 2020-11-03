# Papertrail log archives downloader

`ppad`, stands for _PaPertrail log Archives Downloader_, can download log archives from [Papertrail](https://www.papertrail.com/).

The downloading process works on multi-thread and checking [API's _Rate Limits from the header](https://documentation.solarwinds.com/en/Success_Center/papertrail/Content/kb/how-it-works/http-api.htm#rate-limits) so you can download the archives fastly and safely.

## Install

Please use [pip](https://pip.pypa.io/)

```
pip install ppad
```

## Usage

Please set your token to the environment variable named `PAPERTRAIL_API_TOKEN` to run the script.

```bash
$ PAPERTRAIL_API_TOKEN=YOUR_TOKEN ppad # Download all the log archives
$ PAPERTRAIL_API_TOKEN=YOUR_TOKEN ppad 2020-01-01~2020-02-01 # Download the archives which have logged January 2020
$ PAPERTRAIL_API_TOKEN=YOUR_TOKEN ppad 2020-01-01~ # Specified the since date (including the since date file)
$ PAPERTRAIL_API_TOKEN=YOUR_TOKEN ppad ~2020-02-01 # Specified the until date (NOT including the until date file)
```

By running the above command(s), you can get the log archives named such as `2020-01-01-XX.tsv.gz` in the current directory.

The date format is ISO-8601 format supported.

(The script uses [dateutil.isoparse](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.isoparse))
