import pandas as pd

df = pd.read_csv('post_processed_data/_tmp_cleaned_for_audit.csv')
s = df['generic_name'].astype('string')

print('double_space_count', int(s.str.contains(r'  ', na=False).sum()))
print('double_space_unique', s[s.str.contains(r'  ', na=False)].dropna().unique().tolist())
print('contains_http_count', int(s.str.contains('http', case=False, na=False).sum()))
punct = s[s.str.contains(r"[^a-z0-9\s\-']", regex=True, na=False)].dropna().unique().tolist()
print('punctuation_nonstandard_unique_top30', punct[:30])
