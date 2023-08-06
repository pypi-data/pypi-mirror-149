# PIP GeoIP
## Get ip information offline without api

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

PyGeoIP is a package that can be use to get ip information without any api and it's free.
## Available information
- Continent
- Country
- Iso Code
- City
- Zip
- timezone
- latitude
- longitude
- org

## Features

- Can be use in offile
- It's Free
- No need api key
- Get Dictionary or JSON result

## Tech
- [maxmind] - GeoIP2 Databases

## Installation
PyGeoIP tested on python 3.8. All version of python 3 shoud support.
```sh
pip install pipgeoip
```
## Example JSON object
```python
import pipgeoip
```
```python
print(get_geo_ip_json('204.236.186.159'))
```

```json
{
    "ip": "204.236.186.159",
    "country": "United States",
    "continent": "North America",
    "iso": "US",
    "city": "San Jose",
    "zip": "95141",
    "timezone": "America/Los_Angeles",
    "latitude": 37.3388,
    "longitude": -121.8916,
    "org": "AMAZON-02"
}
```
## Example Dictionary
```python
print(get_geo_ip('204.236.186.159')['country'])
```
```text
United States
```

## MySelf

I am Himel, Software Engineer and Ethical HackerInstructions on how to use them in your own application are linked below.

| Info | Link |
| ------ | ------ |
| Portfolio | https://himelrana.com |
| GitHub | https://github.com/Swe-HImelRana |
| Linkedin | https://www.linkedin.com/in/swe-himelrana |
