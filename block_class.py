import os, json

class block:
    def __init__(self, name, states, x, y, z):
        with open("lookups/block_mappings.json") as block_mappings:
            block_mappings = json.load(block_mappings)
        self.block_name_be = name
        self.block_states_be = states
        self.coords = [x, y, z]