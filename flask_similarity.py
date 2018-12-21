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
	mycursor.execute("SELECT * FROM measurements where neuron_id = " + str(neuron_id))
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


