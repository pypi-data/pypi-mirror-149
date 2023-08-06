import warnings
import pandas as pd
from pandas.core.common import SettingWithCopyWarning
from sqlalchemy import over
warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)
# Sample Balancing Imports
from imblearn import over_sampling 
from imblearn import under_sampling 
from imblearn.pipeline import Pipeline
from sklearn.metrics import recall_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from captum import attr
import torch
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

import torch
import json
import torch.nn as nn
import pandas as pd
import torch.utils.data as TData
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import numpy as np

# General Imports
from cgi import test
import pandas as pd
import numpy as np
import copy
import math
# Sklearn Ensemble Model Import
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
# Sklearn General Model Training Imports
from sklearn.metrics import precision_score, recall_score, roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from sklearn.model_selection import GroupKFold, KFold
from sklearn.metrics import mean_squared_error, multilabel_confusion_matrix, classification_report, confusion_matrix

# Graph Impots
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly





# Sklearn Imports
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder 
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import PowerTransformer
from sklearn.metrics import mean_squared_error, multilabel_confusion_matrix, classification_report
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

# PyTorch Import
import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
import numpy as np
import optuna


class Data():           #type padas datafram
    def __init__(self, df, y_name='distress_level', y_encoded = False, has_distress = False):
        self.x = None
        self.y = None
        self.encoders = {}

        if has_distress:
            if y_encoded:
                # if y is encoded already
                self.y = df.loc[:, [0,1]]
                self.x = df.drop(columns=[0,1])  
                
            else:
                # if y is distress, no distress
                self.y = df[[y_name]]
                self.x = df.drop(columns=[y_name])  
        else:
            self.x=df
        
        self.rows = self.x.shape[0]
        self.cols = self.x.shape[1]

    def __len__(self):
        return len(self.x)

    def __getitem__(self, items):
        return self.x[items]

    def __contains__(self, key):
        return key in self.x.columns

    def iloc(self, rows):
        return self.x.iloc[rows]

    def all(self):
        return self.x

    def dim(self):
        return (self.rows, self.cols)
    
    def scaleEncode(self, numerical_columns=[], ignore_columns=[]):
        for column in self.x:
            if column in ignore_columns:
                continue
            elif column in numerical_columns:
                self.normalize(column)
            else:
                self.encode(column)
    

    def encode(self, column_name):
        self.encoders[column_name] = LabelEncoder()
        self.x[column_name] = self.encoders[column_name].fit_transform(self.x[column_name].values.ravel())
        
    def normalize(self, column_name, method='min_max'):
        if(method == 'min_max'):
            self.x[column_name] = (self.x[column_name]-self.x[column_name].min())/(self.x[column_name].max()-self.x[column_name].min())
        elif(method == 'log'):
            for column in column_name:
                temp_col = self.x[column]
                min_value = temp_col.min()
                if min_value <= 0:
                    pt = PowerTransformer()
                else: 
                    pt = PowerTransformer(method = 'box-cox')
                transformed_col = pt.fit_transform(pd.DataFrame(temp_col))
                self.x[column] = transformed_col.copy()
        else:
            print("method not supported")
    
    def filter(self, method, select_var = 0.05, select_k=15):
        if(method == 'correlation'):
            fs = SelectKBest(score_func=f_classif, k=select_k)
            X_selected = fs.fit_transform(self.x, self.y)
            self.x = X_selected
            self.cols = self.x.shape[1]

        elif(method == 'variance'):
            variance = self.x.var()
            valid_columns = []
            for i in range(len(variance)):
                if variance[i] > select_var:
                    valid_columns.append(self.x.columns[i])
            self.x = self.x[valid_columns]
            self.cols = self.x.shape[1]
        else:
            print("method not supported")

    def split(self, split_ratio, stratify=None):
        if not stratify:
            train, test = train_test_split(self.x, test_size=split_ratio)
        else:
            train, test = train_test_split(self.x, test_size=split_ratio, stratify=stratify)
        return (Data(train), Data(test))

    def getData(self, columns=None):
        if columns:
            return self.x[columns]
        return self.x

    def checkColumn(self, column):
        if column in self.x:
            return True
        return False

    def pca(data:Data, keywords:list, n_components:list):
        #pca
        if len(keywords) != len(n_components):
            print("Keywords and n_components must be of the same length")
            return

        col_list = data.x.columns
        for index in range(0, len(keywords)):
            keyword = keywords[index]
            temp_pca_list = []
            for name in col_list:
                if keyword in name:
                    temp_pca_list.append(name)

            temp_pca = pd.DataFrame(data.x, columns = temp_pca_list)

            data.x = data.x.drop(temp_pca_list, axis=1)

            pca = PCA(n_components = n_components[index])
            result = pca.fit_transform(temp_pca)
            result_df = pd.DataFrame(result)
            result_df.columns = [f'{keyword}_pca_{i}' for i in range(0, n_components[index])]
            result_df.index = temp_pca.index
            #merge pca result and original data horizontally
            data.x = pd.concat([data.x, result_df], axis=1)

    def resample(self, under_ratio:float, over_ratio:float, up_sampling_method:str, y:Data):
        
        merged = y.x[['GUID','distress_level']].set_index('GUID').merge(self.x, on ='GUID', how = 'inner')
        self.x = merged.drop(columns = ['distress_level'])
        self.y = merged['distress_level']
        # d = {0: self.y=='no distress', 1: self.y=='distress'}
        # self.y = pd.DataFrame(data = d).astype(int)
        

        train_counts = self.y.value_counts(ascending = True)
        print(train_counts)

        res_0 = train_counts[1]
        res_1 = train_counts[0]

        # under = under_sampling.RandomUnderSampler(sampling_strategy={0: int(under_ratio * res_0), 1: int(res_1)})
        # over = over_sampling.SMOTE(sampling_strategy= {0: int(res_0), 1: int(over_ratio * res_1)})
        # steps = [('o', over), ('u', under)]
        # pipeline = Pipeline(steps=steps)

        distress_group = self.x[self.y == 'distress']
        nodistress_group = self.x[self.y == 'no_distress'] 
        # self.x, self.y = pipeline.fit_resample(self.x, self.y.to_numpy())
        oversample = distress_group.sample(len(distress_group)*over_ratio, replace = True)
        undersample = nodistress_group.sample((int)(len(nodistress_group)*under_ratio), replace = False)
    
        combined_exp_df = pd.concat([oversample,undersample], axis=0)
        combined_exp_df = combined_exp_df.sample(len(combined_exp_df), replace = False)
        combined_exp_df.reset_index(inplace = True, drop = True)
        self.x = combined_exp_df
        self.rows = len(self.x)

    
    def combine_outcome(self, df, on='GUID', y_name = 'distress_level', na='drop'):
        df = df.set_index('GUID').join(self.x, on=on, how='left')
        
        # deal with NAs
        if(na == 'drop'):
            df = df.dropna()
        elif(na == 'fill'):
            # TODO bug, it should only fillna on distress and drop all no distress with na
            df = df.fillna(df[df['distress_level'] == 'distress'].median)
        self.y = df[[y_name]]
        self.x = df.drop(columns=[y_name])  
        self.rows = self.x.shape[0]
    
    def process(self, pipeline):
        # needs to be in order
        for func_parm_dic in pipeline:
            # for each dict of {methodname : args}
            for func_name in func_parm_dic:
                # get the parameter for each function, unpackit and run the method of self
                parm = func_parm_dic[func_name]
                getattr(self, func_name)(**parm)


def oneHotEncode(data):
    # TODO
    # support OneHotEncode on any other Columns on any Data
    head_col = data['GUID']
    onehot_encoder = OneHotEncoder(sparse=False, handle_unknown = 'ignore')
    arr = onehot_encoder.fit_transform(data[['Site ID']])
    df_site = pd.DataFrame(arr)
    name_col = []
    for i in range(1, 23):
        col_name = "Site_" + str(i)
        name_col.append(col_name)
    df_site.columns = name_col
    return pd.concat([head_col, df_site], axis=1, join="inner")
                

def combine(data_list = [], on='GUID'):
    out_df = data_list[0].x
    for index in range(1, len(data_list)):
        out_df = out_df.merge(data_list[index].x, on=on, how='inner')
    return Data(out_df)

def merge_feature(file_set):
    
    if len(file_set)<=1:
        df = pd.read_csv("Data/data/" + file_set.pop())
        df = df.rename(columns={"The NDAR Global Unique Identifier (GUID) for research subject": "GUID"})

        if ('The event name for which the data was collected' in df):
            df = df.drop(columns='The event name for which the data was collected')
        return  (df.set_index('GUID'))

    else:
        # merging data
        first_data = file_set.pop()
        df_first = pd.read_csv("Data/data/" + first_data)
        df_first = df_first.rename(columns={"The NDAR Global Unique Identifier (GUID) for research subject": "GUID"}).set_index('GUID')
        if ('The event name for which the data was collected' in df_first):
                df_first = df_first.drop(columns='The event name for which the data was collected')

        for data in file_set:
            df = pd.read_csv("Data/data/" + data)
            df = df.rename(columns={"The NDAR Global Unique Identifier (GUID) for research subject": "GUID"})

            if ('The event name for which the data was collected' in df):
                df = df.drop(columns='The event name for which the data was collected')
            df = df.set_index('GUID')

            df_first = df_first.join(df, on="GUID", how = 'inner')
    return df_first

def train_test(data, test_size=0.3):

    X_train, X_test, y_train, y_test = train_test_split(data.x, data.y, test_size=test_size)
    train = Data(X_train)
    train.y = y_train
    test = Data(X_test)
    test.y = y_test
    return train, test

def filterClasifyOutcome(outcome_data, low_threshold, high_threshold, classify=False, discard_threshold=None):
    filtered_outcome_data = []
    outcome = None
    if classify:
        outcome = []

    for _, row in outcome_data.iterrows():
        if discard_threshold and row['baseline_score'] < discard_threshold:
            continue
        low_count = 0
        high_count = 0
        if row['baseline_score'] <= low_threshold:
            low_count = low_count + 1
        if row['baseline_score'] >= high_threshold:
            high_count = high_count + 1
        if row['year1_score'] <= low_threshold:
            low_count = low_count + 1
        if row['year1_score'] >= high_threshold:
            high_count = high_count + 1
        if row['year2_score'] <= low_threshold:
            low_count = low_count + 1
        if row['year2_score'] >= high_threshold:
            high_count = high_count + 1
        
        if low_count >=2 or high_count >= 2:
            filtered_outcome_data.append(row)
            if classify:
                if high_count >=2 :
                    outcome.append("distress")
                else:
                    outcome.append("no distress")

    filtered_outcome_data = pd.DataFrame(filtered_outcome_data)
    if classify:
        filtered_outcome_data["distress_level"] = outcome
        
    return filtered_outcome_data

def pca_check(data:Data, keywords:list, n_components:int):

    data = _check_GUID(data)

    col_list = data.x.columns
    for keyword in keywords:
        temp_pca_list = []
        for name in col_list:
            if keyword in name:
                temp_pca_list.append(name)

        print(f'{keyword}: {len(temp_pca_list)}')
        temp_pca = pd.DataFrame(data.x, columns = temp_pca_list)
        
        pca = PCA(n_components = n_components)
        result = pca.fit_transform(temp_pca)
        x = pd.DataFrame(result)
        cumsum = np.cumsum(pca.explained_variance_ratio_)
        # add 0 to front of the list
        cumsum = np.insert(cumsum, 0, 0)
        plt.plot(range(0,n_components+1), cumsum)
        plt.ylabel('Cumulative Explained Variance')
        plt.xlabel('Num of Principal Components')
        plt.show()
        
        print(cumsum)
        # return graph


def _check_GUID(df:Data):
    if 'GUID' in df.x.columns:
        df.x = df.x.set_index('GUID')
        return df
    else:
        return df





################################################################################

class BinaryNeuralNetwork(nn.Module):
    def __init__(self, model, loss_fn, optimizer="SGD", parameters={}):
        super(BinaryNeuralNetwork, self).__init__()
        
        # Model
        self.model = model
        self.loss_fn = loss_fn
        self.learning_rate = parameters["learning_rate"]
        self._setOptimizer(optimizer)
        
        # Training
        self.batch_size = parameters["batch_size"]
        self.epochs = 1000
        self.validation_split = 0.2
        
        # Early Stopping
        self.patience = 5

    def forward(self, x):
        x = self.model(x)
        return x
    
    def fit(self, x, y, model_name):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.to(device)
        
        train_loader, tensor_X_val, tensor_y_val = self._prepData(x, y)
        
        min_validation_loss = np.inf
        curr_patience = self.patience
        
        for e in range(self.epochs):
            self.train()
            for X, y in train_loader:
                X, y = X.to(device), y.to(device)

                # Compute prediction error
                pred = self(X)
                loss = self.loss_fn(pred, y)

                # Backpropagation
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
            
            validation_loss = 0.0
            self.eval()
            valid_out = self(tensor_X_val)
            validation_loss = self.loss_fn(valid_out, tensor_y_val).item()
            
            if min_validation_loss > validation_loss:
                #print(f'Validation Loss Decreased({min_validation_loss:.6f}--->{validation_loss:.6f}) \t Saving The Model')
                min_validation_loss = validation_loss
                # Saving State Dict
                model_pth = model_name + "_saved_model.pth"
                torch.save(self.state_dict(), model_pth)
                curr_patience = self.patience
            else:
                curr_patience = curr_patience - 1
            
            if curr_patience <= 0:
                #print("Stopping Early due to no improvement")
                break
    
    def predict_proba(self, x):
        tensor_x = self._formatTensor(x)
        return self(tensor_x).detach().numpy()
    
    def predict(self, x):
        a = self.predict_proba(x)
        a = (a == a.max(axis=1)[:,None]).astype(int)
        prediction_df = pd.DataFrame(a)
        return prediction_df
                   
    def configure(self, parameters):
        if "batch_size" in parameters:
            self.batch_size = parameters["batch_size"]
        if "epochs" in parameters:
            self.epochs = parameters["epochs"]
        if "validation_split" in parameters:
            self.validation_split = parameters["validation_split"]
        if "patience" in parameters:
            self.patience = parameters["patience"]
            
    def _oneHoteEncodeOutcome(self, outcome):
        outcome = np.array(outcome)
        if outcome.ndim < 2:
            outcome = outcome.reshape(-1, 1)
        return OneHotEncoder(handle_unknown='ignore', sparse=False).fit_transform(outcome)
            
    def _prepData(self, x, y):
        # merge x and y into one dataframe
    
        train_data = pd.concat([x, y], axis=1)
        
        model_train_data, model_val_data = train_test_split(train_data, test_size=0.1)

        distress_group = model_train_data[model_train_data['distress_level'] == 'distress']
        nodistress_group = model_train_data[model_train_data['distress_level'] == 'no distress']

        oversample_distress_group = distress_group.sample(len(distress_group)*5, replace = True)
        undersample_nodistress_group = nodistress_group.sample((int)(len(nodistress_group)*0.15), replace = False)

        combined_exp_df = pd.concat([oversample_distress_group,undersample_nodistress_group], axis=0)
        combined_exp_df = combined_exp_df.sample(len(combined_exp_df), replace = False)
        combined_exp_df.reset_index(inplace = True, drop = True)

        train_X = combined_exp_df.copy().drop(columns = ['distress_level'])
        train_y = combined_exp_df.copy()['distress_level']

        val_X = model_val_data.copy().drop(columns = ['distress_level'])
        val_y = model_val_data.copy()['distress_level']

        tensor_X_train = torch.from_numpy(np.array(train_X).astype(np.float32))
        tensor_y_train = torch.from_numpy(np.array(self._oneHoteEncodeOutcome(train_y)).astype(np.float32))
        train_dataset = TData.TensorDataset(tensor_X_train.float(), tensor_y_train.float())

        tensor_X_val = torch.from_numpy(np.array(val_X).astype(np.float32))
        tensor_y_val = torch.from_numpy(np.array(self._oneHoteEncodeOutcome(val_y)).astype(np.float32))

        train_loader = TData.DataLoader(dataset=train_dataset, batch_size = self.batch_size)
        
        return (train_loader, tensor_X_val, tensor_y_val)

    
    def _formatTensor(self, data):
        return torch.from_numpy(np.array(data).astype(np.float32)).float()
        
    def _setOptimizer(self, optimizer_name):
        if optimizer_name == "SGD":
            self.optimizer = torch.optim.SGD(self.parameters(), lr=self.learning_rate)
        elif optimizer_name == "Adam":
            self.optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        elif optimizer_name == "RMSprop":
            self.optimizer = torch.optim.RMSprop(self.parameters(), lr=self.learning_rate)
        else:
            print("Optimizer {} not found. Setting to Default SGD.".format(optimizer_name))
            self.optimizer = torch.optim.SGD(self.parameters(), lr=self.learning_rate)

def get_params(location):
    with open(location) as json_file:
        param = json.load(json_file)
    dic_param = {k: v for k, v in param.items()}
    return dic_param

def createNeuralNet(input_dim, param):
    layers = []

    activations = {
        'relu': nn.ReLU(),
        'sigmoid': nn.Sigmoid(),
        'leakyrelu': nn.LeakyReLU()
    }

    in_features = input_dim
    
    for i in range(param['n_layers']):
        
        out_features = param['n_units_l'+str(i)]
        
        layers.append(nn.Linear(in_features, out_features))
        layers.append(activations[param['act_function']])

        in_features = out_features
        
    layers.append(nn.Linear(in_features, 2))
    layers.append(nn.Softmax(dim=1))
    model = nn.Sequential(*layers)

    
    return BinaryNeuralNetwork(model, nn.BCELoss(weight = torch.FloatTensor([param['weight_0'], param['weight_1']]),reduction='mean') , param['optimizer'], param)
    
    ##############################################################################################




class EnsembleClassifier:
    def __init__(self, log=False, ensemble_model=LogisticRegression(class_weight="balanced")):
        self.id_name = ""
        self.outcome_name = ""
        self.log = log
        self.final_result = None
        self.outcome_data = None
        
        self.data = {}
        self.models = {}
        
        self.ensemble_model = ensemble_model
        
    def addDataset(self, dataset, dataset_name, model):
        self.data[dataset_name] = dataset
        self.models[dataset_name] = model
        
    def setOutcome(self, outcome, id_name, outcome_name):
        self.id_name = id_name
        self.outcome_name = outcome_name
        self.outcome_data = outcome
    
    
    def groupFoldCrossValidate(self, group_name, log=None):
        if not group_name in self.outcome_data:
            print("Group Not Found")
            return
        
        no_splits = len(np.unique(self.outcome_data[group_name]))
        group_kfold = GroupKFold(n_splits=no_splits)
        
        splits = group_kfold.split(self.outcome_data.all(), self.outcome_data[self.outcome_name], self.outcome_data[group_name])
        
        print("Group {} Results: ".format(group_name))
        return self._crossValidate(splits, log)
    
    '''
    def kFoldCrossValidation(self, k, shuffle=True, log=None):

        kfold = KFold(n_splits=k, shuffle=shuffle)
        splits = kfold.split(self.outcome_data.all())

        print("K-Fold Results: ")

        return self._crossValidate(splits, log)
    
    
    def trainTest(self, split=0.3, log=None):
        train_ids, test_ids = train_test_split(self.outcome_data[[self.id_name, self.outcome_name]], test_size=split, stratify=self.outcome_data[self.outcome_name])
        return self._trainTest(train_ids, test_ids, log)
    
    def _crossValidate(self, splits, log=None):
        average_accuracy = 0
        average_precision = average_recall = average_fscore = np.array([0, 0])
        iterations = 0
        
        for train_ids, test_ids in splits:
            res = self._trainTest(self.outcome_data.iloc(train_ids)[[self.id_name, self.outcome_name]], self.outcome_data.iloc(test_ids)[[self.id_name, self.outcome_name]], log)
            
            average_accuracy = average_accuracy + res["Accuracy"]
            average_precision = average_precision + res["Metrics"][0]
            average_recall = average_recall + res["Metrics"][1]
            average_fscore = average_fscore + res["Metrics"][2]
            iterations = iterations + 1
         
        average_accuracy = average_accuracy / iterations
        average_precision = average_precision / iterations
        average_recall = average_recall / iterations
        average_fscore = average_fscore / iterations
        
        print("Accuracy: {}".format(average_accuracy))
        print("Precision: {}".format(average_precision))
        print("Recall: {}".format(average_recall))
        print("F-Score: {}".format(average_fscore))
        
        return {"Accuracy" : average_accuracy, "Precision" : average_precision, "Recall" : average_recall, "F-Score" : average_fscore}
        
    def _trainTest(self, train_ids, test_ids, log=None):
        self._ensembleTrain(train_ids, log)
        predictions = self._ensemblePredict(test_ids)
        
        accuracy = accuracy_score(test_ids[self.outcome_name], predictions)
        metrics = precision_recall_fscore_support(test_ids[self.outcome_name], predictions)
        
        print("Ensemble Results: ")
        print(accuracy)
        print(metrics)
        
        return {"Accuracy": accuracy, "Metrics" : metrics}
        
    def _ensemblePredict(self, ids, probs=False):
        ensemble_data = pd.DataFrame(columns=self.data.keys())
        
        for dataset_name in self.data:
            ensemble_data[dataset_name] = self._predict(ids, dataset_name, True)
            
        if probs:
            return self.ensemble_model.predict_proba(np.array(ensemble_data))[:, 1]
        return self.ensemble_model.predict(np.array(ensemble_data))
        
    def _ensembleTrain(self, ids, log=None):
        #ensemble_data = pd.DataFrame(columns=self.data.keys())

        # only temp changes. ideally should be integrated
        ########################################################
        distress_group = ids[ids['distress_level'] == 'distress']
        nodistress_group = ids[ids['distress_level'] == 'no distress']

        oversample_distress_group = distress_group.sample(len(distress_group)*5, replace = True)
        undersample_nodistress_group = nodistress_group.sample((int)(len(nodistress_group)*0.15), replace = False)

        ids = pd.concat([oversample_distress_group,undersample_nodistress_group], axis=0)
        ids["distress_level"] = ids["distress_level"].replace({"no distress": 0})
        ids["distress_level"] = ids["distress_level"].replace({"distress": 1})
        ids = ids.sample(len(ids), replace = False)
        ids.reset_index(inplace = True, drop = True)
        ##########################################################
        
        for dataset_name in self.data:
            self._train(ids, dataset_name)
        
        #self.ensemble_model.fit(np.array(ensemble_data), ids[self.outcome_name])
        
        #self._logResults(np.array(ensemble_data), ids[self.outcome_name], self.ensemble_model, "Ensemble", log)
                
    def _train(self, ids:pd.DataFrame, dataset_name, identifier="", log=None):

        curr_data = ids.merge(self.data[dataset_name].all(), how="left", on=self.id_name).dropna()
        print(self.models[dataset_name])
        self.models[dataset_name].fit(curr_data.drop(columns=[self.id_name, self.outcome_name]), curr_data[self.outcome_name])
        prediction_probs = self.models[dataset_name].predict_proba(curr_data.drop(columns=[self.id_name, self.outcome_name]))[:, 1]

        self._logResults(curr_data.drop(columns=[self.outcome_name, self.id_name]), curr_data[self.outcome_name], self.models[dataset_name], dataset_name + identifier, log)
            
        return prediction_probs
    
    def _predict(self, ids, dataset_name, probs=False):
        curr_data = ids.merge(self.data[dataset_name].all(), how="left", on=self.id_name).fillna(0)
        if probs:
            return self.models[dataset_name].predict_proba(curr_data.drop(columns=[self.id_name, self.outcome_name]))[:, 1]
        return self.models[dataset_name].predict(curr_data.drop(columns=[self.id_name, self.outcome_name]))
        
    def _logResults(self, data, outcome, model, identifier="", log=None):
        if (not log and self.log) or log:
            predictions = model.predict(data)
            print("{} Results: ".format(identifier))
            print(accuracy_score(outcome, predictions))
            print(precision_recall_fscore_support(outcome, predictions))
            print("-" * 20)
    '''

    def kFoldCrossValidation(self, k, shuffle=True, log=None):
        self._setGroupNum(k)
        print(k,"- Fold Results: ")

        return self._crossValidate(k, log)
        
    def _crossValidate(self, k, log=None):
        group_result = []
        for index in range(0, k):
            res = self._ensembleTrainTest((self.outcome_data.x.loc[self.outcome_data.x['test_group'] != index])[['GUID', 'distress_level']], (self.outcome_data.x.loc[self.outcome_data.x['test_group'] == index])[['GUID', 'distress_level']], log)
            group_result.append(res)
         
        # conbine each dataframe in the list
        group_result_df = pd.concat(group_result, axis=0)
        expect_result = group_result_df['distress_level']
        predict_result = group_result_df['combined_result']
        target_names = ['no_distress','distress']
        expect_result = expect_result.replace({'no distress': 0, 'distress' : 1})
        matrix = confusion_matrix(expect_result, predict_result)

        data_matrix = {'TN': [matrix[0][0]],
        'TP': [matrix[1][1]],
        'FN': [matrix[1][0]],
        'FP': [matrix[0][1]]}

        matrix_df = pd.DataFrame(data_matrix, index=['TN', 'TP', 'FN', 'FP'])

        # drop duplicate
        matrix_df.drop_duplicates(inplace=True)
        matrix_df.to_csv("combinedMatrix.csv", index = False)

        print(classification_report(expect_result, predict_result,target_names=target_names))
        # print(accuracy_score(expect_result, predict_result))
        # print(recall_score(expect_result, predict_result))
        # print(precision_score(expect_result, predict_result))
        self.final_result = group_result_df

    def _combineResult(self, test_ids, pred_result):
        ori_df = test_ids[[self.id_name, self.outcome_name]]
        for dataset_name in self.data:
            pred_df= pred_result[dataset_name]
            pred_df.columns = ['GUID', dataset_name, 'no_distress', dataset_name + '_prob']
            pred_df = pred_df.drop(columns=['no_distress'])
            ori_df = ori_df.merge(pred_df, how="left", on=['GUID'])
        ori_df.insert(ori_df.shape[1], 'combined_result', -1.0)
        ori_df = ori_df.fillna(-1.0)
        test_data = ori_df.copy()
        for i in range(0, len(test_data)):
            total_point = 0
            total_weight = 0

            for dataset_name in self.data:
                if test_data.iloc[i][dataset_name] != -1.0:
                    total_point += test_data.iloc[i][dataset_name]*0.25
                    total_weight += 0.25

            if total_weight != 0:
                weighted_score = total_point/total_weight
                if weighted_score >= 0.5:
                    test_data.iloc[i,10] = 1.0
                else:
                    test_data.iloc[i,10] = 0.0
        
        empty_col = test_data[test_data.combined_result == -1]
        test_data = test_data.drop(empty_col.index)
        test_data = test_data.reset_index()
        test_data = test_data.drop(columns = ['index'])

        expect_result = test_data['distress_level']
        predict_result = test_data['combined_result']
        target_names = ['no_distress','distress']
        expect_result = expect_result.replace({'no distress': 0, 'distress' : 1})
        '''
        print("Combined Result")
        print(classification_report(expect_result, predict_result,target_names=target_names))
        '''
        return test_data
                    


    def _ensembleTrainTest(self, train_ids, test_ids, log=None):
        pred_result = {}
        for dataset_name in self.data:
            #print("Training {}".format(dataset_name))
            net = self._train(train_ids, dataset_name)
            predictions = self._predict(net, test_ids, dataset_name)
            self.models[dataset_name] = net
            test_y = pd.merge(predictions['GUID'], test_ids[[self.id_name, self.outcome_name]], how="left", on="GUID")
            real_y = pd.DataFrame(self._oneHoteEncodeOutcome(test_y['distress_level']))
            pred_y = predictions.drop(columns=['GUID', 'prob_result'])
            #print(classification_report(real_y, pred_y, target_names = ['distress', 'no distress']))
            pred_result[dataset_name] = predictions
        ensemble_result = self._combineResult(test_ids, pred_result)
        return ensemble_result

    def _oneHoteEncodeOutcome(self, outcome):
        outcome = np.array(outcome)
        if outcome.ndim < 2:
            outcome = outcome.reshape(-1, 1)
        return OneHotEncoder(handle_unknown='ignore', sparse=False).fit_transform(outcome)


    def _predict(self, net, ids, dataset_name, probs=False):
        curr_data = ids.merge(self.data[dataset_name].all(), how="inner", on=self.id_name).dropna()
        prob_result = net.predict_proba(curr_data.drop(columns=[self.id_name, self.outcome_name]))[:, 0]
        predict_result = net.predict(curr_data.drop(columns=[self.id_name, self.outcome_name]))
        combined_result = pd.concat([curr_data['GUID'],predict_result, pd.DataFrame(prob_result)],axis=1)
        combined_result.columns = ['GUID', dataset_name, 'no_distress', 'prob_result']
        return combined_result


    def _train(self, ids:pd.DataFrame, dataset_name, identifier="", log=None):
        curr_data = ids.merge(self.data[dataset_name].all(), how="inner", on=self.id_name).dropna()
        net = copy.deepcopy(self.models[dataset_name])
        net.fit(curr_data.drop(columns=[self.id_name, self.outcome_name]), curr_data[self.outcome_name],dataset_name)
        return net
    
    def _setGroupNum(self, k):
        self.outcome_data.x = self.outcome_data.x.sample(len(self.outcome_data.x), replace = False)
        self.outcome_data.x.reset_index(inplace = True, drop = True)
        if 'test_group' not in self.outcome_data.x.columns:
            self.outcome_data.x.insert(self.outcome_data.x.shape[1], "test_group", 0)
        GROUP_NUM = k
        df_num = len(self.outcome_data.x)
        every_epoch_num = math.floor((df_num/GROUP_NUM))
        total_count = 0
        group_index = 0
        for i in range(0, df_num):
            self.outcome_data.x.iloc[i,6] = group_index
            total_count += 1
            if total_count == every_epoch_num and group_index != 19:
                group_index += 1
                total_count = 0

    def roc_curve(self, model_name, html = False):
        prob_col_name = model_name + '_prob'

        model_result = self.final_result[['GUID', 'distress_level', prob_col_name]]
        model_result = model_result.replace({'no distress': 0, 'distress' : 1})
        model_result.columns = ['GUID', 'distress_level', 'prob_result']
        model_result = model_result.reset_index()
        model_result = model_result.drop(columns = ['index'])

        empty_col = model_result[model_result.prob_result == -1.0]
        model_result = model_result.drop(empty_col.index)
        model_result = model_result.reset_index()
        model_result = model_result.drop(columns = ['index'])

        test_y = model_result['distress_level']
        prediction_df = model_result['prob_result']

        # roc_curve
        fpr, tpr, thresholds = roc_curve(test_y, prediction_df)
        roc_auc = auc(fpr, tpr)
        print("AUC Score : ", roc_auc)
        # put fpr and tpr into dataframe
        roc_df = pd.DataFrame(data = {'fpr' : fpr, 'tpr' : tpr})
        value_file = model_name + '_roc_curve.csv'
        roc_df.to_csv(value_file, index = False)

        if html:
            # Draw ROC curve and AUC with Plotly
            trace = go.Scatter(
                x = fpr,
                y = tpr,
                mode = 'lines',
                name = ('ROC curve (area = %0.2f)' % roc_auc)
            )

            # draw y = x line
            trace1 = go.Scatter(
                x = [0, 1],
                y = [0, 1],
                mode = 'lines',
                line = dict(
                    color = ('rgb(0,0,0)'),
                    width = 2,
                    dash = 'dot'
                ),
                showlegend = False
            )

            data = [trace, trace1]

            layout = go.Layout(
                title = 'ROC curve',
                xaxis = dict(
                    title = 'False Positive Rate',
                    titlefont = dict(
                        family = 'Courier New, monospace',
                        size = 18,
                        color = '#7f7f7f'
                    )
                ),
                yaxis = dict(
                    title = 'True Positive Rate',
                    titlefont = dict(
                        family = 'Courier New, monospace',
                        size = 18,
                        color = '#7f7f7f'
                    )
                )
            )
                
            fig = go.Figure(data=data, layout=layout)
            file_name = model_name + '_roc_curve.html'
            plotly.offline.plot(fig, filename=file_name)

#####################################################################################################################



supported_methods = {'IntegratedGradients', 'ShapleyValueSampling', 'Lime', 'FeatureAblation', 'FeaturePermutation'}

class BestExplainer:
    def __init__(self, method, model, input, model_name = None):

        self.method = method
        self.model = model
        self.input = torch.from_numpy(np.array(input).astype(np.float32))
        self.input.requires_grad_()
        self.features = input.keys()
        self.test_X = input

        if method not in supported_methods:
            print('supported methods are: ', supported_methods)
            raise NameError

    
        if (method == 'ShapleyValueSampling'):
            explainer = attr.ShapleyValueSampling(model)
            attribution = explainer.attribute(self.input, target=1, n_samples=200)
        
        else:
            explainer = getattr(attr,method)(model)
            attribution = explainer.attribute(self.input, target=1)

        self.attribution = attribution.detach().numpy()
        self.generateAttribution(model_name)


    def generateAttribution(self, model_name):
        total_attribute = self.getAttr()
        attribution = np.mean(total_attribute, axis=0)
        attribution, features = zip(*sorted(zip(attribution, self.features), reverse=True, key = lambda x: np.abs(x[0])))
        attribution_df = pd.DataFrame(attribution, columns=['attribution'])
        feature_df = pd.DataFrame(features, columns=['feature'])
        attribution_df = pd.concat([feature_df, attribution_df], axis=1)
        file_name = model_name + '_attribution.csv'
        attribution_df.to_csv(file_name, index = False)

    def getAttr(self, user = -1):
        if(user == -1):
            return self.attribution
        
        return self.attribution[user]
        
    
    def plot(self, max_features=-1, user = -1, chart = 'bar'):

        title="Feature Importances"
        axis_title="Features"

        if (user == -1):
            attribution = np.mean(self.attribution, axis=0)
        else:
            attribution = self.attribution[user]
        if (max_features == -1):
            max_features = len(attribution)


        
        
        # sort in decreasing order
        attribution, features = zip(*sorted(zip(attribution, self.features),
                                reverse=True,
                                key = lambda x: np.abs(x[0])))


        attribution, features = attribution[0:max_features], features[0:max_features]
        # attribution.append(np.abs(attribution[max_features:]).sum())
        # features.append('others')



        if chart == 'bar':
            for i in range(len(features)):
                print(features[i], ": ", '%.3f'%(attribution[i]), '\n')
            x_pos = (np.arange(len(features)))

            plt.figure(figsize=(12,6))
            plt.bar(x_pos, attribution, align='center')
            plt.xticks(x_pos, list(map(lambda x: x[:3], list(features))), wrap=True)
            plt.xlabel(axis_title)
            plt.title(title)
            
        elif chart == 'pi':
            fig1, ax1 = plt.subplots()


            ax1.pie(np.abs(attribution), labels = features, autopct='%1.1f%%', shadow=True)
            ax1.axis('equal')
        
        plt.savefig(f'{self.method}.jpg')
        
        print(title)
        plt.show()
    
    def plot_feature(self, test_feature):
        
        index = np.where(np.array(self.features) == test_feature)[0][0]


        bin_means, bin_edges, _ = stats.binned_statistic(self.test_X.iloc[:,index], self.attribution[:,index], statistic='mean', bins=6)
        bin_count, _, _ = stats.binned_statistic(self.test_X.iloc[:,index], self.attribution[:,index], statistic='count', bins=6)

        bin_width = (bin_edges[1] - bin_edges[0])
        bin_centers = bin_edges[1:] - bin_width/2  
        plt.scatter(bin_centers, bin_means, s=bin_count)
        plt.xlabel("Average "+ test_feature+ " Feature Value (after normalization)")
        plt.ylabel("Average Attribution")
        plt.show()

