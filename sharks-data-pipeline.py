# coding: utf-8

#Step 1 - Define functions performing desired transformation

import pandas as pd

def read_dataset(dataset_path):
    """Function reading the sharks dataset."""
    
    df = pd.read_csv(dataset_path,engine='python')
    return df
    
def drop_columns(df):
    """Function dropping irrelevant columns for our analysis."""
    
    #Strip column names
    for col in df.columns:
        df.rename(columns={col:col.strip(' ')},inplace=True)
      
    #Drop irrelevant columns
    cols_to_drop =\
        ['Case Number','Name','Sex','Age','Time','Investigator or Source','pdf',\
        'href formula','href','Case Number.1','Case Number.2',\
        'original order','Unnamed: 22','Unnamed: 23']
    df.drop(cols_to_drop,axis=1,inplace=True)
    
    return df

def drop_rows(df):
    """Function dropping irrelevant rows for our analysis.
    Studied perimeter: Australia, 1990-today."""
    
    df.Year = df.Year.astype(int)
    rows_to_drop = df[(df.Country!='AUSTRALIA')|(df.Year<1990)|(df.Type=='Invalid')].index
    df.drop(rows_to_drop,inplace=True)
    
    return df

def fillna_values_rename_columns(df):
    """Function filling NaN values, and renaming columns
    further used in the cleaning process."""
    
    columns = ['Date','Activity','Injury','Type','Species','Area','Location','Fatal (Y/N)']
    for col in columns:
        df[col] = df[col].fillna('NA')
        df[col] = df[col].str.lower()
    
    df.rename(columns={'Injury':'InjuryDescr'},inplace=True)
    df.rename(columns={'Fatal (Y/N)':'Fatal'},inplace=True)
    df.rename(columns={'Area':'State'},inplace=True)

    return df

def create_Month(df):
    """Function extracting months from the Date column,
    and renaming this column into 'Months'."""
    
    months = {1:'jan',2:'feb',3:'mar',4:'apr',5:'may',6:'jun',7:'jul',8:'aug',9:'sep',10:'oct',11:'nov',12:'dec'}
    for key,value in months.items():
        df.loc[df.Date.str.contains(value),'Month'] = key
    df.Month.fillna(0,inplace=True)
    df.Month = df.Month.astype(int)
    df.drop('Date',axis=1,inplace=True)
    
    return df

def clean_Activity(df):
    """Function extracting activity categories from the Activity column."""
    
    activity_groups =\
        {'surfing' : ['surf'],\
        'boarding' : ['board'],\
        'diving' : ['dive','diving','spearfish'],\
        'snorkeling' : ['snorkel'],\
        'fishing' : ['fish'],\
        'swimming' : ['swim'],\
        'boating' : ['sail','row','boat','ship','yacht','kayak']}
    
    for key,values in activity_groups.items():
        for value in values:
            df.loc[df.Activity.str.contains(value),'Activity'] = key
    
    df.loc[(~df.Activity.isin(activity_groups))&(df.Activity!='NA'),'Activity'] = 'other'
    
    return df

def create_BodyInjuries(df):
    """Function creating 4 boolean columns from the InjuryDescr column:
    HeadInjury, ArmInjury, LegInjury and TorsoInjury."""
  
    body_groups =\
        {'HeadInjury' : ['head', 'face', 'forehead', 'ear', 'eye', 'mouth', 'cheek'],\
        'ArmInjury' : ['arm', 'shoulder', 'axilla', 'elbow', 'wrist', 'hand', 'finger'],\
        'LegInjury' : ['leg', 'hip', 'tight', 'knee', 'ankle', 'foot', 'feet', 'buttock', 'calf', 'heel'],\
        'TorsoInjury' : ['torso', 'chest', 'breast', 'abdomen']}
    
    for key, values in body_groups.items():
        for value in values:
            df.loc[df.InjuryDescr.str.contains(value)==True,key] = 1
            df[key].fillna(0,inplace=True)
        df[key] = df[key].astype(int)

    return df

def create_InjuryLevel(df):
    """Function creating an InjuryLevel column, taking the following values:
    - 0: No injury or NA
    - 1: Minor injury
    - 2: Middle injury
    - 3: Severe injury
    - 4: Fatal injury"""

    #Replace InjuryDescr by 'fatal' if appropriate, and drop the Fatal column
    df.loc[df.Fatal=='y','InjuryDescr']='fatal'
    df.drop('Fatal',axis=1,inplace=True)

    #Create InjuryLevel column
    injury_levels = {\
        0:['no injury','uninjured'],\
        1:['minor','abrasion','bruise'],\
        2:['bit','lacerat'],\
        3:['severe','puncture','significant'],\
        4:['fatal']}

    InjuryLevel_array = list()
    for descr in df.InjuryDescr:
        level_list = list()
        for key, values in injury_levels.items():
            for value in values:
                if value in descr:
                    level_list.append(key)
        if (len(level_list)==0)|(0 in level_list):
            selected_level = 0
        else:
            selected_level = max(level_list)
        InjuryLevel_array.append(selected_level)

    df['InjuryLevel'] = InjuryLevel_array

    return df

def create_Provoked(df):
    """Function creating a Provoked column, taking boolean values:
    - 1: Provoked
    - 0: Unprovoked (including Boat)"""
    
    df.loc[df.Type=='provoked','Type']=1
    df.loc[df.Type!=1,'Type']=0
    
    df.Type = df.Type.astype(int)
    df.rename(columns={'Type':'Provoked'},inplace=True)
    
    return df

def clean_Species(df):
    """Function extracting species categories from the Species column."""

    shark_species = ['white shark','wobbegong shark','bronze whaler shark','tiger shark','bull shark']
    for shark in shark_species:
        df.loc[df.Species.str.contains(shark),'Species'] = shark
    df.loc[~df.Species.isin(shark_species),'Species'] = 'other'
    return df

def clean_Location(df):
    """Function extracting location categories from the Location column."""

    locations =['beach', 'island', 'bay', 'reef', 'river', 'port']
    for location in locations:
        df.loc[df.Location.str.contains(location),'Location'] = location
    df.loc[~df.Location.isin(locations),'Location'] = 'other'
    return df

def clean_States(df):
    """Function replacing states by their abbreviation."""

    states =\
        {'NSW':['new south wales'],\
        'QLD':['queensland','torres strait'],\
        'WA':['western australia'],\
        'SA':['south australia'],\
        'TAS':['tasmania'],\
        'VIC':['victoria'],\
        'CC':['territory of cocos (keeling) islands'],\
        'NT':['northern territory']}
    
    for key,values in states.items():
        for value in values:
            df.loc[df.State.str.strip(' ')==value,'State'] = key
    
    return df

def order_columns(df):
    """Function selecting and ordering the columns
    that will appear in the final dataset."""
    
    df = df[['Year','Month','State','Location','Activity','Species','Provoked',\
        'InjuryLevel','HeadInjury','ArmInjury','LegInjury','TorsoInjury']]
    return df

def save_cleaned_file(df):
    """Function saving the final dataset into a .csv format."""
    
    df.to_csv('sharks-dataset-cleaned.csv',sep=',',index=False)

#Step 2 - Define pipeline function, orchestrating above transformations

def pipeline(dataset_path):
    """Data cleaning pipeline, applying
    previously defined transformations."""
    
    save_cleaned_file(\
    order_columns(\
    clean_States(\
    clean_Location(\
    clean_Species(\
    create_Provoked(\
    create_InjuryLevel(\
    create_BodyInjuries(\
    clean_Activity(\
    create_Month(\
    fillna_values_rename_columns(\
    drop_rows(\
    drop_columns(\
    read_dataset(dataset_path)\
    )))))))))))))

#Step 3 - Run cleaning pipeline

pipeline('sharks-dataset.csv')
