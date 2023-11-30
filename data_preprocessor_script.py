import os
import mysql.connector
import time
import pandas as pd
import numpy as np

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
colors_path = './data_sources/The Joy Of Painiting - Colors Used'
subjects_path = './data_sources/The Joy Of Painiting - Subject Matter'
airdates_path = './data_sources/The Joy Of Painting - Episode Dates'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# now, let's put them into pandas DataFrames (awwww yeah)

# with colors, we set index_col to 3 because that is the painting title.
colors = pd.read_csv(colors_path, index_col=3)

# with subjects, we will wait, not yet setting index_col to 1 because while that is
# the painting title, it is in all-caps form as if it is being yelled, and if we set
# it as the index now, we won't be able to manipulate it later on in order to correct
# the capitalization before we do a matching operation to put our dataframes together.
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

# let's clean up colors first.
# let's drop that first column of nonsense values
colors.drop(colors.columns[0], axis=1, inplace=True)


# now let's clean up airdates.
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


# now let's clean up subjects.
subjects['TITLE'] = airdates['title']

pd.set_option('display.max_rows', None)

print(subjects)






#######################################################################################################

# then we will configure the database according to our schema

# then we will populate the database
