import argparse
import sqlite3
import sys

import pandas as pd
import requests
from requests.exceptions import HTTPError

parser = argparse.ArgumentParser(
    prog="Movie Command-Line Utility",
    description="""Using this tool you will be able to retrieve data about movies.\n\n""",
    epilog='Check out the "Portfolio Projects" section to access the project\'sGitHub Page.',
)


parser.add_argument(
    "-t",
    "--title",
    required=True,
    help='movies -t "Fight Club"',
)
parser.add_argument(
    "-o",
    "--output",
    help="""movies -o "id,title,etc.""",
)

parser.add_argument(
    "-f",
    "--format",
    choices=["table", "tuple"],
    default="table",
    help="Format of the output.",
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
            print(f'"{val}" is not a valid option')
            sys.exit(1)
        select_statement += f"{val}, "
    select_statement = select_statement[:-2]  # remove last comma and space
    select_statement += " FROM Movies WHERE normalized_title=?"
else:
    output_variables = "id,title,year,rated,released,runtime,genre,director,writer,actors,plot,language".split(
        ","
    )
    select_statement = "SELECT id, title, year, rated, released, runtime, genre, director, writer, actors, plot, language FROM MOVIES WHERE normalized_title=?"


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
