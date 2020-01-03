import numpy as np
import pandas as pd
import scholarly
import sqlite3
import itertools

def var_extract(auth):

    # Collecting simple variables
    record_name = auth.name
    record_id = auth.id
    record_interests = auth.interests
    affiliation = auth.affiliation
    cited = auth.citedby
    cited5y = auth.citedby5y
    h_index = auth.hindex
    h_index5y = auth.hindex5y
    i10index = auth.i10index
    i10index5y = auth.i10index5y

    print("\nExtracting information for author: " + record_name + "\n")

    # Assembling SQL command to write data to the "metrics" database
    sql_s = "INSERT INTO metrics VALUES(\"" + str(record_id) + "\" , \"" + str(record_name) + "\" , " + str(cited)  + "," + str(cited5y) + "," + str(h_index) + "," + str(h_index5y) + "," + str(i10index) + "," + str(i10index5y) + ")"
    print(f"Importing data for author {record_name} into database\n")
    c.execute(sql_s)
    conn.commit()

    # Assigning the co-authors listed by the user on Google Scholar
#     coauth_manual = [auth.coauthors[i].name for i in range(len(auth.coauthors))]

    cl = [coauthor_extract(auth, i) for i in range(5)] #len(auth.publications))]
    cl_flat = list(itertools.chain.from_iterable(cl)) # Flattening list of lists

    # Constructing the dataframe
    nodeEL = pd.DataFrame({"coauthor": cl_flat})
    nodeEL["author"] = record_name
    nodeEL["id"] = record_id

    # Clean up the dataframe
    # Removing connection to self (coauthor = author)
    nodeEL = nodeEL.loc[nodeEL.coauthor != nodeEL.author]
    # Removing duplicate connections/edges for each author

    return nodeEL

def coauthor_extract(auth, i):
    try:
        coauths = auth.publications[i].fill().bib["author"].split(" and ") # Make list from coauthor string
        coauths = [ca.strip() for ca in coauths] # Remove leading and trailing whitespace

        print("Authors for publication " + str(i))
        print("=" * 60)
        [print(ca) for ca in coauths] # Print the list of names extracted
        print("\n")

        return coauths
    except:
        return("")

def generator_db(gen):
    conn = sqlite3.connect('./kolDB.db')
#     c = conn.cursor()

    for i in list(range(6)):
        el = var_extract(next(gen).fill())
        # Append the current dataframe to the database
        el.to_sql('edgelist', con = conn, index=False, if_exists='append')

    conn.commit()
    conn.close()

#################################################################
#################################################################

conn = sqlite3.connect('./kolDB.db')

c = conn.cursor()

cb_search = scholarly.search_keyword("cerebellum")

generator_db(cb_search)
