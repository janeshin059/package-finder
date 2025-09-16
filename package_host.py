import requests
import json
import sys

# ==============================================================================
# Settings: Enter your API key and Console URL here.
# ==============================================================================
PRISMA_CLOUD_BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiamFzaGluQHBhbG9hbHRvbmV0d29ya3MuY29tIiwicm9sZSI6ImFkbWluIiwicm9sZVBlcm1zIjpbWzI1NSwyNTUsMjU1LDI1NSwyNTUsOTVdLFsyNTUsMjU1LDI1NSwyNTUsMjU1LDk1XV0sInNlc3Npb25UaW1lb3V0U2VjIjo2MDAsInNhYXNUb2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUo5LmV5SnpkV0lpT2lKcVlYTm9hVzVBY0dGc2IyRnNkRzl1WlhSM2IzSnJjeTVqYjIwaUxDSnpaWEoyYVdObFZYTmhaMlZQYm14NUlqcDBjblZsTENKbWFYSnpkRXh2WjJsdUlqcG1ZV3h6WlN3aWNISnBjMjFoU1dRaU9pSXhNak13T0RBeU56YzJPVFk1T1RRNU1UZzBJaXdpYVhCQlpHUnlaWE56SWpvaU16UXVPRGN1TVRNM0xqRTBNU0lzSW1semN5STZJbWgwZEhCek9pOHZZWEJwTG5ObkxuQnlhWE50WVdOc2IzVmtMbWx2SWl3aWNtVnpkSEpwWTNRaU9qQXNJblZ6WlhKU2IyeGxWSGx3WlVSbGRHRnBiSE1pT25zaWFHRnpUMjVzZVZKbFlXUkJZMk5sYzNNaU9tWmhiSE5sZlN3aWRYTmxjbEp2YkdWVWVYQmxUbUZ0WlNJNklsTjVjM1JsYlNCQlpHMXBiaUlzSW1selUxTlBVMlZ6YzJsdmJpSTZabUZzYzJVc0lteGhjM1JNYjJkcGJsUnBiV1VpT2pFM05UZ3dNemN5T1RnME5UWXNJbUYxWkNJNkltaDBkSEJ6T2k4dllYQnBMbk5uTG5CeWFYTnRZV05zYjNWa0xtbHZJaXdpZFhObGNsSnZiR1ZVZVhCbFNXUWlPakVzSW1GMWRHZ3RiV1YwYUc5a0lqb2lVRUZUVTFkUFVrUWlMQ0p6Wld4bFkzUmxaRU4xYzNSdmJXVnlUbUZ0WlNJNklreGxaVWhoYms1VElFTnZjbkF1SUMwZ05qZzJOelE1TURZd09ERTNOVEExTmpJMk1pSXNJbk5sYzNOcGIyNVVhVzFsYjNWMElqb3pNREFzSW5WelpYSlNiMnhsU1dRaU9pSmtaakJoWVROaU1DMWpZemc0TFRRM05UY3RZVGN5WlMwM05UaGhPV1F4TmpjellqUWlMQ0pvWVhORVpXWmxibVJsY2xCbGNtMXBjM05wYjI1eklqcDBjblZsTENKbGVIQWlPakUzTlRnd016Z3lNRElzSW1saGRDSTZNVGMxT0RBek56WXdNaXdpZFhObGNtNWhiV1VpT2lKcVlYTm9hVzVBY0dGc2IyRnNkRzl1WlhSM2IzSnJjeTVqYjIwaUxDSjFjMlZ5VW05c1pVNWhiV1VpT2lKVGVYTjBaVzBnUVdSdGFXNGlmUS5uZmlSRE1JVUZsUjZYcDd6Nm1wblNNX2w2UldtTXdoLXl5SnJIY1NUS1NrIiwiaXNzIjoidHdpc3Rsb2NrIiwiZXhwIjoxNzU4MDQxMjAyfQ.5DLKIBIXOitbs3a6dZ4MYR05CxGK8IkEmvQmA-7YN4I"
PRISMA_CLOUD_URL = "asia-southeast1.cloud.twistlock.com/aws-singapore-961149788"
PRISMA_CLOUD_VERSION = "v34.02"

def get_host_scan_results():
    """
    Retrieves all host scan reports from the Prisma Cloud API.
    
    Returns:
        list or None: A list of host reports, or None if the request fails.
    """
    url = f"https://{PRISMA_CLOUD_URL}/api/{PRISMA_CLOUD_VERSION}/hosts"
    
    headers = {
        "Authorization": f"Bearer {PRISMA_CLOUD_BEARER_TOKEN}",
        "Accept": "application/json"
    }

    print("Retrieving all host scan reports...")

    try:
        # Request all host reports without using pagination for simplicity
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}", file=sys.stderr)
        return None

def find_packages_in_hosts(package_name):
    """
    Retrieves host reports and finds hosts that contain a specific package.
    
    Args:
        package_name (str): The name of the package to search for.
    
    Returns:
        list: A list of hosts that contain the specified package.
    """
    found_hosts = []
    host_reports = get_host_scan_results()

    if not host_reports:
        return []

    for host in host_reports:
        # Check for 'packages' field
        package_groups = host.get('packages')
        if package_groups:
            for pkg_group in package_groups:
                packages_in_group = pkg_group.get('pkgs')
                if packages_in_group:
                    for pkg in packages_in_group:
                        if pkg.get('name') == package_name:
                            found_hosts.append({
                                "hostname": host.get("hostname"),
                                "distro": host.get("distro"),
                                "package_name": pkg.get("name"),
                                "package_version": pkg.get("version"),
                            })
                            # Once found, no need to check other packages in this host
                            break 
                    else:
                        continue
                    break
            else:
                continue
            break
            
    return found_hosts

def main():
    """
    Main function to run the script.
    """
    if "YOUR_" in PRISMA_CLOUD_BEARER_TOKEN or "YOUR_" in PRISMA_CLOUD_URL:
        print("Error: Please set your Prisma Cloud Bearer token and URL.", file=sys.stderr)
        sys.exit(1)

    search_package = input("Enter the package name to search for: ")
    if not search_package:
        print("No package name entered. Exiting.", file=sys.stderr)
        sys.exit(1)

    hosts_with_package = find_packages_in_hosts(search_package)

    if hosts_with_package:
        print(f"\n Found {len(hosts_with_package)} hosts with the '{search_package}' package:")
        for host_info in hosts_with_package:
            print("-" * 20)
            print(f"  Hostname: {host_info.get('hostname', 'N/A')}")
            print(f"  OS Distro: {host_info.get('distro', 'N/A')}")
            print(f"  Package Name: {host_info.get('package_name', 'N/A')}")
            print(f"  Package Version: {host_info.get('package_version', 'N/A')}")
    else:
        print(f"\n No hosts found with the '{search_package}' package.")

if __name__ == "__main__":
    main()