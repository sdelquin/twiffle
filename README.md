# twiffle

![Twiffle Logo](twiffle-logo.svg)

**Tracking of twitter terms to make a funny raffle**

`twiffle` comes from `twitter` + `raffle`. It's a service written in Python to track twitter terms (mainly _hashtags_) in order to retrieve matching tweets and, afterwards, extract unique usernames, perhaps for a funny raffle 🎉.

## Installation

```console
$ git clone https://github.com/sdelquin/twiffle.git
$ cd twiffle
$ python3.9 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Configuration

A `.env` file must be present for `twiffle` to run properly. Write your Twitter API credentials here:

```ini
API_CONSUMER_KEY = '<your-api-token-here>'
API_CONSUMER_SECRET = '<your-api-token-here>'
API_ACCESS_TOKEN = '<your-api-token-here>'
API_ACCESS_TOKEN_SECRET = '<your-api-token-here>'
```

> Manage [here](https://developer.twitter.com/en/portal/dashboard) your Twitter API Tokens.

## Settings

`twiffle` expects to have a `settings.yml` file at the current folder, where the behaviour of the service is configured.

### Example

```yml
database: tabularconf.db
track:
  keywords:
    - "#TabularConf"
    - "#TabularConf2021"
dump_users:
  since: "2021-01-25 07:00:00"
  until: "2021-01-29 22:59:00"
  retweets: false
  output: users.txt
  excluded_users:
    - TabularConf
    - sdelquin
  must_include:
    - "@ThePSF"
    - "@pandas_dev"
```

- **database**: Filename for the SQLite database. \*
- **track**: Tracking service settings. \*
  - **keywords**: List of keywords to be tracked. Hashtags must include quotes. \*
- **dump_users**: Settings when dumping users. (_It can be ommited_)
  - **since**: Users will be extracted since this value. Datetime (as string) in ISO-format. It must include quotes. [Default: **beginning of time**]
  - **until**: Users will be extracted until this value. Datetime (as string) in ISO-format. It must include quotes. [Default: **current datetime**]
  - **retweets**: Boolean value indicating if retweets are included in the dump. [Default: `true`]
  - **output**: Filename where users will be dumped in. If no value is given in this argument, users will be dumped to **stdout**.
  - **excluded_users**: List of Twitter usernames (without `@`) to be excluded on dump. [Default: **empty list**]
  - **must_include**: List of terms which the matching tweets must include. It's an "AND" among all these terms. [Default: **empty list**]

\* Required fields.

## Usage

### Tracking service

To run the tracking service, use the following command:

```console
$ ./twiffle.py track
```

> It will use the **track section** in `settings.yml` to read the proper parameters.

### Dumping users

To dump **unique** usernames from captured tweets (tracking service), use the following command:

```console
$ ./twiffle.py dump-users
```

> It will use the **dump_users** section in `settings.yml` to read the proper parameters.

### Provide custom settings file

Default settings file is `settings.yml` though, you can use your custom settings file with the following command:

```console
$ ./twiffle.py -c mysettingsfile.yml
```

## Logging

Operations performed by `./twiffle.py track` are logged to `twiffle.log` with a default file rotation.

Logging behaviour can be overwrite using the following keys in the `.env` file:

- `LOGFILE_NAME`: filename of the logfile. [Default: `twiffle.log`]
- `LOGFILE_ROTATION`: size of the logfile. [Default: `10MB`]
- `LOGFILE_RETENTION`: number of rotating logfiles. [Default: `5`]
