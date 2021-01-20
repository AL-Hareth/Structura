import os
import json


class Block:
    # Instantiate providing name, blockstates JSON Object and index
    def __init__(self, name, states, index):
        self.block_name_be = name
        self.block_states_be = states
        self.index = index
        # Search the Java equivalent block in the mappings and save it's name and blockstates
        with open("lookups/block_mappings.json") as block_mappings:
            block_mappings = json.load(block_mappings)
        for java_block in block_mappings.keys():
            if block_mappings.get(java_block).get("bedrock_identifier", None) == self.block_name_be and block_mappings.get(java_block).get("bedrock_states", None) == self.block_states_be:

                ## java_block format is minecraft:redstone_wire[east=up,north=up,power=0,south=up,west=up]
                ## So if it has any blockstates it contains '[' character, so we split name and blockstates from java_block
                if "[" in java_block:
                    self.block_name_java = java_block.split("[")[0]
                    self.block_states_java = java_block.split(
                        "[")[1].replace("]", "")
                else:
                    self.block_name_java = java_block
                    self.block_states_java = ""

                break

    def __repr__(self):
        return str(self.block_name_be + ", " + str(self.block_states_be) + ", " + str(self.index))

    def get_bedrock_name(self):
        return self.block_name_be

    def get_bedrock_states(self):
        return self.block_states_be

    def get_java_name(self):
        return self.block_name_java

    def get_java_states(self):
        return self.block_states_java
