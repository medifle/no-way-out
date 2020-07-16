import random

ALL_ITEMS = {
    "book": Item(name="book", description="Pseudo Existence: Universe Simulation", inspection="Not sure there is any connection between the virtual world and my real entity. I gotta be careful here."),
    "game console": Item(name="game console", description="Atari Snake, The Last of Us", inspection="Everything feels so real and familiar! But I still can tell this is a simulated world. I am probably inside my buggy program. Anyway, I need to find a way out of here, hopefully I left a \"backdoor\"."),
    "newspaper": Item(name="newspaper", description="A local newspaper", inspection="An outbreak of 'covid-spores' happened months ago...the city was deprecated…"),
    "crowbar": Item(name="crowbar", description="A small crowbar. Useful for things that are stuck.", inspection="It's a black crowbar made out of iron. It's still slightly wet."),
    "map": Item(name="map", description="Damped handwritten draft.", inspection="[an ascii DRAW]"),
    "vault": Item(name="vault", description="The big vault looks so weird, it is even taller than me.", inspection="Looks like the lock was tampered. The tag on the back shows the default combination is \"00000000\"."),
    "broken draft": Item(name="broken draft", description="It is on top of the vault. Full of cryptic formulas and redacted source code. Looks familiar to me. It vaguely reminds me I was a virtual reality engineer…", inspection="...[redacted]...base64...4 char...no validation...xor..."),
    "living room key": Item(name="living room key", description="A small dirty key.", inspection="That should allow me to get out of the basement."),
    "booklet": Item(name="booklet", description="", inspection=""),
    "stairs room key": Item(name="stairs room key", description=" A small dirty key", inspection="This should let me enter stairs room"),
    "mask": Item(name="mask", description="A medical mask, similar to N95", inspection="the tag reads: FLAG{20200318}")
}

ROOM_MAP = {
    "hall": Room(name="hall", description="The hall is full of spores. I need a mask.", connect=[ROOM_MAP["living room"], ROOM_MAP["exterior door"]], entry_requirement=ALL_ITEMS["mask"], item=[]),
    "living room": Room(name="living room", description=" A dusty living room. The sun pierces through cracks in the wall. I see two doors at each end.", connect=[ROOM_MAP["hall"], ROOM_MAP['basement'], ROOM_MAP['stairs roome']], entry_requirement=ALL_ITEMS['living room key'], item=[ALL_ITEMS['book'], ALL_ITEMS['game console'], ALL_ITEMS['newspaper']]),
    "basement": Room(name="basement", description="I find myself in a basement.", entry_requirement="", connect=[ROOM_MAP["living room"], ROOM_MAP["hidden room"]], item=[ALL_ITEMS['crowbar'], ALL_ITEMS['map']]),
    "hidden room": Room(name="hidden room", description="A very damp and small room. I hear a dripping sound.", connect=[ROOM_MAP["basement"]], entry_requirement=ALL_ITEMS['crowbar'], item=[ALL_ITEMS['vault'], ALL_ITEMS['broken draft'], ALL_ITEMS['living room key']]),
    "stairs room": Room(name="stairs room", description="I am in stairs room.", connect=[ROOM_MAP["living room"], ROOM_MAP["attic"]], entry_requirement=ALL_ITEMS['stairs room key'], item=[ALL_ITEMS['booklet']]),
    "attic": Room(name="attic", description="", connect=[ROOM_MAP["stairs room"]], entry_requirement="", item=[ALL_ITEMS['stairs room key'], ALL_ITEMS['mask']]),
    "exterior door": Room(name="exterior door", description="", connect=[ROOM_MAP["hall"]], entry_requirement="", item=[])
}


class NoWayOutGame:
    PLAYER_ACTIONS = ["help", "goto", "search", "look",
                      "inspect", "pickup", "inventory", "save", "restore"]
    GAME_START = "You wake up, it's cold and dark. You can't remember what happened.\n"
    REQUEST = "What do I do? > "
    DOORS = ["old locked door", "jammed door"]

    def __init__(self, current_room=None, inventory=[]):
        self.current_room = current_room
        self.inventory = inventory

    def check_game_state(self):
        pass

    def check_player_action(self, action):
        if action in self.PLAYER_ACTIONS:
            return True
        return False

    def run_action(self, action):
        response = None
        if not check_player_action(action[0]):
            response = "What? I don't understand. Maybe ask for 'help'?"
            return response

        if (action[0] == "help"):
            response = "You can interract with your environment by using the following commands: \n" +\
                "help, search, goto, pickup, inventory, look, inspect, save, restore"
        elif (action[0] == "goto"):
            room_name = "".join(action[1:], " ")
            print("room: " + room_name)
            if ROOM_MAP.get(room_name) is not None:
                self.current_room = ROOM_MAP[room_name]
                response = self.current_room.description
            else:
                response = "You didn't move, still in the same place."
        elif (action[0] == "search"):
            response = "You search the room, and find the following: \n"
            for item in self.current_room.items:
                response += str(item)
        elif (action[0] == "look"):
            response = "You see the following: \n"
            for room in self.current_room.connect:
                response += str(room)
        elif (action[0] == "inspect"):
            item_name = "".join(action[1:], " ")
            print("item name: " + item_name)
            item = ALL_ITEMS.get(item_name)
            if item is not None and item in self.inventory:
                response = item.inspection
            else:
                response = "The item is not in your inventory yet."
        elif (action[0] == "pickup"):
            item_name = "".join(action[1:], " ")
            print("item name: " + item_name)
            item = ALL_ITEMS.get(item_name)
            if item is not None and item in self.current_room.items:
                self.inventory.append(self.current_room.pickup(item))
                response = "You add it to your inventory"
            else:
                response = "You did nothing"
        elif (action[0] == "inventory"):
            response = "You have the following items: \n"
            for item in self.inventory:
                response += str(item)
        elif (action[0] == "save"):
            pass
        elif (action[0] == "restore"):
            pass
        return response


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
        try:
            return self.items.pop(self.items.index(item))
        except ValueError:
            pass

    def leave_item(self, item):
        if item and item not in self.items:
            self.items.append(item)

    def __str__(self):
        description = ""
        for room in self.connect:
            if room == ROOM_MAP['living room']:
                description += "    - old locked door leading to: " + room.name + "\n"
            elif room == ROOM_MAP['hidden room']:
                description += "    - jammed door leading to: dark room\n"
        return description

    def __eq__(self, other):
        return self.name == other.name and self.description == other.description and self.connect == other.connect and self.entry_requirement == other.entry_requirement
