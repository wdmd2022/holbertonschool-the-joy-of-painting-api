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

UML Diagram:
![UML representation of 'episodes' table record](https://github.com/wdmd2022/holbertonschool-the-joy-of-painting-api/blob/4041a92f50a489ec25ab40ffe1048766815e0f6b/uml.png)
