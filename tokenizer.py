import spacy
import configparser

config = configparser.ConfigParser()
config.read("./config/config.ini")


class Spacy_Tokenizer:
    """
    The main tokenization function
    """

    def __init__(self) -> None:
        self.nlp_lang_model = spacy.load(config["SPACY_PARAM"]["LANG_MODEL"])

    @staticmethod
    def clean_word(word: str) -> str:
        """
        This part is based on visual investigation of the output words.
        """
        if word in ["-", "’", "–", "−"]:
            return ""

        word = word.lower()
        word = word.replace("-", "").replace("–", "").replace("”", "")

        if len(word) > 0:
            if (word[-1] == "’") or (word[-1] == "'"):
                word = word.replace("’", "e")
                word = word.replace("'", "e")
        return word

    def _concatenate_article_text(self, article_data):
        """
        Concatenate the title, description and context into a single string
        """
        return (
            article_data["article_content"]["title"]
            + " "
            + article_data["article_content"]["description"]
            + " "
            + article_data["article_content"]["content"]
        )

    def __call__(self, article_data):
        """
        This is the main function
        Form a single string for the whole article:  title + description + content,
        in order to go for the tokenization.
        """
        article_main_text = self._concatenate_article_text(article_data=article_data)

        (
            _,
            all_words,
            verbs,
            nouns,
            adverbs,
            entities,
        ) = self.get_words_from_article(article_main_text)
        return all_words, verbs, nouns, adverbs, entities

    def tokenize_article(self, article_data):
        """
        This function returns a single tokenized article
        This is useful to ease the analysis later
        """
        article_data["article_content"]["title"], *_ = self.get_words_from_article(
            article_data["article_content"]["title"]
        )
        # print(f'Tokenized title: {article_data["article_content"]["title"]}')

        (
            article_data["article_content"]["description"],
            *_,
        ) = self.get_words_from_article(article_data["article_content"]["description"])

        # print(f'Tokenized title: {article_data["article_content"]["description"]}')

        article_data["article_content"]["content"], *_ = self.get_words_from_article(
            article_data["article_content"]["content"]
        )

        # print(f'Tokenized title: {article_data["article_content"]["content"]}')

        return article_data

    def get_words_from_article(self, article_text):
        """
        Extract the tokens from the article text
        """
        doc = self.nlp_lang_model(article_text)

        words = {}
        verbs = {}
        nouns = {}
        adverbs = {}
        entities = {}

        tokens_sequence = []

        for entity in doc.ents:
            try:
                entities[entity.label_][entity.text.lower()] += 1
            except KeyError:
                try:
                    entities[entity.label_][entity.text.lower()] = 1
                except KeyError:
                    entities[entity.label_] = {entity.text.lower(): 1}

        for token in doc:
            if token.pos_ in ["SPACE", "PUNCT", "NUM", "SYM", "ADP", "DET"]:
                continue

            # Perform extract cleaning on the word
            final_token = self.clean_word(token.lemma_)
            if len(final_token) == 0:
                continue

            tokens_sequence.append(final_token)

            if token.pos_ in ["VERB"]:
                try:
                    verbs[final_token] += 1
                except KeyError:
                    verbs[final_token] = 1

            if token.pos_ in ["NOUN"]:
                try:
                    nouns[final_token] += 1
                except KeyError:
                    nouns[final_token] = 1

            if token.pos_ in ["ADV"]:
                try:
                    adverbs[final_token] += 1
                except KeyError:
                    adverbs[final_token] = 1

            try:
                words[final_token] += 1
            except KeyError:
                words[final_token] = 1
            # all_words.append(final_token)
        # return words, " ".join(all_words)
        tokens_sequence = " ".join(tokens_sequence)
        return tokens_sequence, words, verbs, nouns, adverbs, entities