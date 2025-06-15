"""
Base Library for API Test Automation Framework
"""
import requests
import allure
import json
from config.settings import URLs

class BaseLibrary:
    """
    Base library class that provides core HTTP request functionality
    """
    @allure.step("{url_path} GET request is sent")
    def get(self, url_path, query_params=None):
        """
        Sends a GET request to the specified URL
        """
        allure.attach(f"GET Request URL: {url_path}", 
                     name="Request URL", 
                     attachment_type=allure.attachment_type.TEXT)
        if query_params:
            allure.attach(json.dumps(query_params, indent=2), 
                         name="Query Parameters", 
                         attachment_type=allure.attachment_type.JSON)
            response = requests.get(url_path, params=query_params)
        else:
            response = requests.get(url_path)
        
        allure.attach(f"Response Status Code: {response.status_code}", 
                     name="Response Status", 
                     attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, 
                     name="Response Body", 
                     attachment_type=allure.attachment_type.JSON)
        print(f"GET Request URL: {url_path}")
        print(f"GET Response: {response.text}")
        return response

    @allure.step("{url_path} POST request is sent")
    def post(self, url_path, body_payload, headers_payload):
        """
        Sends a POST request to the specified URL
        """
        allure.attach(f"POST Request URL: {url_path}", 
                     name="Request URL", 
                     attachment_type=allure.attachment_type.TEXT)
        allure.attach(json.dumps(body_payload, indent=2), 
                     name="Request Body", 
                     attachment_type=allure.attachment_type.JSON)
        allure.attach(json.dumps(headers_payload, indent=2), 
                     name="Request Headers", 
                     attachment_type=allure.attachment_type.JSON)
        
        response = requests.post(url_path, json=body_payload, headers=headers_payload)
        
        allure.attach(f"Response Status Code: {response.status_code}", 
                     name="Response Status", 
                     attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, 
                     name="Response Body", 
                     attachment_type=allure.attachment_type.JSON)
        print(f"POST Request URL: {url_path}")
        print(f"POST Request Body: {json.dumps(body_payload, indent=2)}")
        print(f"POST Response: {response.text}")
        return response

    @allure.step("{url_path} PUT request is sent")
    def put(self, url_path, body_payload, headers_payload):
        """
        Sends a PUT request to the specified URL
        """
        allure.attach(f"PUT Request URL: {url_path}", 
                     name="Request URL", 
                     attachment_type=allure.attachment_type.TEXT)
        allure.attach(json.dumps(body_payload, indent=2), 
                     name="Request Body", 
                     attachment_type=allure.attachment_type.JSON)
        allure.attach(json.dumps(headers_payload, indent=2), 
                     name="Request Headers", 
                     attachment_type=allure.attachment_type.JSON)
        
        response = requests.put(url_path, json=body_payload, headers=headers_payload)
        
        allure.attach(f"Response Status Code: {response.status_code}", 
                     name="Response Status", 
                     attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, 
                     name="Response Body", 
                     attachment_type=allure.attachment_type.JSON)
        print(f"PUT Request URL: {url_path}")
        print(f"PUT Request Body: {json.dumps(body_payload, indent=2)}")
        print(f"PUT Response: {response.text}")
        return response

    @allure.step("{url_path} DELETE request is sent")
    def delete(self, url_path):
        """
        Sends a DELETE request to the specified URL
        """
        allure.attach(f"DELETE Request URL: {url_path}", 
                     name="Request URL", 
                     attachment_type=allure.attachment_type.TEXT)
        
        response = requests.delete(url_path)
        
        allure.attach(f"Response Status Code: {response.status_code}", 
                     name="Response Status", 
                     attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, 
                     name="Response Body", 
                     attachment_type=allure.attachment_type.JSON)
        print(f"DELETE Request URL: {url_path}")
        print(f"DELETE Response: {response.text}")
        return response

    @allure.step("Assertion check is performed")
    def assert_equals(self, actual, expected):
        """
        Performs an equality assertion between actual and expected values
        """
        assert actual == expected, f"Expected {expected} but got {actual}" 