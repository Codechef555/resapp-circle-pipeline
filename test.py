import main
import unittest
from unittest.mock import patch
  # assuming the code is saved in a file named main.py

class TestApp(unittest.TestCase):
     @patch('main.dataConnectivity')
     def test_autofill(self, mock_dataConnectivity):
 # Mocking the database connection
        mock_db = {
            "users": [
                {"name": "Tokyo Mia", "emailId": "wijoba5779@hrisland.com", "description": "TOKYO MIA 3 years of experience in development stage at LTI now looking forward to grab more numerous opportunities in other companies EXPERIENCE 2020-2023 SDE-1, LTI Producing clean, efficient code based on specifications, Testing and deploying programs and systems then further Fixing and improving existing software EDUCATION 2016-2020 B.Tech Computer science , CGPA:9.5 Bs abdur Rahman crescent university SKILLS • Agile methodologies • Major skills in test-driven development • DevOps lifecycle and familiar with AWS tools • Coding languages such as C++, C, JavaScript • Excellent communication skills and Kotlin • ORM and hibernate • Angular and Git • Tools like ansible, Nagios and Kubernetes ACTIVITIES Hockey player at St.Joseph college at kovai 125,kk nagar , chennai · 26633301220 Email : tokyo22@gmail.com"}
            ],
            "jd": [
                {"name": "JD1", "desc": "job openings for : react developer 1 year of experience in work space environment, CGPA:7.0 Qualification : B.Tech major skills in react projects and problem solving python c c++ java html css javascript open to work and flexible timings"}
            ]
        }
        mock_dataConnectivity.return_value = mock_db
        
        # Simulating user selection
        main.users = mock_db["users"]
        main.st.sidebar.radio = lambda label, options: "Tokyo Mia"
        main.st.sidebar.title = lambda title: None
        
        # Creating form fields
        username_box = main.st.empty()
        email_box = main.st.empty()
        resume_box = main.st.empty()
        
        # Calling the autofill function and capturing the returned values
        username_value, email_value, resume_value = main.autofill(username_box, email_box, resume_box, mock_db["users"][0])
        
        # Checking if the returned values match the expected values
        self.assertEqual(username_value, "Tokyo Mia")
        self.assertEqual(email_value, "wijoba5779@hrisland.com")
        self.assertEqual(resume_value, "TOKYO MIA 3 years of experience in development stage at LTI now looking forward to grab more numerous opportunities in other companies EXPERIENCE 2020-2023 SDE-1, LTI Producing clean, efficient code based on specifications, Testing and deploying programs and systems then further Fixing and improving existing software EDUCATION 2016-2020 B.Tech Computer science , CGPA:9.5 Bs abdur Rahman crescent university SKILLS • Agile methodologies • Major skills in test-driven development • DevOps lifecycle and familiar with AWS tools • Coding languages such as C++, C, JavaScript • Excellent communication skills and Kotlin • ORM and hibernate • Angular and Git • Tools like ansible, Nagios and Kubernetes ACTIVITIES Hockey player at St.Joseph college at kovai 125,kk nagar , chennai · 26633301220 Email : tokyo22@gmail.com")

        
     @patch('main.dataConnectivity')
     def test_extract_cgpa(self, mock_dataConnectivity):
        # Testing when CGPA is present
        text = "CGPA: 9.5"
        result = main.extract_cgpa(text)
        self.assertEqual(result, 9.5)
        
        # Testing when CGPA is not present
        text = "Bachelor's degree in Computer Science"
        result = main.extract_cgpa(text)
        self.assertIsNone(result)
        
    # Write more test cases for the other functions and scenarios
    
if __name__ == '__main__':
    unittest.main()
