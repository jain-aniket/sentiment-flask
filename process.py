from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump, load
from sklearn.metrics import precision_recall_curve


class sentiment_clf(object):
	
	def __init__(self):
		self.count_vect = TfidfVectorizer(max_df=0.1, min_df=2, ngram_range = (1,2))
		self.clf = load('sentiment_clf.joblib')
		self.count_vect = load('sentiment_vect.joblib')

	def process(self, text):
		vect = self.count_vect.transform([text])
		predicted = self.clf.predict(vect)	
		if predicted[0] == 0:
			return "Negative"
		elif predicted[0] == 4:
			return "Positive"
		return "Error"
