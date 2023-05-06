import unittest
from unittest.mock import patch
import app  # assuming the code is saved in a file named main.py

class TestApp(unittest.TestCase):
    @patch('main.dataConnectivity')
    def test_autofill(self, mock_dataConnectivity):
        # Mocking the database connection
        mock_db = {
            "users": [
                {"name": "John Doe", "emailId": "john@example.com", "description": "Sample resume"}
            ],
            "jd": [
                {"name": "Job Description 1", "desc": "Sample job description"}
            ]
        }
        mock_dataConnectivity.return_value = mock_db
        
        # Simulating user selection
        app.users = mock_db["users"]
        app.st.sidebar.radio = lambda label, options: "John Doe"
        app.st.sidebar.title = lambda title: None
        
        # Creating form fields
        username_box = app.st.empty()
        email_box = app.st.empty()
        resume_box = app.st.empty()
        
        # Calling the autofill function
        app.autofill(username_box, email_box, resume_box, mock_db["users"][0])
        
        # Checking if the form fields are autofilled correctly
        self.assertEqual(username_box.text_input("Username", value=""), "John Doe")
        self.assertEqual(email_box.text_input("Email", value=""), "john@example.com")
        self.assertEqual(resume_box.text_area("Resume", value="", height=200), "Sample resume")
        
    @patch('main.dataConnectivity')
    def test_extract_cgpa(self, mock_dataConnectivity):
        # Testing when CGPA is present
        text = "CGPA: 3.5"
        result = app.extract_cgpa(text)
        self.assertEqual(result, 3.5)
        
        # Testing when CGPA is not present
        text = "Bachelor's degree in Computer Science"
        result = app.extract_cgpa(text)
        self.assertIsNone(result)
        
    # Write more test cases for the other functions and scenarios
    
if __name__ == '__main__':
    unittest.main()
