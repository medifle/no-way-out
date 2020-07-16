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
    cipher_bytes = base64.b64decode(b64_cipher_bytes)
    key = cipher_bytes[:4]
    print(cipher_bytes)
    print("")
    print(key) # BOLD
    print("")
    decrypted_array = xor(key, cipher_bytes[4:])
    return decrypted_array


#saved = 'Qk9BUiEsLiI7EDM3JUUeICcsLjwxOzMnITsuIEg/cVhqLC0zOyA0JkgcICQnKwYzLypLInNFIg0dLTQ7LjsoPB0QSz0gJSQxNkUxYEgBNSJxRRMidkVpNjJ6SwQrITc3LDsuIDtFMWRIZy0idUUmYkhnIj4jNi4nNkUIJiciSyJ6RSZgSAE1IntFEyJzf0t6Jj9wY0gZLzMvKksic31LBCE9LiUgLjNYMn5yWDEZJTcxLDM7MjsoPSxFMWN2RRcTYjwsMy4jYTEwIDYwIz1vchc8JDQ3Iy1yJCAzcjYnKDwlPGEmKi41ciM9JHIxOzQxKWFLInN6SyEUJi8hMioiJkg/cGRIGQgmZTxhM2ItLTMhJGExMCA2MCM9YT8jKyRyLTo1ci0pYTswIC98YgY1dTFvMiYrIy1yMSMoNSo7LStiOCQmSD9wZUg8IzMlf0t6JXdLNXBFDyYyfnlYED9wa0hnJSJwf0s1c31LBCAuMjcvKi8mYiQkK0g/c2NIPCZjdkUXE2I8LDMuI2E2Kz01K2IkJCtsRTFgcEUyNXN5SwQWJyAmYjwpPTcjJXIjIy09NW8sN2I7LnIlKjVyLTo1ci0pYSYqKmEwIzwkPychNXxIP3NhSDwjMzEZIicwPSQ8NhAzPS0iHjwjIiRYMn11WBQrICApbzM9LSJLInB6SyEgYQ=='
#dc = decrypt(saved)
#print(dc)



ss = b"ccopy_reg\n_reconstructor\np0\n(clayout\nSavedGame\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n(dp5\nVinventory\np6\n(lp7\ng0\n(clayout\nItem\np8\ng2\nNtp9\nRp10\n(dp11\nVname\np12\nVcrowbar\np13\nsVdescription\np14\nVA small crowbar. Usefull for things that are stuck.\np15\nsVinspect\np16\nVIt\'s a black crowbar made out of iron. It\'s still slightly wet\np17\nsbag0\n(g8\ng2\nNtp18\nRp19\n(dp20\ng12\nVbasement key\np21\nsg14\nVA small dirty key.\np22\nsg16\nVThat should allow me to get out of the basement.\np23\nsbasVcurrent_room_name\np24\nVattic\np25\nsb."
ec = encrypt(ss)
print(ec)
