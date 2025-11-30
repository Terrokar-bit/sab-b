# WoW 3.3.5a (Build 12340) Offsets
# Note: These are common public offsets. They might vary slightly depending on the server's custom patches.

# Static Addresses (Base)
STATIC_PLAYER_GUID = 0x00CA1238 # This is the GUID of the local player (8 bytes)
# Static Addresses (Base)
STATIC_PLAYER_GUID = 0x00CA1238 # This is the GUID of the local player (8 bytes)
STATIC_CLIENT_CONNECTION = 0x00C79CE0 # Pointer to Client Connection

# Client Connection Offsets
OFFSET_CLIENT_CONN_CUR_MGR = 0x2ED0 # Offset to Object Manager from Client Connection

# Object Manager Offsets
OFFSET_OBJ_MGR_FIRST_OBJ = 0xAC
OFFSET_OBJ_MGR_NEXT_OBJ = 0x3C

# Object Offsets
OFFSET_OBJ_GUID = 0x30
OFFSET_OBJ_TYPE = 0x14 # 4 = Player, 3 = Unit, 2 = GameObject
OFFSET_OBJ_ENTRY = 0x10 # The ID of the object (e.g. Herb/Ore ID)

# Unit/Player Offsets (Descriptors)
# Descriptors usually start at +0x8 from the object base, but let's assume direct offsets for now or check descriptor ptr.
# In 3.3.5a, Unit Fields often start at 0x8 (Descriptor Pointer).
# Health is usually at Descriptor + 0x17 * 4 (0x5C) ?? No, let's stick to the previous ones but check if they are from Descriptor.
# Actually, 0x17D0 looks like a direct offset from Object Base in some contexts, but usually it's Descriptor + Offset.
# Let's try to read the Descriptor Pointer first.
OFFSET_DESCRIPTOR_PTR = 0x8

# Unit Fields (Relative to Descriptor Pointer)
# Verified by user dump:
# Health Index: 24 (0x18) -> 0x60
# Max Health Index: 32 (0x20) -> 0x80
# Level Index: 54 (0x36) -> 0xD8

OFFSET_UNIT_HEALTH = 0x60 
OFFSET_UNIT_MAX_HEALTH = 0x80
OFFSET_UNIT_LEVEL = 0xD8

# Target GUID is usually Index 18 (0x12).
# Verified by user dump: Index 18.
# 0x12 * 4 = 0x48
OFFSET_UNIT_TARGET = 0x48

# Coordinate Offsets (Relative to Object Base, NOT Descriptor)
# In 3.3.5a these are usually at 0x798
OFFSET_POS_X = 0x798
OFFSET_POS_Y = 0x79C
OFFSET_POS_Z = 0x7A0
OFFSET_ROTATION = 0x7A8


# Patterns (Signatures)
# Example pattern to find the player base if static address fails
# This is a placeholder pattern - real ones are long byte sequences.
PATTERN_PLAYER_BASE = b"\x00\x00\x00\x00" 
