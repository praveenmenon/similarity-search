# Similarity Search

The similarity search is a python flask code which uses Facebook's faiss package to find the similarity between neurons using dot product.

# Installation process!

  - download Anaconda 2.7 on the server using the following link. https://www.anaconda.com/distribution/#macos
  - Make sure the mysql is setuo on the server and change the credentials on the code as required for the mysql connection
  - Once anaconda in installed and code is cloned setup the flask app using the following command: export FLASK_APP=flask_similarity.py adn source your bash


Project serup:
  - run all the index.py code.
    Example pthon create_neurites_index.py
  - The above command creates an index file for the given query in the create_neurites_index.py file
  - Finaly run the command to start the server flask run --host=0.0.0.0 &
