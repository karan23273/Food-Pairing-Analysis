import pandas as pd

# Load
df = pd.read_csv('RecipeDB1_ingredient_flavor.csv')

# Normalize text
g = df['generic_name'].astype('string').str.strip().str.lower()
ing = df['ingredient'].astype('string').str.strip().str.lower()

# 1) generic_name variants containing chicken
mask_g = g.str.contains('chicken', case=False, na=False)
chicken_generic = (
    g[mask_g]
    .value_counts()
    .rename_axis('generic_name')
    .reset_index(name='count')
)

print('CHICKEN_GENERIC_VARIANTS')
print(chicken_generic.to_string(index=False))

# 2) ingredient contains chicken but generic_name does NOT contain chicken
mask_ing_chicken = ing.str.contains('chicken', case=False, na=False)
mask_g_not_chicken = ~g.str.contains('chicken', case=False, na=False)
miss = df[mask_ing_chicken & mask_g_not_chicken].copy()

print('\nINGREDIENT_HAS_CHICKEN_BUT_GENERIC_NOT')
if miss.empty:
    print('None')
else:
    print(miss[['IngID','ingredient','generic_name','Dietrx_Category']].to_string(index=False))

# 3) Optional poultry-like non-chicken candidates
keywords = ['hen','broiler','cock','rooster','poulet']
cand = pd.Series(False, index=df.index)
for kw in keywords:
    cand = cand | ing.str.contains(kw, case=False, na=False)

cand_df = df[cand & mask_g_not_chicken][['IngID','ingredient','generic_name','Dietrx_Category']]
print('\nPOSSIBLE_POULTRY_NON_CHICKEN')
if cand_df.empty:
    print('None')
else:
    print(cand_df.to_string(index=False))
