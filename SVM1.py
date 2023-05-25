import pandas as pd
import random
df = pd.read_csv("insta_train.csv")
#df.drop(['length username'], axis=1)
df.to_csv("train.csv", header=False, index=False)
dataset = pd.read_csv("train.csv")
X = dataset.iloc[:, 0:10].values

Y = dataset.iloc[:, 11].values
print('X', X)
print('Y',Y)
#l=pd.unique(dataset.iloc[:,11])
#pred=random.choice(l)

from sklearn.preprocessing import LabelEncoder
#labelencoder_Y = LabelEncoder()
#Y = labelencoder_Y.fit_transform(Y)


from sklearn.model_selection import train_test_split
X_train, X_test1, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 5)

print('X_test_data', X_test1)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
#X_train = sc.fit_transform(X_train)
#X_test1 = sc.transform(X_test)


from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train, Y_train)
#pred=random.choice(l)
X_test = [[1, 0.18, 1, 0, 0, 0, 0, 0, 0, 42]] #For 1
#X_test = [[0, 0.5, 1, 0.33, 0, 0, 0, 0, 3, 43]] For 1
#X_test = [[1, 0, 0, 0, 0, 103, 0, 0, 24, 617]] For 0

Y_pred = classifier.predict(X_test)
print('Y_pred_test',Y_pred)

Y_pred1 = classifier.predict(X_test1)
print('Y_pred',Y_pred)
#print('Y_pred_test',Y_pred1)


from sklearn.metrics import confusion_matrix,classification_report
cm = confusion_matrix(Y_test, Y_pred1)
print("\n",cm)

print(classification_report(Y_test,Y_pred1))

iclf = SVC(kernel='linear', C=1).fit(X_train, Y_train)
#print(iclf)
accuracy2=((iclf.score(X_test1, Y_test))*100)
print("accuracy=",accuracy2)

import matplotlib.pyplot as plt

x = [0, 1, 2]
y = [accuracy2, 0, 0]
plt.title('Accuracy2')
plt.bar(x, y)
plt.show()
