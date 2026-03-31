import pandas as pd
from difflib import SequenceMatcher

df = pd.read_csv('RecipeDB1_ingredient_flavor.csv')
g = df['generic_name'].astype('string').str.strip().str.lower()
vc = g.value_counts()
values = list(vc.index)

problem = [
    'augerbine','beaf gravy','biscut crumb','chocolate cooky','chocolate wafer cooky',
    'deer meet','jello-o','leave','mandarian orangre peel','maria cooky','roasted beaf',
    'tamarind extraxt','atlantic croacker','barlett pear','rotell','spice  mix','spicemix',
    'icecream','sea brass','chile pepper','chile powder','chile paste','muskmallo'
]

print('SUGGESTIONS_BY_SIMILARITY_X_FREQ')
for w in problem:
    cand = []
    for v in values:
        if v == w:
            continue
        sim = SequenceMatcher(None, w, v).ratio()
        if sim >= 0.72:
            score = sim * (1 + min(vc[v], 200)/200)
            cand.append((score, sim, int(vc[v]), v))
    cand = sorted(cand, key=lambda x: (-x[0], -x[2], -x[1]))[:5]
    print('\n', w)
    for sc, sim, cnt, v in cand:
        print(f'  -> {v} | sim={sim:.3f} cnt={cnt}')
