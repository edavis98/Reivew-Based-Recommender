Author: Evan Davis

Building a Recommender Using Reviews

=====================================
Contents of directory:

Preparing Data and Scraping.ipynb
Review Analysis.ipynb
recommender.py
review_scraper.py
chromedriver.exe
adblock (directory)
environments (directory)
data (directory)
models (directory)

=====================================

### IMPORTANT ### 
The path to the 'adblock' folder must be updated to match the path on the local machine.
Otherwise, 'review_scraper.py' will not run within the first notebook!
The commented line of code to alter can be seen on line 29 of 'review_scraper.py'
The chromedriver.exe must be in the same directory as 'review_scraper.py'

The main folder contains two notebooks. 
The notebook 'Preparing Data and Scraping.ipynb' should be run first.
	-Run this notebook using the environment from 'environments/scraping_env.yml'
The notebook 'Reiview Analysis.ipynb' should be run second.
	-Run this notebook using the environment from 'environments/base_env.yml'

To run the Streamlit application, type "streamlit run recommender.py".
Run this in the terminal in the directory where 'recommender.py' is located.
A local instance of the Streamlit application will open up.

The final report for this project is found in 'Report Capstone Final.pdf'.

The main directory contains four sub-directories:
	-'adblock' contains the adblock extension necessary to run 'review_scraper.py'
	-'environments' contains the environment requirement files necessary to run the notebooks
	-'data' contains the .csv files necessary to run the notebooks, and the created .csv files
	-'models' contains the saved KNN model and TF-IDF vectorizer used to build theh Streamlit application
		