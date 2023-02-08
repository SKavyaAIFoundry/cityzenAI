# import required libraries
import contractions
import emoji
import gensim
import nltk
import re
import string

from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords
from unidecode import unidecode

nltk.download('stopwords')
nltk.download('punkt')


#def preprocess(text):
def preprocess(text, minTokenSize=0):

    '''
    Function for text preprocessing before nlp modelling.
    Designed to be a list where functions can easily be removed or added as 
    required by the user.
    '''

    # remove twitter handles/mentions
    text = re.sub('\B@\w+', "", text)
    #text

    # remove url links
    text = re.sub('(http|https):\/\/\S+', "", text)
    #text

    # remove emojis
    text = emoji.demojize(text)
    #text

    # remove contractions (e.g. I've > I have)
    text = contractions.fix(text)
    #text

    # remove numbers
    text = re.sub('[0-9]', '', text)

    # remove stopwords
    token_list = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    token_list = [token for token in token_list if token not in stop_words]
    text = TreebankWordDetokenizer().detokenize(token_list)

    # remove quotes
    text = unidecode(text).replace('"', '').replace("'", '')

    # remove point
    text = unidecode(text).replace('.', '')

    # remove punctuation
    token_list = word_tokenize(text)
    token_list = [token for token in token_list if token not in string.punctuation]
    text = TreebankWordDetokenizer().detokenize(token_list)

    # remove short tokens
    if minTokenSize > 0:
        token_list = word_tokenize(text)
        token_list = gensim.parsing.preprocessing.remove_short_tokens(token_list, minsize=minTokenSize)
        text = TreebankWordDetokenizer().detokenize(token_list)

    # convert to lowercase
    text = text.lower()

    return text