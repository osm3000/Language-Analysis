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
[ ] Make a list of bad article (that returns 404). I am curious about them.
[ ] Scrap the latest articles (most of March)

## Analysis Todo
* N-gram analysis: what is the most 
* TF-IDF: what are the most important words? Different from the most frequent words
  * The most frequent words in all all the document is not important
* What is the average number of unique words per category? how did the numbers evolve over the years?
* Seasonality:
* Discover stop words


## What to do now with all this data?
1. Sync all of them in one place - preferably a local storage
   1. I am not clear on what the point from a database now
   2. It 'might be' interesting to explore BigQuery
      1. Need to re-think about the schema
2. To make it easier to identify the articles, why not changing the choice of using a unique ID for the document, to a hashing of the URL?
   1. Maybe it is a bit too late now for this tbh. 
   2. Let's do it anyway. I will have a big problem soon to sync all the data together. I would like to avoid repeated articles
3. Consolidate all of that in one single place
   1. Do that locally for now.
   2. Remove any replications
      1. Rename the files to be a hashing from md5, thus, by default, no repetitions can happen.
4. A DB or no? what to do? Local or not?
   1. The quickest and cleanest thing is firebase storage
   2. Very cheap
   3. This or a DB? or both?
   4. I am very tempted to use Supabase. It will take a bit to setup on the big machine, but it should resolve the issues
      1. Is it document based or SQL based? (I think the latter)
   5. Let's try. Use SQL-lite, put 50K articles on it. See how it goes from there
5. To ease my queries, I need to find to build:
   1. An async data filtering --> The current data loading is sequential
   2. A random sampling mechanism: for the sake of testing and many other things, working with a small subset of this data is more than enough.
6. Add the 'publication date' metadata to all the articles
7. Make a general check that all articles have the same schema