import os
import requests
import base64
import json
from datetime import datetime
from typing import Optional, Dict, Any


class JiraIntegration:
    def __init__(self):
        self.jira_url = os.getenv('JIRA_URL', 'https://your-domain.atlassian.net')
        self.email = os.getenv('JIRA_EMAIL')
        self.api_token = os.getenv('JIRA_API_TOKEN')
        self.project_key = os.getenv('JIRA_PROJECT_KEY', 'TEST')

        # Validate configuration
        self._validate_config()

        # Create auth header
        auth_string = f"{self.email}:{self.api_token}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')

        self.headers = {
            'Authorization': f'Basic {auth_b64}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def _validate_config(self):
        """Validate Jira configuration"""
        if not all([self.jira_url, self.email, self.api_token, self.project_key]):
            raise ValueError(
                "Missing required Jira configuration. Check JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, and JIRA_PROJECT_KEY")

        # Test connection and validate project
        if not self._test_connection():
            raise ConnectionError("Failed to connect to Jira. Check your credentials and URL.")

        if not self._validate_project():
            available_projects = self._get_available_projects()
            raise ValueError(f"Project '{self.project_key}' not found. Available projects: {available_projects}")

    def _test_connection(self) -> bool:
        """Test Jira connection"""
        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/myself",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    def _validate_project(self) -> bool:
        """Validate if project exists and is accessible"""
        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/project/{self.project_key}",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Project validation failed: {e}")
            return False

    def _get_available_projects(self) -> list:
        """Get list of available projects"""
        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/project",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                projects = response.json()
                return [f"{p['key']} ({p['name']})" for p in projects]
            return []
        except Exception:
            return []

    def get_issue_types(self, project_key: str = None) -> list:
        """Get available issue types for the project"""
        project = project_key or self.project_key
        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/issue/createmeta",
                headers=self.headers,
                params={"projectKeys": project, "expand": "projects.issuetypes"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data['projects']:
                    issue_types = data['projects'][0]['issuetypes']
                    return [{"name": it['name'], "id": it['id']} for it in issue_types]
            return []
        except Exception as e:
            print(f"Failed to get issue types: {e}")
            return []

    def create_bug_ticket(self, test_name: str, error_message: str,
                          test_file: str, screenshot_path: Optional[str] = None) -> Optional[str]:
        """Create a bug ticket in Jira for failed test"""

        # Get available issue types to use the correct one
        issue_types = self.get_issue_types()
        bug_issue_type = None

        # Try to find Bug, Task, or Story issue type
        for issue_type in issue_types:
            if issue_type['name'].lower() in ['bug', 'defect']:
                bug_issue_type = {"name": issue_type['name']}
                break
            elif issue_type['name'].lower() in ['task', 'story']:
                bug_issue_type = {"name": issue_type['name']}

        if not bug_issue_type:
            # Fallback to first available issue type
            if issue_types:
                bug_issue_type = {"name": issue_types[0]['name']}
            else:
                print("No issue types found for project")
                return None

        description = f"""
*Test Failure Report*

*Test Name:* {test_name}
*Test File:* {test_file}
*Timestamp:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

*Error Message:*
{{code}}
{error_message}
{{code}}

*Additional Information:*
- Browser: Chrome/Firefox/Safari
- Environment: Test Environment
- Automated Test: Yes
        """.strip()

        issue_data = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": f"[Automated Test] {test_name} - Test Failure",
                "description": description,
                "issuetype": bug_issue_type,
                "labels": ["automated-test", "playwright", "test-failure"]
            }
        }

        # Add priority if it exists in the project
        try:
            priority_response = requests.get(
                f"{self.jira_url}/rest/api/3/priority",
                headers=self.headers
            )
            if priority_response.status_code == 200:
                priorities = priority_response.json()
                medium_priority = next((p for p in priorities if p['name'].lower() == 'medium'), None)
                if medium_priority:
                    issue_data["fields"]["priority"] = {"name": "Medium"}
        except Exception:
            pass  # Skip priority if not available

        try:
            response = requests.post(
                f"{self.jira_url}/rest/api/3/issue",
                headers=self.headers,
                data=json.dumps(issue_data),
                timeout=30
            )

            if response.status_code == 201:
                issue_key = response.json()['key']
                print(f"Created Jira ticket: {issue_key}")

                # Attach screenshot if provided
                if screenshot_path and os.path.exists(screenshot_path):
                    self.attach_file(issue_key, screenshot_path)

                return issue_key
            else:
                print(f"Failed to create Jira ticket: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"Error creating Jira ticket: {str(e)}")
            return None

    def attach_file(self, issue_key: str, file_path: str) -> bool:
        """Attach a file to a Jira issue"""
        try:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                headers = {'Authorization': self.headers['Authorization']}

                response = requests.post(
                    f"{self.jira_url}/rest/api/3/issue/{issue_key}/attachments",
                    headers=headers,
                    files=files
                )

                return response.status_code == 200
        except Exception as e:
            print(f"Error attaching file: {str(e)}")
            return False

    def update_test_execution(self, test_case_key: str, status: str,
                              execution_comment: str = "") -> bool:
        """Update test execution status in Jira (for Xray or Zephyr)"""
        # This is for Xray integration
        execution_data = {
            "testExecutionKey": test_case_key,
            "status": status,
            "comment": execution_comment,
            "executedOn": datetime.now().isoformat()
        }

        try:
            response = requests.post(
                f"{self.jira_url}/rest/raven/1.0/api/testexec",
                headers=self.headers,
                data=json.dumps(execution_data)
            )

            return response.status_code == 200
        except Exception as e:
            print(f"Error updating test execution: {str(e)}")
            return False

    def search_existing_bug(self, test_name: str) -> Optional[str]:
        """Search for existing bug tickets for the same test"""
        jql = f'project = "{self.project_key}" AND summary ~ "{test_name}" AND status != "Done" AND labels = "automated-test"'

        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/search",
                headers=self.headers,
                params={'jql': jql, 'maxResults': 1}
            )

            if response.status_code == 200:
                issues = response.json().get('issues', [])
                if issues:
                    return issues[0]['key']
            return None
        except Exception as e:
            print(f"Error searching for existing bugs: {str(e)}")
            return None