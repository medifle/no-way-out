import map


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
            if room == 'living room' or room == 'stairs room':
                description += "    - old locked door leading to: " + room + "\n"
            elif room == 'hidden room':
                description += "    - jammed door leading to: " + room + "\n"
            else:
                description += "    - a door leading to: " + room + "\n"
        return description

    def __eq__(self, other):
        return self.name == other.name and self.description == other.description and self.connect == other.connect and self.entry_requirement == other.entry_requirement


ALL_ITEMS = {
    "book": Item(name="book", description="Pseudo Existence: Universe Simulation", inspection="Not sure if there is any connection between the virtual world and my real entity. I gotta be careful here."),
    "game console": Item(name="game console", description="Atari Snake, The Last of Us", inspection="Everything feels so real and familiar! But I still can tell this is a simulated world. I am probably inside my buggy program. Anyway, I need to find a way out of here, hopefully I left a \"backdoor\"."),
    "newspaper": Item(name="newspaper", description="A local newspaper", inspection="An outbreak of 'covid-spores' happened months ago...the city was deprecated…"),
    "crowbar": Item(name="crowbar", description="A small crowbar. Useful for things that are stuck.", inspection="It's a black crowbar made out of iron. It's still slightly wet."),
    "map": Item(name="map", description="A handwritten draft.", inspection=map.content),
    "vault": Item(name="vault", description="The big vault looks so weird, it is even taller than me.", inspection="Looks like the lock was tampered. The tag on the back shows the default combination is \"00000000\"."),
    "broken draft": Item(name="broken draft", description="It is on top of the vault. Full of cryptic formulas and redacted source code. Looks familiar to me. It vaguely reminds me I was a virtual reality engineer…", inspection="...[redacted]...base64...4 char...no validation...xor..."),
    "living room key": Item(name="living room key", description="A small dirty key.", inspection="That should allow me to get out of the basement."),
    "booklet": Item(name="booklet", description="\"How to make smashed pickles\"", inspection="Hmm… Could be tasty"),
    "stairs room key": Item(name="stairs room key", description=" A small dirty key", inspection="This should let me enter stairs room"),
    "mask": Item(name="mask", description="A medical mask, similar to N95", inspection="the tag reads: FLAG{20200318}")
}

ROOM_MAP = {
    "hall": Room(name="hall", description="The hall is full of spores. I need a mask.", connect=["living room", "entry"], entry_requirement=ALL_ITEMS["mask"], items=[]),
    "living room": Room(name="living room", description=" A dusty living room. The sun pierces through cracks in the wall. I see two doors at each end.", connect=["hall", 'basement', 'stairs room'], entry_requirement=ALL_ITEMS['living room key'], items=[ALL_ITEMS['book'], ALL_ITEMS['game console'], ALL_ITEMS['newspaper']]),
    "basement": Room(name="basement", description="I find myself in a basement.", entry_requirement="", connect=["living room", "hidden room"], items=[ALL_ITEMS['crowbar'], ALL_ITEMS['map']]),
    "hidden room": Room(name="hidden room", description="A very damp and small room. I hear a dripping sound.", connect=["basement"], entry_requirement=ALL_ITEMS['crowbar'], items=[ALL_ITEMS['vault'], ALL_ITEMS['broken draft'], ALL_ITEMS['living room key']]),
    "stairs room": Room(name="stairs room", description="I am in stairs room.", connect=["living room", "attic"], entry_requirement=ALL_ITEMS['stairs room key'], items=[ALL_ITEMS['booklet']]),
    "attic": Room(name="attic", description="", connect=["stairs room"], entry_requirement="", items=[ALL_ITEMS['stairs room key'], ALL_ITEMS['mask']]),
    "entry": Room(name="entry", description="", connect=["hall"], entry_requirement="", items=[])
}


class NoWayOutGame:
    PLAYER_ACTIONS = ["help", "goto", "search", "look",
                      "inspect", "pickup", "inventory", "save", "restore"]
    GAME_START = "You wake up, it's cold and dark. You can't remember what happened.\n"
    REQUEST = "What do I do? > "

    def __init__(self, current_room=ROOM_MAP['basement'], inventory=[]):
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
        if not self.check_player_action(action[0]):
            response = "What? I don't understand. Maybe ask for 'help'?"
            return response

        if (action[0] == "help"):
            response = "You can interact with your environment by using the following commands: \n" +\
                "help, search, goto, pickup, inventory, look, inspect, save, restore"
        elif (action[0] == "goto"):
            room_name = " ".join(action[1:])
            print("room: " + room_name)
            if ROOM_MAP.get(room_name) is not None and room_name in self.current_room.connect:
                if ROOM_MAP[room_name].entry_requirement in self.inventory:
                    self.current_room = ROOM_MAP[room_name]
                    response = self.current_room.description
                else:
                    response = "You cannot go to " + room_name + " because you are blocked."
            else:
                response = "You didn't move, still in the same place."
        elif (action[0] == "search"):
            response = "You search the room, and find the following: \n"
            for item in self.current_room.items:
                response += str(item)
        elif (action[0] == "look"):
            response = "You see the following: \n"
            response += str(self.current_room)
        elif (action[0] == "inspect"):
            item_name = " ".join(action[1:])
            print("item name: " + item_name)
            item = ALL_ITEMS.get(item_name)
            if item is not None and item in self.inventory:
                response = item.inspection
            else:
                response = "The item is not in your inventory yet."
        elif (action[0] == "pickup"):
            item_name = " ".join(action[1:])
            print("item name: " + item_name)
            item = ALL_ITEMS.get(item_name)
            if item is not None and item in self.current_room.items:
                self.inventory.append(self.current_room.pick_up_item(item))
                response = "You add it to your inventory"
            else:
                response = "You did nothing"
        elif (action[0] == "inventory"):
            response = "You have the following items: \n"
            for item in self.inventory:
                response += str(item)
        elif (action[0] == "save"):
            a = "Here is your save game: \n"
            pass
        elif (action[0] == "restore"):
            a = "Here is your restore game: \n"
            pass
        return response

    def check_vault(self):
        pass
