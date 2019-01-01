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
detailed_measurements_search_index = faiss.read_index("nmo_detailed_measurements.index")
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
	result["status"] = 200

	return jsonify(result)

@app.route('/similarNeurons/apical/<int:neuron_id>/<int:num_of_neurons>', methods=['GET'])
def get_similar_neurons_measurements_apical(neuron_id,num_of_neurons):
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT neuron_id, Neuron_name, IFNULL(NULLIF(Soma_Surface, '' ), 0) as Soma_Surface, N_stems, N_bifs, N_branch, Width, Height, Depth, Diameter, Length, Surface, Volume, EucDistance, PathDistance, Branch_Order , Contraction, Fragmentation, Partition_asymmetry, Pk_classic, Bif_ampl_local, Bif_ampl_remote, Fractal_Dim FROM measurementsAP where neuron_id = " + str(neuron_id))
	myresult = mycursor.fetchall()
	query_vector = []
	vectors = []

	for x in myresult:
		query_vector.append(x[2:])

	#Check all vectors except Soma_Surface for None value / Null value
	for y in myresult:
		vectors.append(y[3:])
	
	#Iterate the vetors to check if it has None
	result = all(v == None for v in vectors[0])
	print("result:" + str(result))

	if result == True:
		print("true")
		return jsonify({"message": "No Similar Neurons found", "status": 204})

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
	result["status"] = 200

	return jsonify(result)

@app.route('/similarNeurons/axon/<int:neuron_id>/<int:num_of_neurons>', methods=['GET'])
def get_similar_neurons_measurements_axon(neuron_id,num_of_neurons):
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT neuron_id, Neuron_name, IFNULL(NULLIF(Soma_Surface, '' ), 0) as Soma_Surface, N_stems, N_bifs, N_branch, Width, Height, Depth, Diameter, Length, Surface, Volume, EucDistance, PathDistance, Branch_Order , Contraction, Fragmentation, Partition_asymmetry, Pk_classic, Bif_ampl_local, Bif_ampl_remote, Fractal_Dim FROM measurementsAX where neuron_id = " + str(neuron_id))
	myresult = mycursor.fetchall()
	query_vector = []
	vectors = []

	for x in myresult:
		query_vector.append(x[2:])

	#Check all vectors except Soma_Surface for None value / Null value
	for y in myresult:
		vectors.append(y[3:])
	
	#Iterate the vetors to check if it has None
	result = all(v == None for v in vectors[0])
	print("result:" + str(result))

	if result == True:
		print("true")
		return jsonify({"message": "No Similar Neurons found", "status": 204})

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
	result["status"] = 200

	return jsonify(result)

@app.route('/similarNeurons/basal/<int:neuron_id>/<int:num_of_neurons>', methods=['GET'])
def get_similar_neurons_measurements_basal(neuron_id,num_of_neurons):
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT neuron_id, Neuron_name, IFNULL(NULLIF(Soma_Surface, '' ), 0) as Soma_Surface, N_stems, N_bifs, N_branch, Width, Height, Depth, Diameter, Length, Surface, Volume, EucDistance, PathDistance, Branch_Order , Contraction, Fragmentation, Partition_asymmetry, Pk_classic, Bif_ampl_local, Bif_ampl_remote, Fractal_Dim FROM measurementsBS where neuron_id = " + str(neuron_id))
	myresult = mycursor.fetchall()
	query_vector = []
	vectors = []

	for x in myresult:
		query_vector.append(x[2:])

	#Check all vectors except Soma_Surface for None value / Null value
	for y in myresult:
		vectors.append(y[3:])
	
	#Iterate the vetors to check if it has None
	result = all(v == None for v in vectors[0])
	print("result:" + str(result))

	if result == True:
		print("true")
		return jsonify({"message": "No Similar Neurons found", "status": 204})

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
	result["status"] = 200

	return jsonify(result)

@app.route('/similarNeurons/neurites/<int:neuron_id>/<int:num_of_neurons>', methods=['GET'])
def get_similar_neurons_measurements_neurites(neuron_id,num_of_neurons):
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT neuron_id, Neuron_name, IFNULL(NULLIF(Soma_Surface, '' ), 0) as Soma_Surface, N_stems, N_bifs, N_branch, Width, Height, Depth, Diameter, Length, Surface, Volume, EucDistance, PathDistance, Branch_Order , Contraction, Fragmentation, Partition_asymmetry, Pk_classic, Bif_ampl_local, Bif_ampl_remote, Fractal_Dim FROM measurementsNEU where neuron_id = " + str(neuron_id))
	myresult = mycursor.fetchall()
	query_vector = []
	vectors = []

	for x in myresult:
		query_vector.append(x[2:])

	#Check all vectors except Soma_Surface for None value / Null value
	for y in myresult:
		vectors.append(y[3:])
	
	#Iterate the vetors to check if it has None
	result = all(v == None for v in vectors[0])
	print("result:" + str(result))

	if result == True:
		print("true")
		return jsonify({"message": "No Similar Neurons found", "status": 204})

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
	result["status"] = 200

	return jsonify(result)

@app.route('/similarNeurons/processes/<int:neuron_id>/<int:num_of_neurons>', methods=['GET'])
def get_similar_neurons_measurements_processes(neuron_id,num_of_neurons):
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT neuron_id, Neuron_name, IFNULL(NULLIF(Soma_Surface, '' ), 0) as Soma_Surface, N_stems, N_bifs, N_branch, Width, Height, Depth, Diameter, Length, Surface, Volume, EucDistance, PathDistance, Branch_Order , Contraction, Fragmentation, Partition_asymmetry, Pk_classic, Bif_ampl_local, Bif_ampl_remote, Fractal_Dim FROM measurementsPR where neuron_id = " + str(neuron_id))
	myresult = mycursor.fetchall()
	query_vector = []
	vectors = []
	for x in myresult:
		query_vector.append(x[2:])

	#Check all vectors except Soma_Surface for None value / Null value
	for y in myresult:
		vectors.append(y[3:])
	
	#Iterate the vetors to check if it has None
	result = all(v == None for v in vectors[0])
	print("result:" + str(result))

	if result == True:
		print("true")
		return jsonify({"message": "No Similar Neurons found", "status": 204})
	
	result = {}
	s = {}

	# close all database connectivity
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
	result["status"] = 200

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
	result["status"] = 200

	return jsonify(result)

@app.route('/similarNeurons/detailedMorphometry/<int:neuron_id>/<int:num_of_neurons>', methods=['GET'])
def get_similar_neurons_pvec_and_measurements(neuron_id,num_of_neurons):
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="password",database="nmdbDev")
	mycursor = mydb.cursor()
	mycursor.execute("SELECT p.*, IFNULL(NULLIF(m.Soma_Surface, '' ), 0) as Soma_Surface, m.N_stems as M_N_stems, m.N_bifs as M_N_bifs, m.N_branch as M_N_branch, m.Width as M_Width, m.Height as M_Height, m.Depth as M_Depth, m.Diameter as M_Diameter, m.Length as M_Length, m.Surface as M_Surface, m.Volume as M_Volume, m.EucDistance as M_EucDistance, m.PathDistance as M_PathDistance, m.Branch_Order as M_Branch_Order , m.Contraction as M_Contraction, m.Fragmentation as M_Fragmentation, m.Partition_asymmetry as M_Partition_asymmetry, m.Pk_classic as M_Pk_classic, m.Bif_ampl_local as M_Bif_ampl_local, m.Bif_ampl_remote as M_Bif_ampl_remote, m.Fractal_Dim as M_Fractal_Dim,  IFNULL(NULLIF(ap.Soma_Surface, '' ), 0) as AP_Soma_Surface, IFNULL(NULLIF(ap.N_stems, '' ), 0) as AP_N_stems, IFNULL(NULLIF(ap.N_bifs, '' ), 0) as AP_N_bifs, IFNULL(NULLIF(ap.N_branch, '' ), 0) as AP_N_branch, IFNULL(NULLIF(ap.Width, '' ), 0) as AP_Width, IFNULL(NULLIF(ap.Height, '' ), 0) as AP_Height, IFNULL(NULLIF(ap.Depth, '' ), 0) as AP_Depth, IFNULL(NULLIF(ap.Diameter, '' ), 0) as AP_Diameter, IFNULL(NULLIF(ap.Length, '' ), 0) as AP_Length, IFNULL(NULLIF(ap.Surface, '' ), 0) as AP_Surface, IFNULL(NULLIF(ap.Volume, '' ), 0) as AP_Volume, IFNULL(NULLIF(ap.EucDistance, '' ), 0) as AP_EucDistance, IFNULL(NULLIF(ap.PathDistance, '' ), 0) as AP_PathDistance, IFNULL(NULLIF(ap.Branch_Order, '' ), 0) as AP_Branch_Order , IFNULL(NULLIF(ap.Contraction, '' ), 0) as AP_Contraction, IFNULL(NULLIF(ap.Fragmentation, '' ), 0) as AP_Fragmentation, IFNULL(NULLIF(ap.Partition_asymmetry, '' ), 0) as AP_Partition_asymmetry, IFNULL(NULLIF(ap.Pk_classic, '' ), 0) as AP_Pk_classic, IFNULL(NULLIF(ap.Bif_ampl_local, '' ), 0) as AP_Bif_ampl_local, IFNULL(NULLIF(ap.Bif_ampl_remote, '' ), 0) as AP_Bif_ampl_remote, IFNULL(NULLIF(ap.Fractal_Dim, '' ), 0) as AP_Fractal_Dim, IFNULL(NULLIF(ax.Soma_Surface, '' ), 0) as AX_Soma_Surface, IFNULL(NULLIF(ax.N_stems, '' ), 0) as AX_N_stems, IFNULL(NULLIF(ax.N_bifs, '' ), 0) as AX_N_bifs, IFNULL(NULLIF(ax.N_branch, '' ), 0) as AX_N_branch, IFNULL(NULLIF(ax.Width, '' ), 0) as AX_Width, IFNULL(NULLIF(ax.Height, '' ), 0) as AX_Height, IFNULL(NULLIF(ax.Depth, '' ), 0) as AX_Depth, IFNULL(NULLIF(ax.Diameter, '' ), 0) as AX_Diameter, IFNULL(NULLIF(ax.Length, '' ), 0) as AX_Length, IFNULL(NULLIF(ax.Surface, '' ), 0) as AX_Surface, IFNULL(NULLIF(ax.Volume, '' ), 0) as AX_Volume, IFNULL(NULLIF(ax.EucDistance, '' ), 0) as AX_EucDistance, IFNULL(NULLIF(ax.PathDistance, '' ), 0) as AX_PathDistance, IFNULL(NULLIF(ax.Branch_Order, '' ), 0) as AX_Branch_Order , IFNULL(NULLIF(ax.Contraction, '' ), 0) as AX_Contraction, IFNULL(NULLIF(ax.Fragmentation, '' ), 0) as AX_Fragmentation, IFNULL(NULLIF(ax.Partition_asymmetry, '' ), 0) as AX_Partition_asymmetry, IFNULL(NULLIF(ax.Pk_classic, '' ), 0) as AX_Pk_classic, IFNULL(NULLIF(ax.Bif_ampl_local, '' ), 0) as AX_Bif_ampl_local, IFNULL(NULLIF(ax.Bif_ampl_remote, '' ), 0) as AX_Bif_ampl_remote, IFNULL(NULLIF(ax.Fractal_Dim, '' ), 0) as AX_Fractal_Dim, IFNULL(NULLIF(bs.Soma_Surface, '' ), 0) as BS_Soma_Surface, IFNULL(NULLIF(bs.N_stems, '' ), 0) as BS_N_stems, IFNULL(NULLIF(bs.N_bifs, '' ), 0) as BS_N_bifs, IFNULL(NULLIF(bs.N_branch, '' ), 0) as BS_N_branch, IFNULL(NULLIF(bs.Width, '' ), 0) as BS_Width, IFNULL(NULLIF(bs.Height, '' ), 0) as BS_Height, IFNULL(NULLIF(bs.Depth, '' ), 0) as BS_Depth, IFNULL(NULLIF(bs.Diameter, '' ), 0) as BS_Diameter, IFNULL(NULLIF(bs.Length, '' ), 0) as BS_Length, IFNULL(NULLIF(bs.Surface, '' ), 0) as BS_Surface, IFNULL(NULLIF(bs.Volume, '' ), 0) as BS_Volume, IFNULL(NULLIF(bs.EucDistance, '' ), 0) as BS_EucDistance, IFNULL(NULLIF(bs.PathDistance, '' ), 0) as BS_PathDistance, IFNULL(NULLIF(bs.Branch_Order, '' ), 0) as BS_Branch_Order , IFNULL(NULLIF(bs.Contraction, '' ), 0) as BS_Contraction, IFNULL(NULLIF(bs.Fragmentation, '' ), 0) as BS_Fragmentation, IFNULL(NULLIF(bs.Partition_asymmetry, '' ), 0) as BS_Partition_asymmetry, IFNULL(NULLIF(bs.Pk_classic, '' ), 0) as BS_Pk_classic, IFNULL(NULLIF(bs.Bif_ampl_local, '' ), 0) as BS_Bif_ampl_local, IFNULL(NULLIF(bs.Bif_ampl_remote, '' ), 0) as BS_Bif_ampl_remote, IFNULL(NULLIF(bs.Fractal_Dim, '' ), 0) as BS_Fractal_Dim, IFNULL(NULLIF(neu.Soma_Surface, '' ), 0) as NEU_Soma_Surface, IFNULL(NULLIF(neu.N_stems, '' ), 0) as NEU_N_stems, IFNULL(NULLIF(neu.N_bifs, '' ), 0) as NEU_N_bifs, IFNULL(NULLIF(neu.N_branch, '' ), 0) as NEU_N_branch, IFNULL(NULLIF(neu.Width, '' ), 0) as NEU_Width, IFNULL(NULLIF(neu.Height, '' ), 0) as NEU_Height, IFNULL(NULLIF(neu.Depth, '' ), 0) as NEU_Depth, IFNULL(NULLIF(neu.Diameter, '' ), 0) as NEU_Diameter, IFNULL(NULLIF(neu.Length, '' ), 0) as NEU_Length, IFNULL(NULLIF(neu.Surface, '' ), 0) as NEU_Surface, IFNULL(NULLIF(neu.Volume, '' ), 0) as NEU_Volume, IFNULL(NULLIF(neu.EucDistance, '' ), 0) as NEU_EucDistance, IFNULL(NULLIF(neu.PathDistance, '' ), 0) as NEU_PathDistance, IFNULL(NULLIF(neu.Branch_Order, '' ), 0) as NEU_Branch_Order , IFNULL(NULLIF(neu.Contraction, '' ), 0) as NEU_Contraction, IFNULL(NULLIF(neu.Fragmentation, '' ), 0) as NEU_Fragmentation, IFNULL(NULLIF(neu.Partition_asymmetry, '' ), 0) as NEU_Partition_asymmetry, IFNULL(NULLIF(neu.Pk_classic, '' ), 0) as NEU_Pk_classic, IFNULL(NULLIF(neu.Bif_ampl_local, '' ), 0) as NEU_Bif_ampl_local, IFNULL(NULLIF(neu.Bif_ampl_remote, '' ), 0) as NEU_Bif_ampl_remote, IFNULL(NULLIF(neu.Fractal_Dim, '' ), 0) as NEU_Fractal_Dim, IFNULL(NULLIF(pr.Soma_Surface, '' ), 0) as PR_Soma_Surface, IFNULL(NULLIF(pr.N_stems, '' ), 0) as PR_N_stems, IFNULL(NULLIF(pr.N_bifs, '' ), 0) as PR_N_bifs, IFNULL(NULLIF(pr.N_branch, '' ), 0) as PR_N_branch, IFNULL(NULLIF(pr.Width, '' ), 0) as PR_Width, IFNULL(NULLIF(pr.Height, '' ), 0) as PR_Height, IFNULL(NULLIF(pr.Depth, '' ), 0) as PR_Depth, IFNULL(NULLIF(pr.Diameter, '' ), 0) as PR_Diameter, IFNULL(NULLIF(pr.Length, '' ), 0) as PR_Length, IFNULL(NULLIF(pr.Surface, '' ), 0) as PR_Surface, IFNULL(NULLIF(pr.Volume, '' ), 0) as PR_Volume, IFNULL(NULLIF(pr.EucDistance, '' ), 0) as PR_EucDistance, IFNULL(NULLIF(pr.PathDistance, '' ), 0) as PR_PathDistance, IFNULL(NULLIF(pr.Branch_Order, '' ), 0) as PR_Branch_Order , IFNULL(NULLIF(pr.Contraction, '' ), 0) as PR_Contraction, IFNULL(NULLIF(pr.Fragmentation, '' ), 0) as PR_Fragmentation, IFNULL(NULLIF(pr.Partition_asymmetry, '' ), 0) as PR_Partition_asymmetry, IFNULL(NULLIF(pr.Pk_classic, '' ), 0) as PR_Pk_classic, IFNULL(NULLIF(pr.Bif_ampl_local, '' ), 0) as PR_Bif_ampl_local, IFNULL(NULLIF(pr.Bif_ampl_remote, '' ), 0) as PR_Bif_ampl_remote, IFNULL(NULLIF(pr.Fractal_Dim, '' ), 0) as PR_Fractal_Dim  FROM persistance_vector p JOIN measurements m on p.neuron_id  = m.neuron_id  JOIN measurementsAP ap on p.neuron_id = ap.neuron_id JOIN measurementsAX ax on p.neuron_id = ax.neuron_id  JOIN measurementsBS bs on p.neuron_id = bs.neuron_id JOIN measurementsNEU neu on p.neuron_id = neu.neuron_id JOIN measurementsPR pr on p.neuron_id = pr.neuron_id where p.neuron_id = " + str(neuron_id))
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
	D, I = detailed_measurements_search_index.search(query_vector, num_of_neurons+1)

	for index,val in enumerate(I[0][1:]):
		s[neuron_ids[val]] = str(D[0][index+1])

	result["similar_neuron_ids"] = s
	result["status"] = 200

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
	result["status"] = 200

	return jsonify(result)


