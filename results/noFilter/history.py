import json
import pandas as pd
all_words = json.load(open("logs.json", "r"))
all_words = all_words['unique_words']
len(all_words)
all_words
len(all_words)
summation = 0
for item in all_words:
    summation += all_words[item]
summation
df = pd.DataFrame()
df.append(all_words)
df = pd.DataFrame({'words': list(all_words.keys()), 'freq': [all_words[item] for item in all_words]})
df
df = df.sort_values(by='freq')
df
df = df.sort_values(by='freq', ascending=False)
df
df['percentage'] = df['freq'] / df['freq'].sum()
df
df['percentage'] *= 100
df
df['per_cum'] = df['percentage'].cumsum()
df
df[df['per_cum'] <= 20]
df[df['per_cum'] <= 20].shape
df[df['per_cum'] <= 40].shape
df[df['per_cum'] <= 50].shape
df[df['per_cum'] <= 80].shape
df[df['per_cum'] <= 90].shape
df[df['per_cum'] <= 10].shape
df[df['per_cum'] <= 91].shape
df[df['per_cum'] <= 92].shape
df[df['per_cum'] <= 95].shape
def analyze_field(field_name):
    df = pd.DataFrame({'words': [], 'freq': []})
    df.append(all_words[field_name])
all_words = json.load(open("logs.json", "r"))
def analyze_field(field_name):
    df = pd.DataFrame({'words': [], 'freq': []})
    df.append(all_words[field_name])
    print(df.shape)
analyze_field('unique_words')
def analyze_field(field_name):
    df = pd.DataFrame({'words': [], 'freq': []})
    df.append(all_words[field_name], ignore_index=True)
    print(df.shape)
analyze_field('unique_words')
def analyze_field(field_name):
    df = pd.DataFrame({'words': list(all_words[field_name]), 'freq': [all_words[field_name][item] for item in all_words[field_name]]})
    print(df.shape)
analyze_field('unique_words')
analyze_field('unique_verbs')
def analyze_field(field_name):
    df = pd.DataFrame({'words': list(all_words[field_name]), 'freq': [all_words[field_name][item] for item in all_words[field_name]]})
    print(df.shape)
    
    df = df.sort_by(by='freq', ascending=False)
    df['percent'] = df['freq'] * 100/ df['freq'].sum()
    df['per_cum'] =  df['freq'].cumsum()
    return df
analyze_field('unique_verbs')
def analyze_field(field_name):
    df = pd.DataFrame({'words': list(all_words[field_name]), 'freq': [all_words[field_name][item] for item in all_words[field_name]]})
    print(df.shape)
    
    df = df.sortby(by='freq', ascending=False)
    df['percent'] = df['freq'] * 100/ df['freq'].sum()
    df['per_cum'] =  df['freq'].cumsum()
    return df
analyze_field('unique_verbs')
def analyze_field(field_name):
    df = pd.DataFrame({'words': list(all_words[field_name]), 'freq': [all_words[field_name][item] for item in all_words[field_name]]})
    print(df.shape)
    
    df = df.sort_values(by='freq', ascending=False)
    df['percent'] = df['freq'] * 100/ df['freq'].sum()
    df['per_cum'] =  df['freq'].cumsum()
    return df
analyze_field('unique_verbs')
def analyze_field(field_name):
    df = pd.DataFrame({'words': list(all_words[field_name]), 'freq': [all_words[field_name][item] for item in all_words[field_name]]})
    print(df.shape)
    print(f'Total number: {df["freq"].sum()}')
    
    df = df.sort_values(by='freq', ascending=False)
    df['percent'] = df['freq'] * 100/ df['freq'].sum()
    df['per_cum'] =  df['freq'].cumsum()
    return df
analyze_field('unique_verbs')
def analyze_field(field_name):
    df = pd.DataFrame({'words': list(all_words[field_name]), 'freq': [all_words[field_name][item] for item in all_words[field_name]]})
    print(df.shape)
    print(f'Total number: {df["freq"].sum()}')
    
    df = df.sort_values(by='freq', ascending=False)
    df['percent'] = df['freq'] * 100/ df['freq'].sum()
    df['per_cum'] =  df['freq'].cumsum()
    
    percentages = [10, 20, 50, 80, 90]
    for percentage_of_interest in percentages:
        print(f'{percentage_of_interest}%: {df[df["per_cum"] <= percentage_of_interest].shape}')
    return df
analyze_field('unique_verbs')
def analyze_field(field_name):
    df = pd.DataFrame({'words': list(all_words[field_name]), 'freq': [all_words[field_name][item] for item in all_words[field_name]]})
    print(df.shape)
    print(f'Total number: {df["freq"].sum()}')
    
    df = df.sort_values(by='freq', ascending=False)
    df['percent'] = df['freq'] * 100/ df['freq'].sum()
    df['per_cum'] =  df['percent'].cumsum()
    
    percentages = [10, 20, 50, 80, 90]
    for percentage_of_interest in percentages:
        print(f'{percentage_of_interest}%: {df[df["per_cum"] <= percentage_of_interest].shape}')
    return df
analyze_field('unique_verbs')
analyze_field('unique_nouns')
analyze_field('unique_adverbs')
analyze_field('unique_nouns')
%history -f ./history.py
analyze_field('unique_adverbs')
%history -f ./history.py
