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

examples:
"I want all the episodes from Feb or March (I'm in a Wintery mood)"
[http://localhost:5000/api/episodes?month=February&month=March](http://localhost:5000/api/episodes?month=February&month=March)

"I want to see ones where it's snowy or beachy (I'm indecisive)"
[http://localhost:5000/api/episodes?subject_matter=SNOW&subject_matter=BEACH&filter_mode=any](http://localhost:5000/api/episodes?subject_matter=SNOW&subject_matter=BEACH&filter_mode=any)

"I want to see ones where it's snowy AND beachy (I'm ready to be disappointed)"
[http://localhost:5000/api/episodes?subject_matter=SNOW&subject_matter=BEACH](http://localhost:5000/api/episodes?subject_matter=SNOW&subject_matter=BEACH)

UML Diagram:
This is what the dabatase records look like.

![UML representation of 'episodes' table record](https://github.com/wdmd2022/holbertonschool-the-joy-of-painting-api/blob/4041a92f50a489ec25ab40ffe1048766815e0f6b/uml.png)
