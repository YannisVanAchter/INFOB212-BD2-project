# encoding uft-8

BLOOD_PRICE_FACTOR = 2.5

ORGAN_LIST = (
    "lung",
    "heart",
    "liver",
    "stomach",
    "small intestine",
    "large intestine",
    "pancreas",
    "brain",
    "rates",
    "foot",
    "arm",
    "hand",
    "kidney",
    "bladder",
    "ear",
    "nose",
)

ORGAN_PRICEBASE_LIST = (
    "10 000",
    "2 000 000",
    "15 000",
    "12 100",
    "5 000",
    "13 000",
    "15 000",
    "4 000 000",
    "400 000",
    "5 000",
    "5 000",
    "6 000",
    "1 000 000", 
    "1 000 000",
    "5 000",
    "7 000",
)

PRODUCT_LIST = ORGAN_LIST

ORGAN_STATE_LIST = (
    "well",
    "very well",
    "good",
    "bad",
    "unknown",
    "very bad",   
)

BLOOD_TYPE = (
    "A", 
    "B", 
    "AB", 
    "O",
)

TABLE_FOR_PRICE_UPDATES = (
    "ORGANE",
    "BLOOD",
    "TYPE_DELIVERY",
    "TRANSPLATATION",
)