import pandas as pd
from difflib import get_close_matches, SequenceMatcher

# Load source
df = pd.read_csv('RecipeDB1_ingredient_flavor.csv')

# Lower-normalize generic_name for comparison
g = df['generic_name'].astype('string').str.strip().str.lower()
ing = df['ingredient'].astype('string').str.strip().str.lower()

# Typo map from notebook section under review
typo_map = {
    'asofoetida': 'asafoetida',
    'augerbine': 'aubergine',
    'avocardo': 'avocado',
    'beaf gravy': 'beef gravy',
    'biscut crumb': 'biscuit crumb',
    'blue ceese': 'blue cheese',
    'blue chesse': 'blue cheese',
    'brerad': 'bread',
    'brocolli': 'broccoli',
    'buuter cake': 'butter cake',
    'cheery pepper': 'cherry pepper',
    'chery pepper': 'cherry pepper',
    'chile con quesco': 'chile con queso',
    'chocolate cooky': 'chocolate cookie',
    'chocolate wafer cooky': 'chocolate wafer cookie',
    'deer meet': 'deer meat',
    'drak chocolate': 'dark chocolate',
    'enchliada': 'enchilada',
    'jalepeno': 'jalapeno',
    'jello-o': 'jello',
    'lavendar': 'lavender',
    'leave': 'leaf',
    'lingoberry': 'lingonberry',
    'macroni': 'macaroni',
    'mandarian orangre peel': 'mandarin orange peel',
    'maria cooky': 'maria cookie',
    'mozzarrella': 'mozzarella',
    'mung brean': 'mung bean',
    'muskmallo': 'muskmelon',
    'oyester': 'oyster',
    'patry': 'pastry',
    'roasted beaf': 'roasted beef',
    'salad dcressing': 'salad dressing',
    'salad dressong': 'salad dressing',
    'seasoend salt': 'seasoned salt',
    'spioce mix': 'spice mix',
    'spixe mix': 'spice mix',
    'tamarind extraxt': 'tamarind extract',
    'vanilla extraxt': 'vanilla extract',
    'vension': 'venison',
}

values = sorted(set(v for v in g.dropna().unique().tolist() if isinstance(v, str)))
vc = g.value_counts(dropna=False)

print('MAP_CHECK')
for wrong, right in typo_map.items():
    wrong_ct = int(vc.get(wrong, 0))
    right_ct = int(vc.get(right, 0))

    # rows where this wrong value appears
    rows = df[g == wrong][['IngID','ingredient','generic_name']].head(3)

    # find nearest alternatives besides the chosen right target
    cands = [c for c in get_close_matches(wrong, values, n=5, cutoff=0.78) if c != wrong]
    alt = ', '.join(cands[:4]) if cands else '-'

    status = 'OK'
    if wrong_ct == 0:
        status = 'NOT_PRESENT'
    elif right_ct == 0:
        status = 'TARGET_MISSING'

    print(f"{wrong} -> {right} | wrong_ct={wrong_ct} right_ct={right_ct} status={status} alts={alt}")
    if wrong_ct > 0:
        for _, r in rows.iterrows():
            print(f"  sample IngID={int(r['IngID'])} ingredient={str(r['ingredient'])}")

# Check commented uncertain ones + known leftovers
extra = [
    ('atlantic croacker','atlantic croaker'),
    ('barlett pear','bartlett pear'),
    ('rotell','rotelle'),
    ('spice  mix','spice mix'),
    ('spicemix','spice mix'),
    ('icecream','ice cream'),
    ('sea brass','sea bass'),
    ('chile pepper','chili pepper'),
    ('chile powder','chili powder'),
    ('chile paste','chili paste')
]

print('\nEXTRA_CHECK')
for wrong, right in extra:
    wrong_ct = int(vc.get(wrong, 0))
    right_ct = int(vc.get(right, 0))
    rows = df[g == wrong][['IngID','ingredient','generic_name']].head(5)
    print(f"{wrong} -> {right} | wrong_ct={wrong_ct} right_ct={right_ct}")
    if wrong_ct > 0:
        for _, r in rows.iterrows():
            print(f"  sample IngID={int(r['IngID'])} ingredient={str(r['ingredient'])}")

# Null generic names after your current style of cleaning (without hard-coded index edits)
print('\nNULL_GENERIC_ROWS')
null_rows = df[df['generic_name'].isna()][['IngID','ingredient','Flavor_DB_Link','Dietrx_Category']]
print(null_rows.to_string(index=False))
