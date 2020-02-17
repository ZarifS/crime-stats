# crime-stats

# Project Key Requirements
Suppose that, in subsequent discussions, the city council of Ottawa voted to create a crime data mart to study trends in crime in the Ottawa region. Your team is hired to complete a feasibility study and to produce a proof of concept. 

## Requirements (R)
1. The council is interested in looking into seasonal trends and pinpointing locations that may benefit from additional policing. 
2. Identify trends in the types and frequencies of violations over time. 
3. Exploring the trends in different types of crimes, such as crimes against a person, and crimes against property.
4. Exploring the trends in different types of specific crimes such as fraud and theft. 
5. Explore whether there are specific times of the day, or days of the week, when certain crimes occur more frequently. 
6. Determine if there is any interplay between holidays and special events (e.g. New Year, Winterlude or Fall Rhapsody) and the frequency and types of crimes committed on those days.
7. Verify if crimes against properties are more frequent during July and August, since this perception is based on hear-say, rather than facts.
8. Contrasting the occurrences in crimes in Ottawa to other major cities, such as Toronto, Vancouver or Edmonton.

Note: In order to win this contract, your team would thus need to convince the city council to secure substantial financial and human resources.

# Dataset Features

[Denver](https://www.notion.so/ee23c42609bd40e48f2a080b6ca793bf)

## Vancouver

**Data for each column is available in the PDF in the project folder.**

TYPE - Type of Crime

YEAR - Year when the reported crime activity occurred

MONTH - Month when the reported crime activity occurred

DAY - Day when the reported crime activity occurred

HOUR - Hour when the reported crime activity occurred

MINUTE - Minute when the reported crime activity occurred

HUNDRED_BLOCK- Generalized location of the report crime activity

NEIGHBOURHOOD - Neighbourhood where the reported crime activity occurred

X - Coordinate values projected in UTM Zone 10

Y - Coordinate values projected in UTM Zone 10

Latitude - Coordinate values converted to Latitude

Longitude - Coordinate values converted to Longitude

[Combination](https://www.notion.so/d746798faa854f92a3020e8495eaad94)


###Contributing

##GIT LFS
1) run 'git lfs install' in the project directory
2) run 'git lfs pull' to pull the dataset into the correct directory 

#Python VENV
0) Install jupyter notebook on your machine
1) Create a virtual environment called venv in the project directory
2) Activate the virtual environment
3) run 'pip3 -r install requirements.txt'
4) run 'ipython kernel install --user --name=venv'
5) start jupyter notebook from the project directory
6) change the jupyter notebook kernel to 'venv' (Look at the Kernel tab in toolbar')
4) start jupyter notebook from with in the project directory
