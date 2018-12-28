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
    user="root",
    passwd="password",
    database="nmdbDev"
    )

  # Fetach all persistance vectors from DB 
  # ordering by neuron_id important as we receive only id of the array from faiss, not the neuron_id iteslf.
  mycursor = mydb.cursor()
  mycursor.execute("SELECT p.*, IFNULL(NULLIF(m.Soma_Surface, '' ), 0) as Soma_Surface, m.N_stems, m.N_bifs, m.N_branch, m.Width, m.Height, m.Depth, m.Diameter, m.Length, m.Surface, m.Volume, m.EucDistance, m.PathDistance, m.Branch_Order , m.Contraction, m.Fragmentation, m.Partition_asymmetry, m.Pk_classic, m.Bif_ampl_local, m.Bif_ampl_remote, m.Fractal_Dim FROM persistance_vector p JOIN measurements m on p.neuron_id = m.neuron_id order by neuron_id")
  myresult = mycursor.fetchall()

  vectors = []
  for x in myresult:
    # Slice array to store from third co-efficients
    v = x[4:]
    vectors.append(v)

  # Convert co-efficients to float32
  vectors = np.asarray(vectors).astype('float32')
  mycursor.close()
  mydb.close()

  # Set dimension of vector
  d = 121
  # Build the index
  index = faiss.IndexFlatIP(d)   
  print("Index trained : " + str(index.is_trained))
  # Normalize vectors for indexing (faiss cosine similarity requires normalized vectors)
  normalize_L2(vectors)
  # Add vectors to the index
  index.add(vectors)                  
  print("Number of vectors indexed : " + str(index.ntotal))
  # Write the index to file
  faiss.write_index(index, "nmo_pvec_measurements.index")

main()      