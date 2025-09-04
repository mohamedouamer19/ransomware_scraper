"""
MCP Server for Ransomware.live API Client

This MCP server exposes all functions from the ransomware_client.py module
as MCP tools, allowing AI assistants to interact with the ransomware.live API
through the Model Context Protocol.

The server provides tools for:
- Fetching ransomware groups, victims, IOCs
- Retrieving statistics and negotiations
- Accessing press releases and ransom notes
- Validating API keys and more

Usage:
    python mcp_server_ransomware.py

Author: Generated for MCP integration with ransomware.live API
Version: 1.0
"""

import sys
import os
from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, Any
import requests
import json

# Import all functions from ransomware_client
from ransomware_client import (
    API_KEY, BASE_URL,
    _get,
    fetch_ransomware_data,
    fetch_csirt_data,
    fetch_ransomware_groups,
    fetch_group_data,
    fetch_iocs,
    fetch_group_iocs,
    get_akira_iocs,
    fetch_sectors,
    fetch_negotiations,
    fetch_negotiation_group_chats,
    fetch_negotiation_chat_detail,
    fetch_press_releases,
    fetch_recent_press,
    fetch_victims,
    fetch_recent_victims,
    search_victims,
    fetch_all_victims,
    fetch_ransomnote_groups,
    fetch_ransomnote_group_list,
    fetch_ransomnote_detail,
    fetch_stats,
    validate_api_key,
    fetch_single_victim,
    fetch_yara_rules_list,
    fetch_yara_rules_detail
)

# Initialize MCP server
mcp = FastMCP("ransomware-api-server", host="0.0.0.0", port=23001)

# Tool definitions for all ransomware client functions

@mcp.tool()
def fetch_ransomware_data_tool(url: str) -> Dict[str, Any]:
    """
    Fetch general ransomware data from the specified API endpoint.

    This endpoint provides an overview of ransomware incidents. By default, it fetches
    data from the "/8k" endpoint, which typically contains recent or summarized data.
    Can be used to get a snapshot of current ransomware activity.

    Args:
        url (str): The full API endpoint URL. Use "/8k" for default data.

    Returns:
        Dict[str, Any]: A dictionary containing the JSON response with ransomware data.
    """
    return fetch_ransomware_data(API_KEY, url)

@mcp.tool()
def fetch_csirt_data_tool(country_code: str) -> Dict[str, Any]:
    """
    Fetch Computer Security Incident Response Team (CSIRT) data for a specific country.

    Args:
        country_code (str): Two-letter ISO country code (e.g., 'US', 'FR', 'DE').

    Returns:
        Dict[str, Any]: A dictionary with CSIRT information.
    """
    return fetch_csirt_data(country_code, API_KEY)

@mcp.tool()
def fetch_ransomware_groups_tool() -> Dict[str, Any]:
    """
    Fetch the complete list of known ransomware groups.

    Returns:
        Dict[str, Any]: A dictionary containing a list of ransomware groups with their details.
    """
    return fetch_ransomware_groups(API_KEY)

@mcp.tool()
def fetch_group_data_tool(group_name: str) -> Dict[str, Any]:
    """
    Fetch detailed information about a specific ransomware group.

    Args:
        group_name (str): The name of the ransomware group (case-insensitive).

    Returns:
        Dict[str, Any]: A dictionary with detailed group information.
    """
    return fetch_group_data(group_name, API_KEY)

@mcp.tool()
def fetch_iocs_tool(ioc_type: str = "") -> Dict[str, Any]:
    """
    Fetch Indicators of Compromise (IOCs) from the ransomware.live API.

    Args:
        ioc_type (str): Type of IOC to filter by (e.g., 'domain', 'ip', 'hash'). Use empty string for all.

    Returns:
        Dict[str, Any]: A dictionary containing IOC data.
    """
    if ioc_type == "":
        ioc_type = None
    return fetch_iocs(API_KEY, ioc_type)

@mcp.tool()
def fetch_group_iocs_tool(group: str, ioc_type: str = "") -> Dict[str, Any]:
    """
    Fetch IOCs specific to a particular ransomware group.

    Args:
        group (str): Name of the ransomware group (case-insensitive).
        ioc_type (str): Type of IOC to filter by. Use empty string for all.

    Returns:
        Dict[str, Any]: A dictionary with IOCs for the specified group.
    """
    if ioc_type == "":
        ioc_type = None
    return fetch_group_iocs(group, API_KEY, ioc_type)

@mcp.tool()
def get_akira_iocs_tool(group_name: str) -> Dict[str, Any]:
    """
    Fetch IOCs for the Akira ransomware group or related groups.

    Args:
        group_name (str): The ransomware group name to filter IOCs.

    Returns:
        Dict[str, Any]: A dictionary containing Akira-related IOCs.
    """
    return get_akira_iocs(API_KEY, group_name)

@mcp.tool()
def fetch_sectors_tool() -> Dict[str, Any]:
    """
    Fetch the list of industry sectors affected by ransomware.

    Returns:
        Dict[str, Any]: A dictionary with sector data.
    """
    return fetch_sectors(API_KEY)

@mcp.tool()
def fetch_negotiations_tool() -> Dict[str, Any]:
    """
    Fetch data on ongoing or completed ransomware negotiations.

    Returns:
        Dict[str, Any]: A dictionary with negotiation data.
    """
    return fetch_negotiations(API_KEY)

@mcp.tool()
def fetch_negotiation_group_chats_tool(group: str) -> Dict[str, Any]:
    """
    Fetch metadata for all negotiation chats for a specific ransomware group.

    Args:
        group (str): Name of the ransomware group.

    Returns:
        Dict[str, Any]: A dictionary with chat metadata.
    """
    return fetch_negotiation_group_chats(group, API_KEY)

@mcp.tool()
def fetch_negotiation_chat_detail_tool(group: str, chat_id: str) -> Dict[str, Any]:
    """
    Fetch detailed messages and ransom information for a specific negotiation chat.

    Args:
        group (str): Name of the ransomware group.
        chat_id (str): Unique identifier for the negotiation chat.

    Returns:
        Dict[str, Any]: A dictionary with chat messages and ransom details.
    """
    return fetch_negotiation_chat_detail(group, chat_id, API_KEY)

@mcp.tool()
def fetch_press_releases_tool(year: int, month: int, country: str) -> Dict[str, Any]:
    """
    Fetch press releases for ransomware incidents in a specific year, month, and country.

    Args:
        year (int): Year to filter press releases.
        month (int): Month to filter press releases (1-12).
        country (str): Two-letter country code.

    Returns:
        Dict[str, Any]: A dictionary with press release data.
    """
    return fetch_press_releases(API_KEY, year, month, country)

@mcp.tool()
def fetch_recent_press_tool(country: str) -> Dict[str, Any]:
    """
    Fetch recent press releases for a specific country.

    Args:
        country (str): Two-letter country code.

    Returns:
        Dict[str, Any]: A dictionary with recent press release data.
    """
    return fetch_recent_press(API_KEY, country)

@mcp.tool()
def fetch_victims_tool(
    group: str,
    sector: str,
    country: str,
    year: int,
    month: int
) -> Dict[str, Any]:
    """
    Fetch victim data filtered by multiple criteria.

    Args:
        group (str): Ransomware group name.
        sector (str): Industry sector.
        country (str): Two-letter country code.
        year (int): Year of the incident.
        month (int): Month of the incident (1-12).

    Returns:
        Dict[str, Any]: A dictionary with victim data.
    """
    return fetch_victims(API_KEY, group, sector, country, year, month)

@mcp.tool()
def fetch_recent_victims_tool(order: str) -> Dict[str, Any]:
    """
    Fetch recent victim data ordered by discovery or attack date.

    Args:
        order (str): Ordering criterion ('discovered' or 'attacked').

    Returns:
        Dict[str, Any]: A dictionary with recent victim data.
    """
    return fetch_recent_victims(API_KEY, order)

@mcp.tool()
def search_victims_tool(group: str, sector: str, country: str) -> Dict[str, Any]:
    """
    Search for victims using flexible criteria.

    Args:
        group (str): Ransomware group name.
        sector (str): Industry sector.
        country (str): Two-letter country code.

    Returns:
        Dict[str, Any]: A dictionary with matching victim data.
    """
    return search_victims(API_KEY, group, sector, country)

@mcp.tool()
def fetch_all_victims_tool() -> Dict[str, Any]:
    """
    Attempt to fetch all victim data without filters.

    Returns:
        Dict[str, Any]: A dictionary with victim data.
    """
    return fetch_all_victims(API_KEY)

@mcp.tool()
def fetch_ransomnote_groups_tool() -> Dict[str, Any]:
    """
    Fetch the list of ransomware groups that have ransom notes available.

    Returns:
        Dict[str, Any]: A dictionary with groups that have ransom notes.
    """
    return fetch_ransomnote_groups(API_KEY)

@mcp.tool()
def fetch_ransomnote_group_list_tool(group: str) -> Dict[str, Any]:
    """
    Fetch the list of ransom note filenames for a specific group.

    Args:
        group (str): Name of the ransomware group.

    Returns:
        Dict[str, Any]: A dictionary with filenames of ransom notes.
    """
    return fetch_ransomnote_group_list(group, API_KEY)

@mcp.tool()
def fetch_ransomnote_detail_tool(group: str, note_name: str) -> Dict[str, Any]:
    """
    Fetch the full content of a specific ransom note.

    Args:
        group (str): Name of the ransomware group.
        note_name (str): Filename of the ransom note.

    Returns:
        Dict[str, Any]: A dictionary with the ransom note content.
    """
    return fetch_ransomnote_detail(group, note_name, API_KEY)

@mcp.tool()
def fetch_stats_tool() -> Dict[str, Any]:
    """
    Fetch overall statistics about the ransomware database.

    Returns:
        Dict[str, Any]: A dictionary with various statistics.
    """
    return fetch_stats(API_KEY)

@mcp.tool()
def validate_api_key_tool() -> Dict[str, Any]:
    """
    Validate the API key from the environment.

    Returns:
        Dict[str, Any]: A dictionary with validation status.
    """
    return validate_api_key(API_KEY)

@mcp.tool()
def fetch_single_victim_tool(victim_id: str) -> Dict[str, Any]:
    """
    Fetch detailed information about a specific victim.

    Args:
        victim_id (str): Unique identifier for the victim.

    Returns:
        Dict[str, Any]: A dictionary with detailed victim information.
    """
    return fetch_single_victim(victim_id, API_KEY)

@mcp.tool()
def fetch_yara_rules_list_tool() -> Dict[str, Any]:
    """
    Fetch the list of ransomware groups with available YARA rules.

    Returns:
        Dict[str, Any]: A dictionary with groups and their YARA rule counts.
    """
    return fetch_yara_rules_list(API_KEY)

@mcp.tool()
def fetch_yara_rules_detail_tool(group: str) -> Dict[str, Any]:
    """
    Fetch YARA rules for a specific ransomware group.

    Args:
        group (str): Name of the ransomware group.

    Returns:
        Dict[str, Any]: A dictionary with YARA rule content.
    """
    return fetch_yara_rules_detail(group, API_KEY)

if __name__ == "__main__":
    print("Starting MCP Server for Ransomware.live API...")
    print("Available tools:")
    for tool_name in [
        "fetch_ransomware_data_tool", "fetch_csirt_data_tool", "fetch_ransomware_groups_tool",
        "fetch_group_data_tool", "fetch_iocs_tool", "fetch_group_iocs_tool", "get_akira_iocs_tool",
        "fetch_sectors_tool", "fetch_negotiations_tool", "fetch_negotiation_group_chats_tool",
        "fetch_negotiation_chat_detail_tool", "fetch_press_releases_tool", "fetch_recent_press_tool",
        "fetch_victims_tool", "fetch_recent_victims_tool", "search_victims_tool", "fetch_all_victims_tool",
        "fetch_ransomnote_groups_tool", "fetch_ransomnote_group_list_tool", "fetch_ransomnote_detail_tool",
        "fetch_stats_tool", "validate_api_key_tool", "fetch_single_victim_tool",
        "fetch_yara_rules_list_tool", "fetch_yara_rules_detail_tool"
    ]:
        print(f"  - {tool_name}")
    print("\nServer running on http://0.0.0.0:23001")
    mcp.run(transport="sse")
