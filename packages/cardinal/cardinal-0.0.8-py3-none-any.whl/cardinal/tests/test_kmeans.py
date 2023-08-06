import numpy as np
from cardinal.kmeans import IncrementalKMeans


def test_incremental_kmeans():
    
    data = np.random.random((50, 4))
    kmeans = IncrementalKMeans(n_clusters=4)
    kmeans.fit_transform(data)
    current_centers = kmeans.centers_.copy()
    new_clusters = kmeans.transform(data, fixed_cluster_centers=current_centers_)
