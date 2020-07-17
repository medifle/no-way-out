import map
import encryption
import pickle
from typing import List

ENCODING = 'utf-8'

class Item:
    def __init__(self, description=None, inspection=None, name=None):
        self.description = description
        self.inspection = inspection
        self.name = name

    def __str__(self):
        return "    - {}: {}\n".format(self.name, self.description)

    def __eq__(self, other):
        return self.description == other.description and self.inspection == other.inspection and self.name == other.name


class Room:
    def __init__(self, name=None, description=None, connect=[], entry_requirement=None, items=[]):
        self.name = name
        self.description = description
        self.connect = connect
        self.entry_requirement = entry_requirement
        self.items = items

    def pick_up_item(self, item):
        for i in self.items:
            if item == i:
                self.items.remove(i)

    def leave_item(self, item):
        if item and item not in self.items:
            self.items.append(item)

    def __str__(self):
        description = ""
        for room in self.connect:
            if room == 'living room' or room == 'stairs room':
                description += "    - old locked door leading to: " + room + "\n"
            elif room == 'hidden room':
                description += "    - jammed door leading to: " + room + "\n"
            else:
                description += "    - a door leading to: " + room + "\n"
        return description

    def __eq__(self, other):
        return self.name == other.name and self.description == other.description and self.connect == other.connect and self.entry_requirement == other.entry_requirement


def gen_inventory_outline(inventory: List[Item]) -> List[str]:
    outline = []
    for i in inventory:
        outline.append(i.name)
    return outline


class SavedGame():
    def __init__(self, room_name: str, inventory: List[str]):
        self.current_room_name = room_name
        self.inventory = inventory


class NoWayOutGame:
    PLAYER_ACTIONS = ["help", "goto", "search", "look", "inspect",
                      "pickup", "inventory", "operate", "save", "restore", "exit"]
    GAME_START = "You wake up, it's cold and dark. You can't remember what happened.\n"
    REQUEST = "What do I do? > "

    def __init__(self):
        self.all_items = {
            "book": Item(name="book", description="Pseudo Existence: Universe Simulation",
                         inspection="The book mentioned that a loose connection between simulation and host world was found. Not sure if there is any connection between the virtual world and my real entity. I gotta be careful here."),
            "game console": Item(name="game console", description="Atari Snake, The Last of Us",
                                 inspection="Classic games. Everything feels so real and familiar! But I can still tell this is a simulated world. I am probably inside my buggy program. Anyway, I need to find a way out of here, hopefully I left a \"backdoor\"."),
            "newspaper": Item(name="newspaper", description="A local newspaper",
                              inspection="An outbreak of 'covid-spores' happened months ago...the city was deprecated..."),
            "crowbar": Item(name="crowbar", description="A small crowbar. Useful for things that are stuck.",
                            inspection="It's a black crowbar made out of iron. It's still slightly wet."),
            "map": Item(name="map", description="A handwritten draft.", inspection=map.content),
            "vault": Item(name="vault", description="The big vault looks so weird. It is even taller than me.",
                          inspection="Looks like the lock was tampered.\nThe tag on the back shows the default combination is 00000000."),
            "broken draft": Item(name="broken draft", description="It is on top of the vault.",
                                 inspection="Full of cryptic formulas and redacted source code. Looks familiar to me. It vaguely reminds me I was a virtual reality engineer.\nFound some strange words on the back: ...base64...4 char...no validation...xor..."),
            "living room key": Item(name="living room key", description="A small dirty key.",
                                    inspection="That should allow me to get out of the basement."),
            "booklet": Item(name="booklet", description="\"How to make smashed pickles\"",
                            inspection="Hmm… Could be tasty"),
            "stairs room key": Item(name="stairs room key", description=" A small dirty key",
                                    inspection="This should let me enter stairs room"),
            "mask": Item(name="mask", description="A medical mask, similar to N95",
                         inspection="the tag reads: FLAG{20200318}")
        }
        self.room_map = {
            "hall": Room(name="hall", description="The hall is full of spores. I see the entry at the end.",
                         connect=["living room", "entry"], entry_requirement=self.all_items["mask"], items=[]),
            "living room": Room(name="living room",
                                description=" A dusty living room. The sun pierces through cracks in the wall. I see two doors at each end.",
                                connect=["hall", 'basement', 'stairs room'],
                                entry_requirement=self.all_items['living room key'],
                                items=[self.all_items['book'], self.all_items['game console'],
                                       self.all_items['newspaper']]),
            "basement": Room(name="basement", description="I find myself in a basement.", entry_requirement=None,
                             connect=["living room", "hidden room"],
                             items=[self.all_items['crowbar'], self.all_items['map']]),
            "hidden room": Room(name="hidden room", description="A very damp and small room. I hear a dripping sound.",
                                connect=["basement"], entry_requirement=self.all_items['crowbar'],
                                items=[self.all_items['vault'], self.all_items['broken draft'],
                                       self.all_items['living room key']]),
            "stairs room": Room(name="stairs room", description="I am in stairs room.",
                                connect=["living room", "attic"], entry_requirement=self.all_items['stairs room key'],
                                items=[self.all_items['booklet']]),
            "attic": Room(name="attic", description="I am in attic.", connect=["stairs room"], entry_requirement=None,
                          items=[self.all_items['stairs room key'], self.all_items['mask']]),
            "entry": Room(name="entry", description="", connect=["hall"], entry_requirement=None, items=[])
        }
        self.current_room = self.room_map['basement']
        self.inventory = []
        self.game_ended = False

    def check_player_action(self, action):
        if action in self.PLAYER_ACTIONS:
            return True
        return False

    def run_action(self, action):
        response = None
        if not self.check_player_action(action[0]):
            response = "What? I don't understand. Maybe ask for 'help'?"
            return response

        if action[0] == "help":
            response = "You can interact with your environment by using the following commands: \n" + \
                       " ".join(self.PLAYER_ACTIONS)
        elif action[0] == "goto":
            room_name = " ".join(action[1:])
            print("room: " + room_name)
            if self.room_map.get(room_name) is not None and room_name in self.current_room.connect:
                entry_requirement = self.room_map[room_name].entry_requirement
                if entry_requirement is None or (entry_requirement is not None and entry_requirement in self.inventory):
                    self.current_room = self.room_map[room_name]
                    response = self.current_room.description
                elif entry_requirement is not None and entry_requirement not in self.inventory:
                    if room_name == "hall":
                        response = "I can see spores in the air through the door window. Maybe I need a mask."
                    elif room_name == "entry":
                        response = "Damn! It's totally blocked by the outside"
                    elif room_name == "stairs room":
                        response = room_name + " is locked inside."
                    else:
                        response = room_name + " is blocked."
            else:
                response = "I am still in the same place."
        elif action[0] == "search":
            response = "You search the room, and find the following: \n"
            for item in self.current_room.items:
                response += str(item)
        elif action[0] == "look":
            response = "You see the following: \n"
            response += str(self.current_room)
        elif action[0] == "inspect":
            item_name = " ".join(action[1:])
            item = self.all_items.get(item_name)
            if item is not None and (item in self.inventory or item in self.current_room.items):
                response = item.inspection
            else:
                response = "Item not found."
        elif action[0] == "pickup":
            item_name = " ".join(action[1:])
            print("item name: " + item_name)
            if item_name == "vault":  # cannot pickup vault, but you can operate it
                response = "Can't pickup that big vault. You can use operate command to open it.\nTry to use " \
                           "'operate vault [8 digits]', e.g. operate vault 00000000."
            else:
                item = self.all_items.get(item_name)
                if item is not None and item in self.current_room.items:
                    self.current_room.pick_up_item(item)
                    self.inventory.append(item)
                    response = "You added it to your inventory"
                else:
                    response = "You did nothing"

        elif action[0] == "inventory":
            response = "You have the following items: \n"
            for item in self.inventory:
                response += str(item)
        elif action[0] == "save":
            response = "Here is your saved game: \n"
            response += self.gen_save().decode(ENCODING)
        elif action[0] == "restore":
            a = "Saved game successfully restored! \n"
            pass
        elif action[0] == "operate":
            item_name = " ".join(action[1:])
            if action[1] != "vault":
                response = "There is nothing you can do with the item: " + item_name
            else:
                if action[-1] == "00000000":
                    response = "The vault opened, but there is nothing inside.\n" \
                               "It closed automatically a few seconds later."
                elif action[-1] == "15200717":  # PERFECT_END
                    self.game_ended = True
                    response = "The vault opened! It looks like a portal I can enter... [PERFECT_END]"
                else:
                    response = "Failed to open the vault."
        elif action[0] == "exit":
            self.game_ended = True
            response = "Game exited."

        return response

    def gen_save(self):
        saved_game = SavedGame(self.current_room.name, gen_inventory_outline(self.inventory))
        pickled_save = pickle.dumps(saved_game, 0)  # protocol version 0
        return encryption.encrypt(pickled_save)
