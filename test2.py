import pandas as pd
import string
def call(sentance):
    Vowels='aeiouAEIOU'
    alpha_num={}
    for index,i in enumerate(sentance):
        alpha_num[i]=index+1
    
    vowels=[ch for ch in  sentance if ch  in  Vowels and ch.isalpha()]
    consonents=[ch for ch in  sentance if ch not in  vowels and ch.isalpha()]
   
    max_len = max(len(vowels), len( consonents))
    vowels += [None] * (max_len - len(vowels))
    consonents += [None] * (max_len - len(consonents))
    df = pd.DataFrame({'vowels': vowels, 'consonants': consonents})

    
    

    df['Vowel_Num'] = df['vowels'].apply(lambda x: alpha_num[x.lower()] if isinstance(x, str) else 0).astype(int)
    df['Consonant_Num'] = df['consonants'].apply(lambda x: alpha_num[x.lower()] if isinstance(x, str) else None)

    return df
    
data=input('enter data:')

result=call(data)
    



print(result)

