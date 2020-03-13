## Creating a data cleaning pipeline on Australian shark attacks

*This project was completed as part of my cursus at Ironhack (a 9-week intensive coding bootcamp).*

The objective of this project was to create **a data cleaning pipeline**.
This repository contains **three files**:
 - `sharks-dataset.csv` : the **original dataset**, i.e. a table of Shark Attacks Incidents (source: [Kaggle](https://www.kaggle.com/teajay/global-shark-attacks/version/1)) 
 - `sharks-data-pipeline.py` : a **cleaning pipeline** performing successive transformations to clean the original dataset, for the purpose described in the *Context* section below
 - `sharks-dataset-cleaned.csv` : the **final dataset** (output of the above Python file)
    
#### CONTEXT OF THE STUDY

To design this cleaning pipeline, I took the following assumptions :
- **Client**: Tourism Australia wants to design an educational campaign, to avoid dangerous behaviors that could expose Australian inhabitants and visitors to shark attacks.
- **Perimeter (region and time period) of the analysis**: Australia, 1990-today
- **Question to answer**: which activities, and which areas are the most at risk?
    
#### DESCRIPTION OF THE OUTPUT FILE

The cleaned file covers the **study perimeter only** (i.e. Australia, 1990-today).
It is composed of **12 columns**:
 - **Year** (`int`) : year of the incident
 - **Month** (`str`) : month of the incident
 - **State** (`str`) : Australian state where the incident occurred (designated by their abbreviation)
 - **Location** (`str`) : location where the incident occurred (*Beach, Island, Bay, Reef, River, Port, Other*)
 - **Activity** (`str`) : activity performed when the incident occurred (*Surfing, Boarding, Diving, Snorkeling, Fishing, Swimming, Boating, Other*)
 - **Species** (`str`) : shark species involved in the incident (*White Shark, Wobbegong Shark, Bronze Whaler Shark, Tiger Shark, Bull Shark, Other*)
 - **Provoked** (`bool`) : 1 if the attack was provoked by a human, 0 if initiated by the shark (0 includes boat situations)
 - **InjuryLevel** (`int`) : severity level of the injury, from 0 to 4 (0: *No injury or NA* - 1: *Minor injury* - 2: *Middle injury* - 3: *Severe injury* - 4: *Fatal injury*)
 - **HeadInjury, ArmInjury, LegInjury, TorsoInjury** (`bool`) : 1 if the body part was injured, 0 if not .
 Elements that were unspecified in the original dataset are indicated as *NA*.

#### KEY TAKEAWAYS

- **Create categorical columns from a set of unstandardized testimonies**:
	- Rank words from high to low frequency (in a sorted dictionary `{word : frequency}`)
	- Define top-ranked words as your main categories, by making sure to include all word variations
	- Classify testimonies under these categories (for those that cannot be classified, create an *Others* category)
	- Check that the volume of unclassified elements only represents less than 10% of the whole set
- **Simplify information by dividing content between separate columns** (1 column = 1 dimension) **and using booleans** (e.g. the *InjuryLevel*, *HeadInjury*, *ArmInjury*, *LegInjury* and *TorsoInjury* columns were created from the *Injury* column, and the last 4 are booleans)
- **Merge columns if they contain overlapping information** (e.g. the *Fatal* and *InjuryLevel* columns were merged : an *InjuryLevel* of 4 represents a fatal shark incident).

#### MAIN LIBRARIES

Pandas
