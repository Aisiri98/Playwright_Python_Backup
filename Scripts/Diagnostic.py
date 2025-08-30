#!/usr/bin/env python3
"""
Jira Diagnostic Script
Run this to diagnose and fix Jira integration issues
"""

import os
import sys
import requests
import base64
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class JiraDiagnostic:
    def __init__(self):
        self.jira_url = os.getenv('JIRA_URL')
        self.email = os.getenv('JIRA_EMAIL')
        self.api_token = os.getenv('JIRA_API_TOKEN')
        self.project_key = os.getenv('JIRA_PROJECT_KEY')

        if not all([self.jira_url, self.email, self.api_token]):
            print("❌ Missing required environment variables:")
            print("   - JIRA_URL")
            print("   - JIRA_EMAIL")
            print("   - JIRA_API_TOKEN")
            print("   - JIRA_PROJECT_KEY")
            sys.exit(1)

        # Create auth header
        auth_string = f"{self.email}:{self.api_token}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')

        self.headers = {
            'Authorization': f'Basic {auth_b64}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def test_connection(self):
        """Test basic connection to Jira"""
        print("🔍 Testing Jira connection...")
        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/myself",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                user_info = response.json()
                print(
                    f"✅ Connected successfully as: {user_info.get('displayName', 'Unknown')} ({user_info.get('emailAddress', 'No email')})")
                return True
            else:
                print(f"❌ Connection failed: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def list_projects(self):
        """List all available projects"""
        print("\n🔍 Fetching available projects...")
        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/project",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                projects = response.json()
                print(f"✅ Found {len(projects)} projects:")
                print("\nProject Key | Project Name | Type")
                print("-" * 50)
                for project in projects:
                    print(f"{project['key']:11} | {project['name'][:25]:25} | {project.get('projectTypeKey', 'N/A')}")
                return projects
            else:
                print(f"❌ Failed to fetch projects: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            print(f"❌ Error fetching projects: {e}")
            return []

    def validate_project(self, project_key=None):
        """Validate specific project"""
        key = project_key or self.project_key
        if not key:
            print("❌ No project key provided")
            return False

        print(f"\n🔍 Validating project: {key}")
        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/project/{key}",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                project = response.json()
                print(f"✅ Project '{key}' is valid:")
                print(f"   Name: {project.get('name')}")
                print(f"   Type: {project.get('projectTypeKey')}")
                print(f"   Lead: {project.get('lead', {}).get('displayName', 'Unknown')}")
                return True
            elif response.status_code == 404:
                print(f"❌ Project '{key}' not found")
                return False
            else:
                print(f"❌ Project validation failed: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"❌ Error validating project: {e}")
            return False

    def get_issue_types(self, project_key=None):
        """Get available issue types for project"""
        key = project_key or self.project_key
        if not key:
            print("❌ No project key provided")
            return []

        print(f"\n🔍 Fetching issue types for project: {key}")
        try:
            response = requests.get(
                f"{self.jira_url}/rest/api/3/issue/createmeta",
                headers=self.headers,
                params={"projectKeys": key, "expand": "projects.issuetypes"},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if data['projects']:
                    issue_types = data['projects'][0]['issuetypes']
                    print(f"✅ Available issue types:")
                    for it in issue_types:
                        print(f"   - {it['name']} (ID: {it['id']})")
                    return issue_types
                else:
                    print(f"❌ No projects found in createmeta response")
                    return []
            else:
                print(f"❌ Failed to fetch issue types: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            print(f"❌ Error fetching issue types: {e}")
            return []

    def test_create_issue(self, project_key=None):
        """Test creating a sample issue"""
        key = project_key or self.project_key
        if not key:
            print("❌ No project key provided")
            return False

        print(f"\n🔍 Testing issue creation in project: {key}")

        # Get issue types first
        issue_types = self.get_issue_types(key)
        if not issue_types:
            print("❌ Cannot create issue without valid issue types")
            return False

        # Use first available issue type
        issue_type = issue_types[0]

        issue_data = {
            "fields": {
                "project": {"key": key},
                "summary": "[TEST] Diagnostic test issue - Please ignore",
                "description": "This is a test issue created by the Jira diagnostic script. You can safely delete this.",
                "issuetype": {"name": issue_type['name']},
                "labels": ["diagnostic-test", "automated-test"]
            }
        }

        try:
            response = requests.post(
                f"{self.jira_url}/rest/api/3/issue",
                headers=self.headers,
                data=json.dumps(issue_data),
                timeout=30
            )

            if response.status_code == 201:
                issue_key = response.json()['key']
                print(f"✅ Successfully created test issue: {issue_key}")
                print(f"   You can view it at: {self.jira_url}/browse/{issue_key}")

                # Optionally delete the test issue
                delete = input("\n❓ Delete the test issue? (y/N): ").lower().strip()
                if delete == 'y':
                    self.delete_issue(issue_key)

                return True
            else:
                print(f"❌ Failed to create test issue: {response.status_code}")
                print(f"   Response: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Error creating test issue: {e}")
            return False

    def delete_issue(self, issue_key):
        """Delete a test issue"""
        try:
            response = requests.delete(
                f"{self.jira_url}/rest/api/3/issue/{issue_key}",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 204:
                print(f"✅ Successfully deleted test issue: {issue_key}")
            else:
                print(f"❌ Failed to delete test issue: {response.status_code}")

        except Exception as e:
            print(f"❌ Error deleting test issue: {e}")

    def run_full_diagnostic(self):
        """Run complete diagnostic"""
        print("🚀 Starting Jira Integration Diagnostic\n")
        print(f"Jira URL: {self.jira_url}")
        print(f"Email: {self.email}")
        print(f"Project Key: {self.project_key}")
        print("=" * 50)

        # Test connection
        if not self.test_connection():
            print("\n❌ Cannot proceed without valid connection")
            return False

        # List all projects
        projects = self.list_projects()

        # Validate current project
        project_valid = False
        if self.project_key:
            project_valid = self.validate_project()

        if not project_valid and projects:
            print(f"\n❓ Current project key '{self.project_key}' is invalid.")
            print("Available projects:")
            for i, project in enumerate(projects[:10]):  # Show first 10
                print(f"  {i + 1}. {project['key']} - {project['name']}")

            try:
                choice = input("\nEnter project number to test (or 'q' to quit): ").strip()
                if choice.lower() == 'q':
                    return False

                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(projects):
                    selected_project = projects[choice_idx]['key']
                    print(f"\n📝 Testing with project: {selected_project}")

                    # Update environment suggestion
                    print(f"\n💡 Update your .env file with:")
                    print(f"JIRA_PROJECT_KEY={selected_project}")

                    # Validate and test selected project
                    if self.validate_project(selected_project):
                        self.get_issue_types(selected_project)
                        return self.test_create_issue(selected_project)

            except (ValueError, IndexError):
                print("❌ Invalid selection")
                return False

        elif project_valid:
            # Test issue types and creation
            self.get_issue_types()
            return self.test_create_issue()

        return False


def main():
    diagnostic = JiraDiagnostic()
    success = diagnostic.run_full_diagnostic()

    if success:
        print("\n🎉 Jira integration is working correctly!")
        print("You can now run your Playwright tests with Jira integration.")
    else:
        print("\n❌ Jira integration needs configuration.")
        print("Please fix the issues above and try again.")


if __name__ == "__main__":
    main()