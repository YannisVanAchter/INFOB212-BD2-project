# encoding uft-8

BLOOD_PRICE_FACTOR = 2.5

#prix d'une poche de sang, peu importe la quantité, ça reste le même prix
BLOODPOCHE = 250

#Dico des organes avec leur prix et les quantités de poches de sang qu'il faut pour une opération d'un organe particulier 
ORGAN_DICO = {
    "lung": [10 000, 1, 0, 5], #1ere val = prix, 2eme val = nbr poche 500ml, 3eme val = nbr poche 480ml, 4eme val = nbr poche 450ml
    "heart": [2 000 000, 1, 0, 5],
    "liver": [15 000, 1, 0, 5],
    "stomach": [12 100, 1, 0, 5],
    "small intestine": [5 000, 1, 0, 5],
    "large intestine": [13 000, 1, 0, 5],
    "pancreas": [15 000, 1, 0, 5],
    "brain": [4 000 000, 1, 0, 5],
    "rates": [400 000, 1, 0, 5],
    "foot": [5 000, 1, 0, 5],
    "arm": [5 000, 1, 0, 5],
    "hand": [6 000, 1, 0, 5],
    "kidney": [1 000 000, 1, 0, 5],
    "bladder": [1 000 000, 1, 0, 5],
    "ear": [5 000, 1, 0, 5],
    "nose": [7 000, 1, 0, 5],
}

SALARY_DOCTOR_TRANSPL = {
    "lung": ,
    "heart": ,
    "liver": ,
    "stomach": ,
    "small intestine": ,
    "large intestine": ,
    "pancreas": ,
    "brain": ,
    "rates": ,
    "foot": ,
    "arm": ,
    "hand": ,
    "kidney": ,
    "bladder": ,
    "ear": ,
    "nose": ,

}

SALARY_ANESTHESIST_TRANSPL = {
    "lung": ,
    "heart": ,
    "liver": ,
    "stomach": ,
    "small intestine": ,
    "large intestine": ,
    "pancreas": ,
    "brain": ,
    "rates": ,
    "foot": ,
    "arm": ,
    "hand": ,
    "kidney": ,
    "bladder": ,
    "ear": ,
    "nose": ,

}

SALARY_NURSE_TRANSPL = {
    "lung": ,
    "heart": ,
    "liver": ,
    "stomach": ,
    "small intestine": ,
    "large intestine": ,
    "pancreas": ,
    "brain": ,
    "rates": ,
    "foot": ,
    "arm": ,
    "hand": ,
    "kidney": ,
    "bladder": ,
    "ear": ,
    "nose": ,

}


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