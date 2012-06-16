"A filtering system for rss feeds."
version="0.1"
from .rss import *
from data_file import *
import processing
import rssxml
import nltk_filters

# TODO:
#   * 0.2 Configurable pipeline, multi output
#   * 0.3 Keyword specific rules
#   * 0.4 Fuzzy dropping (if score is not reached)
#   * 0.5 AI scoring
#   * 1.0 Hot-trainable AI (links in posts)
