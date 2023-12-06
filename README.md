the joy of painting api

run
```
docker-compose up --build
```

endpoint:

URL: /episodes
method: GET
Get list of episodes, optionally filtered by:
- broadcast month. Multiple months can be specified.
- subject matter. Multiple subjects can be specified.
- colors used. Multiple colors can be specified.
- filter_mode (default: all)
    - all: episodes matching all specified filters
    - any: episodes matching any of the specified filters
Returns: JSON array of episode objects
