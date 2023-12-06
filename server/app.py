from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

##############################################################################
######################### Joy of Painting API Server #########################
##############################################################################
################## Hello, and welcome to my cool Flask app! ##################
############## This will be our API server for our Bob Ross API ##############
##############################################################################
################# We'll use Flask to create the server itself, ###############
############## Flask-SQLAlchemy to connect to our MySQL database, ############
############# and we'll return results in JSON to our happy users. ###########
######### Users will be able to query 3 multi-select filter fields, ##########
#### and to choose between 'I-want-it-all' and 'Match-any-filter' modes. #####
##############################################################################

# first let's initialize the Flask app
app = Flask(__name__)

# Now, with that out of the way let's get this cool little app connected to
# our MySQL database (I say ours, but really, it's mine. I'm just being gracious.)
alc_dialect_driver = 'mysql+mysqlconnector'
alc_user = os.environ['MYSQL_USER']
alc_pass = os.environ['MYSQL_PASSWORD']
alc_host = os.environ['MYSQL_HOST']
alc_db = os.environ['MYSQL_DATABASE']
alc_uri = f"{alc_dialect_driver}://{alc_user}:{alc_pass}@{alc_host}/{alc_db}"

# Now we can use this cavalcade of variables to configure our Flask app for
# connecting to our (MY!) MySQL database (c'mon, 'My' is even in the name)
app.config['SQLALCHEMY_DATABASE_URI'] = alc_uri

# Then we can us Flask-SQLAlchemy's help to initialize the database connection
db = SQLAlchemy(app)

# And finally we can turn our episode records into some sweet sweet python code
# by creating a class to represent our records.
class Episode(db.Model):
    __tablename__ = 'episodes'
    sequence = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(27))
    aired = db.Column(db.String(18))
    month = db.Column(db.String(9))
    extra_episode_info = db.Column(db.String(150))
    painting_index = db.Column(db.Integer)
    img_src = db.Column(db.String(51))
    season = db.Column(db.Integer)
    episode = db.Column(db.Integer)
    num_colors = db.Column(db.Integer)
    youtube_src = db.Column(db.String(42))
    colors = db.Column(db.String(249))
    color_hex = db.Column(db.String(165))
    Black_Gesso = db.Column(db.Boolean)
    Bright_Red = db.Column(db.Boolean)
    Burnt_Umber = db.Column(db.Boolean)
    Cadmium_Yellow = db.Column(db.Boolean)
    Dark_Sienna = db.Column(db.Boolean)
    Indian_Red = db.Column(db.Boolean)
    Indian_Yellow = db.Column(db.Boolean)
    Liquid_Black = db.Column(db.Boolean)
    Liquid_Clear = db.Column(db.Boolean)
    Midnight_Black = db.Column(db.Boolean)
    Phthalo_Blue = db.Column(db.Boolean)
    Phthalo_Green = db.Column(db.Boolean)
    Prussian_Blue = db.Column(db.Boolean)
    Sap_Green = db.Column(db.Boolean)
    Titanium_White = db.Column(db.Boolean)
    Van_Dyke_Brown = db.Column(db.Boolean)
    Yellow_Ochre = db.Column(db.Boolean)
    Alizarin_Crimson = db.Column(db.Boolean)
    season_and_episode = db.Column(db.String(6))
    APPLE_FRAME = db.Column(db.Boolean)
    AURORA_BOREALIS = db.Column(db.Boolean)
    BARN = db.Column(db.Boolean)
    BEACH = db.Column(db.Boolean)
    BOAT = db.Column(db.Boolean)
    BRIDGE = db.Column(db.Boolean)
    BUILDING = db.Column(db.Boolean)
    BUSHES = db.Column(db.Boolean)
    CABIN = db.Column(db.Boolean)
    CACTUS = db.Column(db.Boolean)
    CIRCLE_FRAME = db.Column(db.Boolean)
    CIRRUS = db.Column(db.Boolean)
    CLIFF = db.Column(db.Boolean)
    CLOUDS = db.Column(db.Boolean)
    CONIFER = db.Column(db.Boolean)
    CUMULUS = db.Column(db.Boolean)
    DECIDUOUS = db.Column(db.Boolean)
    DIANE_ANDRE = db.Column(db.Boolean)
    DOCK = db.Column(db.Boolean)
    DOUBLE_OVAL_FRAME = db.Column(db.Boolean)
    FARM = db.Column(db.Boolean)
    FENCE = db.Column(db.Boolean)
    FIRE = db.Column(db.Boolean)
    FLORIDA_FRAME = db.Column(db.Boolean)
    FLOWERS = db.Column(db.Boolean)
    FOG = db.Column(db.Boolean)
    FRAMED = db.Column(db.Boolean)
    GRASS = db.Column(db.Boolean)
    GUEST = db.Column(db.Boolean)
    HALF_CIRCLE_FRAME = db.Column(db.Boolean)
    HALF_OVAL_FRAME = db.Column(db.Boolean)
    HILLS = db.Column(db.Boolean)
    LAKE = db.Column(db.Boolean)
    LAKES = db.Column(db.Boolean)
    LIGHTHOUSE = db.Column(db.Boolean)
    MILL = db.Column(db.Boolean)
    MOON = db.Column(db.Boolean)
    MOUNTAIN = db.Column(db.Boolean)
    MOUNTAINS = db.Column(db.Boolean)
    NIGHT = db.Column(db.Boolean)
    OCEAN = db.Column(db.Boolean)
    OVAL_FRAME = db.Column(db.Boolean)
    PALM_TREES = db.Column(db.Boolean)
    PATH = db.Column(db.Boolean)
    PERSON = db.Column(db.Boolean)
    PORTRAIT = db.Column(db.Boolean)
    RECTANGLE_3D_FRAME = db.Column(db.Boolean)
    RECTANGULAR_FRAME = db.Column(db.Boolean)
    RIVER = db.Column(db.Boolean)
    ROCKS = db.Column(db.Boolean)
    SEASHELL_FRAME = db.Column(db.Boolean)
    SNOW = db.Column(db.Boolean)
    SNOWY_MOUNTAIN = db.Column(db.Boolean)
    SPLIT_FRAME = db.Column(db.Boolean)
    STEVE_ROSS = db.Column(db.Boolean)
    STRUCTURE = db.Column(db.Boolean)
    SUN = db.Column(db.Boolean)
    TOMB_FRAME = db.Column(db.Boolean)
    TREE = db.Column(db.Boolean)
    TREES = db.Column(db.Boolean)
    TRIPLE_FRAME = db.Column(db.Boolean)
    WATERFALL = db.Column(db.Boolean)
    WAVES = db.Column(db.Boolean)
    WINDMILL = db.Column(db.Boolean)
    WINDOW_FRAME = db.Column(db.Boolean)
    WINTER = db.Column(db.Boolean)
    WOOD_FRAMED = db.Column(db.Boolean)

# and now we can define our route to either return all episodes or filtered
@app.route('/api/episodes', methods=['GET'])
def list_episodes():
    # let's grab those query parameters
    month = request.args.getlist('month')
    subject_matter = request.args.getlist('subject_matter')
    colors_used = request.args.getlist('colors_used')
    # including the filter mode (which defaults to 'all')
    filter_mode = request.args.get('filter_mode', 'all')
    # now we reference a query to the entire data set before filtering
    query = Episode.query
    # and we filter down based on the mode (any or all)
    if filter_mode == 'any':
        month_filter = [Episode.month == mon for mon in month] if month else []
        subject_filter = [getattr(Episode, subj) == True for subj in subject_matter] if subject_matter else []
        colors_filter = [getattr(Episode, color) == True for color in colors_used] if colors_used else []
        # put it all together and what do you get? (a big pile of filters)
        filters = month_filter + subject_filter + colors_filter
        if filters:
            query = query.filter(db.or_(*filters))
    else:
        if month:
            query = query.filter(Episode.month.in_(month))
        for subj in subject_matter:
            query = query.filter(getattr(Episode, subj) == True)
        for color in colors_used:
            query = query.filter(getattr(Episode, color) == True)
    # now actually execute the really well-constructe query
    episodes_to_return = query.all()
    episodes_data = [{"title": ep.title,
                      "episode": ep.season_and_episode,
                      "aired": ep.aired,
                      "img_src": ep.img_src,
                      "youtube_src": ep.youtube_src,
                      "colors": ep.colors,
                      } for ep in episodes_to_return]
    # and finally we (I, thanklessly) turn it into JSON
    return jsonify(episodes_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
