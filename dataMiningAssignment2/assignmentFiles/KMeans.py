#from dataPreprocessing import data_preprocessing
import  numpy as np

#data, outliers = data_preprocessing('D:\\Collage\\4th_year\\second_semester\\Data Mining\\dataMiningAssignment2\\assignmentFiles\\SS2025_Clustering_SuperMarketCustomers.csv')

class Cluster:
    def __init__(self):
        self.curr_centroid = {}
        self.members = {}

def Ecludien(x1, x2, x3):
    sum = x1 * x1 + x2 * x2 + x3 * x3
    result = sum ** 0.5
    return result


def k_means(data, k):
    start_centroid_indices = []
    while len(start_centroid_indices) != k:
        ind = np.random.randint(0, data.shape[0] - 1)
        if ind not in start_centroid_indices:
            start_centroid_indices.append(ind)

    clusters = []
    for i in range(len(start_centroid_indices)):
        cluster = Cluster()
        cluster.curr_centroid = data.iloc[start_centroid_indices[i]].copy()
        clusters.append(cluster)

    check = True
    while check:
        change_count = 0
        new_cluster_members = [{} for c in range(k)]

        for i in range(data.shape[0]):
            rec = data.iloc[i]
            distances = []

            for c in clusters:
                print(rec['CustomerID'])
                x1 = c.curr_centroid['Age'] - rec['Age']
                x2 = c.curr_centroid['Annual Income (k$)'] - rec['Annual Income (k$)']
                x3 = c.curr_centroid['Spending Score (1-100)'] - rec['Spending Score (1-100)']
                dis = Ecludien(x1, x2, x3)
                distances.append(dis)
            min_dis = min(distances)
            assign_to = [l for l in range(len(distances)) if distances[l] == min_dis]
            new_cluster_members[assign_to[0]][rec["CustomerID"]] = rec.copy()

        for i in range(len(clusters)):
            if set(clusters[i].members.keys()) != set(new_cluster_members[i].keys()):
                change_count += 1

        if change_count == 0:
            check = False
        else:
            for i in range(len(clusters)):
                clusters[i].members = new_cluster_members[i]

            for c in clusters:
                mem_count = len(c.members)
                Age = sum([v['Age'] for v in c.members.values()]) / mem_count
                Annual = sum([v['Annual Income (k$)'] for v in c.members.values()]) / mem_count
                Score = sum([v['Spending Score (1-100)'] for v in c.members.values()]) / mem_count
                c.curr_centroid['Age'] = Age
                c.curr_centroid['Annual Income (k$)'] = Annual
                c.curr_centroid['Spending Score (1-100)'] = Score


    final_clusters, outliers = extract_outliers(clusters)
    final_outliers = []

    for o in outliers:
        customer_id = list(o.keys())[0]
        record = data[data['CustomerID'] == customer_id].to_dict('records')[0]  # Efficient record extraction
        final_outliers.append({customer_id: record})

    return final_clusters, final_outliers


#k_means(data, 3)


def extract_outliers(clusters):
    outliers = []
    new_clusters = []
    for c in clusters:
        new_cluster = Cluster()
        centroid = c.curr_centroid
        result = []

        for member in c.members.values():
            x1 = centroid['Age'] - member['Age']
            x2 = centroid['Annual Income (k$)'] - member['Annual Income (k$)']
            x3 = centroid['Spending Score (1-100)'] - member['Spending Score (1-100)']
            distance = Ecludien(x1, x2, x3)

            result.append({member['CustomerID'] : distance})

        result = sorted(result, key=lambda d: list(d.values())[0],reverse= True)
        count = int(0.05 * len(result))
        ID = []
        #print("test1")
        for i in range(count):
            outliers.append(result[i])
            ID.append(list(result[i].keys())[0])

        #print("test2")
        new_cluster.curr_centroid = c.curr_centroid
        for i in range(len(c.members)):
            if list(c.members.keys())[i] not in ID:
                new_cluster.members[list(c.members.keys())[i]] = list(c.members.values())[i]

        new_clusters.append(new_cluster)

    #print("yesssssssssss")
    return new_clusters, outliers


