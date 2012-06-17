"A filtering system for rss feeds."
version="0.2"
from filters import *
from data_file import *

# TODO:
#   * 0.2 Configurable pipeline, multi output        [ok]
#   * 0.3 Keyword specific rules                     [ok?]
#         -> html parsing
#   * 0.4 Fuzzy dropping (if score is not reached)
#   * 0.5 AI scoring
#   * 1.0 Hot-trainable AI (links in posts)
