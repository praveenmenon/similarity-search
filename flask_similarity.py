import mysql.connector
import numpy as np
import faiss
from flask import Flask
from faiss import normalize_L2
from flask import jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
# Set the database parameters to connect

neuron_ids = {}
measurements_neuron_ids = {}
search_index = faiss.read_index("nmo_pvecs.index")
measurements_search_index = faiss.read_index("nmo_measurements.index")
pvec_measurements_search_index = faiss.read_index("nmo_pvec_measurements.index")
apical_measurements_search_index = faiss.read_index("nmo_measurements_apical.index")
axon_measurements_search_index = faiss.read_index("nmo_measurements_axon.index")
basal_measurements_search_index = faiss.read_index("nmo_measurements_basal.index")
neurites_measurements_search_index = faiss.read_index("nmo_measurements_neurites.index")
processes_measurements_search_index = faiss.read_index("nmo_measurements_processes.index")

@app.before_first_request
def init_neuron_ids():
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT neuron_id FROM persistance_vector order by neuron_id")
	myresult = mycursor.fetchall()

	mycursor.execute("SELECT neuron_id FROM measurements order by neuron_id")
	measurementsResults = mycursor.fetchall()

	for index,neuron_id in enumerate(measurementsResults):
		measurements_neuron_ids[index] = neuron_id[0]

	for index,neuron_id in enumerate(myresult):
		neuron_ids[index] = neuron_id[0]

	mycursor.close()
	mydb.close()

@app.route('/', methods=['GET'])
def get():
	return "similarity search main route"

@app.route('/similarNeurons/measurements/<int:neuron_id>/<int:num_of_neurons>', methods=['GET'])
def get_similar_neurons_measurements(neuron_id,num_of_neurons):
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT neuron_id, Neuron_name, IFNULL(NULLIF(Soma_Surface, '' ), 0) as Soma_Surface, N_stems, N_bifs, N_branch, Width, Height, Depth, Diameter, Length, Surface, Volume, EucDistance, PathDistance, Branch_Order , Contraction, Fragmentation, Partition_asymmetry, Pk_classic, Bif_ampl_local, Bif_ampl_remote, Fractal_Dim FROM measurements where neuron_id = " + str(neuron_id))
	myresult = mycursor.fetchall()
	query_vector = []
	for x in myresult:
		query_vector.append(x[2:])	
	result = {}
	s = {}
	mycursor.close()
	mydb.close()

	# Normalize the query vector before searching (for cosine inner product search)
	query_vector = np.asarray(query_vector).astype('float32')
	normalize_L2(query_vector)
	
	# Actual Search
	D, I = measurements_search_index.search(query_vector, num_of_neurons+1)

	for index,val in enumerate(I[0][1:]):
		s[neuron_ids[val]] = str(D[0][index+1])

	result["similar_neuron_ids"] = s

	return jsonify(result)

@app.route('/similarNeurons/apical/<int:neuron_id>/<int:num_of_neurons>', methods=['GET'])
def get_similar_neurons_measurements_apical(neuron_id,num_of_neurons):
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT neuron_id, Neuron_name, IFNULL(NULLIF(Soma_Surface, '' ), 0) as Soma_Surface, N_stems, N_bifs, N_branch, Width, Height, Depth, Diameter, Length, Surface, Volume, EucDistance, PathDistance, Branch_Order , Contraction, Fragmentation, Partition_asymmetry, Pk_classic, Bif_ampl_local, Bif_ampl_remote, Fractal_Dim FROM measurementsAP where neuron_id = " + str(neuron_id))
	myresult = mycursor.fetchall()
	query_vector = []
	for x in myresult:
		query_vector.append(x[2:])	
	result = {}
	s = {}
	mycursor.close()
	mydb.close()

	# Normalize the query vector before searching (for cosine inner product search)
	query_vector = np.asarray(query_vector).astype('float32')
	normalize_L2(query_vector)
	
	# Actual Search
	D, I = apical_measurements_search_index.search(query_vector, num_of_neurons+1)

	for index,val in enumerate(I[0][1:]):
		s[neuron_ids[val]] = str(D[0][index+1])

	result["similar_neuron_ids"] = s

	return jsonify(result)

@app.route('/similarNeurons/axon/<int:neuron_id>/<int:num_of_neurons>', methods=['GET'])
def get_similar_neurons_measurements_axon(neuron_id,num_of_neurons):
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT neuron_id, Neuron_name, IFNULL(NULLIF(Soma_Surface, '' ), 0) as Soma_Surface, N_stems, N_bifs, N_branch, Width, Height, Depth, Diameter, Length, Surface, Volume, EucDistance, PathDistance, Branch_Order , Contraction, Fragmentation, Partition_asymmetry, Pk_classic, Bif_ampl_local, Bif_ampl_remote, Fractal_Dim FROM measurementsAX where neuron_id = " + str(neuron_id))
	myresult = mycursor.fetchall()
	query_vector = []
	for x in myresult:
		query_vector.append(x[2:])	
	result = {}
	s = {}
	mycursor.close()
	mydb.close()

	# Normalize the query vector before searching (for cosine inner product search)
	query_vector = np.asarray(query_vector).astype('float32')
	normalize_L2(query_vector)
	
	# Actual Search
	D, I = axon_measurements_search_index.search(query_vector, num_of_neurons+1)

	for index,val in enumerate(I[0][1:]):
		s[neuron_ids[val]] = str(D[0][index+1])

	result["similar_neuron_ids"] = s

	return jsonify(result)

@app.route('/similarNeurons/basal/<int:neuron_id>/<int:num_of_neurons>', methods=['GET'])
def get_similar_neurons_measurements_basal(neuron_id,num_of_neurons):
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT neuron_id, Neuron_name, IFNULL(NULLIF(Soma_Surface, '' ), 0) as Soma_Surface, N_stems, N_bifs, N_branch, Width, Height, Depth, Diameter, Length, Surface, Volume, EucDistance, PathDistance, Branch_Order , Contraction, Fragmentation, Partition_asymmetry, Pk_classic, Bif_ampl_local, Bif_ampl_remote, Fractal_Dim FROM measurementsBS where neuron_id = " + str(neuron_id))
	myresult = mycursor.fetchall()
	query_vector = []
	for x in myresult:
		query_vector.append(x[2:])	
	result = {}
	s = {}
	mycursor.close()
	mydb.close()

	# Normalize the query vector before searching (for cosine inner product search)
	query_vector = np.asarray(query_vector).astype('float32')
	normalize_L2(query_vector)
	
	# Actual Search
	D, I = basal_measurements_search_index.search(query_vector, num_of_neurons+1)

	for index,val in enumerate(I[0][1:]):
		s[neuron_ids[val]] = str(D[0][index+1])

	result["similar_neuron_ids"] = s

	return jsonify(result)

@app.route('/similarNeurons/neurites/<int:neuron_id>/<int:num_of_neurons>', methods=['GET'])
def get_similar_neurons_measurements_neurites(neuron_id,num_of_neurons):
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT neuron_id, Neuron_name, IFNULL(NULLIF(Soma_Surface, '' ), 0) as Soma_Surface, N_stems, N_bifs, N_branch, Width, Height, Depth, Diameter, Length, Surface, Volume, EucDistance, PathDistance, Branch_Order , Contraction, Fragmentation, Partition_asymmetry, Pk_classic, Bif_ampl_local, Bif_ampl_remote, Fractal_Dim FROM measurementsNEU where neuron_id = " + str(neuron_id))
	myresult = mycursor.fetchall()
	query_vector = []
	for x in myresult:
		query_vector.append(x[2:])	
	result = {}
	s = {}
	mycursor.close()
	mydb.close()

	# Normalize the query vector before searching (for cosine inner product search)
	query_vector = np.asarray(query_vector).astype('float32')
	normalize_L2(query_vector)
	
	# Actual Search
	D, I = neurites_measurements_search_index.search(query_vector, num_of_neurons+1)

	for index,val in enumerate(I[0][1:]):
		s[neuron_ids[val]] = str(D[0][index+1])

	result["similar_neuron_ids"] = s

	return jsonify(result)

@app.route('/similarNeurons/processes/<int:neuron_id>/<int:num_of_neurons>', methods=['GET'])
def get_similar_neurons_measurements_processes(neuron_id,num_of_neurons):
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT neuron_id, Neuron_name, IFNULL(NULLIF(Soma_Surface, '' ), 0) as Soma_Surface, N_stems, N_bifs, N_branch, Width, Height, Depth, Diameter, Length, Surface, Volume, EucDistance, PathDistance, Branch_Order , Contraction, Fragmentation, Partition_asymmetry, Pk_classic, Bif_ampl_local, Bif_ampl_remote, Fractal_Dim FROM measurementsPR where neuron_id = " + str(neuron_id))
	myresult = mycursor.fetchall()
	query_vector = []
	for x in myresult:
		query_vector.append(x[2:])	
	result = {}
	s = {}
	mycursor.close()
	mydb.close()

	# Normalize the query vector before searching (for cosine inner product search)
	query_vector = np.asarray(query_vector).astype('float32')
	normalize_L2(query_vector)
	
	# Actual Search
	D, I = processes_measurements_search_index.search(query_vector, num_of_neurons+1)

	for index,val in enumerate(I[0][1:]):
		s[neuron_ids[val]] = str(D[0][index+1])

	result["similar_neuron_ids"] = s

	return jsonify(result)

@app.route('/similarNeurons/<int:neuron_id>/<int:num_of_neurons>', methods=['GET'])
def get_similar_neurons(neuron_id,num_of_neurons):
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT * FROM persistance_vector where neuron_id = " + str(neuron_id))
	myresult = mycursor.fetchall()
	query_vector = []
	for x in myresult:
		query_vector.append(x[4:])	
	result = {}
	s = {}
	mycursor.close()
	mydb.close()

	# Normalize the query vector before searching (for cosine inner product search)
	query_vector = np.asarray(query_vector).astype('float32')
	normalize_L2(query_vector)
	
	# Actual Search
	D, I = search_index.search(query_vector, num_of_neurons+1)

	for index,val in enumerate(I[0][1:]):
		s[neuron_ids[val]] = str(D[0][index+1])

	result["similar_neuron_ids"] = s

	return jsonify(result)

@app.route('/similarNeurons/pvecAndMeasurements/<int:neuron_id>/<int:num_of_neurons>', methods=['GET'])
def get_similar_neurons_pvec_and_measurements(neuron_id,num_of_neurons):
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT p.*, IFNULL(NULLIF(m.Soma_Surface, '' ), 0) as Soma_Surface, m.N_stems, m.N_bifs, m.N_branch, m.Width, m.Height, m.Depth, m.Diameter, m.Length, m.Surface, m.Volume, m.EucDistance, m.PathDistance, m.Branch_Order , m.Contraction, m.Fragmentation, m.Partition_asymmetry, m.Pk_classic, m.Bif_ampl_local, m.Bif_ampl_remote, m.Fractal_Dim FROM persistance_vector p JOIN measurements m on p.neuron_id = m.neuron_id where p.neuron_id = " + str(neuron_id))
	myresult = mycursor.fetchall()
	query_vector = []
	for x in myresult:
		query_vector.append(x[4:])	
	result = {}
	s = {}
	mycursor.close()
	mydb.close()

	# Normalize the query vector before searching (for cosine inner product search)
	query_vector = np.asarray(query_vector).astype('float32')
	normalize_L2(query_vector)
	
	# Actual Search
	D, I = pvec_measurements_search_index.search(query_vector, num_of_neurons+1)

	for index,val in enumerate(I[0][1:]):
		s[neuron_ids[val]] = str(D[0][index+1])

	result["similar_neuron_ids"] = s

	return jsonify(result)


