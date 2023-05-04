# encoding uft-8

#prix d'une poche de sang, peu importe la quantité, ça reste le même prix
BLOODPOCHE = 250
BLOOD_PRICE_FACTOR = BLOODPOCHE

#Dico des organes avec leur prix et les quantités de poches de sang qu'il faut pour une opération d'un organe particulier 
ORGAN_DICO = {
    "lung": [10000, 1, 0, 5], #1ere val = prix, 2eme val = nbr poche 500ml, 3eme val = nbr poche 480ml, 4eme val = nbr poche 450ml
    "heart": [2000000, 1, 0, 5],
    "liver": [15000, 1, 0, 5],
    "stomach": [12100, 1, 0, 5],
    "small intestine": [5000, 1, 0, 5],
    "large intestine": [13000, 1, 0, 5],
    "pancreas": [15000, 1, 0, 5],
    "brain": [4000000, 1, 0, 5],
    "rates": [400000, 1, 0, 5],
    "foot": [5000, 1, 0, 5],
    "arm": [5000, 1, 0, 5],
    "hand": [6000, 1, 0, 5],
    "kidney": [1000000, 1, 0, 5],
    "bladder": [1000000, 1, 0, 5],
    "ear": [5000, 1, 0, 5],
    "nose": [7000, 1, 0, 5]
}

ORGAN_DICO_TRANSPLANTATION = ORGAN_DICO

SALARY_DOCTOR_TRANSPL = {
    "lung": 500,
    "heart": 1200,
    "liver": 700, #foie
    "stomach": 500,
    "small intestine": 800,
    "large intestine": 750,
    "pancreas": 700,
    "brain": 2000,
    "rates": 1000,
    "foot": 400,
    "arm": 400,
    "hand": 400,
    "kidney": 900, #rein
    "bladder": 780, #vessie
    "ear": 900,
    "nose": 800,

}

SALARY_ANESTHESIST_TRANSPL = {
    "lung": 400,
    "heart": 1100,
    "liver": 600,
    "stomach": 400,
    "small intestine": 700,
    "large intestine": 650,
    "pancreas": 600,
    "brain": 1900,
    "rates": 900,
    "foot": 300,
    "arm": 300,
    "hand": 300,
    "kidney": 800,
    "bladder": 680,
    "ear": 800,
    "nose": 700

}

SALARY_NURSE_TRANSPL = {
    "lung": 200,
    "heart": 550,
    "liver": 300,
    "stomach": 200,
    "small intestine": 350,
    "large intestine": 325,
    "pancreas": 300,
    "brain": 950,
    "rates": 450,
    "foot": 150,
    "arm": 150,
    "hand": 150,
    "kidney": 400,
    "bladder": 340,
    "ear": 400,
    "nose": 350

}


ORGAN_STATE_LIST = (
    "well",
    "very well",
    "good",
    "bad",
    "unknown",
    "very bad"
)

BLOOD_TYPE = (
    "A", 
    "B", 
    "AB", 
    "O"
)

TABLE_FOR_PRICE_UPDATES = (
    "ORGANE",
    "BLOOD",
    "TYPE_DELIVERY",
    "TRANSPLATATION"
)