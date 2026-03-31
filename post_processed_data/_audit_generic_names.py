import pandas as pd
from difflib import SequenceMatcher, get_close_matches

# Load
df2 = pd.read_csv('RecipeDB1_ingredient_flavor.csv')

# Reproduce notebook cleaning logic
df2['generic_name'] = (
    df2['generic_name']
    .astype('string')
    .str.replace(r'^[\s\u00A0]+|[\s\u00A0]+$', '', regex=True)
    .str.lower()
)

noise_mask = df2['generic_name'].str.contains('http', case=False, na=False)
df2.loc[noise_mask, 'generic_name'] = (
    df2.loc[noise_mask, 'Flavor_DB_Link']
    .astype('string')
    .str.split('~')
    .str[0]
    .str.strip()
    .str.lower()
)

if 562 in df2.index:
    df2.loc[562, 'generic_name'] = 'Cheese'

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
df2['generic_name'] = df2['generic_name'].replace(typo_map)

if 4195 in df2.index:
    df2.loc[4195, 'generic_name'] = 'Alfalfa'

raw_beef = [
    'Beef','Beef Steak','Beef Brisket','Beef Tenderloin','Beef Sirloin','Beef Shank',
    'Beef Oxtail','Beef Tongue','Beef Round','Beef Skirt Steak','Beef Rib Eye Roast',
    'Beef Tri Tip','Beef Silverside','Beef Spare Ribs','Beef Ribs','Beef blade steak',
    'Beef heart','Beef Top','Beef Tripe','Stew Beef','Beef Stew Meat','Ground Beef',
    'Ground beef','Shredded Beef'
]
for beef in raw_beef:
    df2.loc[df2['generic_name'].str.lower() == beef.lower(), 'generic_name'] = 'Beef'

raw_chicken = ['chicken','chicken leg','chicken liver','stew chicken','white meat chicken']
for chicken in raw_chicken:
    df2.loc[df2['generic_name'].str.lower() == chicken.lower(), 'generic_name'] = 'Chicken'

all_cheese = df2.loc[df2['generic_name'].str.contains('cheese', case=False, na=False), 'generic_name'].unique().tolist()
for cheese in all_cheese:
    df2.loc[df2['generic_name'].str.lower() == cheese.lower(), 'generic_name'] = 'Cheese'

all_mushroom = df2.loc[df2['generic_name'].str.contains('mushroom', case=False, na=False), 'generic_name'].unique().tolist()
for mushroom in all_mushroom:
    df2.loc[df2['generic_name'].str.lower() == mushroom.lower(), 'generic_name'] = 'Mushroom'

all_pasta = df2.loc[df2['generic_name'].str.contains('pasta', case=False, na=False), 'generic_name'].unique().tolist()
all_noodle = df2.loc[df2['generic_name'].str.contains('noodle', case=False, na=False), 'generic_name'].unique().tolist()
for pasta in all_pasta:
    df2.loc[df2['generic_name'].str.lower() == pasta.lower(), 'generic_name'] = 'Pasta'
for noodle in all_noodle:
    df2.loc[df2['generic_name'].str.lower() == noodle.lower(), 'generic_name'] = 'Noodle'

raw_pea = ['pea','peas','snow pea','snap pea','english pea','split pea','black-eyed pea','pigeon pea','pea bean']
for pea in raw_pea:
    df2.loc[df2['generic_name'] == pea, 'generic_name'] = 'Pea'

bread_types = [
    'Bread','White Bread','Pita Bread','Wheat Bread','Sourdough Bread','Rye Bread','Rye bread',
    'White bread','Sandwich Bread','Whole Grain Bread','Multigrain Bread','Multigrain bread',
    'Potato bread','French Bread','Savory Bread','Crisp bread','Cornbread','Frybread','Fry Bread',
    'Bread Roll','Bread '
]
for bread in bread_types:
    df2.loc[df2['generic_name'].str.lower() == bread.lower(), 'generic_name'] = 'Bread'

wine_types = [
    'wine','white wine','red wine','rose wine','sparkling wine','port wine','marsala wine',
    'burgundy wine','madeira wine','dessert winee','ice wine','aromatic wine','muscat wine',
    'blanc wine','argentine whine'
]
for wine in wine_types:
    df2.loc[df2['generic_name'].str.lower() == wine.lower(), 'generic_name'] = 'Wine'

tomato_types = [
    'tomato','plum tomato','roma tomato','cherry tomato','grape tomato','beefsteak tomato',
    'heirloom tomato','san marzano tomato','pear tomato'
]
for tomato in tomato_types:
    df2.loc[df2['generic_name'].str.lower() == tomato.lower(), 'generic_name'] = 'Tomato'

raw_pork = [
    'pork','pork chop','pork tenderloin','pork loin','pork butt','pork belly','pork neck bone',
    'pork ribs','pork rib','baby back pork ribs','pork stew meat','pork meat','pork skin',
    'pork back','pork leg','pork jowl','pork lung'
]
for pork in raw_pork:
    df2.loc[df2['generic_name'].str.lower() == pork.lower(), 'generic_name'] = 'Pork'

# Final cleanup
df2['generic_name'] = df2['generic_name'].astype('string').str.strip().str.lower()
freq = df2['generic_name'].value_counts(dropna=False)

print('rows', len(df2), 'unique_generic', df2['generic_name'].nunique(dropna=True), 'null_generic', int(df2['generic_name'].isna().sum()))

known_candidates = [
    'atlantic croacker', 'barlett pear', 'rotell', 'dessert winee', 'argentine whine',
    'chery pepper', 'cheery pepper', 'atlantic croaker'
]
print('\nKNOWN_CANDIDATES_PRESENT')
for k in known_candidates:
    if k in freq.index:
        print(k, int(freq[k]))

patterns = [
    'lamb','turkey','duck','goat','shrimp','prawn','chili','chilli','pepper',
    'onion','garlic','vinegar','oil','bean','rice','potato','apple','orange'
]
print('\nPATTERN_VARIANTS')
for p in patterns:
    vals = sorted(df2.loc[df2['generic_name'].str.contains(p, case=False, na=False), 'generic_name'].dropna().unique().tolist())
    if len(vals) >= 4:
        print(f'[{p}] {len(vals)} variants')
        print(vals[:30])

values = [v for v in freq.index.tolist() if isinstance(v, str)]
low = [v for v in values if freq[v] <= 5 and len(v) >= 5]
high = [v for v in values if freq[v] >= 20 and len(v) >= 5]

suggestions = []
for v in low:
    matches = get_close_matches(v, high, n=1, cutoff=0.90)
    if matches:
        m = matches[0]
        ratio = SequenceMatcher(None, v, m).ratio()
        if ratio >= 0.90 and v != m:
            suggestions.append((v, m, round(ratio,3), int(freq[v]), int(freq[m])))

print('\nTYPO_LIKE_SUGGESTIONS_TOP80')
for s in sorted(suggestions, key=lambda x: (-x[2], x[3], x[0]))[:80]:
    print(s)

pairs = []
small = [v for v in values if len(v) >= 6]
for i, a in enumerate(small):
    for b in small[i+1:]:
        if a[0] != b[0]:
            continue
        if abs(len(a) - len(b)) > 2:
            continue
        r = SequenceMatcher(None, a, b).ratio()
        if r >= 0.92 and a != b:
            pairs.append((a, b, round(r,3), int(freq[a]), int(freq[b])))

print('\nNEAR_DUP_PAIRS_TOP120')
for p in sorted(pairs, key=lambda x: (-x[2], x[3] + x[4]))[:120]:
    print(p)

sset = set(values)
sp = []
for v in values:
    if v.endswith('s') and len(v) > 4:
        base = v[:-1]
        if base in sset:
            sp.append((base, v, int(freq.get(base,0)), int(freq.get(v,0))))

print('\nSINGULAR_PLURAL_VARIANTS_TOP120')
for x in sorted(sp, key=lambda t: (t[0], -(t[2]+t[3])))[:120]:
    print(x)

# additional high-value outputs
print('\nTOP80_MOST_FREQUENT')
print(freq.head(80).to_string())

# Save snapshot
out = df2[['IngID','ingredient','generic_name','Dietrx_Category']].copy()
out.to_csv('post_processed_data/_tmp_cleaned_for_audit.csv', index=False)
print('\nSaved audit file: post_processed_data/_tmp_cleaned_for_audit.csv')
