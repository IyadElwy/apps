import argparse
import sqlite3
import sys

import pandas as pd
import requests
from requests.exceptions import HTTPError

parser = argparse.ArgumentParser(
    prog="Movie Command-Line Utility",
    description='Using this tool you will be able to traverse movies \
        people before you have searched for, retrieve data about\
            newer movies and more. You can specify the title of the movie. The title needs to be \
     spelled correctly. If the title includes spaces use double quotes Ex. -t "Fight Club".\
         If it exists then the data can be viewed and changed using the -o and -f flags but if not, an airflow dag will \
            be triggered to extract, transform and load the data for you to see. If the movie cannot be found by the dags then\
                check the spelling of the movie.',
    epilog='If you are interested in how this system works, how you are able to freely access\
        a command line and run this app view the "Portfolio Projects" section down bellow to access \
            the project\'s GitHub Page.',
)


parser.add_argument(
    "-t",
    "--title",
    help='The title of the movie. Ex. movie -t "Fight Clube"',
)
parser.add_argument(
    "-o",
    "--output",
    help='Output the data you wish to see about the specific movie.Output must be a comma seperated \
        string of values (no space in between).\
                Ex. movies -o "id,title,year,rated,released,runtime,genre,director,writer,actors,plot,language"',
)

parser.add_argument(
    "-f",
    "--format",
    choices=["table", "tuple"],
    default="table",
    help='Format of the output. Choices are between "table" and "tuple".',
)

args = parser.parse_args()


if not args.title:
    print("Movie title must be specified")


allowed_output_variables = {
    "id",
    "title",
    "year",
    "rated",
    "released",
    "runtime",
    "genre",
    "director",
    "writer",
    "actors",
    "plot",
    "language",
}

if args.output:
    output_variables = args.output.split(",")
    select_statement = "SELECT "
    for val in output_variables:
        if val not in allowed_output_variables:
            sys.exit(1)
        select_statement += f"{val}, "
    select_statement = select_statement[:-2]  # remove last comma and space
    select_statement += " FROM Movies WHERE normalized_title=?"
else:
    output_variables = "id,title,year,rated,released,runtime,genre,director,writer,actors,plot,language".split(
        ","
    )
    select_statement = "SELECT * FROM MOVIES WHERE normalized_title=?"


con = sqlite3.connect("/appdata/db.sqlite")
cur = con.cursor()
res = cur.execute(
    select_statement,
    (args.title.lower().replace(" ", ""),),
)
res = res.fetchone()
con.close()


if res is None:
    print(
        f'Movie with title "{args.title}" not found in Database. Running Dag to extract, transform and then load movie into Database. Check again in a minute.'
    )
    res_dag_req = requests.post(
        "http://portfolio-api-1:5003/initdag",
        json={"title": args.title},
        headers={"Content-type": "application/json"},
    )
    try:
        res_dag_req.raise_for_status()
    except HTTPError:
        print("Network Error")
else:
    if args.format == "table":
        df = pd.DataFrame.from_records((res,), columns=output_variables)
        print(df)
    elif args.format == "tuple":
        print(res)
