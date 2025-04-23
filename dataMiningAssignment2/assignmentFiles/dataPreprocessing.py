import pandas as pd

def read_data(path):
    customers = pd.read_csv(path)
    return customers

#data = read_data('D:\\Collage\\4th_year\\second_semester\\Data Mining\\dataMiningAssignment2\\assignmentFiles\\SS2025_Clustering_SuperMarketCustomers.csv')

def data_cleansing(data):
    columns = data.dtypes
    outliers = []
    #print(data.count())
    for key in columns.keys():
        if pd.api.types.is_numeric_dtype(data[key]):
            if key != 'CustomerID':
                Q1 = data[key].quantile(0.25)
                Q3 = data[key].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 -(1.5 * IQR)
                upper = Q3 + (1.5 * IQR)
                rejected = data[(data[key] < lower) | (data[key] > upper)]
                if len(rejected) != 0:
                    outliers.append(rejected) 
                data = data[(data[key] >= lower) & (data[key] <= upper)]

    #print(outliers)
    return data, outliers

def data_transformation(data):
    data = data.drop(columns='Gender')

    columns = data.dtypes
    for key in columns.keys():
        if pd.api.types.is_numeric_dtype(data[key]):
            if key != 'CustomerID':
                data[key] = (data[key] - data[key].min()) / (data[key].max() - data[key].min())

    return data

def data_preprocessing(path, percentage):
    customers = read_data(path)
    customers = customers.iloc[:int(customers.shape[0] * (percentage/100))]
    #customers, outliers = data_cleansing(customers)
    customers = data_transformation(customers)
    return customers
#print(data_preprocessing('D:\\Collage\\4th_year\\second_semester\\Data Mining\\dataMiningAssignment2\\assignmentFiles\\SS2025_Clustering_SuperMarketCustomers.csv'))
