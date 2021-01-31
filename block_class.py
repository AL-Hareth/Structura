import os
import json


class Block:
    # Instantiate providing name, blockstates JSON Object and index
    def __init__(self, name, states, index):
        self.block_name_be = name
        self.block_states_be = states
        self.index = index
        self.find_java_equivalent()
        self.find_bedrock_model()

    # Search the Java equivalent block in the mappings and save it's name and blockstates
    def find_java_equivalent(self):
        with open("lookups/block_mappings.json") as block_mappings:
            block_mappings = json.load(block_mappings)
        for java_block in block_mappings.keys():
            if block_mappings.get(java_block).get("bedrock_identifier", None) == self.block_name_be and block_mappings.get(java_block).get("bedrock_states", None) == self.block_states_be:

                # java_block format is minecraft:redstone_wire[east=up,north=up,power=0,south=up,west=up]
                # So if it has any blockstates it contains '[' character, so we split name and blockstates from java_block
                if "[" in java_block:
                    self.block_name_java = java_block.split("[")[0]
                    self.block_states_java = java_block.split(
                        "[")[1].replace("]", "")
                else:
                    self.block_name_java = java_block
                    self.block_states_java = ""

                break

    # Will be needed in the future
    # # Search the model of the block and it's rotation
    # def find_java_model(self):
    #     path = "Vanilla_Java_Resource_Pack/blockstates"
    #     with open(path + "/" + self.block_name_java.replace("minecraft:", "") + ".json") as blockstates_file:
    #         blockstates = json.load(blockstates_file)

    #     if blockstates.get("variants") != None:
    #         for blockstate in blockstates["variants"].keys():
    #             if blockstate == self.block_states_java:
    #                 self.model = blockstates["variants"][blockstate]["model"]

    #                 x = blockstates["variants"][blockstate].get("x")
    #                 y = blockstates["variants"][blockstate].get("y")
    #                 z = blockstates["variants"][blockstate].get("z")

    #                 self.rotation = [x if x != None else 0,
    #                                  y if y != None else 0, z if z != None else 0]
    #     # If there is no variants option, that means is a multipart block
    #     # (fence, glass pane, wall, iron bars, bamboo, brewing stand, mushroom block mushroom stem, chorus, composter, fire, soulfire or redstone wire)
    #     # Will hardcode those models
    #     else:
    #         self.model = "UNDEFINED"
    #         self.rotation = [0, 0, 0]
    #     print(self.model)
    #     print(self.rotation)

    def find_bedrock_model(self):
        with open("lookups/blockshapes.json") as block_shapes:
            block_shapes = json.load(block_shapes)
        for be_block in block_shapes.keys():
            if be_block == self.block_name_be:
                self.blockshape_be = block_shapes.get(be_block)
                print(self.blockshape_be)

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
