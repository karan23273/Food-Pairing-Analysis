import pandas as pd

df = pd.read_csv('RecipeDB1_ingredient_flavor.csv')
g = df['generic_name'].astype('string').str.strip().str.lower()
vc = g.value_counts(dropna=False)

queries = [
    # problem mappings
    'aubergine','eggplant','beef gravy','gravy','beef stock','biscuit crumb','bread crumb','biscuit',
    'chocolate cookie','cookie','chocolate wafer cookie','wafer','venison','deer meat',
    'jello','gelatin','leaf','mandarin orange peel','orange peel','mandarin orange',
    'maria cookie','roasted beef','roast beef','tamarind extract','tamarind',
    # extras
    'atlantic croacker','atlantic croaker','croaker','pear','bartlett pear','barlett pear',
    'rotell','rotelle','rotini','pasta','spice  mix','spicemix','spice mix',
    'icecream','ice cream','sea brass','sea bass','chile pepper','chili pepper',
    'chile powder','chili powder','chile paste','chili paste'
]

print('TERM_COUNTS')
for q in queries:
    print(q, int(vc.get(q,0)))

print('\nPROBLEM_ROWS_CONTEXT')
problem_terms = ['augerbine','beaf gravy','biscut crumb','chocolate cooky','chocolate wafer cooky','deer meet','jello-o','leave','mandarian orangre peel','maria cooky','roasted beaf','tamarind extraxt','atlantic croacker','barlett pear','rotell']
for t in problem_terms:
    sub = df[g == t][['IngID','ingredient','generic_name','Dietrx_Category']]
    if len(sub):
        print('\n---', t, '---')
        print(sub.to_string(index=False))
