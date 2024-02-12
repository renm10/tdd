"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from counter import app 

# we need to import the file that contains the status codes
from src import status 

class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update the counter"""
        client = self.client

        #Creating the Counter
        createCounter = client.post('/counters/update_counter')
        self.assertEqual(createCounter.status_code, status.HTTP_201_CREATED)

        #Baseline Value
        baselineValue = createCounter.json["update_counter"]

        #Update Counter
        update_counter = client.put('/counters/update_counter')
        self.assertEqual(update_counter.status_code, status.HTTP_200_OK)
        
        #Grab Updated value
        updatedValue = update_counter.json["update_counter"]

        #Compare value with base line value
        self.assertEqual(updatedValue, baselineValue + 1)

    def test_read_a_counter(self):
        """ It should read from the counter """
        client = self.client

        #Creating the counter
        createCounter = client.post('/counters/read_counter')
        self.assertEqual(createCounter.status_code, status.HTTP_201_CREATED)

        #Update Counter
        update_counter = client.put('/counters/read_counter')
        self.assertEqual(update_counter.status_code, status.HTTP_200_OK)

        #Check value stored in the counter
        readCounterValue = client.get('/counters/read_counter').text

        #Check if it is equal to the updated value
        self.assertEqual(int(readCounterValue), update_counter.json["read_counter"]) #Change returned string to int

    def test_delete_a_counter(self):
        """ It should delete a counter """
        client = self.client

        #Creating the counter
        createCounter = client.post('/counters/delete_counter')
        self.assertEqual(createCounter.status_code, status.HTTP_201_CREATED)

        #Delete Counter
        deleteCounter = client.delete('/counters/delete_counter')
        self.assertEqual(deleteCounter.status_code, status.HTTP_204_NO_CONTENT)

        #Try deleting one more time  (Counter does not exist because deleted already)
        deleteCounter = client.delete('/counters/delete_counter')
        self.assertEqual(deleteCounter.status_code, status.HTTP_404_NOT_FOUND)