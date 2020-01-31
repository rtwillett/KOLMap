import numpy as np
import pandas as pd
import sqlite3


def cleanName(n):
    s_list = [i.capitalize() for i in n.split(" ")]

    f_init = s_list[0][:1]
    l_name = s_list[-1]

    new_name = f_init + " " + l_name


#     name = ' '.join(s_list)
    return new_name


conn = sqlite3.connect('./kolDB.db')
conn.cursor()

c.execute("SELECT author1,author2 FROM edgelist") # Extracting the edgelist from the database
el = c.fetchall() # Save all of the data saved by the cursor
el_df = pd.DataFrame(el, columns=["author1", "author2"]) # Make a dataframe from the list of tuples

# Clean the names to align name format and remove duplicates. Will simplify the nodes in the final graph.
el_df['author1'] = el_df.author1.apply(lambda x: cleanName(x))
el_df['author2'] = el_df.author2.apply(lambda x: cleanName(x))
el_df = el_df.loc[el_df.author1 != el_df.author2] # Remove any self connections after cleaning the name

# Post the dataframe to the a clean table
el_df.to_sql('edgelist_clean', conn, index=None)

# Commit and close changes to the database
conn.commit()
conn.close()
