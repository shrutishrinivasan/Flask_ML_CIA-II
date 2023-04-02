import pandas as pd 

# reading the csv file
df = pd.read_csv('classification.csv')

X = df.iloc[:,:-1].values
y = df.iloc[:,-1].values

# import decision tree classifier
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=0)

from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier()
dt.fit(X_train,y_train)

# sample output
# print(dt.predict([[36,144000]]))
# print(dt.predict([[30,87000]]))

# dumping the model using pickled files to store data in binary format
import pickle
pickle.dump(dt,open('model.pkl','wb'))