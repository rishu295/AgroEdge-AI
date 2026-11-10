"""
remedies.py
===========
Agronomic treatment and prevention database for crop leaf diseases.
Provides organic cures, chemical fungicides, and preventive advice.
"""

REMEDIES_DATABASE = {
    "Apple Scab": {
        "crop": "Apple",
        "pathogen": "Fungal (Venturia inaequalis)",
        "symptoms": "Olive-green to black velvety spots on leaves, leading to premature leaf drop and cracked fruit.",
        "organic": "Spray wettable sulfur, liquid copper, or neem oil extract at bud break. Rake and destroy fallen leaves to remove overwintering fungal spores.",
        "chemical": "Apply Captan 50 WP, Mancozeb, or Myclobutanil according to local agricultural extension spray schedules.",
        "prevention": "Prune tree canopies to encourage rapid drying through air circulation; plant scab-resistant cultivars such as Liberty or Enterprise."
    },
    "Apple with Black Rot": {
        "crop": "Apple",
        "pathogen": "Fungal (Diplodia seriata)",
        "symptoms": "Frog-eye leaf spots with purple borders and brown centers; cankers on branches and mummified black fruit.",
        "organic": "Prune out diseased twigs and cankers 6 inches below dead tissue. Remove and burn mummified fruit.",
        "chemical": "Captan or Thiophanate-methyl sprays applied from silver tip through petal fall.",
        "prevention": "Maintain tree vigor with balanced fertilization and avoid mechanical bark injuries."
    },
    "Cedar Apple Rust": {
        "crop": "Apple",
        "pathogen": "Fungal (Gymnosporangium juniperi-virginianae)",
        "symptoms": "Bright orange-yellow circular spots on the upper leaf surfaces with tiny black dots inside.",
        "organic": "Apply sulfur-based sprays or bio-fungicide Bacillus amyloliquefaciens at pink bud stage.",
        "chemical": "Triazole fungicides (e.g., Immunox / Myclobutanil) applied when apple blossoms first show color.",
        "prevention": "Remove nearby wild Eastern red cedar and juniper trees within a 1-mile radius if feasible."
    },
    "Healthy Apple": {
        "crop": "Apple",
        "pathogen": "None (Healthy)",
        "symptoms": "Vibrant green foliage with no lesions, spotting, or defoliation.",
        "organic": "Continue balanced organic compost feeding, maintain mulch layers, and conduct seasonal pruning.",
        "chemical": "No chemical treatment required.",
        "prevention": "Monitor weekly for early signs of aphids, mites, or foliar spotting."
    },
    "Cherry with Powdery Mildew": {
        "crop": "Cherry",
        "pathogen": "Fungal (Podosphaera clandestina)",
        "symptoms": "White powdery circular patches on younger leaves, curling leaf margins, and stunted shoots.",
        "organic": "Potassium bicarbonate spray, dilute milk spray (1:9 with water), or horticultural neem oil.",
        "chemical": "Myclobutanil or Quinoxyfen fungicides applied at shuck fall and repeated after 14 days.",
        "prevention": "Avoid high-nitrogen fertilizers that spur lush susceptible foliage; ensure good sunlight penetration."
    },
    "Corn (Maize) with Cercospora and Gray Leaf Spot": {
        "crop": "Corn / Maize",
        "pathogen": "Fungal (Cercospora zeae-maydis)",
        "symptoms": "Rectangular, brown to gray lesions strictly delimited by leaf veins; blighting of upper leaves.",
        "organic": "Practice minimum 2-year crop rotation with non-host crops (soybean, sunflower); deep plow crop residue.",
        "chemical": "Strobilurin or Triazole group foliar fungicides (e.g., Azoxystrobin, Pyraclostrobin) applied at VT/R1 stage.",
        "prevention": "Select high-yielding hybrid corn varieties with certified Cercospora genetic tolerance."
    },
    "Corn (Maize) with Common Rust": {
        "crop": "Corn / Maize",
        "pathogen": "Fungal (Puccinia sorghi)",
        "symptoms": "Golden-brown to cinnamon-brown powdery pustules scattered across both upper and lower leaf surfaces.",
        "organic": "Copper soap fungicide early in the season; encourage beneficial canopy aeration.",
        "chemical": "Foliar fungicides containing Pyraclostrobin or Propiconazole when rust pustules reach 5% leaf area.",
        "prevention": "Plant resistant hybrid seed varieties; early planting helps evade high mid-summer spore loads."
    },
    "Corn (Maize) with Northern Leaf Blight": {
        "crop": "Corn / Maize",
        "pathogen": "Fungal (Exserohilum turcicum)",
        "symptoms": "Long, elliptical, cigar-shaped grayish-green lesions that turn tan as leaf tissue dies.",
        "organic": "Rotate fields to legumes; chop and incorporate infested corn debris into soil to accelerate decay.",
        "chemical": "Fungicides containing Azoxystrobin + Difenoconazole or Fluxapyroxad at early silking stage.",
        "prevention": "Avoid continuous corn-on-corn planting; utilize resistant seed hybrids."
    },
    "Healthy Corn": {
        "crop": "Corn / Maize",
        "pathogen": "None (Healthy)",
        "symptoms": "Healthy dark green, broad leaves with strong erect stalks and uniform canopy.",
        "organic": "Apply balanced organic nitrogen (blood meal or vermicompost) and monitor soil moisture.",
        "chemical": "No intervention necessary.",
        "prevention": "Inspect lower canopy weekly for early rust or leaf spot symptoms."
    },
    "Grape with Black Rot": {
        "crop": "Grape",
        "pathogen": "Fungal (Guignardia bidwellii)",
        "symptoms": "Reddish-brown circular spots with dark borders on leaves; shriveled, hard, mummified black grapes.",
        "organic": "Copper and sulfur sprays starting at 3-inch shoot growth. Prune and burn infected canes.",
        "chemical": "Mancozeb, Ziram, or Tebuconazole applied from pre-bloom through 4 weeks post-bloom.",
        "prevention": "Canopy management through shoot positioning and leaf pulling to speed drying after rain."
    },
    "Bell Pepper with Bacterial Spot": {
        "crop": "Bell Pepper",
        "pathogen": "Bacterial (Xanthomonas campestris pv. vesicatoria)",
        "symptoms": "Small, water-soaked, dark angular spots on leaves and raised blister-like spots on peppers.",
        "organic": "Apply OMRI-listed Copper hydroxide mixed with biological spray Bacillus subtilis.",
        "chemical": "Fixed copper fungicides tank-mixed with Mancozeb to overcome copper-resistant bacterial strains.",
        "prevention": "Use certified pathogen-free seeds, avoid overhead sprinkler irrigation, and disinfect garden tools."
    },
    "Potato with Early Blight": {
        "crop": "Potato",
        "pathogen": "Fungal (Alternaria solani)",
        "symptoms": "Concentric rings resembling a target board or bullseye pattern on older foliage with yellow halos.",
        "organic": "Bordeaux mixture (copper sulfate + lime) or copper octanoate applied every 7-10 days.",
        "chemical": "Chlorothalonil, Azoxystrobin, or Difenoconazole applied when lower canopy leaves touch.",
        "prevention": "Drip irrigation to keep leaves dry; avoid nitrogen deficiency which increases plant susceptibility."
    },
    "Potato with Late Blight": {
        "crop": "Potato",
        "pathogen": "Oomycete (Phytophthora infestans)",
        "symptoms": "Rapidly expanding water-soaked dark green to black blotches with white fungal mold beneath leaves in moist air.",
        "organic": "Copper-based preventive sprays; immediately destroy severely infected potato vines to save tubers.",
        "chemical": "Systemic fungicides: Metalaxyl, Dimethomorph, or Cyazofamid applied ahead of cool, humid weather.",
        "prevention": "Destroy cull piles; plant only certified disease-free seed potatoes."
    },
    "Tomato with Early Blight": {
        "crop": "Tomato",
        "pathogen": "Fungal (Alternaria linariae)",
        "symptoms": "Dark brown spots with distinct concentric rings (target spots) primarily on lower, older leaves.",
        "organic": "Prune off bottom 12 inches of foliage; spray liquid copper fungicide or Serenade (Bacillus subtilis).",
        "chemical": "Chlorothalonil (Daconil) or Mancozeb sprays applied proactively every 7-10 days.",
        "prevention": "Mulch soil heavily to prevent soil-borne spores from splashing onto leaves during watering."
    },
    "Tomato with Late Blight": {
        "crop": "Tomato",
        "pathogen": "Oomycete (Phytophthora infestans)",
        "symptoms": "Greasy, dark water-soaked patches on leaves and stems; rapid wilting and brown leathery tomato fruit.",
        "organic": "Copper soap spray applied before rain events; harvest unaffected green tomatoes immediately.",
        "chemical": "Mandipropamid (Revus) or Chlorothalonil applied immediately upon regional blight warnings.",
        "prevention": "Space tomato plants 24-36 inches apart; water strictly at soil level using soaker hoses."
    },
    "Tomato with Yellow Leaf Curl Virus": {
        "crop": "Tomato",
        "pathogen": "Viral (Tomato yellow leaf curl virus - TYLCV)",
        "symptoms": "Severe stunting, upward curling of leaf margins, yellowing (chlorosis), and significant flower drop.",
        "organic": "Control the whitefly vector using insecticidal soap, yellow sticky traps, and neem oil repellent.",
        "chemical": "Systemic neonicotinoids or pyrethroids targeted strictly against the Bemisia tabaci whitefly vector.",
        "prevention": "Use fine insect netting (50-mesh); install silver reflective mulches to deter whiteflies."
    },
    "Healthy Tomato": {
        "crop": "Tomato",
        "pathogen": "None (Healthy)",
        "symptoms": "Deep green foliage, robust flowering clusters, and vigorous upright growth.",
        "organic": "Feed with balanced calcium-rich organic fertilizer to prevent blossom end rot; maintain even watering.",
        "chemical": "No chemical treatment required.",
        "prevention": "Stake plants properly to keep foliage elevated off soil and inspect underside of leaves weekly."
    }
}

DEFAULT_DISEASE_REMEDY = {
    "crop": "Agricultural Crop",
    "pathogen": "Foliar Pathogen (Fungal / Bacterial)",
    "symptoms": "Irregular discoloration, chlorosis, or necrotic spots observed across the foliar canopy.",
    "organic": "Remove and safely discard visibly affected leaves. Spray cold-pressed neem oil (1% emulsion) or organic copper soap in the early morning.",
    "chemical": "Apply broad-spectrum foliar protective fungicide (e.g., Mancozeb or Chlorothalonil 75 WP) at recommended label rates.",
    "prevention": "Ensure adequate plant spacing for ventilation, transition to drip irrigation, and rotate crops annually."
}

def get_remedy(disease_name: str) -> dict:
    """
    Retrieve treatment, prevention, and pathogen profile for any diagnosed plant class.
    """
    # Direct match
    if disease_name in REMEDIES_DATABASE:
        return REMEDIES_DATABASE[disease_name]
    
    # Partial key match
    for key, data in REMEDIES_DATABASE.items():
        if key.lower() in disease_name.lower() or disease_name.lower() in key.lower():
            return data
            
    # If classified as healthy
    if "healthy" in disease_name.lower():
        return {
            "crop": disease_name.replace("Healthy", "").strip(),
            "pathogen": "None (Healthy Crop)",
            "symptoms": "Normal leaf morphology, healthy green pigmentation, and active photosynthesis.",
            "organic": "Maintain regular balanced organic compost or vermicompost application and optimal soil hydration.",
            "chemical": "No chemical pesticides or fungicides required.",
            "prevention": "Continue standard crop rotation, routine scouting, and weed management."
        }

    # Fallback to standard agricultural remedy
    fallback = DEFAULT_DISEASE_REMEDY.copy()
    fallback["crop"] = disease_name.split()[0] if disease_name else "Crop"
    return fallback

