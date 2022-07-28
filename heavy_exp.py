from glob import glob
import json
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import random
import tokenizer
import numpy as np
from multiprocessing import Pool
import multiprocessing
import copy
import time
import string

tokenizer_object = tokenizer.Spacy_Tokenizer()
DATA_PATH = './ALL_DATA_2/'
FRESH_EXP = False
all_data_file_names = os.listdir(DATA_PATH)


all_words = pd.read_csv("./results/all_data_big/allWords.csv")

all_words.dropna(inplace=True)


bad_words = ['ii', 'xix', 'c', 'amazon', 'sébastien',
            'fo', 'nathalie', 'mark', 'william', 'simon', 'raymond', 'kosovo', 'kim', 'camion', 'jo', 'om', 'cnrs', 'bretagne', 'airbus', 'maria', 'microsoft', 'maurice', 'x', 'gallimard', 'aîné', 'los',
            'carlos', 'wall', 'californie', 'milan', 'lot', 'ivoire', 'isabelle', 'christine', 'martine', 'arafat', 's.', 'ei', 'lit', 'julien', 'edouard', 'xavier', 'i', 'jérôme',
            'nantes', 'arnaud', 'tony', 'marin', 'xx', 'sixième', 'denis', 'angela', 'vivendi', 'alpes', 'alexandre', 'irelande', 'bce', 'cfdt', 'hussein', 'guy', 'tf1', 'cap', 'd.', 'tokyo', 'hamas', 'afghan',
            'to', 'michael', 'noël', 'yves', 'ali', 'f', 'taliban', 'lille']
for word_index, word in enumerate(all_words['words']):
    if word in ['covid19']:
        continue
    for i in word:
        if i not in list(string.ascii_lowercase) + ['ê', 'ù', 'é', 'è', 'ç', 'à', 'î', 'ô', 'û', 'â', 'œ', 'ë', '\'', 'ï', 'ü']:
            # print(word)
            bad_words.append(word)
            break

all_words = all_words[~all_words['words'].isin(bad_words)]
all_words['cumulative'] = all_words['frequency'].cumsum()
important_words_80 = all_words[all_words['cumulative'] <= 80]['words'].tolist()


experiment_configs = {
    'max_of_epochcs': 5,
    'nb_of_repetition_to_success': 10,
    'nb_of_articles_per_epoch': 100,
    # 'nb_of_articles_per_epoch': 5,
    'sample_size': 30
}
def init_freq_dict():
    global important_words_80

    print(f'important_words_80: {len(important_words_80)}')

    important_words_80_freq = {}
    recently_visited_word_80_freq = {}
    for word in important_words_80:
        important_words_80_freq[word] = 0
        recently_visited_word_80_freq[word] = False
    return important_words_80_freq, recently_visited_word_80_freq

def select_optimal_article_one_simulation(trial_index:int):
    global experiment_configs
    print(f'Trial {trial_index} just started')
    
    important_words_80_freq, recently_visited_word_80_freq = init_freq_dict()

    objective_reached = False
    record_numbers = {}
    meta_data = {}
    article_cnt = 1
    
    max_of_epochcs = experiment_configs['max_of_epochcs']
    while (max_of_epochcs > 0) and (objective_reached==False):
        meta_data[article_cnt] = {'date': [], 'topic': []}
        
        for article_index in range(experiment_configs['nb_of_articles_per_epoch']):
            # print(f'Article index: {article_index}')
            max_objective = 0
            sample_article_filenames = random.choices(all_data_file_names, k=experiment_configs['sample_size'])
            
            important_words_80_freq_best = None
            recently_visited_word_80_freq_best = None
            
            article_year_best = None
            article_topic_best = None
            for single_article_filename in sample_article_filenames:
                time_0 = time.time()
                important_words_80_freq_copy = copy.deepcopy(important_words_80_freq)
                recently_visited_word_80_freq_copy = copy.deepcopy(recently_visited_word_80_freq)
                # time_1 = time.time()
                # print(f'Time to copy the dicts = {time_1 - time_0}')        
                
                with open(DATA_PATH + single_article_filename, 'r') as file_handle:
                    article_content = json.load(file_handle)
                    article_year = article_content['publication_date']
                    article_topic = article_content['topic_category']
                    
                    # time_2 = time.time()                    
                    all_words, verbs, nouns, adverbs, entities = tokenizer_object(article_content)
                    # time_3 = time.time()
                    # print(f'Tokenization time = {time_3 - time_2}')        
                    
                    # Add to the observations
                    for word in all_words:
                        try:
                            important_words_80_freq_copy[word] += all_words[word]
                            recently_visited_word_80_freq_copy[word] = True
                        except:
                            continue
 
                    # Calculate the current rewards - cap each word at at
                    # time_4 = time.time()
                    observed_words = 0
                    for word in important_words_80_freq_copy:
                        if important_words_80_freq_copy[word] > experiment_configs['nb_of_repetition_to_success']:
                            observed_words += experiment_configs['nb_of_repetition_to_success']
                        else:
                            observed_words += important_words_80_freq_copy[word]
                            
                    if observed_words > max_objective: # Consider this article
                        max_objective = observed_words
                        important_words_80_freq_best = copy.deepcopy(important_words_80_freq_copy)
                        recently_visited_word_80_freq_best = copy.deepcopy(important_words_80_freq_copy)
                        
                        article_year_best = article_year
                        article_topic_best = article_topic
                    # time_5 = time.time()
                    # print(f'Calculate the reward and decide the best = {time_5 - time_4}')        
                    
                    # print(f'Total time to scan one artice from the sample: {time_5 - time_0}')
                    
                    
                                                                
            important_words_80_freq = copy.deepcopy(important_words_80_freq_best)
            recently_visited_word_80_freq = copy.deepcopy(recently_visited_word_80_freq_best)
            
            meta_data[article_cnt]['date'].append(article_year_best)
            meta_data[article_cnt]['topic'].append(article_topic_best)
                
        # Account for forgetting - each non-visited word will get a -1
        for word in recently_visited_word_80_freq: 
            if recently_visited_word_80_freq[word] == False: # Apply the memory forgetting
                important_words_80_freq[word] -= 1
                if important_words_80_freq[word] < 0:
                    important_words_80_freq[word] = 0

            elif recently_visited_word_80_freq[word] == True: # Toggle it
                recently_visited_word_80_freq[word] = False
        
        
        observed_words = 0
        for word in important_words_80_freq_copy:
            if important_words_80_freq_copy[word] > experiment_configs['nb_of_repetition_to_success']:
                observed_words += experiment_configs['nb_of_repetition_to_success']
            else:
                observed_words += important_words_80_freq_copy[word]

        success_criteria = observed_words / (len(important_words_80_freq.keys()) * experiment_configs['nb_of_repetition_to_success'])
        if success_criteria >= 1:
            objective_reached = True
            print("Mission Accomplished!")

        max_of_epochcs -= 1
        print(f'Epoch # : {max_of_epochcs} - Objective Tracking: {observed_words} - Progress Bar: {success_criteria}')

        record_numbers[article_cnt] = success_criteria

        article_cnt += 1
    
    print(f'Trial {trial_index} ENDED -------------')
    
    with open(f'heavy_exp_results_{trial_index}.json', 'w') as file_handle:
        json.dump([record_numbers, meta_data], file_handle)
        
    return record_numbers, meta_data

# select_optimal_article_one_simulation(trial_index=0)
if __name__ == "__main__":
    results = None
    time_0 = time.time()
    # trial_indices = list(range(10))
    trial_indices = list(range(30, 40))
    with Pool(multiprocessing.cpu_count()) as p:
        results = p.map(select_optimal_article_one_simulation, trial_indices)

    time_1 = time.time()

    print(f'Total time = {time_1 - time_0}')

    # with open('heavy_exp_results.json', 'w') as file_handle:
    #     json.dump(results, file_handle)