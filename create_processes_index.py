# Author : Pruthvik Narayan Narayanaswamy (pnarayan@gmu.edu)
# Script to index persistance vectors and write index to file
# Using FAISS (see https://github.com/facebookresearch/faiss for official documentation and source code)

import numpy as np
import mysql.connector
import faiss
from faiss import normalize_L2

def main():
  # Set the database parameters to connect
  mydb = mysql.connector.connect(
    host="localhost",
    user="Swami",
    passwd="cngpassspv",
    database="nmdbDev"
    )

  # Fetach all persistance vectors from DB 
  # ordering by neuron_id important as we receive only id of the array from faiss, not the neuron_id iteslf.
  mycursor = mydb.cursor()
  mycursor.execute("SELECT neuron_id, Neuron_name, IFNULL(NULLIF(Soma_Surface, '' ), 0) as Soma_Surface, N_stems, N_bifs, N_branch, Width, Height, Depth, Diameter, Length, Surface, Volume, EucDistance, PathDistance, Branch_Order , Contraction, Fragmentation, Partition_asymmetry, Pk_classic, Bif_ampl_local, Bif_ampl_remote, Fractal_Dim FROM measurementsPR order by neuron_id")
  myresult = mycursor.fetchall()

  vectors = []
  for x in myresult:
    # Slice array to store only co-efficients
    v = x[2:]
    vectors.append(v)

  # Convert co-efficients to float32
  vectors = np.asarray(vectors).astype('float32')

  # Set dimension of vector
  d = 21
  # Build the index
  index = faiss.IndexFlatIP(d)   
  print("Index trained : " + str(index.is_trained))
  # Normalize vectors for indexing (faiss cosine similarity requires normalized vectors)
  normalize_L2(vectors)
  # Add vectors to the index
  index.add(vectors)                  
  print("Number of vectors indexed : " + str(index.ntotal))
  # Write the index to file
  faiss.write_index(index, "nmo_measurements_processes.index")

main()      