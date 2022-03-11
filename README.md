# French-Analysis
This is a simple analysis for the articles provided from LeMonde.

## Technincal Todo
[ ] Easy filtering for the articles
  [ ] Create a list of all the articles ID, with the following fields: day, month, year, category, title
  [ ] Create a function that will select the articles, filtered by the previous points
[ ] Make unified config files, and environment-dependant ones
  * For example, I want to choose a specific data path in the VM
  [x] Create a `config.py` file, to handle this logic. Replace the direct import of config files with `config.py`
  [ ] Write a script to generate the config files - in a valid format, with valid initial values
[x] Be able to recover from an abrupture in the connection/scrapping process

## Analysis Todo
* N-gram analysis: what is the most 
* TF-IDF: what are the most important words? Different from the most frequent words
  * The most frequent words in all all the document is not important
* 