# Methods

## Dataset

The present study draws upon RecipeDB [1, 2], a large-scale structured repository of culinary data curated by the Complex Systems Laboratory (CoSyLab) at IIIT-Delhi. RecipeDB aggregates recipe information from four prominent web-based platforms—AllRecipes [3] (16,177 recipes), Food Network [4] (15,917 recipes), Epicurious [5] (11,069 recipes), and TarlaDalal [6] (2,609 recipes)—yielding a combined corpus of 118,083 recipes after inclusion of extended entries. The dataset encompasses three interlinked relational tables: (i) a *general metadata table* (`RecipeDB1_general.csv`) containing 118,083 recipes annotated with attributes including caloric content, preparation and cooking times, nutritional composition, dietary classifications, geographic region, sub-region, and continental affiliation; (ii) an *ingredient–phrase table* (`RecipeDB1_Ingredient_Phrases.csv`) comprising 1,154,404 ingredient-phrase entries that map each recipe to its constituent ingredients via standardized ingredient identifiers; and (iii) an *ingredient–flavor table* (`RecipeDB1_ingredient_flavor.csv`) cataloguing 19,019 unique ingredient entries, each annotated with a generic canonical name, a DietRx nutritional category, and a FlavorDB sensory link.

Recipes in the dataset are organized into 26 regional cuisines spanning 6 continents (African, Asian, Australasian, European, Latin American, and North American), with 75 sub-regional designations capturing finer-grained geographic provenance. The 26 cuisines include: Australian, Belgian, Canadian, Caribbean, Central American, Chinese and Mongolian, Deutschland (German), Eastern European, French, Greek, Indian Subcontinent, Irish, Italian, Japanese, Korean, Mexican, Middle Eastern, Northern Africa, Rest Africa, Scandinavian, South American, Southeast Asian, Spanish and Portuguese, Thai, UK, and US. This geographic breadth, substantially exceeding the 23 cuisines analysed in Caprioli et al. [7], affords a more comprehensive cross-cultural comparison of culinary traditions.

Each ingredient in the dataset is assigned to one of *T* = 22 culinary categories (hereafter referred to as *ingredient types*), namely: Additive, Bakery, Beverage, Beverage Alcoholic, Cereal, Condiment, Dairy, Dish, Essential Oil, Fish, Flower, Fruit, Fungus, Herb, Legume, Maize, Meat, Nuts and Seeds, Plant, Seafood, Spice, and Vegetable. This classification schema, inherited from the DietRx taxonomy within RecipeDB [1], follows a coherent set of principles grounded in biological origin, dominant culinary function, and degree of processing. Ingredients are primarily categorized by their natural source—for instance, Meat (terrestrial animal tissue), Fish (aquatic vertebrates), Seafood (aquatic invertebrates and marine organisms), and Plant (leaves, stems, and roots)—and secondarily by their prevailing culinary role, whereby aromatic leaves are designated as Herbs, flavoring seeds as Spices, and concentrated botanical extracts as Essential Oils. Items undergoing substantial transformation (e.g., Dairy, Bakery, Beverages) or employed predominantly as process aids (e.g., Additives) are assigned to dedicated classes. Notably, the present classification introduces two additional categories—Condiment and Dish—absent from the 20-type schema employed by Caprioli et al. [7], thereby enabling a more granular differentiation of processed and composite food items.


## Data Preprocessing and Ingredient Canonicalization

A rigorous multi-stage preprocessing pipeline was implemented to standardize the ingredient set, mitigate lexicographic noise, and reduce dimensional complexity while preserving the semantic integrity of the culinary data. The pipeline consisted of the following sequential stages:

### Stage 1: Schema Reduction and Deduplication

From the general metadata table, all columns not pertinent to the network construction—including caloric content, macronutrient profiles, preparation times, dietary flags, utensil listings, and processing annotations—were excised, retaining exclusively the recipe identifier, geographic region, sub-region, and continental affiliation. Duplicate recipe entries were subsequently removed. From the ingredient–flavor table, extraneous metadata fields (frequency counts, Wikipedia links, FlavorDB category designations, and DietRx linkage URLs) were discarded, preserving the ingredient identifier, raw ingredient name, canonical generic name, DietRx category, and FlavorDB link. From the ingredient–phrase table, all columns beyond the recipe number and ingredient identifier were eliminated, and entries lacking valid ingredient identifiers were excluded.

### Stage 2: Missing Value Imputation

A small number of ingredient entries (*n* = 3) exhibited null values in the `generic_name` field. These were resolved by extracting the canonical name from the associated FlavorDB link string (e.g., `Vanilla~https://...` to "Vanilla"), thereby obviating the need for row deletion and preserving the completeness of the ingredient catalogue.

### Stage 3: Noise Remediation in Generic Names

A subset of generic name entries was found to contain embedded URL fragments rather than valid ingredient labels. These anomalous entries were identified programmatically via substring matching on "http" and corrected by parsing the name component from the corresponding FlavorDB link field, followed by whitespace normalization and case standardization.

### Stage 4: Typographic Error Correction

A curated dictionary of 33 typographic mappings was manually compiled to rectify orthographic errors in the canonical ingredient names. Examples include: "asofoetida" to "asafoetida", "brocolli" to "broccoli", "jalepeno" to "jalapeno", "mozzarrella" to "mozzarella", and "vension" to "venison". All corrections were applied via exact string replacement to avoid unintended partial matches.

### Stage 5: Semantic Canonicalization

The most substantive preprocessing step involved the systematic consolidation of ingredient entries that, while lexicographically distinct, serve equivalent or overlapping culinary functions. This canonicalization followed a principled set of rules:

1. **Aggregation by Animal Species**: All anatomical cuts and preparations of a given animal were unified under a single species-level label. For instance, beef steak, beef brisket, beef tenderloin, beef sirloin, beef shank, beef oxtail, beef tongue, ground beef, and shredded beef were all mapped to "Beef". Analogous consolidations were performed for chicken (including chicken leg, chicken liver, white meat chicken), pork (including pork chop, pork tenderloin, pork belly, pork ribs, pork loin), and venison (remapped to "Deer Meat").

2. **Unification of Dairy Subtypes**: All cheese varieties—encompassing cheddar, mozzarella, parmesan, blue cheese, goat cheese, cream cheese, cottage cheese, feta, and numerous others—were collapsed into a single "Cheese" category.

3. **Consolidation of Fungal Varieties**: All mushroom cultivars and wild varieties (portobello, shiitake, chanterelle, enoki, oyster mushroom, etc.) were merged under "Mushroom".

4. **Harmonization of Starch Products**: All pasta types (spaghetti, penne, fettuccine, lasagna, etc.) were grouped as "Pasta", while all noodle varieties (ramen, udon, rice noodle, egg noodle, etc.) were unified as "Noodle".

5. **Standardization of Legume Preparations**: Pea variants—including snow pea, snap pea, English pea, split pea, black-eyed pea, and pigeon pea—were consolidated under "Pea".

6. **Grouping by Transformative Process**: All bread types produced from cereal sources (white bread, rye bread, sourdough, pita, French bread, cornbread, etc.) were aggregated as "Bread". Similarly, all fermented grape-based beverages (red wine, white wine, port wine, marsala wine, etc.) were merged as "Wine".

7. **Generalization of Ingredient Subtypes**: Specific cultivars or commercial variations were merged into their encompassing general class. For instance, cherry tomatoes, plum tomatoes, Roma tomatoes, grape tomatoes, and heirloom tomatoes were all grouped under "Tomato".

### Stage 6: Category Normalization

The DietRx category labels were standardized through a mapping schema that consolidated sub-categories into their parent classes. Notable consolidations include: all Additive sub-types (Additive-Salt, Additive-Sugar, Additive-Vinegar, Additive-Yeast) into "Additive"; Berry into "Fruit"; Gourd, Vegetable Fruit, and Vegetable Tuber into "Vegetable"; Fungi and Fungus into "Fungus"; Seed into "Nuts and Seeds"; Plant Derivative into "Plant"; and Beverage Caffeinated into "Beverage". This normalization yielded the final set of *T* = 22 ingredient types.

### Stage 7: Relational Integration and Edge List Construction

The three preprocessed tables were merged through a sequence of relational joins. The ingredient–phrase table was first joined with the ingredient–flavor table on the ingredient identifier, attaching to each recipe–ingredient pair its canonical name and category. Entries lacking a valid category assignment were discarded. The resulting intermediate table was then joined with the general metadata table on the recipe identifier, attaching the cuisine label. The final edge list, comprising 1,076,814 records with columns {recipe_id, aliased_ingredient_name, cuisine, category}, was deduplicated on the (recipe_id, aliased_ingredient_name) pair to ensure that each ingredient appears at most once per recipe. This edge list constitutes the foundational data structure from which all subsequent network analyses were derived.


## Network Representations

### Bipartite Recipe-Ingredient Graphs

For each cuisine *c* (with *c* = 1, ..., 26), the edge list was used to construct a bipartite multigraph *G_c* = (*R_c* U *I_c*, *E_c*), where *R_c* denotes the set of recipe nodes (bipartite partition 0), *I_c* denotes the set of ingredient nodes (bipartite partition 1), and *E_c* is the set of edges connecting each recipe to its constituent ingredients. Each ingredient node *i* in *I_c* carries a node attribute recording its ingredient type *t_i*. The degree of a recipe node *r* in *R_c* in this bipartite graph directly corresponds to the recipe size *n_r* (i.e., the number of distinct ingredients in recipe *r*). The resulting per-cuisine bipartite graphs were serialized in GraphML format for interoperability and additionally persisted as a pickled Python dictionary for computational efficiency.

### Ingredient-Type Co-occurrence Graphs

To construct the ingredient-type graph for a cuisine *c*, we employed the following procedure, adapted from Caprioli et al. [7]. For each recipe *r* within the cuisine, we compiled the multiset of type pairs (*t_i*, *t_j*) for every unordered pair of ingredients *i*, *j* in *r*. We then computed the co-occurrence frequency *n*(*t_i*, *t_j*) of each type pair across all recipes. An undirected edge (*t_i*, *t_j*) was added to the ingredient-type network with edge weight *w(t_i, t_j)* set equal to the computed co-occurrence frequency. The network nodes were further enriched with a relative abundance attribute *v_t*, computed as the fraction of recipes containing at least one ingredient of type *t*.

The resulting ingredient-type graphs are simple weighted graphs with *T* = 22 nodes each, enabling direct structural comparison across cuisines.

### Network Backbone Extraction via Disparity Filter

Due to the high density of the ingredient-type graphs (arising from the tendency of most type pairs to co-occur in at least some recipes), we applied the disparity filter method introduced by Serrano et al. [8] to extract statistically significant network backbones. For each node, this method tests whether the observed distribution of edge weights deviates significantly from a null model in which weights are uniformly distributed among the node's links. Edges whose weights represent statistically significant deviations (at a significance level alpha = 0.2) were retained, yielding sparser backbone networks that preserve the most informative structural features while suppressing noise.

### Maximum Spanning Trees

To further distil the essential topology of ingredient-type associations, we computed the Maximum Spanning Tree (MST) for each cuisine's ingredient-type graph using Kruskal's algorithm [9]. Prior to MST extraction, edge weights were normalized so that they summed to unity within each graph, ensuring scale-invariant comparisons across cuisines. The MST retains exactly *T* - 1 = 21 edges while maximizing the total edge weight, thereby yielding a connected tree that captures the most prominent type-type associations. MSTs serve as parsimonious "culinary fingerprints" that highlight the hierarchical organization of ingredient types within each cuisine [7, 10].


## Statistical Analysis

### Recipe Size Distribution

For each cuisine, the recipe size *n_r* (number of distinct ingredients) was computed for every recipe. The resulting distributions were visualized as a ridge plot using kernel density estimation (KDE), with cuisines ordered by their mean recipe size. Each distribution was colour-coded according to the cuisine's continental affiliation.

### Ingredient Popularity Profiles

The *popularity* of an ingredient type *t* within a cuisine *c* was defined as the fraction of total ingredient occurrences belonging to type *t* across all recipes in *c*:

> *f_c(t) = [sum over all recipes r in R_c of (sum over all ingredients i in r of delta(t_i, t))] / [sum over all recipes r in R_c of n_r]*

where delta(a, b) denotes the Kronecker delta. These popularity values were assembled into a cuisine x type matrix and visualized as a heatmap, with rows corresponding to cuisines and columns to ingredient types. To emphasize inter-cuisine deviations from the global average, column-wise *z*-scores were computed:

> *z_c(t) = [f_c(t) - mean(f(t))] / std(f(t))*

where mean(f(t)) and std(f(t)) are the mean and standard deviation of the popularity of type *t* across all 26 cuisines. The *z*-score matrix was visualized using a diverging Red-Blue colour palette (RdBu) to highlight positive and negative deviations.

### Edge Weight Z-scores

For each unique edge (type pair) across all cuisine graphs, we compiled the vector of edge weights across the 26 cuisines (assigning zero weight where the edge was absent). The per-edge *z*-score for each cuisine was then computed as:

> *z_c(e) = [w_c(e) - mean(w(e))] / std(w(e))*

These scores were visualized as strip plots, with jittered data points for each cuisine and annotated highlights identifying the edges exhibiting the maximum and minimum *z*-scores per cuisine.

### Top Co-occurrence Pairs

For each cuisine, edges in the ingredient-type graph were ranked by weight. The top 5 and top 50 edges were identified, and their cumulative weight fractions (relative to the total graph weight) were computed. Additionally, the 10 type pairs with the highest average weight across all cuisines and the 10 type pairs with the highest weight variance were tabulated.


## Implementation

All analyses were implemented in Python 3 using the following principal libraries: pandas [11] for data manipulation, NumPy [12] for numerical computation, NetworkX [13] for graph construction and analysis, Matplotlib [14] and Seaborn [15] for visualization, SciPy [16] for statistical computations (z-score), and the backbone_network package [17] for disparity filter implementation. Maximum spanning tree layouts were rendered using PyGraphviz [18] with the `twopi` radial layout engine. Category-specific SVG icons were converted to raster format via CairoSVG [19] and overlaid on network visualizations using Matplotlib's AnnotationBbox facility.

---

# Results

## Statistical Descriptors of World Cuisines

We analysed a dataset comprising *R* = 118,083 recipes distributed across 26 world cuisines, encompassing 6 continents. Following the multi-stage preprocessing pipeline described in the Methods, the original set of 19,019 raw ingredient entries was consolidated into a canonicalized set of approximately 3,337 distinct ingredient names (after typo correction, semantic canonicalization, and deduplication). Each ingredient was classified into one of *T* = 22 ingredient types, and the final edge list comprised 1,076,814 recipe-ingredient associations.

### Scaling of Recipes versus Ingredients

Figure 1 reports the relationship between the total number of distinct ingredients and the total number of recipes for each of the 26 cuisines, plotted on a lin-log scale. The distribution of distinct ingredients exhibits substantial heterogeneity across cuisines, ranging from cuisines with relatively compact ingredient repertoires to those exhibiting markedly expansive inventories. Notably, the US cuisine dominates the dataset in terms of both ingredient diversity and recipe count, consistent with its historically documented role as a melting-pot cuisine shaped by successive waves of immigration [20]. At the opposite extreme, smaller or more geographically circumscribed cuisines (e.g., Central American, Belgian) occupy the lower end of both scales.

An exponential scaling relationship is observed between the number of recipes and the number of ingredients, consistent with the findings of Caprioli et al. [7] and Kinouchi et al. [21]. A linear fit in the log-transformed recipe count against ingredient count yields a positive relationship, indicating that cuisines possessing a broader ingredient palette tend to generate exponentially more distinct recipes. This scaling behaviour suggests a combinatorial principle governing recipe creation: as the ingredient vocabulary of a cuisine expands, the space of achievable combinations grows super-linearly, reflecting both creative experimentation and the accumulation of culinary tradition.

Cuisines positioned above the best-fit curve—such as Italian and French—exhibit more recipes than their ingredient count alone would predict, suggesting a tradition of intensive recombination of a moderately sized ingredient set. Conversely, cuisines situated below the trend line maintain fewer recipes relative to their ingredient diversity, potentially reflecting a culinary tradition that favours a broader palette of ingredients distributed across fewer canonical preparations.

### Recipe Size Distributions

Figure 2a presents a ridge plot of the kernel density estimates of recipe sizes (number of ingredients per recipe) across all 26 cuisines, ordered by ascending mean recipe size. Pronounced inter-cuisine variation is evident. Scandinavian and French cuisines exhibit distributions concentrated at smaller recipe sizes (mean of approximately 6-7 ingredients), characteristic of minimalist culinary traditions that emphasize the intrinsic qualities of a few select ingredients. In contrast, Thai and African cuisines tend to favour larger recipe sizes (mean of approximately 9-10 ingredients), reflecting culinary traditions that layer multiple aromatics, spices, and complementary components within a single preparation. Asian cuisines more broadly—including Indian Subcontinent, Southeast Asian, Chinese and Mongolian, and Korean—cluster towards the right of the distribution, consistent with the empirical observation that East and South Asian culinary traditions frequently employ complex spice blends, multiple sauce components, and layered condiment systems.

European cuisines occupy an intermediate-to-low range, with notable internal diversity: Italian and Greek cuisines tend towards moderate recipe sizes, while Eastern European and Scandinavian cuisines favour more parsimonious ingredient lists. The American (US) and Canadian cuisines display broad, relatively flat distributions, reflecting the amalgamation of diverse global traditions into a heterogeneous recipe landscape. These observations align qualitatively with those reported by Caprioli et al. [7] on the smaller CulinaryDB dataset, while the expanded RecipeDB1 corpus reveals finer-grained distinctions, particularly among African, Central American, and Caribbean cuisines that were not individually represented in the earlier study.

### Ingredient Type Popularity Profiles

To characterize how different cuisines allocate their recipes across the 22 ingredient types, we computed the row-normalized popularity matrix and visualized it as a heatmap (Figure 2b). Each cell encodes the fraction of total ingredient occurrences belonging to a given type within a given cuisine. A universal pattern of ingredient utilization emerges across all cuisines: a small number of ingredient types—notably Vegetable, Additive, Spice, and Herb—exhibit consistently elevated popularity, while types such as Flower, Maize, Plant, and Essential Oil occupy the lowest-frequency tier. This hierarchical pattern of type prevalence is remarkably stable across geographically and culturally remote cuisines, suggesting that fundamental nutritional, functional, and sensory requirements impose convergent constraints on culinary composition [7, 22].

However, superimposed on this universal hierarchy are cuisine-specific deviations that encode the distinctive character of individual culinary traditions. These deviations are made explicit in the *z*-score heatmap (Figure 2d), which reveals the following notable patterns:

- **Indian Subcontinent cuisine** exhibits dramatically elevated *z*-scores for Spice, Legume, and Flower, and markedly depressed *z*-scores for Meat. This profile is consistent with the well-documented predominance of vegetarian dietary traditions in India [23], where spice-intensive preparations and the culinary use of edible flowers (e.g., as cooking oils derived from flowering plants) constitute defining features of the cuisine.

- **Scandinavian cuisine** displays below-average utilization of Vegetable, Herb, and Plant categories, reflecting the limited agricultural growing season at high latitudes, which historically constrained access to fresh produce and necessitated reliance on preserved, dairy-based, and cereal-based foodstuffs [24].

- **Japanese and Korean cuisines** exhibit elevated usage of Seafood and Fish relative to other cuisines, consistent with the island/peninsular geography and maritime culinary traditions of these nations [25].

- **US and Canadian cuisines** show relatively uniform *z*-score profiles, with most type scores falling within the +/-1 range. This flatness is interpretable as a signature of culinary homogenization driven by mass immigration and the consequent blending of diverse global traditions [7].

- **Mexican cuisine** exhibits elevated Maize usage—a geographically and culturally distinctive feature reflecting the centrality of corn-based preparations (tortillas, tamales, pozole) in Mesoamerican culinary heritage [26].

The *z*-score bar charts for five selected cuisines (Northern Africa, US, Australian, Indian Subcontinent, and Italian; Figure 2e) further illustrate these divergences, providing cuisine-level resolution that confirms the capacity of ingredient-type popularity profiles to encode culturally and geographically meaningful information.


## The Networks of Ingredient Combinations

### Backbone Networks

We constructed the ingredient-type co-occurrence graphs for each of the 26 cuisines and applied the disparity filter with a significance threshold of alpha = 0.2 to extract the statistically significant backbones. The resulting backbone networks reveal substantial inter-cuisine variation in the density and structural organization of ingredient-type associations (Figure 3a-d).

The backbone networks of US and Italian cuisines retain a high percentage of their original edges, yielding dense graphs with broadly distributed connectivity. This structural density reflects the combinatorial richness of these cuisines, wherein a wide diversity of ingredient types are paired in numerous combinations. Both cuisines also exhibit broadly similar backbone architectures, consistent with the Mediterranean-influenced character of the American recipe canon and the global diffusion of Italian culinary practices.

In contrast, the backbone networks of Indian and Japanese cuisines present markedly sparser structures, with fewer edges surviving the disparity filter. For Indian cuisine, the retained edges are heavily concentrated around the Spice node, which serves as a dominant hub connecting to nearly all other ingredient types. This star-like topology quantitatively corroborates the qualitative assessment that spices constitute the organizational axis of Indian culinary practice [23, 27]. For Japanese cuisine, the backbone emphasizes Fish, Seafood, and Additive connections, reflecting the umami-centric and marine-ingredient-focused character of traditional Japanese preparations [25].

Node sizes in the backbone visualizations are proportional to the relative frequency with which each ingredient type appears across the cuisine's recipes, providing an integrated representation of both type prevalence (node size) and type co-occurrence structure (edge topology).

### Edge Weight Z-scores Across Cuisines

Figure 3e presents the strip plot of edge weight *z*-scores for all type pairs across the 26 cuisines. For each cuisine, the *z*-scores of all edges in its ingredient-type graph are plotted along the horizontal axis, revealing the spread and extremity of the cuisine's co-occurrence patterns relative to the global distribution.

Several patterns emerge from this analysis:

- **Asian cuisines** (Indian Subcontinent, Thai, Korean, Japanese, Southeast Asian) exhibit notably long right tails in their *z*-score distributions, indicating the presence of highly distinctive type pairings that are substantially overrepresented relative to the global average. For example, the Flower-Legume pairing in Indian cuisine and the Fish-Beverage pairing in Thai cuisine attain *z*-scores exceeding +3, marking these as cuisine-defining co-occurrence signatures.

- **European and North American cuisines** (US, Canadian, Australian, UK, Irish) display comparatively compressed *z*-score distributions, with most scores falling within the [-2, +2] interval. This distributional compactness is consistent with the culinary homogenization hypothesis: cuisines shaped by extensive immigration and cultural exchange exhibit more "average" co-occurrence patterns, as the distinctive signatures of contributing traditions are diluted by blending [7].

- **African cuisines** (Northern Africa, Rest Africa) occupy intermediate positions, with moderately extended tails reflecting distinctive but less extreme type-pairing preferences—for instance, elevated Cereal-Legume co-occurrence reflecting the prevalence of grain-and-pulse-based staple preparations.

For each cuisine, the edge with the highest and lowest *z*-score is annotated in the strip plot. The annotation includes the raw co-occurrence count (number of recipes in which the type pair appears), providing a quantitative anchor for the *z*-score magnitude.

### Top Ingredient-Type Co-occurrence Pairs

Table 1 reports, for each of the 26 cuisines, the 5 edges with the largest weight in the ingredient-type graph, along with the cumulative weight fractions of the top 5 and top 50 edges. For most cuisines, the top 5 edges (representing approximately 2.5% of the 231 possible type pairs) account for approximately 13-17% of the total edge weight. The top 50 edges (approximately 22% of all possible pairs) capture 70-80% of the total weight. This concentration indicates that the co-occurrence landscape is highly heterogeneous, with a small number of type pairings dominating the weight distribution.

Table 2 (left panel) presents the 10 type pairs with the highest average weight across all 26 cuisines. The three most prominent pairings are Spice-Vegetable, Additive-Spice, and Additive-Vegetable. Notably, 9 of the top 10 pairs include at least one of Spice, Vegetable, or Additive—underscoring the universal centrality of these ingredient types in the architecture of global culinary practice. The sole exception, Additive-Meat, reflects the near-universal practice of seasoning protein preparations with salt, sugar, or acid.

Table 2 (right panel) reports the 10 type pairs with the highest weight variance (standard deviation) across cuisines. The Dairy category is implicated in 4 of the top 5 most variable pairs (Additive-Dairy, Cereal-Dairy, Dairy-Meat, Dairy-Spice), reflecting the sharp continental divide in dairy utilization: Dairy products constitute a staple of Central and Northern European cuisines but are largely absent from East and Southeast Asian culinary traditions [7, 28]. The Herb-Spice pair also exhibits high variance, reflecting divergent aromatic strategies across cuisines—some (e.g., Italian, Thai) emphasize fresh herbs, while others (e.g., Indian, Middle Eastern) rely predominantly on dried spice blends.


## Maximum Spanning Trees as Culinary Fingerprints

The maximum spanning trees (MSTs) of the ingredient-type graphs for six representative cuisines are presented in Figure 4. The MSTs distil each cuisine's co-occurrence network into a connected tree of 21 edges that maximizes the total retained weight, thereby capturing the most significant type-type associations while eliminating redundant or weak connections.

### Structural Diversity of MSTs

Clear topological distinctions among the MSTs underscore the effectiveness of this representation in highlighting culinary differences:

- **Indian Subcontinent** (Figure 4c): The MST assumes an approximately star-like topology, with Spice occupying the central hub position (highest closeness centrality). Nearly all other ingredient types connect directly to Spice or through a single intermediary, reflecting the overwhelming organizational role of spices in Indian cuisine. This configuration corroborates the findings of Jain et al. [23, 27], who demonstrated that the negative food pairing tendency in Indian cuisines—the preference for combining ingredients sharing few flavour compounds—can be attributed to the ubiquitous mediating role of spices.

- **Italian cuisine** (Figure 4d): The MST exhibits a more distributed topology, with Herb and Spice sharing central positions. This dual-core structure reflects the defining character of Italian cookery, in which fresh herbs (basil, oregano, rosemary, parsley) and spices (black pepper, chili flake) jointly orchestrate flavour construction. The Dairy node (reflecting the prominence of cheeses such as Parmigiano-Reggiano, mozzarella, and ricotta) occupies a prominent secondary position.

- **French cuisine** (Figure 4b): The MST features Dairy in a prominent position, with high-weight connections to Meat and Fungus—a configuration that encodes the centrality of butter, cream, and cheese in French culinary technique, as well as the celebrated affinity of dairy with umami-rich ingredients such as mushrooms and red meat [29].

- **US (American) cuisine** (Figure 4a): The MST displays a relatively elongated topology with a larger diameter, reflecting the absence of a single dominant organizational principle. Multiple ingredient types (Vegetable, Additive, Spice, Dairy) share intermediate centrality, consistent with the heterogeneous, multi-tradition character of American cuisine.

- **Japanese cuisine** (Figure 4e): The MST highlights the central roles of Additive (soy sauce, mirin, dashi), Seafood, and Fish, with Spice playing a subordinate role—a topology that reflects the umami-centric and marine-focused character of traditional Japanese culinary practice [25].

- **Mexican cuisine** (Figure 4f): The MST centres on Vegetable, reflecting the foundational role of tomato, onion, pepper, and squash in Mexican preparations. Maize occupies a distinctive secondary position, encoding the cultural centrality of corn in Mesoamerican food systems [26].

### MST Diameter as a Structural Metric

The diameter of the MST—defined as the length of the longest shortest path between any two nodes—provides a scalar summary of the tree's topology. Cuisines with small-diameter MSTs (e.g., Indian Subcontinent, diameter of approximately 3-4) exhibit concentrated, hub-dominated structures in which a single ingredient type mediates most co-occurrence relationships. Cuisines with large-diameter MSTs (e.g., US, Eastern European, diameter of approximately 5-6) feature more chain-like topologies, suggesting that ingredient types are combined through longer associative pathways and that no single type serves as a universal mediator. This metric thus captures, in a single number, the degree of centralization versus distribution in a cuisine's ingredient-type architecture.


## Continental and Geo-cultural Patterns

The analyses presented above converge on a set of recurring geo-cultural patterns that structure the landscape of world cuisines:

1. **Asian cuisines** are consistently distinguished by elevated Spice usage, larger recipe sizes, sparser but more distinctive backbone networks, and MSTs exhibiting star-like topologies centred on Spice or Additive. The Indian Subcontinent cuisine stands as the most extreme exemplar of this pattern, while Southeast Asian, Thai, and Korean cuisines share related but modulated versions of this structural signature.

2. **European cuisines** divide into a Northern/Continental cluster (Scandinavian, Eastern European, German, Belgian, Irish, UK) characterized by elevated Dairy and Cereal usage, moderate recipe sizes, and MSTs featuring Dairy as a prominent hub; and a Southern/Mediterranean cluster (Italian, Greek, French, Spanish and Portuguese) characterized by elevated Herb usage, moderate-to-large recipe sizes, and MSTs with distributed multi-hub topologies.

3. **American (New World) cuisines** (US, Canadian, Australian) display the most homogeneous co-occurrence profiles, compressed *z*-score distributions, and distributed MST topologies—signatures consistent with their status as immigrant-amalgamation cuisines.

4. **Latin American cuisines** (Mexican, South American, Central American, Caribbean) share elevated Vegetable and Maize usage with distinctive regional emphasis on specific type pairings (e.g., Maize-Spice, Legume-Vegetable) that encode indigenous Mesoamerican and Andean culinary traditions.

5. **African cuisines** (Northern Africa, Rest Africa) occupy an intermediate position in most analyses, with co-occurrence profiles reflecting both indigenous culinary traditions and historical exchange with Mediterranean and Middle Eastern food systems.

---

# Discussion

In this study, we have replicated and extended the network-based framework introduced by Caprioli et al. [7] for characterizing world cuisines through the structural analysis of ingredient-type combinations. By employing the substantially larger RecipeDB1 dataset—comprising 118,083 recipes across 26 cuisines compared to the 45,661 recipes across 23 cuisines analysed in the original study—we have demonstrated that the principal findings of the earlier work are robust to changes in data source, dataset scale, and ingredient classification schema. Moreover, the expanded dataset has enabled the identification of finer-grained culinary distinctions and the inclusion of regional cuisines (Central American, Belgian, Rest Africa) not represented in the previous analysis.

### Consistency with Prior Findings

The exponential scaling relationship between the number of recipes and the number of ingredients, first reported by Caprioli et al. [7] and theoretically grounded in the evolutionary framework of Kinouchi et al. [21], is reproduced in the present dataset. This scaling law appears to reflect a fundamental combinatorial principle: as a cuisine's ingredient vocabulary expands, the space of realizable recipes grows exponentially, yet only a minute fraction of the astronomically large space of possible combinations is actually realized in culinary practice. This parsimonious use of combinatorial space—what Kinouchi et al. [21] term the "non-equilibrium nature of culinary evolution"—suggests that cuisines preferentially explore the neighbourhood of known successful combinations rather than venturing into unexplored regions of ingredient space.

The hierarchical organization of ingredient-type popularity, with Vegetable, Spice, and Additive consistently dominating across cuisines, is also reproduced. This universal hierarchy likely reflects convergent evolutionary pressures: Vegetables provide essential micronutrients and fibre; Spices confer antimicrobial properties [30, 31] and enhance palatability; and Additives (salt, sugar, oil, vinegar) serve fundamental biochemical functions in preservation, flavour enhancement, and cooking technique.

### Novel Contributions

The present study contributes several extensions beyond the original framework:

1. **Expanded Geographic Coverage**: The inclusion of 26 cuisines with finer sub-regional resolution (75 sub-regions) enables a more nuanced mapping of culinary diversity, particularly within Africa, Latin America, and East Asia.

2. **Enhanced Ingredient Taxonomy**: The use of 22 rather than 20 ingredient types—with the addition of Condiment and Dish categories—provides a more granular classification that better captures the role of processed and composite food items in recipe construction.

3. **Larger Statistical Base**: The more than 2.5-fold increase in recipe count strengthens the statistical reliability of the computed co-occurrence weights, z-scores, and backbone structures, particularly for cuisines that were sparsely represented in the earlier dataset.

4. **Methodological Refinement**: The extensive preprocessing pipeline documented herein—encompassing typographic correction, semantic canonicalization, category normalization, and relational integration—establishes a reproducible and transparent workflow for the preparation of culinary network data.

### Limitations and Future Directions

Several limitations of the present analysis warrant acknowledgement. First, the ingredient classification schema, while more granular than that of Caprioli et al. [7], still inherits a degree of cultural arbitrariness from its source taxonomy. Ingredients that are perceived as functionally distinct in certain culinary traditions (e.g., seaweeds in Japanese cuisine, various rice preparations in Southeast Asian cuisines) may be conflated under broader categories, potentially obscuring culturally significant distinctions. Second, the preprocessing pipeline, despite its rigour, involves subjective decisions regarding which ingredients to merge (e.g., the aggregation of all cheese types into a single category), and alternative canonicalization strategies could yield different network structures. Third, the present analysis treats each cuisine as a static snapshot, disregarding the temporal evolution of culinary practices. Implementing a temporal network analysis—tracking how ingredient-type co-occurrence patterns shift over historical periods—would capture the dynamic, evolving nature of culinary traditions [7, 21].

Additionally, the pairwise nature of network representations inherently limits the analysis to dyadic ingredient-type associations. Higher-order representations, such as hypergraphs or simplicial complexes [32], could capture the synergistic effects of multi-ingredient combinations that are not reducible to pairwise interactions. Furthermore, integrating the present structural analysis with chemical composition data from flavour compound databases [33] could bridge the gap between the network-topological and chemosensory perspectives on food pairing.

Finally, the classification experiment conducted by Caprioli et al. [7]—in which Support Vector Machine classifiers were trained to identify cuisines from subsets of recipes using ingredient-type frequency vectors, MSTs, and full type-type graphs—was not replicated in the present study. Future work should extend this classification framework to the RecipeDB1 dataset, potentially incorporating more recent machine learning architectures (e.g., graph neural networks [34]) that can natively operate on graph-structured inputs.

### Concluding Remarks

The present study confirms that the networks of ingredient-type combinations serve as effective "culinary fingerprints" capable of encoding the distinctive character of world cuisines. The remarkable consistency of our findings with those of Caprioli et al. [7]—despite substantial differences in dataset provenance, scale, and preprocessing—attests to the robustness and generality of the network-based framework. At the same time, the richer dataset employed here has enabled the identification of additional culinary patterns and distinctions, particularly among cuisines underrepresented in previous analyses. These results collectively demonstrate that the structural organization of ingredient combinations, rather than ingredient identity alone, constitutes a fundamental axis along which world cuisines differentiate and can be systematically characterized.

---

# References

[1] Batra, D., Diwan, N., Upadhyay, U., Kalra, S., Sharma, T., Sharma, A. K., Parulekar, A., Bhensdadia, V., and Bagler, G. RecipeDB: A resource for exploring recipes. *Database*, 2020, baz131 (2020).

[2] CulinaryDB / RecipeDB. https://cosylab.iiitd.edu.in/recipedb/ (Accessed 2026).

[3] AllRecipes. AllRecipes | Recipes, How-Tos, Videos and More. https://www.allrecipes.com/ (Accessed 2026).

[4] Food Network. Food Network: Easy Recipes, Healthy Eating Ideas and Chef Recipes. https://www.foodnetwork.com/ (Accessed 2026).

[5] Epicurious. Epicurious - Recipes, Menu Ideas, Videos and Cooking Tips. https://www.epicurious.com/ (Accessed 2026).

[6] TarlaDalal.com. Tarla Dalal - Indian Recipes. https://www.tarladalal.com/ (Accessed 2026).

[7] Caprioli, C., Kulkarni, S., Battiston, F., Iacopini, I., Santoro, A., and Latora, V. The networks of ingredient combinations as culinary fingerprints of world cuisines. *npj Science of Food*, 9, 242 (2025).

[8] Serrano, M. A., Boguna, M., and Vespignani, A. Extracting the multiscale backbone of complex weighted networks. *Proceedings of the National Academy of Sciences*, 106(16), 6483-6488 (2009).

[9] Kruskal, J. B. On the shortest spanning subtree of a graph and the traveling salesman problem. *Proceedings of the American Mathematical Society*, 7(1), 48-50 (1956).

[10] Latora, V., Nicosia, V., and Russo, G. *Complex Networks: Principles, Methods and Applications*. Cambridge University Press (2017).

[11] McKinney, W. Data Structures for Statistical Computing in Python. *Proceedings of the 9th Python in Science Conference*, 56-61 (2010).

[12] Harris, C. R., et al. Array programming with NumPy. *Nature*, 585, 357-362 (2020).

[13] Hagberg, A. A., Schult, D. A., and Swart, P. J. Exploring network structure, dynamics, and function using NetworkX. *Proceedings of the 7th Python in Science Conference*, 11-15 (2008).

[14] Hunter, J. D. Matplotlib: A 2D Graphics Environment. *Computing in Science and Engineering*, 9(3), 90-95 (2007).

[15] Waskom, M. seaborn: statistical data visualization. *Journal of Open Source Software*, 6(60), 3021 (2021).

[16] Virtanen, P., et al. SciPy 1.0: fundamental algorithms for scientific computing in Python. *Nature Methods*, 17, 261-272 (2020).

[17] backbone_network Python package. https://github.com/malcolmvr/backbone_network (Accessed 2026).

[18] PyGraphviz. https://pygraphviz.github.io/ (Accessed 2026).

[19] CairoSVG. https://cairosvg.org/ (Accessed 2026).

[20] Pilcher, J. M. *The Oxford Handbook of Food History*. Oxford University Press (2012).

[21] Kinouchi, O., Diez-Garcia, R. W., Holanda, A. J., Zambianchi, P., and Roque, A. C. The non-equilibrium nature of culinary evolution. *New Journal of Physics*, 10, 073020 (2008).

[22] Goel, M. and Bagler, G. Computational gastronomy: a data science approach to food. *Journal of Biosciences*, 47, 12 (2022).

[23] Jain, A., N K, R., and Bagler, G. Analysis of food pairing in regional cuisines of India. *PLoS One*, 10, e0139539 (2015).

[24] Civitello, L. *Cuisine and Culture: A History of Food and People*. Wiley (2004).

[25] Ashkenazi, M. and Jacob, J. *The Essence of Japanese Cuisine: An Essay on Food and Culture*. University of Pennsylvania Press (2000).

[26] Pilcher, J. M. *Que Vivan los Tamales! Food and the Making of Mexican Identity*. University of New Mexico Press (1998).

[27] Jain, A., et al. Spices form the basis of food pairing in Indian cuisine. *arXiv preprint arXiv:1502.03815* (2015).

[28] Diamond, J. *Guns, Germs, and Steel: The Fates of Human Societies*. W.W. Norton (1997).

[29] This, H. *Molecular Gastronomy: Exploring the Science of Flavor*. Columbia University Press (2006).

[30] Billing, J. and Sherman, P. W. Antimicrobial functions of spices: why some like it hot. *The Quarterly Review of Biology*, 73(1), 3-49 (1998).

[31] Sherman, P. W. and Hash, G. A. Why vegetable recipes are not very spicy. *Evolution and Human Behavior*, 22, 147-163 (2001).

[32] Battiston, F., et al. Networks beyond pairwise interactions: Structure and dynamics. *Physics Reports*, 874, 1-92 (2020).

[33] Ahn, Y.-Y., Ahnert, S. E., Bagrow, J. P., and Barabasi, A.-L. Flavor network and the principles of food pairing. *Scientific Reports*, 1, 196 (2011).

[34] Wu, Z., Pan, S., Chen, F., Long, G., Zhang, C., and Yu, P. S. A comprehensive survey on graph neural networks. *IEEE Transactions on Neural Networks and Learning Systems*, 32(1), 4-24 (2021).
