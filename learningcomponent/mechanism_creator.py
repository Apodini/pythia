import time
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from data_preprocessor import DataPreprocessor
from entities.mechanism import Mechansim


class MechansimCreator():
    ''' Class responsible for creating the mechanism for the prediction
    '''

    def __init__(self, algorithm):
        ''' init data preprocessor and classifier
        '''
        self.data_preprocessor = DataPreprocessor()
        if str(algorithm).lower() == 'decisiontree':
            self.clf = DecisionTreeClassifier()
        elif str(algorithm).lower() == 'randomforest':
            self.clf = RandomForestClassifier()


    def run(self):
        ''' create and store mechanism
        '''
        df = self.data_preprocessor.get_data()
        df = self.data_preprocessor.preprocess_data(df)
        # nextcluster as label for ML algorithm
        y = df['nextcluster'].values
        y = y.astype('int')


        X_train, X_test, y_train, y_test = train_test_split(df[['currentclusternumber']].values, y)

        # TODO: imbalanced classes?
        print(df.nextcluster.value_counts())

        # Classifer
        self.clf = self.clf.fit(X_train, y_train)
        y_pred = self.clf.predict(X_test)
        print("Accuracy of Classifier:", metrics.accuracy_score(y_test, y_pred))

        '''
        dot_data = StringIO()
        export_graphviz(clf, out_file=dot_data,
                        filled=True, rounded=True,
                        special_characters=True,feature_names = feature_cols)
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph.write_png('./data/images/decisiontree/tree.png')

        # Random Forest classifier
        clf=RandomForestClassifier(n_estimators=32)
        clf.fit(X_train,y_train)
        y_pred=clf.predict(X_test)
        print("Accuracy of RandomForest:",metrics.accuracy_score(y_test, y_pred))

        i_tree = 0
        for tree_in_forest in clf.estimators_:
            if (i_tree < 10):
                dot_data = StringIO()
                export_graphviz(tree_in_forest, out_file=dot_data,
                        filled=True, rounded=True,
                        special_characters=True,feature_names = feature_cols)
            graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
            graph.write_png('./data/images/foresttrees/foresttree{}.png'.format(i_tree))
            i_tree += 1
        '''

        # save the model to db
        mechanism = Mechansim(self.clf, self.data_preprocessor.le, int(round(time.time() * 1000)))
        mechanism.save()

if __name__ == "__main__":
    MECHANISM_CREATOR = MechansimCreator(algorithm='decisiontree')
    MECHANISM_CREATOR.run()
