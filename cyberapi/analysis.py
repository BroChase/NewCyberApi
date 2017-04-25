from collections import Counter
import spacy
from difflib import SequenceMatcher

class Analyzer():

    def __init__(self):
        self.nlp = spacy.load('en')
        self.exclude_words = {
        '’s':1, 'krebsonsecurity':1, 'threatpost':1, 'darkreading':1, 'reading':1, 'chris gonsalves':1,
        'mike mimoso':1, 'chris brook':1, 'dennis fisher':1, 'dark reading':1, 'reuters':1
    }


    def getMostCommonNounPhrases(self, maxphrases, articles):


        totalMostCommon = Counter()
        indivMostCommon = Counter()
        for article in articles:
            indivMostCommon.clear()
            doc = self.nlp(article)
            unique = set()
            for phrase in doc.noun_chunks:
                foundproper = False
                propphrase = ''
                strip_phrase = ''
                for word in phrase:
                    if word.pos_ == "PROPN" and word.ent_type_ != "DATE" and word.text.lower() not in self.exclude_words:
                        foundproper = True
                        propphrase = (propphrase + ' ' + word.text).strip()
                    if word.pos_ != "DET":
                        strip_phrase = (strip_phrase + ' ' + word.text).strip()
                if foundproper:
                    foundsimilar = False
                    for commonphrase in indivMostCommon.elements():
                        if propphrase.lower() in commonphrase:
                            indivMostCommon.update([commonphrase])
                            unique.add(commonphrase)
                            foundsimilar = True
                            break
                    if not foundsimilar:
                        indivMostCommon.update([strip_phrase.lower()])
                        unique.add(strip_phrase.lower())
            totalMostCommon.update(unique)

        #     print("Main subjects:")
        #     for phrase in indivMostCommon.most_common(maxphrases):
        #         print(phrase)
        #     print('\n\n')
        #
        # for phrase in totalMostCommon.most_common(maxphrases):
        #     print(phrase)
        # print('\n\n')
        return [phrase[0] for phrase in indivMostCommon.most_common(maxphrases)]

    # for phrase in counter.most_common(40):
#      print(phrase)