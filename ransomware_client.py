"""
Ransomware  API Client

This module provides a comprehensive Python client for interacting with the
ransomware.live API (https://api-pro.ransomware.live). It includes functions
for fetching data about ransomware groups, victims, IOCs, negotiations,
press releases, and more.

The client is designed to be modular and easy to use, with each function
corresponding to a specific API endpoint. All functions include proper
error handling and type hints for better development experience.

Usage:
    from ransomware_client import fetch_stats, fetch_ransomware_groups

    # API_KEY is automatically loaded from .env file
    stats = fetch_stats(API_KEY)
    groups = fetch_ransomware_groups(API_KEY)

For MCP (Model Context Protocol) usage, each function is well-documented
with clear descriptions of parameters, return values, and use cases.

Author: Generated for ransomware.live API integration
Version: 1.0
"""

import requests
from typing import Optional, Dict, Any
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise ValueError("API_KEY not found in environment variables. Please create a .env file with your API key.")
BASE_URL = "https://api-pro.ransomware.live"

def _get(endpoint: str, api_key: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Internal helper function to send GET requests to the ransomware.live API.

    This function handles the common logic for making authenticated requests,
    including setting headers, handling timeouts, and parsing JSON responses.
    It is used by all public functions in this module.

    Args:
        endpoint (str): The API endpoint path (e.g., "/groups").
        api_key (str): The API key for authentication.
        params (Optional[Dict[str, Any]]): Optional query parameters for the request.

    Returns:
        Dict[str, Any]: The parsed JSON response from the API.

    Raises:
        requests.RequestException: If there's a network error or HTTP error (4xx/5xx).
        ValueError: If the response cannot be parsed as valid JSON.
    """
    headers = {
        "Accept": "application/json",
        "X-API-KEY": api_key
    }
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params, timeout=10)
    response.raise_for_status()
    try:
        return response.json()
    except ValueError as e:
        raise ValueError(f"Invalid JSON response: {response.text}") from e

def fetch_ransomware_data(api_key: str, url: str = f"{BASE_URL}/8k") -> dict:
    """
    Fetch general ransomware data from the specified API endpoint.

    This endpoint provides an overview of ransomware incidents. By default, it fetches
    data from the "/8k" endpoint, which typically contains recent or summarized data.
    Can be used to get a snapshot of current ransomware activity.

    Args:
        api_key (str): Your API key for authentication with ransomware.live.
        url (str): The full API endpoint URL. Defaults to the "/8k" endpoint.

    Returns:
        dict: A dictionary containing the JSON response with ransomware data.
              Typically includes incident details, timestamps, and metadata.

    Raises:
        requests.RequestException: If the request fails due to network issues or HTTP errors.
        ValueError: If the API response is not valid JSON.

    Example:
        >>> data = fetch_ransomware_data("your_api_key")
        >>> print(data.keys())
        dict_keys(['data', 'count', ...])
    """
    headers = {
        "Accept": "application/json",
        "X-API-KEY": api_key
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx

    try:
        return response.json()
    except ValueError as e:
        raise ValueError(f"Invalid JSON response: {response.text}") from e

def fetch_csirt_data(country_code: str, api_key: str) -> dict:
    """
    Fetch Computer Security Incident Response Team (CSIRT) data for a specific country.

    This endpoint provides information about CSIRT contacts and resources for handling
    ransomware incidents in the specified country. Useful for incident response coordination.

    Args:
        country_code (str): Two-letter ISO country code (e.g., 'US', 'FR', 'DE').
        api_key (str): Your API key for authentication.

    Returns:
        dict: A dictionary with CSIRT information including contact details,
              response procedures, and country-specific resources.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> csirt = fetch_csirt_data("US", "your_api_key")
        >>> print(csirt.get('country'))
        'US'
    """
    return _get(f"/csirt/{country_code.upper()}", api_key)

def fetch_ransomware_groups(api_key: str) -> dict:
    """
    Fetch the complete list of known ransomware groups.

    This endpoint returns metadata about all ransomware groups tracked by the API,
    including their names, aliases, and basic information. Essential for understanding
    the threat landscape and selecting groups for further analysis.

    Args:
        api_key (str): Your API key for authentication.

    Returns:
        dict: A dictionary containing a list of ransomware groups with their details.
              Typically includes fields like 'name', 'aliases', 'first_seen', etc.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> groups = fetch_ransomware_groups("your_api_key")
        >>> print(f"Total groups: {len(groups.get('data', []))}")
        Total groups: 284
    """
    return _get("/groups", api_key)

def fetch_group_data(group_name: str, api_key: str) -> dict:
    """
    Fetch detailed information about a specific ransomware group.

    This endpoint provides comprehensive data about a particular ransomware group,
    including their tactics, techniques, procedures (TTPs), known victims, and more.
    Useful for in-depth analysis of a specific threat actor.

    Args:
        group_name (str): The name of the ransomware group (case-insensitive).
        api_key (str): Your API key for authentication.

    Returns:
        dict: A dictionary with detailed group information including description,
              aliases, first/last seen dates, attack patterns, and statistics.

    Raises:
        requests.RequestException: If the request fails (e.g., group not found).
        ValueError: If the response is not valid JSON.

    Example:
        >>> group = fetch_group_data("lockbit", "your_api_key")
        >>> print(group.get('name'))
        'LockBit'
    """
    return _get(f"/groups/{group_name.lower()}", api_key)

def fetch_iocs(api_key: str, ioc_type: Optional[str] = None) -> dict:
    """
    Fetch Indicators of Compromise (IOCs) from the ransomware.live API.

    IOCs include IP addresses, domains, file hashes, and other indicators associated
    with ransomware activity. This endpoint can return all IOCs or filter by type.

    Args:
        api_key (str): Your API key for authentication.
        ioc_type (Optional[str]): Type of IOC to filter by. Valid values include
            'domain', 'ip', 'hash', 'email', etc. If None, returns all IOCs.

    Returns:
        dict: A dictionary containing IOC data with fields like 'type', 'value',
              'group', 'first_seen', 'last_seen', etc.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> iocs = fetch_iocs("your_api_key", "domain")
        >>> print(f"Domain IOCs: {len(iocs.get('data', []))}")
    """
    endpoint = f"/iocs/{ioc_type}" if ioc_type else "/iocs"
    return _get(endpoint, api_key)

def fetch_group_iocs(group: str, api_key: str, ioc_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch IOCs specific to a particular ransomware group.

    This endpoint provides IOCs associated with a specific ransomware group,
    which can be filtered by IOC type. Useful for targeted threat hunting.

    Args:
        group (str): Name of the ransomware group (case-insensitive).
        api_key (str): Your API key for authentication.
        ioc_type (Optional[str]): Type of IOC to filter by (e.g., 'domain', 'ip').

    Returns:
        Dict[str, Any]: A dictionary with IOCs for the specified group.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> iocs = fetch_group_iocs("akira", "your_api_key", "domain")
        >>> print(iocs.get('group'))
        'Akira'
    """
    params = {"type": ioc_type} if ioc_type else None
    return _get(f"/iocs/{group}", api_key, params)

def get_akira_iocs(api_key: str, group_name: str) -> dict:
    """
    Fetch IOCs for the Akira ransomware group or related groups.

    This is a specialized endpoint for Akira IOCs, which may include additional
    parameters for filtering by related groups or campaigns.

    Args:
        api_key (str): Your API key for authentication.
        group_name (str): The ransomware group name to filter IOCs.

    Returns:
        dict: A dictionary containing Akira-related IOCs.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> iocs = get_akira_iocs("your_api_key", "akira")
        >>> print(len(iocs.get('data', [])))
    """
    params = {"group_name": group_name}
    return _get("/iocs/akira", api_key, params)

def fetch_sectors(api_key: str) -> Dict[str, Any]:
    """
    Fetch the list of industry sectors affected by ransomware.

    This endpoint provides statistics on ransomware attacks by industry sector,
    helping to identify which sectors are most targeted.

    Args:
        api_key (str): Your API key for authentication.

    Returns:
        Dict[str, Any]: A dictionary with sector data including names and victim counts.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> sectors = fetch_sectors("your_api_key")
        >>> print(f"Sectors: {sectors.get('count')}")
    """
    return _get("/listsectors", api_key)

def fetch_negotiations(api_key: str) -> Dict[str, Any]:
    """
    Fetch data on ongoing or completed ransomware negotiations.

    This endpoint provides information about ransom negotiations between victims
    and ransomware groups, including amounts, status, and timelines.

    Args:
        api_key (str): Your API key for authentication.

    Returns:
        Dict[str, Any]: A dictionary with negotiation data including victim details,
                        ransom amounts, and negotiation status.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> negotiations = fetch_negotiations("your_api_key")
        >>> print(f"Ongoing negotiations: {len(negotiations.get('data', []))}")
    """
    return _get("/negotiations", api_key)

def fetch_negotiation_group_chats(group: str, api_key: str) -> Dict[str, Any]:
    """
    Fetch metadata for all negotiation chats for a specific ransomware group.

    This endpoint lists all negotiation conversations for a group, providing
    an overview of their negotiation activities.

    Args:
        group (str): Name of the ransomware group.
        api_key (str): Your API key for authentication.

    Returns:
        Dict[str, Any]: A dictionary with chat metadata including chat IDs,
                        victim info, and timestamps.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> chats = fetch_negotiation_group_chats("lockbit", "your_api_key")
        >>> print(chats.get('group'))
        'LockBit'
    """
    return _get(f"/negotiations/{group}", api_key)

def fetch_negotiation_chat_detail(group: str, chat_id: str, api_key: str) -> Dict[str, Any]:
    """
    Fetch detailed messages and ransom information for a specific negotiation chat.

    This endpoint provides the full conversation transcript and ransom details
    for a particular negotiation, offering insights into negotiation tactics.

    Args:
        group (str): Name of the ransomware group.
        chat_id (str): Unique identifier for the negotiation chat.
        api_key (str): Your API key for authentication.

    Returns:
        Dict[str, Any]: A dictionary with chat messages, ransom amounts,
                        and negotiation details.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> chat = fetch_negotiation_chat_detail("lockbit", "chat123", "your_api_key")
        >>> print(chat.get('messages', []))
    """
    return _get(f"/negotiations/{group}/{chat_id}", api_key)

def fetch_press_releases(api_key: str, year: int, month: int, country: str) -> Dict[str, Any]:
    """
    Fetch press releases for ransomware incidents in a specific year, month, and country.

    This endpoint provides official press releases about ransomware attacks,
    useful for understanding incident impact and response.

    Args:
        api_key (str): Your API key for authentication.
        year (int): Year to filter press releases (e.g., 2024).
        month (int): Month to filter press releases (1-12).
        country (str): Two-letter country code (e.g., 'US').

    Returns:
        Dict[str, Any]: A dictionary with press release data including titles,
                        dates, and content summaries.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> press = fetch_press_releases("your_api_key", 2024, 9, "US")
        >>> print(f"Press releases: {len(press.get('data', []))}")
    """
    params = {
        "year": year,
        "month": f"{month:02d}",  # zero-padded month
        "country": country
    }
    return _get("/press/all", api_key, params)

def fetch_recent_press(api_key: str, country: str) -> Dict[str, Any]:
    """
    Fetch recent press releases for a specific country.

    This endpoint provides the most recent press releases about ransomware
    incidents in the specified country.

    Args:
        api_key (str): Your API key for authentication.
        country (str): Two-letter country code (e.g., 'FR').

    Returns:
        Dict[str, Any]: A dictionary with recent press release data.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> press = fetch_recent_press("your_api_key", "US")
        >>> print(press.get('country'))
        'US'
    """
    params = {"country": country}
    return _get("/press/recent", api_key, params)

def fetch_victims(
    api_key: str,
    group: str,
    sector: str,
    country: str,
    year: int,
    month: int
) -> Dict[str, Any]:
    """
    Fetch victim data filtered by multiple criteria.

    This endpoint provides detailed information about ransomware victims based on
    specific filters. All parameters are required for this endpoint.

    Args:
        api_key (str): Your API key for authentication.
        group (str): Ransomware group name (e.g., 'lockbit').
        sector (str): Industry sector (e.g., 'healthcare').
        country (str): Two-letter country code (e.g., 'US').
        year (int): Year of the incident (e.g., 2024).
        month (int): Month of the incident (1-12).

    Returns:
        Dict[str, Any]: A dictionary with victim data including company names,
                        attack dates, ransom amounts, and impact details.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> victims = fetch_victims("your_api_key", "lockbit", "healthcare", "US", 2024, 9)
        >>> print(f"Victims: {len(victims.get('data', []))}")
    """
    params = {
        "group": group,
        "sector": sector,
        "country": country,
        "year": year,
        "month": f"{month:02d}"  # zero-padded month
    }
    return _get("/victims/", api_key, params)

def fetch_recent_victims(api_key: str, order: str = "discovered") -> Dict[str, Any]:
    """
    Fetch recent victim data ordered by discovery or attack date.

    This endpoint provides the most recent ransomware victims, useful for
    monitoring current threats.

    Args:
        api_key (str): Your API key for authentication.
        order (str): Ordering criterion. Must be 'discovered' or 'attacked'.

    Returns:
        Dict[str, Any]: A dictionary with recent victim data.

    Raises:
        ValueError: If the 'order' parameter is invalid.
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> victims = fetch_recent_victims("your_api_key", "attacked")
        >>> print(f"Recent victims: {len(victims.get('data', []))}")
    """
    valid_orders = {"discovered", "attacked"}
    if order not in valid_orders:
        raise ValueError(f"Invalid order value: {order}. Must be one of {valid_orders}.")
    params = {"order": order}
    return _get("/victims/recent", api_key, params)

def search_victims(api_key: str, group: str, sector: str, country: str) -> Dict[str, Any]:
    """
    Search for victims using flexible criteria.

    This endpoint allows searching victims by group, sector, and country,
    providing more flexibility than the strict fetch_victims endpoint.

    Args:
        api_key (str): Your API key for authentication.
        group (str): Ransomware group name.
        sector (str): Industry sector.
        country (str): Two-letter country code.

    Returns:
        Dict[str, Any]: A dictionary with matching victim data.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> victims = search_victims("your_api_key", "akira", "healthcare", "US")
        >>> print(victims.get('count'))
    """
    params = {
        "group": group,
        "sector": sector,
        "country": country
    }
    return _get("/victims/search", api_key, params)

def fetch_all_victims(api_key: str) -> Dict[str, Any]:
    """
    Attempt to fetch all victim data without filters.

    Note: This endpoint may not return all victims due to API limitations.
    For comprehensive data, use filtered endpoints like fetch_victims or search_victims.

    Args:
        api_key (str): Your API key for authentication.

    Returns:
        Dict[str, Any]: A dictionary with victim data (may be empty or limited).

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> victims = fetch_all_victims("your_api_key")
        >>> print(f"All victims: {len(victims.get('data', []))}")
    """
    return _get("/victims/search", api_key, {})

def fetch_recent_victims(api_key: str, order: str = "discovered") -> Dict[str, Any]:
    """
    Fetch recent victim data from the ransomware.live API, ordered by a given criterion.

    Args:
        api_key (str): Your API key for authentication.
        order (str): Ordering criterion. Can be 'discovered' or 'attacked'.

    Returns:
        dict: Parsed JSON response.

    Raises:
        ValueError: If the 'order' parameter is invalid.
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.
    """
    valid_orders = {"discovered", "attacked"}
    if order not in valid_orders:
        raise ValueError(f"Invalid order value: {order}. Must be one of {valid_orders}.")
    params = {"order": order}
    return _get("/victims/recent", api_key, params)

def fetch_all_victims(api_key: str) -> Dict[str, Any]:
    """
    Fetch all victim data from the ransomware.live API.

    Args:
        api_key (str): Your API key for authentication.

    Returns:
        dict: Parsed JSON response.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.
    """
    return _get("/victims/search", api_key, {})

def fetch_ransomnote_groups(api_key: str) -> Dict[str, Any]:
    """
    Fetch the list of ransomware groups that have ransom notes available.

    This endpoint provides an overview of groups for which ransom note samples
    are available in the database.

    Args:
        api_key (str): Your API key for authentication.

    Returns:
        Dict[str, Any]: A dictionary with groups that have ransom notes.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> groups = fetch_ransomnote_groups("your_api_key")
        >>> print(f"Groups with notes: {len(groups.get('data', []))}")
    """
    return _get("/ransomnotes", api_key)

def fetch_ransomnote_group_list(group: str, api_key: str) -> Dict[str, Any]:
    """
    Fetch the list of ransom note filenames for a specific group.

    This endpoint lists all available ransom note files for a particular
    ransomware group.

    Args:
        group (str): Name of the ransomware group.
        api_key (str): Your API key for authentication.

    Returns:
        Dict[str, Any]: A dictionary with filenames of ransom notes.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> notes = fetch_ransomnote_group_list("lockbit", "your_api_key")
        >>> print(notes.get('filenames', []))
    """
    return _get(f"/ransomnotes/{group}", api_key)

def fetch_ransomnote_detail(group: str, note_name: str, api_key: str) -> Dict[str, Any]:
    """
    Fetch the full content of a specific ransom note.

    This endpoint provides the complete text content of a ransom note,
    useful for analysis of ransom demands and communication patterns.

    Args:
        group (str): Name of the ransomware group.
        note_name (str): Filename of the ransom note.
        api_key (str): Your API key for authentication.

    Returns:
        Dict[str, Any]: A dictionary with the ransom note content and metadata.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> note = fetch_ransomnote_detail("lockbit", "README.txt", "your_api_key")
        >>> print(note.get('content'))
    """
    return _get(f"/ransomnotes/{group}/{note_name}", api_key)

def fetch_stats(api_key: str) -> Dict[str, Any]:
    """
    Fetch overall statistics about the ransomware database.

    This endpoint provides summary statistics including total victims,
    groups, press releases, and other metrics.

    Args:
        api_key (str): Your API key for authentication.

    Returns:
        Dict[str, Any]: A dictionary with various statistics and counts.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> stats = fetch_stats("your_api_key")
        >>> print(f"Total victims: {stats.get('stats', {}).get('victims')}")
    """
    return _get("/stats", api_key)

def validate_api_key(api_key: str) -> Dict[str, Any]:
    """
    Validate the provided API key.

    This endpoint checks if the API key is valid and returns information
    about the associated account.

    Args:
        api_key (str): The API key to validate.

    Returns:
        Dict[str, Any]: A dictionary with validation status and user information.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> validation = validate_api_key("your_api_key")
        >>> print(validation.get('status'))
        'valid'
    """
    return _get("/validate", api_key)

def fetch_single_victim(victim_id: str, api_key: str) -> Dict[str, Any]:
    """
    Fetch detailed information about a specific victim.

    This endpoint provides enriched data about a single victim identified
    by their unique ID.

    Args:
        victim_id (str): Unique identifier for the victim.
        api_key (str): Your API key for authentication.

    Returns:
        Dict[str, Any]: A dictionary with detailed victim information.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> victim = fetch_single_victim("victim123", "your_api_key")
        >>> print(victim.get('company_name'))
    """
    return _get(f"/victim/{victim_id}", api_key)

def fetch_yara_rules_list(api_key: str) -> Dict[str, Any]:
    """
    Fetch the list of ransomware groups with available YARA rules.

    YARA rules are used for detecting malware signatures. This endpoint
    lists groups for which detection rules are available.

    Args:
        api_key (str): Your API key for authentication.

    Returns:
        Dict[str, Any]: A dictionary with groups and their YARA rule counts.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> yara = fetch_yara_rules_list("your_api_key")
        >>> print(f"Groups with YARA: {len(yara.get('groups', []))}")
    """
    return _get("/yara", api_key)

def fetch_yara_rules_detail(group: str, api_key: str) -> Dict[str, Any]:
    """
    Fetch YARA rules for a specific ransomware group.

    This endpoint provides the actual YARA rule content for detecting
    malware associated with a particular group.

    Args:
        group (str): Name of the ransomware group.
        api_key (str): Your API key for authentication.

    Returns:
        Dict[str, Any]: A dictionary with YARA rule content and metadata.

    Raises:
        requests.RequestException: If the request fails.
        ValueError: If the response is not valid JSON.

    Example:
        >>> rules = fetch_yara_rules_detail("lockbit", "your_api_key")
        >>> print(rules.get('rules', []))
    """
    return _get(f"/yara/{group}", api_key)

if __name__ == "__main__":
    """
    Main execution block for scraping ransomware data.

    This section demonstrates how to use the API client to fetch various
    types of data from ransomware.live. It creates a 'scraped_data' directory
    and saves all retrieved data as JSON files for analysis.

    The scraper performs the following operations:
    1. Validates the API key
    2. Fetches general statistics
    3. Retrieves the list of ransomware groups
    4. Gets sector information
    5. Fetches recent victims
    6. Retrieves all victims (if available)
    7. Gets negotiation data
    8. Fetches YARA rules list
    9. For the first group, fetches detailed data and IOCs

    All data is saved to JSON files in the 'scraped_data/' directory.
    """
    # Create output directory
    output_dir = "scraped_data"
    os.makedirs(output_dir, exist_ok=True)

    # Example usage: Scrape general data
    try:
        print("Validating API key...")
        validate = validate_api_key(API_KEY)
        print("API Key valid:", validate)
        with open(f"{output_dir}/validate.json", "w") as f:
            json.dump(validate, f, indent=4)

        print("\nFetching stats...")
        stats = fetch_stats(API_KEY)
        print("Stats:", stats)
        with open(f"{output_dir}/stats.json", "w") as f:
            json.dump(stats, f, indent=4)

        print("\nFetching ransomware groups...")
        groups = fetch_ransomware_groups(API_KEY)
        groups_data = groups.get('data') or groups.get('groups', [])
        print("Groups count:", len(groups_data))
        with open(f"{output_dir}/groups.json", "w") as f:
            json.dump(groups, f, indent=4)

        print("\nFetching sectors...")
        sectors = fetch_sectors(API_KEY)
        print("Sectors:", sectors)
        with open(f"{output_dir}/sectors.json", "w") as f:
            json.dump(sectors, f, indent=4)

        print("\nFetching recent victims...")
        recent_victims = fetch_recent_victims(API_KEY, order="attacked")
        victims_data = recent_victims.get('data') or recent_victims.get('victims', [])
        print("Recent victims count:", len(victims_data))
        with open(f"{output_dir}/recent_victims.json", "w") as f:
            json.dump(recent_victims, f, indent=4)

        print("\nFetching all victims...")
        all_victims = fetch_all_victims(API_KEY)
        print("All victims count:", len(all_victims.get('data', [])))
        with open(f"{output_dir}/all_victims.json", "w") as f:
            json.dump(all_victims, f, indent=4)

        print("\nFetching negotiations...")
        negotiations = fetch_negotiations(API_KEY)
        print("Negotiations count:", len(negotiations.get('data', [])))
        with open(f"{output_dir}/negotiations.json", "w") as f:
            json.dump(negotiations, f, indent=4)

        print("\nFetching YARA rules list...")
        yara_list = fetch_yara_rules_list(API_KEY)
        print("YARA groups:", yara_list)
        with open(f"{output_dir}/yara_list.json", "w") as f:
            json.dump(yara_list, f, indent=4)

        # Example for specific group
        if 'data' in groups and groups['data']:
            group_name = groups['data'][0]['name'].lower()
            print(f"\nFetching data for group: {group_name}")
            group_data = fetch_group_data(group_name, API_KEY)
            print("Group data keys:", list(group_data.keys()))
            with open(f"{output_dir}/group_{group_name}.json", "w") as f:
                json.dump(group_data, f, indent=4)

            # Fetch IOCs for the group
            print(f"Fetching IOCs for group: {group_name}")
            group_iocs = fetch_group_iocs(group_name, API_KEY)
            print("IOCs count:", len(group_iocs.get('data', [])))
            with open(f"{output_dir}/iocs_{group_name}.json", "w") as f:
                json.dump(group_iocs, f, indent=4)

        print(f"\nScraping complete. Data saved to {output_dir}/")

    except Exception as e:
        print(f"Error: {e}")
