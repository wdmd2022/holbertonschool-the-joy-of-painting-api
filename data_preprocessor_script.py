import os
import mysql.connector
import time
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

#######################################################################
################### GENERAL STRUCTURE OF THE SCRIPT ###################
#######################################################################
# - make sure the MySQL database has been created using docker-compose
# - connect to it
# - get the original, uncleaned data loaded in
# - use pandas to clean it and prepare for upload in one table
# - use mysql.connector to create the table with its schema defined
# - use sqlalchemy to make an engine so we can:
# - upload the cleaned data into our MySQL database using pandas
#######################################################################

def first_connect_to_the_database():
    while True:
        try:
            return mysql.connector.connect(host=os.environ['MYSQL_HOST'],
                                           user=os.environ['MYSQL_USER'],
                                           password=os.environ['MYSQL_PASSWORD'],
                                           database=os.environ['MYSQL_DATABASE'])
        except mysql.connector.Error as whoops:
            print(f"Whoops! it didn't work: {whoops}")
            time.sleep(5)

# let's make sure that database is actually available
my_connection = first_connect_to_the_database()
print("awesome we did it")


# after this, we will import and process the data

# let's get our data loaded in!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# first let's make a shorthand so we don't have to type these paths
colors_path = '/data_sources/The Joy Of Painiting - Colors Used'
subjects_path = '/data_sources/The Joy Of Painiting - Subject Matter'
airdates_path = '/data_sources/The Joy Of Painting - Episode Dates'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# now, let's put them into pandas DataFrames (awwww yeah)

# first colors
colors = pd.read_csv(colors_path)

# now subjects
subjects = pd.read_csv(subjects_path)

# with airdates, there isn't a delimiter, but each column looks something like:
# "A Walk in the Woods" (January 11, 1983)
# so we need to set up a regular expression as a delimiter, and that will allow us
# to split on the first space that follows a quotation mark. Later, we'll remove the
# extra quotation marks.
# we will use the python engine to parse our command, because we are using re.
# header is set to None because there is no header row
airdate_delim = r'(?<=") '
airdates = pd.read_csv(airdates_path, header=None, sep=airdate_delim, engine='python')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# now we clean!

# let's start our cleaning with the airdates DataFrame.
# first, let's get rid of the quotation marks in the strings representing the episode titles
# And since airdates.columns[0] would only refer to the label (like above), we need to use
# airdates[0] to get a reference to the entire first column of the DataFrame.
airdates[0] = airdates[0].str.strip('"')
# now we need to add a third column, one that will be ultimately used for filtering by the month
# in which the episode aired. Since some records in this second column contain more than just
# the date, i.e., `(May 3, 1994) (featuring Steve Ross)`, we will have to grab it by using a
# regular expression that looks for the first word after the first opening parentheses in the
# second column of airdates. We'll use pandas' `str.extract` function to pull this string out
airdates['month'] = airdates[1].str.extract(r'\((\w+)')
# now let's go back to that second column, and clean it up a little bit. First, we'll extract the
# extra episode information (like guest stars) and put it into a column of its own
airdates['extra_episode_info'] = airdates[1].str.extract(r'\)\s*(.*)')
# and let's remove that extracted part from the second column
airdates[1] = airdates[1].str.replace(r'\)\s*.*', ')', regex=True)
# and now let's make sure all the columns (i.e., Series) have sensible column names
airdates.columns = ['title', 'aired', 'month', 'extra_episode_info']
# since there are so many typos in the other DataFrames, let's convert 'aired' to a datetime
# that can be sorted then we can match based on order in which they aired.
airdates['aired_datetime'] = pd.to_datetime(airdates['aired'].str.extract(r'\((.*?)\)')[0])
# now let's sort it in place
airdates.sort_values(by='aired_datetime', inplace=True)
# and let's remove those silly parentheses from the original `aired` column
airdates['aired'] = airdates['aired'].str.replace(r'\(|\)', '', regex=True)

# now let's clean up subjects using the nice titles from airdates
subjects['TITLE'] = airdates['title']

# and since that was so much fun, let's do it to colors too:
# first let's drop that first column of nonsense values
colors.drop(colors.columns[0], axis=1, inplace=True)
# and now perform the matching and updating based on airdates
colors['painting_title'] = airdates['title']
# and let's remove the weird `\r\n` that appears in some color names in one column
colors['colors'] = colors['colors'].str.replace(r'\\r\\n', '', regex=True)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# now we get ready to merge!

# first, let's set some indexes
# let's make a column in each, to match them appropriately
airdates['sequence'] = range(1, len(airdates) + 1)
colors['sequence'] = range(1, len(colors) + 1)
subjects['sequence'] = range(1, len(subjects) + 1)

# now let's set the pandas indices for airdates, colors, and subjects
airdates.set_index('sequence', inplace=True)
colors.set_index('sequence', inplace=True)
subjects.set_index('sequence', inplace=True)

# now we can join them!

# first let's join airdates with colors
aircolor = airdates.join(colors, how='outer')
# then let's join the resulting dataframe with subjects
final_data = aircolor.join(subjects, how='outer')
# now we have one nice, big table! Alright!

# and let's drop that column we made for sorting earlier
final_data = final_data.drop(columns=['aired_datetime'])
# and let's drop other extraneous columns
final_data = final_data.drop(columns=['painting_title', 'TITLE'])
# and let's also rename EPISODE because mysql is case-insensitive
final_data = final_data.rename(columns={'EPISODE': 'season_and_episode'})

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# now we get ready to import!

# first let's make our SQL query that we'll use to create the table
let_there_be_a_table = """
CREATE TABLE IF NOT EXISTS episodes (
    sequence INT,
    title VARCHAR(27),
    aired VARCHAR(18),
    month VARCHAR(9),
    extra_episode_info VARCHAR(150),
    painting_index INT,
    img_src VARCHAR(51),
    season INT,
    episode INT,
    num_colors INT,
    youtube_src VARCHAR(42),
    colors VARCHAR(249),
    color_hex VARCHAR(165),
    Black_Gesso BOOLEAN,
    Bright_Red BOOLEAN,
    Burnt_Umber BOOLEAN,
    Cadmium_Yellow BOOLEAN,
    Dark_Sienna BOOLEAN,
    Indian_Red BOOLEAN,
    Indian_Yellow BOOLEAN,
    Liquid_Black BOOLEAN,
    Liquid_Clear BOOLEAN,
    Midnight_Black BOOLEAN,
    Phthalo_Blue BOOLEAN,
    Phthalo_Green BOOLEAN,
    Prussian_Blue BOOLEAN,
    Sap_Green BOOLEAN,
    Titanium_White BOOLEAN,
    Van_Dyke_Brown BOOLEAN,
    Yellow_Ochre BOOLEAN,
    Alizarin_Crimson BOOLEAN,
    season_and_episode VARCHAR(6),
    APPLE_FRAME BOOLEAN,
    AURORA_BOREALIS BOOLEAN,
    BARN BOOLEAN,
    BEACH BOOLEAN,
    BOAT BOOLEAN,
    BRIDGE BOOLEAN,
    BUILDING BOOLEAN,
    BUSHES BOOLEAN,
    CABIN BOOLEAN,
    CACTUS BOOLEAN,
    CIRCLE_FRAME BOOLEAN,
    CIRRUS BOOLEAN,
    CLIFF BOOLEAN,
    CLOUDS BOOLEAN,
    CONIFER BOOLEAN,
    CUMULUS BOOLEAN,
    DECIDUOUS BOOLEAN,
    DIANE_ANDRE BOOLEAN,
    DOCK BOOLEAN,
    DOUBLE_OVAL_FRAME BOOLEAN,
    FARM BOOLEAN,
    FENCE BOOLEAN,
    FIRE BOOLEAN,
    FLORIDA_FRAME BOOLEAN,
    FLOWERS BOOLEAN,
    FOG BOOLEAN,
    FRAMED BOOLEAN,
    GRASS BOOLEAN,
    GUEST BOOLEAN,
    HALF_CIRCLE_FRAME BOOLEAN,
    HALF_OVAL_FRAME BOOLEAN,
    HILLS BOOLEAN,
    LAKE BOOLEAN,
    LAKES BOOLEAN,
    LIGHTHOUSE BOOLEAN,
    MILL BOOLEAN,
    MOON BOOLEAN,
    MOUNTAIN BOOLEAN,
    MOUNTAINS BOOLEAN,
    NIGHT BOOLEAN,
    OCEAN BOOLEAN,
    OVAL_FRAME BOOLEAN,
    PALM_TREES BOOLEAN,
    PATH BOOLEAN,
    PERSON BOOLEAN,
    PORTRAIT BOOLEAN,
    RECTANGLE_3D_FRAME BOOLEAN,
    RECTANGULAR_FRAME BOOLEAN,
    RIVER BOOLEAN,
    ROCKS BOOLEAN,
    SEASHELL_FRAME BOOLEAN,
    SNOW BOOLEAN,
    SNOWY_MOUNTAIN BOOLEAN,
    SPLIT_FRAME BOOLEAN,
    STEVE_ROSS BOOLEAN,
    STRUCTURE BOOLEAN,
    SUN BOOLEAN,
    TOMB_FRAME BOOLEAN,
    TREE BOOLEAN,
    TREES BOOLEAN,
    TRIPLE_FRAME BOOLEAN,
    WATERFALL BOOLEAN,
    WAVES BOOLEAN,
    WINDMILL BOOLEAN,
    WINDOW_FRAME BOOLEAN,
    WINTER BOOLEAN,
    WOOD_FRAMED BOOLEAN,
    PRIMARY KEY (sequence),
    INDEX idx_month (month)
);
"""
# let's us the MySQL connection we established earlier to create a cursor
cursor = my_connection.cursor()
# then use that cursor to run the table creation command
cursor.execute(let_there_be_a_table)
# and let's commit our changes to the db
my_connection.commit()
# and close our cursor
cursor.close()
# and close our connection
my_connection.close()
# hooray, the table has been created! Now we can move on to filling it up

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# now we can actually import our data!

# the first step is creating a sqlalchemy engine, because pandas requires
# that we feed it a sqlalchemy.engine (engine or connection) as `con` arg
alc_dialect_driver = 'mysql+mysqlconnector'
alc_user = os.environ['MYSQL_USER']
alc_pass = os.environ['MYSQL_PASSWORD']
alc_host = os.environ['MYSQL_HOST']
alc_db = os.environ['MYSQL_DATABASE']
alchemy_engine = create_engine(
    f"{alc_dialect_driver}://{alc_user}:{alc_pass}@{alc_host}/{alc_db}"
)

# the next step is to use this engine to make the pandas to_sql command work.
# first we'll copy our index over to a normal column (so it goes into the database as a named column)
final_data['sequence'] = final_data.index
# and now we'll use pandas' awesome to_sql function to move it into our database
final_data.to_sql(
    'episodes',
    con=alchemy_engine,
    if_exists='replace',
    index=False
)
