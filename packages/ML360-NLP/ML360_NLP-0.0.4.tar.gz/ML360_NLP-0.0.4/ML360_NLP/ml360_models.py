from sklearn.model_selection import train_test_split  # importing train and test
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVR, SVC  # importing SVr
from xgboost import XGBClassifier
from sklearn import metrics
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix  # import metrics
from sklearn.metrics import roc_curve, auc, roc_auc_score, precision_recall_curve  # import metrics
from sklearn.model_selection import GridSearchCV, cross_validate  # importing gridsearch
from sklearn.model_selection import RandomizedSearchCV  # importing Randomsearch
from sklearn.base import BaseEstimator, TransformerMixin
import swifter  # Speed up your Pandas Processing with Swifter
import re
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVR, SVC  # importing SVr
from xgboost import XGBClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import numpy as np

nltk.download('punkt')
# bag of words
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

# for word embedding
import gensim
from gensim.parsing.preprocessing import preprocess_string
from sklearn.pipeline import FeatureUnion, Pipeline
from gensim.models import Word2Vec
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument, Doc2Vec

from tqdm import tqdm  # for pregress bar

tqdm.pandas(desc="progress-bar")
from sklearn.preprocessing import FunctionTransformer
from sklearn import utils
from sklearn.pipeline import FeatureUnion, Pipeline

import multiprocessing

cores = multiprocessing.cpu_count()  # in doc2vec:-use these many worker threads to train the model (=faster training with multicore machines)

import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')


class MlModles:
    def tfidf_SVC(self, X_train, y_train, X_test, y_test):
        parameters = {
            'max_df': (0.25, 0.5, 0.75),
            'ngram_range': [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)],
            'use_idf': [True, False],
            'smooth_idf': (True, False),
            'max_features': (5000, 10000),
            'sublinear_tf': (True, False)

        }

        grid_search_tune = GridSearchCV(TfidfVectorizer(), parameters, cv=2, n_jobs=2, verbose=3, scoring="accuracy")

        X_train_vectors_tfidf = grid_search_tune.fit(X_train)
        X_train_vectors_tfidf = grid_search_tune.transform(X_train)

        X_test_vectors_tfidf = grid_search_tune.transform(X_test)

        # FITTING THE CLASSIFICATION MODEL using SVC(tf-idf)
        tfidf_SVC_model = SVC(probability=True)

        tfidf_SVC_model.fit(X_train_vectors_tfidf, y_train)

        # Predict y value for test dataset
        predicted = tfidf_SVC_model.predict(X_test_vectors_tfidf)
        predicted_prob = tfidf_SVC_model.predict_proba(X_test_vectors_tfidf)[:, 1]

        ## Accuracy, Precision, Recall
        accuracy = accuracy_score(y_test, predicted)

        classificationreport = classification_report(y_test, predicted)

        ## Plot confusion matrix
        cm = confusion_matrix(y_test, predicted)

        return tfidf_SVC_model, accuracy, classificationreport, cm

    def Svc_model_auto_hyper_tfidf(self, X_train, X_test, y_train, y_test):

        print(" this resuls showing for Svc_model_auto_hyper_tfidf")

        parameters = {
            'max_df': (0.25, 0.5, 0.75),
            'ngram_range': [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)],
            'use_idf': [True, False],
            'smooth_idf': (True, False),
            'max_features': (5000, 10000),
            'sublinear_tf': (True, False)

        }

        grid_search_tune = GridSearchCV(TfidfVectorizer(), parameters, cv=2, n_jobs=2, verbose=3, scoring="accuracy")

        grid_search_tune.fit(X_train, y_train)

        tfidf_vectorizer = TfidfVectorizer(max_df=grid_search_tune.best_params_['max_df'],

                                           max_features=grid_search_tune.best_params_['max_features'],

                                           ngram_range=grid_search_tune.best_params_['ngram_range'],

                                           smooth_idf=grid_search_tune.best_params_['smooth_idf'],

                                           use_idf=grid_search_tune.best_params_['use_idf'],

                                           sublinear_tf=grid_search_tune.best_params_['sublinear_tf'])

        X_train_vectors_tfidf = tfidf_vectorizer.fit_transform(X_train)

        X_test_vectors_tfidf = tfidf_vectorizer.transform(X_test)

        print("tfidf_best_parameters:-", grid_search_tune.best_params_)

        param_grid = [{'C': [0.01, 0.1, 10, 100, 1000], 'kernel': ['linear']},
                      {'C': [0.01, 0.1, 10, 100, 1000], 'gamma': [0.0001, 0.001, 0.01, 1, 10, 100], 'kernel': ['rbf']},
                      {'C': [0.01, 0.1, 10, 100, 1000], 'gamma': [0.0001, 0.001, 0.01, 1, 10, 100],
                       'kernel': ['sigmoid']},
                      {'C': [0.01, 0.1, 10, 100, 1000], 'gamma': [0.0001, 0.001, 0.01, 1, 10, 100], 'kernel': ['poly'],
                       'degree': [2, 4, 5, 6, 7]}]
        # parameters for svc

        rnd_search = RandomizedSearchCV(SVC(), param_grid, n_iter=10, cv=2, scoring="accuracy",
                                        verbose=0)  # Running the random search

        rnd_search.fit(X_train_vectors_tfidf, y_train)  # fitting the X_train and y_train

        print("random_search_best_parameters:-", rnd_search.best_params_)

        param = {'C': [0.01, 0.1, 10, 100, 1000], 'gamma': [0.0001, 0.001, 0.01, 1, 10, 100],
                 'degree': [2, 4, 5, 6, 7, 8]}
        # fixed parameters for SVC

        kernel = []  # Empty list of kernel
        kernel.append(list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('kernel')])
        # accessing the kernel values through indexing from random search best parameters dictonary
        # appending the kernel from random search to empty list

        gamma = []  # Empty list of gamma
        if 'gamma' in list(
                rnd_search.best_params_.keys()):  # checking if the gamma key is present in the random search best parameters dictonary
            # checking gamma value from random search best parameters in fixed parameter dict
            # if the value of gamma is in last position telling to take last 3 position values
            if param['gamma'][param['gamma'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('gamma')])] == \
                    param['gamma'][-1]:
                gamma.append(param['gamma'][param['gamma'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('gamma')]) - 2])
                gamma.append(param['gamma'][param['gamma'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('gamma')]) - 1])
                gamma.append(param['gamma'][param['gamma'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('gamma')])])

            # if the value of gamma is in first position telling to take first 3 position values
            elif param['gamma'][param['gamma'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('gamma')])] == \
                    param['gamma'][0]:
                gamma.append(param['gamma'][param['gamma'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('gamma')])])
                gamma.append(param['gamma'][param['gamma'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('gamma')]) + 1])
                gamma.append(param['gamma'][param['gamma'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('gamma')]) + 2])

            # if the value of gamma is in between position telling to take front and back of the values of the gamma values
            else:
                gamma.append(param['gamma'][param['gamma'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('gamma')]) - 1])
                gamma.append(param['gamma'][param['gamma'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('gamma')])])
                gamma.append(param['gamma'][param['gamma'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('gamma')]) + 1])

                # if the gamma value is not in the random search best parameters dictonary
                # appending the default value to the list
        else:
            gamma.append('scale')

        degree = []  # Empty list of degree
        if 'degree' in list(
                rnd_search.best_params_.keys()):  # checking if the degree key is present in the random search best parameters dictonary

            # checking degree value from random search best parameters in fixed parameter dict
            # if the value of degree is in last position telling to take last 3 position values
            if param['degree'][param['degree'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('degree')])] == \
                    param['degree'][-1]:
                degree.append(param['degree'][param['degree'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('degree')]) - 2])
                degree.append(param['degree'][param['degree'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('degree')]) - 1])
                degree.append(param['degree'][param['degree'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('degree')])])

            # if the value of degree is in first position telling to take first 3 position values
            elif param['degree'][param['degree'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('degree')])] == \
                    param['degree'][0]:
                degree.append(param['degree'][param['degree'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('degree')])])
                degree.append(param['degree'][param['degree'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('degree')]) + 1])
                degree.append(param['degree'][param['degree'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('degree')]) + 2])

            # if the value of degree is in between position telling to take front and back of the values of the degree values
            else:
                degree.append(param['degree'][param['degree'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('degree')]) - 1])
                degree.append(param['degree'][param['degree'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('degree')])])
                degree.append(param['degree'][param['degree'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('degree')]) + 1])

                # if the degree value is not in the random search best parameters dictonary
                # appending the default value to the list
        else:
            degree.append(3)

        C = []  # Empty list of C
        if 'C' in list(
                rnd_search.best_params_.keys()):  # checking if the C key is present in the random search best parameters dictonary

            # checking C value from random search best parameters in fixed parameter dict
            # if the value of C is in last position telling to take last 3 position values
            if param['C'][param['C'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('C')])] == \
                    param['C'][-1]:
                C.append(param['C'][param['C'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('C')]) - 2])
                C.append(param['C'][param['C'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('C')]) - 1])
                C.append(param['C'][param['C'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('C')])])

            # if the value of C is in first position telling to take first 3 position values
            elif param['C'][param['C'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('C')])] == \
                    param['C'][0]:
                C.append(param['C'][param['C'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('C')])])
                C.append(param['C'][param['C'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('C')]) + 1])
                C.append(param['C'][param['C'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('C')]) + 2])

            # if the value of C is in between position telling to take front and back of the values of the C values
            else:
                C.append(param['C'][param['C'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('C')]) - 1])
                C.append(param['C'][param['C'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('C')])])
                C.append(param['C'][param['C'].index(
                    list(rnd_search.best_params_.values())[list(rnd_search.best_params_.keys()).index('C')]) + 1])

        param_dist = {'kernel': kernel, 'gamma': gamma, 'degree': degree, 'C': C}
        # Creating the dictonary parameters values from random search

        clf = GridSearchCV(SVC(), param_dist, cv=2, scoring="accuracy", n_jobs=-1, verbose=0)
        # running the Gridsearch from the parameters from random search

        clf.fit(X_train_vectors_tfidf, y_train)  # fitting the grid search
        print("gridserach parameters:-", clf.best_params_)

        Svc_model_auto_hyper_tfidf_model = SVC(C=clf.best_params_['C'], kernel=clf.best_params_['kernel'],
                                               gamma=clf.best_params_['gamma'],
                                               degree=clf.best_params_['degree'])

        # fitting the SVC
        Svc_model_auto_hyper_tfidf_model.fit(X_train_vectors_tfidf, y_train)

        predicted = Svc_model_auto_hyper_tfidf_model.predict(X_test_vectors_tfidf)  # predicting

        ## Accuracy, Precision, Recall
        accuracy = accuracy_score(y_test, predicted)

        classificationreport = classification_report(y_test, predicted)

        ## Plot confusion matrix
        cm = confusion_matrix(y_test, predicted)
        return Svc_model_auto_hyper_tfidf_model, accuracy, classificationreport, cm

    def tfidf_MNB(self, X_train, y_train, X_test, y_test):

        # creating the vectors
        tfidf_vectorizer = TfidfVectorizer(use_idf=True, max_df=0.5)
        X_train_vectors_tfidf = tfidf_vectorizer.fit_transform(X_train)
        X_test_vectors_tfidf = tfidf_vectorizer.transform(X_test)

        # FITTING THE CLASSIFICATION MODEL using (tf-idf)
        model = MultinomialNB()
        model.fit(X_train_vectors_tfidf, y_train)

        # Predict y value for test dataset
        predicted = model.predict(X_test_vectors_tfidf)

        ## Accuracy, Precision, Recall
        accuracy = accuracy_score(y_test, predicted)

        classificationreport = classification_report(y_test, predicted)

        ## Plot confusion matrix
        cm = confusion_matrix(y_test, predicted)
        return model, accuracy, classificationreport, cm

    def tfidf_logistic(self, X_train, y_train, X_test, y_test):
        parameters = {
            'max_df': (0.25, 0.5, 0.75),
            'ngram_range': [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)],
            'use_idf': [True, False],
            'smooth_idf': (True, False),
            'max_features': (5000, 10000),
            'sublinear_tf': (True, False)

        }

        grid_search_tune = GridSearchCV(TfidfVectorizer(), parameters, cv=2, n_jobs=2, verbose=3, scoring="accuracy")

        X_train_vectors_tfidf = grid_search_tune.fit(X_train)
        X_train_vectors_tfidf = grid_search_tune.transform(X_train)

        X_test_vectors_tfidf = grid_search_tune.transform(X_test)
        print(grid_search_tune.best_params_)

        model = LogisticRegression(C=10, penalty='l2')

        model.fit(X_train_vectors_tfidf, y_train)

        # Predict y value for test dataset
        predicted = model.predict(X_test_vectors_tfidf)
        predicted_prob = model.predict_proba(X_test_vectors_tfidf)[:, 1]
        ## Accuracy, Precision, Recall
        accuracy = accuracy_score(y_test, predicted)

        classificationreport = classification_report(y_test, predicted)

        ## Plot confusion matrix
        cm = confusion_matrix(y_test, predicted)

        return model, accuracy, classificationreport, cm

    def tfidf_RandomForestClassifier(self, X_train, y_train, X_test, y_test):
        parameters = {
            'max_df': (0.25, 0.5, 0.75),
            'ngram_range': [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)],
            'use_idf': [True, False],
            'smooth_idf': (True, False),
            'max_features': (5000, 10000),
            'sublinear_tf': (True, False)

        }

        grid_search_tune = GridSearchCV(TfidfVectorizer(), parameters, cv=2, n_jobs=2, verbose=3, scoring="accuracy")

        X_train_vectors_tfidf = grid_search_tune.fit(X_train)
        X_train_vectors_tfidf = grid_search_tune.transform(X_train)

        X_test_vectors_tfidf = grid_search_tune.transform(X_test)
        print(grid_search_tune.best_params_)

        # FITTING THE CLASSIFICATION MODEL using  randomclassfier(tf-idf)
        model = RandomForestClassifier()

        model.fit(X_train_vectors_tfidf, y_train)

        # Predict y value for test dataset
        predicted = model.predict(X_test_vectors_tfidf)
        predicted_prob = model.predict_proba(X_test_vectors_tfidf)[:, 1]

        ## Accuracy, Precision, Recall
        accuracy = accuracy_score(y_test, predicted)

        classificationreport = classification_report(y_test, predicted)

        ## Plot confusion matrix
        cm = confusion_matrix(y_test, predicted)
        return model, accuracy, classificationreport, cm

    def tfidf_XGBClassifier(self, X_train, y_train, X_test, y_test):
        parameters = {
            'max_df': (0.25, 0.5, 0.75),
            'ngram_range': [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)],
            'use_idf': [True, False],
            'smooth_idf': (True, False),
            'max_features': (5000, 10000),
            'sublinear_tf': (True, False)

        }

        grid_search_tune = GridSearchCV(TfidfVectorizer(), parameters, cv=2, n_jobs=2, verbose=3, scoring="accuracy")

        X_train_vectors_tfidf = grid_search_tune.fit(X_train)
        X_train_vectors_tfidf = grid_search_tune.transform(X_train)

        X_test_vectors_tfidf = grid_search_tune.transform(X_test)
        print(grid_search_tune.best_params_)

        # FITTING THE CLASSIFICATION MODEL using  XGBClassifier(tf-idf)
        model = XGBClassifier(tree_method="hist")
        model.fit(X_train_vectors_tfidf, y_train)

        # Predict y value for test dataset
        predicted = model.predict(X_test_vectors_tfidf)
        predicted_prob = model.predict_proba(X_test_vectors_tfidf)[:, 1]
        classes = np.unique(y_test)

        ## Accuracy, Precision, Recall
        accuracy = accuracy_score(y_test, predicted)

        classificationreport = classification_report(y_test, predicted)

        ## Plot confusion matrix
        cm = confusion_matrix(y_test, predicted)

        return model, accuracy, classificationreport, cm

    def word2vec_logistic(self, X_train, X_test, y_train, y_test):

        # Word2Vec runs on tokenized sentences
        X_train_tok = [nltk.word_tokenize(i) for i in X_train]
        X_test_tok = [nltk.word_tokenize(i) for i in X_test]

        # defining model parmeters
        Min_count = 2  # It will ignore all the words with a total frequency lower than this
        Size = 100  # It tells the dimensionality of the word vectors
        Workers = 4  # These are the threads to train the model
        Window = 5  # Maximum distance between the current and predicted word within a sentence

        # train word2vec model
        model = Word2Vec(X_train_tok, window=Window, size=Size, workers=Workers, min_count=Min_count)
        w2v = dict(zip(model.wv.index2word, model.wv.syn0))
        modelw = MeanEmbeddingVectorizer(w2v)

        # converting text to numerical data using Word2Vec
        X_train_vectors_w2v = modelw.transform(X_train_tok)
        X_test_vectors_w2v = modelw.transform(X_test_tok)

        # FITTING THE CLASSIFICATION MODEL using Logistic Regression (W2v)

        model = LogisticRegression(multi_class='auto')
        model.fit(X_train_vectors_w2v, y_train)  # model

        # Predict y value for test dataset
        predicted = model.predict(X_test_vectors_w2v)
        predicted_prob = model.predict_proba(X_test_vectors_w2v)[:, 1]

        ## Accuracy, Precision, Recall
        accuracy = accuracy_score(y_test, predicted)

        classificationreport = classification_report(y_test, predicted)

        ## Plot confusion matrix
        cm = confusion_matrix(y_test, predicted)

        return model, accuracy, classificationreport, cm

    def word2vec_randomclassfier(self, X_train, X_test, y_train, y_test):

        # Word2Vec runs on tokenized sentences
        X_train_tok = [nltk.word_tokenize(i) for i in X_train]
        X_test_tok = [nltk.word_tokenize(i) for i in X_test]

        # defining model parmeters
        Min_count = 2  # It will ignore all the words with a total frequency lower than this
        Size = 100  # It tells the dimensionality of the word vectors
        Workers = 4  # These are the threads to train the model
        Window = 5  # Maximum distance between the current and predicted word within a sentence

        # train word2vec model
        model = Word2Vec(X_train_tok, size=Size, window=Window, workers=Workers, min_count=Min_count)
        w2v = dict(zip(model.wv.index2word, model.wv.syn0))
        modelw = MeanEmbeddingVectorizer(w2v)

        # converting text to numerical data using Word2Vec
        X_train_vectors_w2v = modelw.transform(X_train_tok)
        X_test_vectors_w2v = modelw.transform(X_test_tok)

        # FITTING THE CLASSIFICATION MODEL using Logistic Regression (W2v)

        model = RandomForestClassifier()
        model.fit(X_train_vectors_w2v, y_train)  # model

        # Predict y value for test dataset
        predicted = model.predict(X_test_vectors_w2v)
        predicted_prob = model.predict_proba(X_test_vectors_w2v)[:, 1]

        ## Accuracy, Precision, Recall
        accuracy = accuracy_score(y_test, predicted)

        classificationreport = classification_report(y_test, predicted)

        ## Plot confusion matrix
        cm = confusion_matrix(y_test, predicted)

        return model, accuracy, classificationreport, cm

    def word2vec_svc(self, X_train, X_test, y_train, y_test):

        # Word2Vec runs on tokenized sentences
        X_train_tok = [nltk.word_tokenize(i) for i in X_train]
        X_test_tok = [nltk.word_tokenize(i) for i in X_test]

        # defining model parmeters
        Min_count = 2  # It will ignore all the words with a total frequency lower than this
        Size = 100  # It tells the dimensionality of the word vectors
        Workers = 4  # These are the threads to train the model
        Window = 5  # Maximum distance between the current and predicted word within a sentence

        # train word2vec model
        model = Word2Vec(X_train_tok, size=Size, window=Window, workers=Workers, min_count=Min_count)
        w2v = dict(zip(model.wv.index2word, model.wv.syn0))
        modelw = MeanEmbeddingVectorizer(w2v)

        # converting text to numerical data using Word2Vec
        X_train_vectors_w2v = modelw.transform(X_train_tok)
        X_test_vectors_w2v = modelw.transform(X_test_tok)

        # FITTING THE CLASSIFICATION MODEL using SVC(W2v)

        model = SVC(probability=True)
        model.fit(X_train_vectors_w2v, y_train)  # model

        # Predict y value for test dataset
        predicted = model.predict(X_test_vectors_w2v)
        predicted_prob = model.predict_proba(X_test_vectors_w2v)[:, 1]

        ## Accuracy, Precision, Recall
        accuracy = accuracy_score(y_test, predicted)

        classificationreport = classification_report(y_test, predicted)

        ## Plot confusion matrix
        cm = confusion_matrix(y_test, predicted)

        return model, accuracy, classificationreport, cm

    def word2vec_xgboost(self, X_train, X_test, y_train, y_test):

        # Word2Vec runs on tokenized sentences
        X_train_tok = [nltk.word_tokenize(i) for i in X_train]
        X_test_tok = [nltk.word_tokenize(i) for i in X_test]

        # defining model parmeters
        Min_count = 2  # It will ignore all the words with a total frequency lower than this
        Size = 100  # It tells the dimensionality of the word vectors
        Workers = 4  # These are the threads to train the model
        Window = 5  # Maximum distance between the current and predicted word within a sentence

        # train word2vec model
        model = Word2Vec(X_train_tok, size=Size, window=Window, workers=Workers, min_count=Min_count)
        w2v = dict(zip(model.wv.index2word, model.wv.syn0))
        modelw = MeanEmbeddingVectorizer(w2v)

        # converting text to numerical data using Word2Vec
        X_train_vectors_w2v = modelw.transform(X_train_tok)
        X_test_vectors_w2v = modelw.transform(X_test_tok)

        # FITTING THE CLASSIFICATION MODEL using Logistic Regression (W2v)

        model = XGBClassifier(tree_method="hist")
        model.fit(X_train_vectors_w2v, y_train)  # model

        # Predict y value for test dataset
        predicted = model.predict(X_test_vectors_w2v)
        predicted_prob = model.predict_proba(X_test_vectors_w2v)[:, 1]

        ## Accuracy, Precision, Recall
        accuracy = accuracy_score(y_test, predicted)

        classificationreport = classification_report(y_test, predicted)

        ## Plot confusion matrix
        cm = confusion_matrix(y_test, predicted)

        return model, accuracy, classificationreport, cm

    def pipelinize(function, active=True):
        def list_comprehend_a_function(list_or_series, active=True):
            if active:
                return [function(i) for i in list_or_series]
            else:  # if it's not active, just pass it right back
                return list_or_series

        return FunctionTransformer(list_comprehend_a_function, validate=False, kw_args={'active': active})

    def create_model_estimator(self, X_train=None, y_train=None, X_test=None, y_test=None):

        estimators_1 = [('tfidf_SVC', self.pipelinize(self.tfidf_SVC(X_train, y_train, X_test, y_test))),
                        ('Svc_model_auto_hyper_tfidf',
                         self.pipelinize(self.Svc_model_auto_hyper_tfidf(X_train, X_test, y_train, y_test))),
                        ('tfidf_MNB', self.pipelinize(self.tfidf_MNB(X_train, y_train, X_test, y_test))),
                        ('tfidf_RandomForestClassifier',
                         self.pipelinize(self.tfidf_RandomForestClassifier(X_train, y_train, X_test, y_test))),
                        ('tfidf_XGBClassifier',
                         self.pipelinize(self.tfidf_XGBClassifier(X_train, y_train, X_test, y_test))),
                        (
                        'word2vec_logistic', self.pipelinize(self.word2vec_logistic(X_train, X_test, y_train, y_test))),
                        ('word2vec_randomclassfier',
                         self.pipelinize(self.word2vec_randomclassfier(X_train, X_test, y_train, y_test))),
                        ('word2vec_svc', self.pipelinize(self.word2vec_svc(X_train, X_test, y_train, y_test))),
                        ('word2vec_xgboost', self.pipelinize(self.word2vec_xgboost(X_train, X_test, y_train, y_test)))]
        return estimators_1

    def get_model(self, estimator=None, model_name_dict=None, model_name=None):
        model_dict = estimator[model_name_dict[model_name]][1]
        model_accuracy = model_dict.kw_args['active'][1]
        select_model = model_dict.kw_args['active'][0]
        model_confusion_matrix = model_dict.kw_args['active'][3]
        return select_model, model_accuracy, model_confusion_matrix

    def get_model_name_dict(self):
        model_name_dict = {'tfidf_SVC': 0,
                           'Svc_model_auto_hyper_tfidf': 1,
                           'tfidf_MNB': 2,
                           'tfidf_RandomForestClassifier': 3,
                           'tfidf_XGBClassifier': 4,
                           'word2vec_logistic': 5,
                           'word2vec_randomclassfier': 6,
                           'word2vec_svc': 7,
                           'word2vec_xgboost': 8}
        return model_name_dict


class MeanEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        self.dim = len(next(iter(word2vec.values())))

    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in X
        ])

