import nltk
import random
from nltk.corpus import movie_reviews
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB



documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

print(documents[1])

all_words = []
for w in movie_reviews.words():
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())[:3000] # Train over 3000 words


def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words) # Gives it a 1 or 0 based on sentiment

    return features


# print((find_features(movie_reviews.words('neg/cv000_29416.txt'))))

featuresets = [(find_features(rev), category) for (rev, category) in documents]
# print(featuresets)

training_set = featuresets[:2000]

testing_set = featuresets[2000:]

# pos_lines = [line.rstrip('\n') for line in open(
#     'short_reviews/positive.txt', 'r', encoding='ISO-8859-1')]



# classifier = nltk.NaiveBayesClassifier.train(training_set)
# print(nltk.classify.accuracy(classifier, testing_set)*100)

# save_classfier = open("naivebayes.pickle", "wb")
# pickle.dump(classifier, save_classfier)
# save_classfier.close()

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
# print("MultinomialNB accuracy percent:",
#       nltk.classify.accuracy(MNB_classifier, testing_set))

BNB_classifier = SklearnClassifier(BernoulliNB())
BNB_classifier.train(training_set)
# print("BernoulliNB accuracy percent:",
#       nltk.classify.accuracy(BNB_classifier, testing_set))
