#!/usr/bin/env python
# coding: utf-8
#
# The class to do all the translation
#
# Author: Alex Simonides

import re
from heapq import heappush

from flask.ext.restful import Resource

from emoji_tags import tags


def flip_mapping(dict_):
    flipped = {}
    for (outer_key, inner_dict) in dict_.iteritems():
        for (inner_key, value) in inner_dict.iteritems():
            inner_flip = flipped.get(inner_key, [])
            heappush(inner_flip, (value, outer_key))
            flipped[inner_key] = inner_flip
    return flipped


def sanitize(string_):
    clean = re.sub(r"[,.?!]", "", string_)
    clean = clean.replace("_", " ")
    return clean


class EmojiTranslation(Resource):

    emoji_to_keywords = tags
    keywords_to_emoji = flip_mapping(tags)

    def get(self, input, threshold):
        """ Return up to threshold emoji for the input.
        """
        words = sanitize(input).split()
        related_emojis = {}

        # Find all the emojis that apply to any of the words
        for word in words:
            temp_emojis = self.keywords_to_emoji.get(word)

            if temp_emojis is not None:
                for weight, emoji in temp_emojis:
                    total_weight = related_emojis.get(emoji, 0)
                    related_emojis[emoji] = total_weight + weight

        # Build a list of the appropriate number of emojis
        list_of_emojis = []
        while len(list_of_emojis) < threshold and max(
                related_emojis, key=related_emojis.get) > 0:
            top = max(related_emojis, key=related_emojis.get)
            list_of_emojis.append(top)
            related_emojis[top] = 0
        return ''.join(list_of_emojis)

if __name__ == "__main__":
    em = EmojiTranslation()
    print em.get("happy firetruck", 4)