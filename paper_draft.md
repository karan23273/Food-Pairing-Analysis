# Food Pairing Analysis Across Cuisines Using a New Recipe Dataset

Authors:

## Abstract

Food pairing research studies how ingredients co-occur within recipes and how these patterns vary across cuisines. We present a first analysis using a newly curated recipe dataset derived from RecipeDB1, with standardized ingredient names and harmonized food categories. We construct recipe-ingredient bipartite graphs and project them to ingredient-type co-occurrence graphs per cuisine. We then analyze recipe size distributions, ingredient type profiles, and statistically significant co-occurrence backbones. Results highlight cuisine-specific signatures and shared global structure while providing a reproducible pipeline for cross-cuisine comparison. 

## Keywords

food pairing; recipe networks; cuisine analysis; ingredient standardization; co-occurrence graphs

## 1. Introduction

Food pairing analysis has become a useful lens for understanding cultural preferences, ingredient availability, and culinary structure. Network-based approaches enable comparisons across cuisines, revealing both universal and localized patterns in ingredient usage. While prior studies have used specialized datasets, our goal is to provide an updated analysis using a newly curated dataset and a transparent preprocessing pipeline. This draft presents the dataset construction, graph methods, and preliminary findings, and outlines how the final paper will report quantitative results.

## 2. Related Work

Prior work on food pairing and flavor networks has demonstrated that ingredient co-occurrence patterns differ by cuisine and can be modeled as networks. Studies also emphasize the importance of ingredient standardization to avoid spurious nodes and inconsistent category assignments. [Add specific citations to prior food pairing papers and network methodology references.]

## 3. Data

### 3.1 Source files

We use three CSV tables derived from RecipeDB1 of CoSyLab:

- Recipe metadata: RecipeDB1_general.csv (region, sub-region, continent, timing, servings)
- Ingredient metadata: RecipeDB1_ingredient_flavor.csv (ingredient, generic_name, Dietrx_Category, Flavor_DB_Link)
- Recipe-ingredient aliases: RecipeDB1_Ingredient_Phrases.csv (recipe–ingredient links with phrase-level details)

### 3.2 Preprocessing and standardization

We implement a reproducible cleaning pipeline (see IP_updated.ipynb, preprocessing section):

- Normalize text: lower-case, strip whitespace and non-breaking spaces for generic_name and category.
- Fill missing generic_name from Flavor_DB_Link for a small set of rows; manually set three nulls (vanilla, pepper, alcohol) by index.
- Remove noisy generic_name values containing URLs by replacing them with the leading token of Flavor_DB_Link.
- Typo map: correct systematic misspellings (e.g., asofoetida→asafoetida, barlett pear→pear, rotell→pasta, roasted beaf→roasted beef, spioce mix→spice mix, vension→venison).
- Canonicalize variants to parent classes using exact-name matches: beef cuts→beef; chicken variants (chicken, chicken leg, chicken liver, stew chicken, white meat chicken, plus broth/stock/soup/roast/fried/rotisserie as needed)→chicken; all cheeses→cheese; mushrooms→mushroom; pasta/noodle families→pasta or noodle; pea forms→pea; bread varieties→bread; wine styles→wine; tomato varieties→tomato; pork cuts→pork. Venison is mapped to deer meat.
- Category harmonization: map Dietrx_Category to a concise taxonomy (e.g., additive-salt/sugar→Additive, fungus→Fungus, seed→Nuts and Seeds, beverage-alcoholic→Beverage Alcoholic, plant/plant derivative→Plant).
- Final trim and lower-case pass on generic_name and categories to ensure join consistency.

### 3.3 Merging

We rename columns and join aliases→ingredients→recipes to build a recipe–ingredient–category table, then drop duplicates per recipe–ingredient. The merged edge list is saved as ingredient_edgelist.csv and used downstream.

### 3.4 Dataset summary (placeholders)

After cleaning and merging (to be updated after execution):

- Number of recipes:
- Number of cuisines:
- Number of unique canonical ingredients:
- Number of ingredient categories:

## 4. Methods

### 4.1 Recipe-ingredient bipartite graphs

We build a bipartite graph per cuisine where recipes connect to canonicalized ingredients. Each ingredient node stores its standardized category. The resulting edge list is saved as ingredient_edgelist.csv.

### 4.2 Ingredient-type co-occurrence graphs

For each cuisine, we create a weighted ingredient-type graph where nodes are categories and edge weights represent the number of recipes in which two categories co-occur. Node attributes store the fraction of recipes that include each category.

### 4.3 Backbone extraction

We apply a disparity filter to each ingredient-type graph to identify statistically significant co-occurrences (Serrano et al., 2009), yielding a sparse backbone that highlights the strongest cross-category relationships per cuisine.

### 4.4 Maximum spanning trees

To visualize dominant structures, we compute the maximum spanning tree of each cuisine's ingredient-type graph using normalized edge weights. This provides a comparable skeleton of category interactions.

### 4.5 Statistical profiles

We compute cuisine-level summary statistics, including:

- Recipe size distributions (number of ingredients per recipe)
- Ingredient type prevalence by cuisine
- Z-score profiles of category co-occurrences across cuisines

### 4.6 Reproducibility

All preprocessing, graph construction, and plotting steps are implemented in IP_updated.ipynb. Outputs (ingredient_edgelist.csv, graph_dict_from_edgelist.pkl, per-cuisine GraphMLs, MSTs, backbones, and figures) are written under post_processed_data/ and figures/ to enable exact regeneration.

## 5. Results

### 5.1 Recipe size distributions

We observe distinct recipe size distributions across cuisines. Figure 1 shows ridge plots of recipe sizes by cuisine, revealing [insert key contrasts such as heavier tails or narrower distributions for specific cuisines].

### 5.2 Ingredient type profiles

Figure 2 reports the normalized ingredient category profiles by cuisine. Some cuisines emphasize [add categories] while others show higher prevalence of [add categories]. Figure 3 presents Z-score heatmaps that reveal cuisine-specific deviations from the global mean.

### 5.3 Backbone structure

Backbone graphs highlight stable co-occurrence pairs. For example, [insert example pair] appears strongly in [cuisine], while [insert example pair] is characteristic of [cuisine].

### 5.4 Maximum spanning trees

MST visualizations summarize dominant category flows within each cuisine, suggesting [insert structural interpretation].

## 6. Discussion

The new dataset reproduces several known patterns from prior food pairing studies while offering improved ingredient standardization and category alignment. Our results support the idea that cuisines exhibit distinct category mixing signatures, likely reflecting both cultural preferences and ingredient availability. The backbone and MST analyses provide interpretable summaries that complement frequency-based statistics.

## 7. Limitations

This draft does not yet report final statistical values, effect sizes, or hypothesis tests. Ingredient standardization choices may also affect conclusions, especially for ambiguous ingredient names or overlapping categories. In future revisions, we will report sensitivity analyses and cross-validation of category mappings.

## 8. Conclusion

We provide a reproducible analysis pipeline and initial insights into cross-cuisine food pairing using a newly curated dataset. The final paper will include quantitative results, robust statistical comparisons, and finalized figures derived from the cleaned ingredient edgelist and category co-occurrence graphs.

## Acknowledgments

[Add acknowledgments or funding statements.]

## References

[Placeholders]

- Ahn et al., 2011. Flavor network and the principles of food pairing.
- Serrano, Boguná, Vespignani, 2009. Extracting the multiscale backbone of complex weighted networks.
- Barabási et al., network science texts for methodological grounding.
- RecipeDB / FlavorDB documentation for source data.
