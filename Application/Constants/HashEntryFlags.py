"""
Different Flags for Hash entries.
HASH_EXACT - Full calculation to the corresponding depth
HASH_BETA - Beta cutoff -> The state was too good for the minimizing player
HASH_ALPHA - Alpha cutoff -> The state was too bad for the maximizing player
"""

HASH_EXACT = "HASH_EXACT"
HASH_BETA = "HASH_BETA"
HASH_ALPHA = "HASH_ALPHA"