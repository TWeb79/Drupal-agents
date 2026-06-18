"""
Design Agent - Drupal Theme Design Functions
"""

author = "Inventions4All - github:TWeb79"

import base64
import json
import urllib.request
import urllib.error
import os


def get_drupal_auth(drupal_url: str = None, api_token: str = None, 
                   username: str = None, password: str = None) -> tuple:
    """Build authentication headers for Drupal API."""
    if not drupal_url:
        drupal_url = os.environ.get("DRUPAL_BASE_URL")
    
    auth_header = None
    if api_token:
        auth_header = "Bearer " + api_token
    elif username and password:
        creds = base64.b64encode((username + ":" + password).encode()).decode()
        auth_header = "Basic " + creds
    else:
        api_token = os.environ.get("DRUPAL_API_TOKEN")
        if api_token:
            auth_header = "Bearer " + api_token
        else:
            username = os.environ.get("DRUPAL_USERNAME")
            password = os.environ.get("DRUPAL_PASSWORD")
            if username and password:
                creds = base64.b64encode((username + ":" + password).encode()).decode()
                auth_header = "Basic " + creds
    
    if not drupal_url or not auth_header:
        return None, None
    
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
        "Authorization": auth_header,
    }
    
    return drupal_url, headers


def publish_to_drupal(drupal_url: str = None, api_token: str = None, 
                      username: str = None, password: str = None, 
                      payloads: list = None) -> list:
    """Execute JSON:API payloads against a live Drupal site."""
    if payloads is None:
        payloads = []
    
    drupal_url, headers = get_drupal_auth(drupal_url, api_token, username, password)
    
    if not drupal_url or not headers:
        return [{"error": "Drupal authentication not configured"}]
    
    results = []
    for i, payload in enumerate(payloads):
        endpoint = payload.get("endpoint", "")
        url = drupal_url.rstrip('/') + endpoint
        
        try:
            data = json.dumps(payload.get("data", {})).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
                results.append({
                    "step": i + 1,
                    "endpoint": endpoint,
                    "status": "success",
                    "response": result,
                })
        except urllib.error.HTTPError as e:
            results.append({
                "step": i + 1,
                "endpoint": endpoint,
                "status": "error",
                "code": e.code,
                "response": e.read().decode(),
            })
        except Exception as e:
            results.append({
                "step": i + 1,
                "endpoint": endpoint,
                "status": "error",
                "error": str(e),
            })
    
    return results


def generate_theme_files(theme_name: str, design_system: dict) -> dict:
    """Generate Drupal theme file structure."""
    return {
        "files": {
            theme_name + ".info.yml": _generate_info_yml(theme_name),
            theme_name + ".libraries.yml": _generate_libraries_yml(theme_name),
            "css/dist/styles.css": _generate_css_variables(design_system),
        }
    }


def _generate_info_yml(theme_name: str) -> str:
    """Generate theme info.yml content."""
    return "name: " + theme_name.title() + "\ntype: theme\ndescription: 'Custom theme built by AI agent'\ncore_version_requirement: '^11'\npackage: Custom"


def _generate_libraries_yml(theme_name: str) -> str:
    """Generate theme libraries.yml content."""
    return theme_name + ":\n  version: VERSION\n  global-styling:\n    css:\n      theme:\n        css/dist/styles.css: {}"


def _generate_css_variables(design_system: dict) -> str:
    """Generate CSS custom properties from design system."""
    return ":root {\n  --color-primary: #0a0a0a;\n  --color-accent: #d4af37;\n}"