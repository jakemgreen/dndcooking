# constant variables for main
TRAINING_LIST = [str(num) for num in range(6)]

SPICE_DICT = {
    "Keys": ["0-3", "4-6", "7-9", "10+"],
    "0-3": 0,
    "4-6": 1,
    "7-9": 2,
    "10+": 3
}

INGREDIENT_DICT = {
    "Keys": ["Fruit", "Vegetables", "Artisan Goods", "Legumes", "Grains", "Raw Animal Products", "Herbs", "Red Meat",
             "Seafood"],
    "Fruit": 1,
    "Vegetables": 1,
    "Artisan Goods": 1,
    "Legumes": 0,
    "Grains": 0,
    "Raw Animal Products": -1,
    "Herbs": 1,
    "Red Meat": -1,
    "Seafood": -1
}

QUALITY_DICT = {
    "Keys": ["☆", "☆☆", "☆☆☆", "☆☆☆☆", "☆☆☆☆☆"],
    "☆": 0,
    "☆☆": 1,
    "☆☆☆": 2,
    "☆☆☆☆": 4,
    "☆☆☆☆☆": 5
}
