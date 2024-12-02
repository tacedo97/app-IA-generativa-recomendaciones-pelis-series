import requests

def test_correct_login():
    #Checking that the user is able to log correctly in the app 
    url = 'http://localhost:8000/'
    response = requests.get(url)
    assert response.status_code == 200

def test_recommendation_endpoint_empty_query():
    url = 'http://localhost:8000/recommendation_ui'
    user_query = "       "
    response = requests.post(url, data={'user_query': user_query})
    assert response.status_code == 200
    assert "Empty query. Please, include some details in order to be able to recommend you a movie/series based on these details" in response.text

def test_recommendation_endpoint_empty_data():
    url = 'http://localhost:8000/recommendation_ui'
    response = requests.post(url, data={})
    assert response.status_code != 200
    

def test_recommendation_endpoint():
    url = 'http://localhost:8000/recommendation_ui'
    user_query = "I want to watch a Spanish series similar to Stranger Things"
    response = requests.post(url, data={'user_query': user_query})
    assert response.status_code == 200
    assert len(response.content) != 0