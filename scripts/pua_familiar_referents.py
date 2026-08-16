#!/usr/bin/env python3
"""Canonical standard-emoji anatomy reused by synonymous PUA referents.

Each source is unique so the PUA review corpus does not gain duplicate
silhouettes.  The mapping deliberately covers physical, nameable referents;
abstract concepts keep their authored sumi-e studies and monochrome fallback.
"""

from __future__ import annotations


FAMILIAR_REFERENTS = {
    # Science: physical referents, not abstract scientific concepts.
    "science/body.svg": "1F9CD.svg",          # standing person
    "science/clinic.svg": "1F3E5.svg",        # hospital
    "science/globe.svg": "1F310.svg",         # globe with meridians
    "science/medicine.svg": "1F48A.svg",      # pill
    "science/planet.svg": "1FA90.svg",        # ringed planet
    "science/sensor.svg": "1F4E1.svg",        # satellite antenna
    "science/tool.svg": "1F6E0.svg",          # hammer and wrench
    "science/vaccine.svg": "1F489.svg",       # syringe

    # People: the small concrete subset embedded in the social vocabulary.
    "people/clothing.svg": "1F455.svg",       # T-shirt
    "people/food.svg": "1F372.svg",           # pot of food
    "people/gift.svg": "1F381.svg",           # wrapped present
    "people/shelter.svg": "1F3E0.svg",        # house
    "people/shrine.svg": "26E9.svg",          # Shinto shrine
    "people/temple.svg": "1F6D5.svg",         # Hindu temple

    # Objects: use conventional object silhouettes a young child can name.
    "objects/bill.svg": "1F4B5.svg",           # banknote
    "objects/board.svg": "1F4CB.svg",          # clipboard
    "objects/bowl.svg": "1F963.svg",           # bowl with spoon
    "objects/brush.svg": "1F58C.svg",          # paintbrush
    "objects/canvas.svg": "1F5BC.svg",         # framed picture
    "objects/caravan.svg": "1F699.svg",        # recreational vehicle
    "objects/castle.svg": "1F3F0.svg",         # European castle
    "objects/computer.svg": "1F4BB.svg",       # personal computer
    "objects/currency.svg": "1F4B0.svg",       # money bag
    "objects/doll.svg": "1FA86.svg",           # nesting dolls
    "objects/drum.svg": "1F941.svg",           # drum with drumsticks
    "objects/engine.svg": "1F682.svg",         # steam locomotive
    "objects/fork.svg": "1F374.svg",           # fork and knife
    "objects/gift.svg": "1F9E7.svg",           # red gift envelope
    "objects/goods.svg": "1F4E6.svg",          # package
    "objects/knife.svg": "1F5E1.svg",          # dagger knife
    "objects/letter.svg": "2709.svg",          # envelope
    "objects/motor.svg": "2699.svg",           # gear
    "objects/note.svg": "1F4DD.svg",           # memo
    "objects/paint.svg": "1F3A8.svg",          # artist palette
    "objects/pan.svg": "1F373.svg",            # cooking pan
    "objects/puzzle.svg": "1F9E9.svg",         # jigsaw puzzle piece
    "objects/robot.svg": "1F916.svg",          # robot face
    "objects/sock.svg": "1F9E6.svg",           # socks
    "objects/spice.svg": "1F336.svg",          # hot pepper
    "objects/treasure.svg": "1F48E.svg",       # gem stone
    "objects/wagon.svg": "E344.svg",           # wheelbarrow

    # Locations: one landmark or activity cue per place type.
    "locations/academy.svg": "1F3EB.svg",      # school
    "locations/archive.svg": "1F5C2.svg",      # card-index dividers
    "locations/bakery.svg": "1F35E.svg",       # bread
    "locations/cafe.svg": "2615.svg",          # hot beverage
    "locations/dock.svg": "2693.svg",          # anchor
    "locations/encyclopedia.svg": "1F4D6.svg", # open book
    "locations/hive.svg": "1F36F.svg",         # honey pot
    "locations/laboratory.svg": "2697.svg",    # alembic
    "locations/library.svg": "1F4DA.svg",      # books
    "locations/market.svg": "1F6D2.svg",       # shopping trolley
    "locations/museum.svg": "1F3DB.svg",       # classical building
    "locations/park.svg": "1F3DE.svg",         # national park
    "locations/sign.svg": "1FAA7.svg",         # placard
    "locations/store.svg": "1F3EA.svg",        # convenience store
    "locations/street.svg": "1F6E3.svg",       # motorway
    "locations/theater.svg": "1F3AD.svg",      # performing arts
    "locations/tower.svg": "1F5FC.svg",        # Tokyo tower
    "locations/workshop.svg": "1F528.svg",     # hammer
}


if len(set(FAMILIAR_REFERENTS.values())) != len(FAMILIAR_REFERENTS):
    raise RuntimeError("familiar PUA referents must use distinct canonical silhouettes")
