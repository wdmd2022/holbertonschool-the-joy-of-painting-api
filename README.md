# the joy of painting api

requires: docker, docker-compose

run
```
docker-compose up --build
```

## endpoint:

### URL: /api/episodes
### method: GET
Get list of episodes, optionally filtered by:
- broadcast month. Multiple months can be specified.
- subject matter. Multiple subjects can be specified.
- colors used. Multiple colors can be specified.
- filter_mode (default: all)
    - all: episodes matching all specified filters
    - any: episodes matching any of the specified filters
### Returns: JSON array of episode objects

### examples:
"I want all the episodes from Feb or March (I'm in a Wintery mood)"
[http://localhost:5000/api/episodes?month=February&month=March](http://localhost:5000/api/episodes?month=February&month=March)

"I want to see ones where it's snowy or beachy (I'm indecisive)"
[http://localhost:5000/api/episodes?subject_matter=SNOW&subject_matter=BEACH&filter_mode=any](http://localhost:5000/api/episodes?subject_matter=SNOW&subject_matter=BEACH&filter_mode=any)

"I want to see ones where it's snowy AND beachy (I'm ready to be disappointed)"
[http://localhost:5000/api/episodes?subject_matter=SNOW&subject_matter=BEACH](http://localhost:5000/api/episodes?subject_matter=SNOW&subject_matter=BEACH)

### Constructing your API Query:

#### Months (month=)
January
February
March
April
May
June
July
August
September
October
November
December

#### Colors (colors_used=)
Black_Gesso
Bright_Red
Burnt_Umber
Cadmium_Yellow
Dark_Sienna
Indian_Red
Indian_Yellow
Liquid_Black
Liquid_Clear
Midnight_Black
Phthalo_Blue
Phthalo_Green
Prussian_Blue
Sap_Green
Titanium_White
Van_Dyke_Brown
Yellow_Ochre
Alizarin_Crimson

#### Subjects (subject_matter=)

##### nature ones
AURORA_BOREALIS
BEACH
BOAT
BUSHES
CACTUS
CIRRUS
CLIFF
CLOUDS
CONIFER
CUMULUS
DECIDUOUS
FIRE
FLOWERS
FOG
GRASS
HILLS
LAKE
LAKES
MOON
MOUNTAIN
MOUNTAINS
NIGHT
OCEAN
PALM_TREES
RIVER
ROCKS
SNOW
SNOWY_MOUNTAIN
SUN
TREE
TREES
WATERFALL
WAVES
WINTER
PERSON

##### structures
PATH
STRUCTURE
WINDMILL
FARM
BARN
CABIN
BRIDGE
BUILDING
DOCK
FENCE
LIGHTHOUSE
MILL

##### frame types
FRAMED
APPLE_FRAME
CIRCLE_FRAME
DOUBLE_OVAL_FRAME
FLORIDA_FRAME
HALF_CIRCLE_FRAME
HALF_OVAL_FRAME
OVAL_FRAME
RECTANGLE_3D_FRAME
RECTANGULAR_FRAME
SEASHELL_FRAME
SPLIT_FRAME
TRIPLE_FRAME
TOMB_FRAME
WINDOW_FRAME
WOOD_FRAMED

##### Guest-related ones
GUEST
STEVE_ROSS
DIANE_ANDRE
PORTRAIT

## UML Diagram:
This is what the dabatase records look like.

![UML representation of 'episodes' table record](https://github.com/wdmd2022/holbertonschool-the-joy-of-painting-api/blob/4041a92f50a489ec25ab40ffe1048766815e0f6b/uml.png)
