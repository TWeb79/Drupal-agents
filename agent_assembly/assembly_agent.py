"""
Assembly Agent - Drupal Site Assembly Functions
"""

author = "Inventions4All - github:TWeb79"

import json
import os
import urllib.request
import urllib.error
import base64


def get_drupal_auth(drupal_url: str = None, api_token: str = None,
                   username: str = None, password: str = None) -> tuple:
    """Build authentication headers for Drupal API."""
    if not drupal_url:
        drupal_url = os.environ.get("DRUPAL_BASE_URL")
    
    auth_header = None
    if api_token:
        auth_header = f"Bearer {api_token}"
    elif username and password:
        creds = base64.b64encode(f"{username}:{password}".encode()).decode()
        auth_header = f"Basic {creds}"
    else:
        api_token = os.environ.get("DRUPAL_API_TOKEN")
        if api_token:
            auth_header = f"Bearer {api_token}"
        else:
            username = os.environ.get("DRUPAL_USERNAME")
            password = os.environ.get("DRUPAL_PASSWORD")
            if username and password:
                creds = base64.b64encode(f"{username}:{password}".encode()).decode()
                auth_header = f"Basic {creds}"
    
    if not drupal_url or not auth_header:
        return None, None
    
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
        "Authorization": auth_header,
    }
    
    return drupal_url, headers


def assemble_website(site_config: dict, drupal_url: str = None, 
                     api_token: str = None, username: str = None, 
                     password: str = None) -> dict:
    """
    Assemble complete Drupal website.
    
    Creates content, menu, and configuration entities.
    
    Args:
        site_config: Site configuration with pages, menu, settings
    """
    results = {
        "pages": [],
        "menu": [],
        "config": [],
    }
    
    drupal_url, headers = get_drupal_auth(drupal_url, api_token, username, password)
    
    for page in site_config.get("pages", []):
        result = _create_page(page, drupal_url, headers)
        results["pages"].append(result)
    
    for menu_item in site_config.get("menu", []):
        result = _create_menu_link(menu_item, drupal_url, headers)
        results["menu"].append(result)
    
    return results


def _create_page(page_data: dict, drupal_url: str, headers: dict) -> dict:
    """Create a page via JSON:API."""
    if not drupal_url:
        return {"error": "No Drupal URL configured"}
    
    url = f"{drupal_url}/jsonapi/node/page"
    data = json.dumps({"data": page_data}).encode("utf-8")
    
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:
            return {"status": "success", "response": json.loads(resp.read())}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def _create_menu_link(menu_data: dict, drupal_url: str, headers: dict) -> dict:
    """Create menu link via JSON:API."""
    if not drupal_url:
        return {"error": "No Drupal URL configured"}
    
    url = f"{drupal_url}/jsonapi/menu_link_content/menu_link_content"
    data = json.dumps({"data": menu_data}).encode("utf-8")
    
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:
            return {"status": "success", "response": json.loads(resp.read())}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def generate_sitemap(pages: list) -> dict:
    """Generate site map from page list."""
    return {
        "site": "generated",
        "pages": pages,
        "structure": {
            "main_navigation": [p.get("title") for p in pages if p.get("type") == "page"]
        }
    }