import numpy as np
import pandas as pd
import scholarly
import sqlite3
import itertools

keysearch = input("Enter keyword for network map: ")

def var_extract(auth):
    '''
    Take a Scholarly author object and extracts informatino about the author and their publications.
    '''

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
#     print(sql_s)
    c.execute(sql_s)
    conn.commit()

    # Assigning the co-authors listed by the user on Google Scholar
#     coauth_manual = [auth.coauthors[i].name for i in range(len(auth.coauthors))]

    # Extracts relevant information from each publication in an author's record
    cl = [pub_extract(auth, i) for i in range(len(auth.publications))]

    # Unpack data from publication extraction into dataframe and upload to database
    [pub_unpacker(l, record_name) for l in cl]

#     return pd.concat(testOut)

def pub_unpacker(d, name):

    coauths, pub_title, pub_url, pub_journal = d

#     cl_flat = list(itertools.chain.from_iterable(coauths)) # Flattening list of lists

    coauths.append(name)

    if len(coauths) >2:

        pubEL = edgelister(coauths)

    #     list1 = [[a] * len(coauths) for a in coauths]
    #     list1a = list(itertools.chain.from_iterable(list1))

    #     list2 = [coauths] * len(coauths)
    #     list2a = list(itertools.chain.from_iterable(list2))

    #     pubEL = pd.DataFrame({"author1": list1a, "author2": list2a})
        pubEL["title"] = pub_title
        pubEL["url"] = pub_url
        pubEL["journal"] = pub_journal

            # Clean up the dataframe
        # Removing connection to self (coauthor = author)
    #     pubEL = pubEL.loc[pubEL.author1 != pubEL.author2]

        # Removing duplicate connections/edges for each author
        pubEL.drop_duplicates(inplace=True)

        # Enter the dataframe into a database
        pubEL.to_sql('edgelist', con = conn, index=False, if_exists='append')

        conn.commit()

    #     return pubEL

    else:
        print("No coauthors found")

def edgelister(simple_list):

    listSet1 = []
    for i in range(len(simple_list)-1):
        test = [simple_list[i]] * (len(simple_list) -1 -i)
        listSet1.append(test)

    listSet2 = []
    for i in range(1, len(simple_list)):
#         print(simple_list[i:])
        test2 = simple_list[i:]
        listSet2.append(test2)

    listSet1_expanded = list(itertools.chain.from_iterable(listSet1))
    listSet2_expanded = list(itertools.chain.from_iterable(listSet2))

    el_df = pd.DataFrame({'author1': listSet1_expanded, 'author2': listSet2_expanded})

    return el_df

def pub_extract(auth, i):

    '''
    Expands the publications field of the scholarly author object and extracts the coauthor names and manuscript
    title from each publication. Returns a tuple of coauthor (list), pub title (string), pub url (string) and the
    journal name (string).
    '''

    try:
        pubStub = auth.publications[i].fill()
        coauths = pubStub.bib["author"].split(" and ") # Make list from coauthor string
        coauths = [ca.strip() for ca in coauths] # Remove leading and trailing whitespace

        print("Authors for publication " + str(i))
        print("=" * 60)
        [print(ca) for ca in coauths] # Print the list of names extracted
        print("\n")

        pub_title = pubStub.bib["title"]
        pub_url = pubStub.bib["url"]
        pub_journal = pubStub.bib["journal"]

        return (coauths, pub_title, pub_url, pub_journal)
    except:
        return([], "", "", "")

def generator_db(gen):

    '''
    Opens up a connection to a sqlite database, iterates through the scholarly generator and extracts the information
    for each author.
    '''

    conn = sqlite3.connect('./kolDB.db')
#     c = conn.cursor()


    for i in gen:
        var_extract(i.fill())

    # conn.commit() # Commits the SQL queries specified by functions to the sqlite datebase.
    conn.close()

#################################################################
#################################################################

conn = sqlite3.connect('./kolDB.db')

c = conn.cursor()

cb_search = scholarly.search_keyword(keysearch) #("air_quality")

generator_db(cb_search)
