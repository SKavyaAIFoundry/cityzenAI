# import required libraries
from collections import defaultdict
from gensim import corpora
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize


# defined stoplist library for NLP works
stoplist = stopwords.words('english')

# establish english language stemmer
# can be replaced with lemmatizer if required
stemmer = SnowballStemmer('english')
lemmatizer = WordNetLemmatizer()


def create_dictionary(corpus, no_above, no_below, keep_n):
    '''
    Defines an lsi model for the imported library data.  Returns a filtered 
    dictionary created from the library texts, a vectorised lsi corpus and the
    trained lsi model.
    '''

    # create lists of corpus texts
    #summaries = corpus['texts']
    summaries = corpus

    # normalise the text - get root words
    texts = [
        [lemmatizer.lemmatize(word, pos='v') for word in word_tokenize(summary.lower()) if word not in stoplist]
        for summary in summaries
    ]
    # https://www.nltk.org/_modules/nltk/stem/wordnet.html
    # param pos: The Part Of Speech tag. Valid options are:
    # "n" for nouns
    # "v" for verbs
    # "a" for adjectives
    # "r" for adverbs
    # "s" for satellite adjectives

    # tokenize and stem summary texts and remove stopwords
    #texts = [
    #    [stemmer.stem(word) for word in word_tokenize(summary.lower()) if word not in stoplist]
    #    for summary in summaries
    #]

    # count token frequencies in the summaries
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    # append frequency counts to texts
    texts = [
        #[token for token in text if frequency[token] >= 1]
        [token for token in text if frequency[token] > 1]
        for text in texts
    ]

    # vectorize texts and create a bag of words corpus
    dictionary = corpora.Dictionary(texts)
    dictionary.filter_extremes(no_below=no_below, 
                                no_above=no_above, 
                                keep_n= keep_n)

    return dictionary