# KOLMap
This project pulls data from Google Scholar using the Scholarly Python package to identify Key Opinion Leaders in the field. Relevant data about authors are extracted including: the name of coauthors, publications metrics (e.g. number of times cited and h-index), the name of publications, and where/when they were published. These data are stored in a MySQL database along with an edge list for how authors are connected in the publication network.

An R notebook is included of example code for how the edgelist may be used to build the publication network (with the [igraph](https://igraph.org/r/) package) and components of it visualized (with the [Sigmanet](https://github.com/iankloo/sigmaNet) package). 
