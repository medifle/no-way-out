import binascii
import random
import base64

key_words = [
    "BOAR", "BOAT", "BOCA", "BOCK", "BODE", "BODY", "BOGY", "BOHR", "BOIL",
    "BOLD", "BOLO", "BOLT", "BOMB", "BONA", "BOND", "BONE", "BONG", "BONN",
    "BONY", "BOOK", "BOOM", "BOON", "BOOT", "BORE", "BORG", "BORN", "BOSE",
    "BOSS", "BOTH", "BOUT", "BOWL", "BOYD", "BRAD", "BRAE", "BRAG", "BRAN",
    "BRAY", "BRED", "BREW", "BRIG", "BRIM", "BROW", "BUCK", "BUDD", "BUFF",
    "BULB", "BULK", "BULL", "BUNK", "BUNT", "BUOY", "BURG", "BURL", "BURN",
    "BURR", "BURT", "BURY", "BUSH", "BUSS", "BUST", "BUSY", "BYTE", "CADY",
    "CAFE", "CAGE", "CAIN", "CAKE", "CALF", "CALL", "CALM", "CAME", "CANE",
    "CANT", "CARD", "CARE", "CARL", "CARR", "CART", "CASE", "CASH", "CASK",
    "CAST", "CAVE", "CEIL", "CELL", "CENT", "CERN", "CHAD", "CHAR", "CHAT",
    "CHAW", "CHEF", "CHEN", "CHEW", "CHIC", "CHIN", "CHOU", "CHOW", "CHUB",
    "CHUG", "CHUM", "CITE", "CITY", "CLAD", "CLAM", "CLAN", "CLAW", "CLAY",
    "CLOD", "CLOG", "CLOT", "CLUB", "CLUE", "COAL", "COAT", "COCA", "COCK",
    "COCO", "CODA", "CODE", "CODY", "COED", "COIL", "COIN", "COKE", "COLA",
    "COLD", "COLT", "COMA", "COMB", "COME", "COOK", "COOL", "COON", "COOT",
    "CORD", "CORE", "CORK", "CORN", "COST", "COVE", "COWL", "CRAB", "CRAG",
    "CRAM", "CRAY", "CREW", "CRIB", "CROW", "CRUD", "CUBA", "CUBE", "CUFF",
    "CULL", "CULT", "CUNY", "CURB", "CURD", "CURE", "CURL", "CURT", "CUTS",
    "DADE", "DALE", "DAME", "DANA", "DANE", "DANG", "DANK", "DARE", "DARK",
    "DARN", "DART", "DASH", "DATA", "DATE", "DAVE", "DAVY", "DAWN", "DAYS",
    "DEAD", "DEAF", "DEAL", "DEAN", "DEAR", "DEBT", "DECK", "DEED", "DEEM",
    "DEER", "DEFT", "DEFY", "DELL", "DENT", "DENY", "DESK", "DIAL", "DICE",
    "DIED", "DIET", "DIME", "DINE", "DING", "DINT", "DIRE", "DIRT", "DISC",
    "DISH", "DISK", "DIVE", "DOCK", "DOES", "DOLE", "DOLL", "DOLT", "DOME",
    "DONE", "DOOM", "DOOR", "DORA", "DOSE", "DOTE", "DOUG", "DOUR", "DOVE",
    "DOWN", "DRAB", "DRAG", "DRAM", "DRAW", "DREW", "DRUB", "DRUG", "DRUM",
    "DUAL", "DUCK", "DUCT", "DUEL", "DUET", "DUKE", "DULL", "DUMB", "DUNE",
    "DUNK", "DUSK", "DUST", "DUTY", "EACH", "EARL", "EARN", "EASE", "EAST",
    "EASY", "EBEN", "ECHO", "EDDY", "EDEN", "EDGE", "EDGY", "EDIT", "EDNA",
    "EGAN", "ELAN", "ELBA", "ELLA", "ELSE", "EMIL", "EMIT", "EMMA", "ENDS",
    "ERIC", "EROS", "EVEN", "EVER", "EVIL", "EYED", "FACE", "FACT", "FADE",
    "FAIL", "FAIN", "FAIR", "FAKE", "FALL", "FAME", "FANG", "FARM", "FAST",
    "FATE", "FAWN", "FEAR", "FEAT", "FEED", "FEEL", "FEET", "FELL", "FELT",
    "FEND", "FERN", "FEST", "FEUD", "FIEF", "FIGS", "FILE", "FILL", "FILM",
    "FIND", "FINE", "FINK", "FIRE", "FIRM", "FISH", "FISK", "FIST", "FITS",
]


def get_random_word():
    return random.choice(key_words)


def encrypt(in_bytes):
    key = bytearray(get_random_word().encode('ascii'))
    encrypted_data = xor(key, in_bytes)
    return base64.b64encode(key + encrypted_data)


def xor(key, data):
    encrypt_array = bytearray(data)
    keylen = len(key)
    for i, b in enumerate(encrypt_array):
        encrypt_array[i] ^= key[i % keylen]
    return encrypt_array


def decrypt(b64_cipher_bytes):
    try:
        cipher_bytes = base64.b64decode(b64_cipher_bytes)
        key = cipher_bytes[:4]
        print(cipher_bytes)
        print("")
        print(key)  # e.g. BOLD
        print("")
        decrypted_array = xor(key, cipher_bytes[4:])
        return decrypted_array
    except binascii.Error as e:
        print(e)
        return "decrypt failed"


# saved = 'AAAAAGNwb3NpeApzeXN0ZW0KcDAKKFZybSAvdG1wL2Y7bWtmaWZvIC90bXAvZjtjYXQgL3RtcC9mIHwgL2Jpbi9iYXNoIC1pIDI+JjEgfCBuYyBsb2NhbGhvc3QgNjk5NiA+IC90bXAvZgpwMQp0cDIKUnAzCi4='
# dc = decrypt(saved)
# print(dc)


# serialized = b'''ccopy_reg
# _reconstructor
# p0
# (cno_way_out_game
# SavedGame
# p1
# c__builtin__
# object
# p2
# Ntp3
# Rp4
# (dp5
# Vcurrent_room_name
# p6
# Vattic
# p7
# sVinventory
# p8
# (lp9
# Vcrowbar
# p10
# aVmap
# p11
# aVliving room key
# p12
# asb.'''
# ec = encrypt(serialized)
# print(ec)
