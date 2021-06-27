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

`twiffle` expects to have a `data/settings.yml` file where the behaviour of the service is configured.

### Example

```yml
label: tabularconf
track:
  keywords:
    - "#TabularConf"
    - "#TabularConf2021"
dump_users:
  books:
    since: "2021-01-25 07:00:00"
    until: "2021-01-29 22:59:00"
    retweets: false
    excluded_users:
      - "@TabularConf"
      - sdelquin
    must_include:
      - "#SuperGift"
      - "@pandas_dev"
  rpi:
    must_include:
      - "#iwantrpi"
      - "@Raspberry_Pi"
```

- **label**: Give a unique name for the whole configuration. \*
- **track**: Tracking service settings. \*
  - **keywords**: List of keywords to be tracked. It's an "OR" among all these terms. _Hashtags_ and _accounts_ must include double quotes. \*
- **dump_users**: Settings when dumping users. It contains "blocks" to define dumping features:
  - **since**: Users will be extracted since this value. Datetime (as string) in ISO-format. It must include quotes. [Default: **beginning of time**]
  - **until**: Users will be extracted until this value. Datetime (as string) in ISO-format. It must include quotes. [Default: **current datetime**]
  - **retweets**: Boolean value indicating if retweets are included in the dump. [Default: `true`]
  - **excluded_users**: List of Twitter usernames to be excluded on dump. If `@` is prefixed, the text must be double-quoted. [Default: **empty list**]
  - **must_include**: List of terms which the matching tweets must include. It's an "AND" among all these terms. If _hashtags_ or _accounts_ are added, they must be double-quoted. [Default: **empty list**]

\* Required fields.

## Usage

### Tracking service

To run the tracking service, use the following command:

```console
$ ./main.py track
```

It will use the **track section** defined in `data/settings.yml` to read the proper parameters. Output will be a sqlite file in `data/tabularconf.db`.

You can provide a custom settings file using:

```console
$ ./main.py track -c custom-settings.yml
```

### Dumping users

To dump **unique** usernames from captured tweets (tracking service), use the following command:

```console
$ ./main.py dump-users
```

It will use the **dump_users** section in `data/settings.yml` to read the proper parameters. Output will these two files:

- `data/tabularconf-books.dump`
- `data/tabularconf-rpi.dump`

You can provide a custom settings file using:

```console
$ ./main.py dump-users -c custom-settings.yml
```

#### DUMP SINGLE BLOCK

Instead of dumping all the existing blocks from settings file, you can dump a single one using:

```console
$ ./main.py dump-users books  # generate tabularconf-books.dump
```

#### DUMP TO STDOUT

Instead of dumping users to a file, you can show them in stdout using:

```console
$ ./main.py dump-users -o books
```

## Logging

Operations performed by `./main.py track` are logged to `twiffle.log` with a default file rotation.

Logging behaviour can be overwrite using the following keys in the `.env` file:

- `LOGFILE_NAME`: filename of the logfile. [Default: `twiffle.log`]
- `LOGFILE_ROTATION`: size of the logfile. [Default: `10MB`]
- `LOGFILE_RETENTION`: number of rotating logfiles. [Default: `5`]
