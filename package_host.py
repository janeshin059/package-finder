import requests
import json
import sys

# ==============================================================================
# 설정: API 키와 URL을 여기에 직접 입력하세요.
# ==============================================================================
PRISMA_CLOUD_BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiamFzaGluQHBhbG9hbHRvbmV0d29ya3MuY29tIiwicm9sZSI6ImFkbWluIiwicm9sZVBlcm1zIjpbWzI1NSwyNTUsMjU1LDI1NSwyNTUsOTVdLFsyNTUsMjU1LDI1NSwyNTUsMjU1LDk1XV0sInNlc3Npb25UaW1lb3V0U2VjIjo2MDAsInNhYXNUb2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUo5LmV5SnpkV0lpT2lKcVlYTm9hVzVBY0dGc2IyRnNkRzl1WlhSM2IzSnJjeTVqYjIwaUxDSnpaWEoyYVdObFZYTmhaMlZQYm14NUlqcDBjblZsTENKbWFYSnpkRXh2WjJsdUlqcG1ZV3h6WlN3aWNISnBjMjFoU1dRaU9pSXhNak13T0RBeU56YzJPVFk1T1RRNU1UZzBJaXdpYVhCQlpHUnlaWE56SWpvaU16UXVPRGN1TVRNM0xqRTBNU0lzSW1semN5STZJbWgwZEhCek9pOHZZWEJwTG5ObkxuQnlhWE50WVdOc2IzVmtMbWx2SWl3aWNtVnpkSEpwWTNRaU9qQXNJblZ6WlhKU2IyeGxWSGx3WlVSbGRHRnBiSE1pT25zaWFHRnpUMjVzZVZKbFlXUkJZMk5sYzNNaU9tWmhiSE5sZlN3aWRYTmxjbEp2YkdWVWVYQmxUbUZ0WlNJNklsTjVjM1JsYlNCQlpHMXBiaUlzSW1selUxTlBVMlZ6YzJsdmJpSTZabUZzYzJVc0lteGhjM1JNYjJkcGJsUnBiV1VpT2pFM05UZ3dNemN5T1RnME5UWXNJbUYxWkNJNkltaDBkSEJ6T2k4dllYQnBMbk5uTG5CeWFYTnRZV05zYjNWa0xtbHZJaXdpZFhObGNsSnZiR1ZVZVhCbFNXUWlPakVzSW1GMWRHZ3RiV1YwYUc5a0lqb2lVRUZUVTFkUFVrUWlMQ0p6Wld4bFkzUmxaRU4xYzNSdmJXVnlUbUZ0WlNJNklreGxaVWhoYms1VElFTnZjbkF1SUMwZ05qZzJOelE1TURZd09ERTNOVEExTmpJMk1pSXNJbk5sYzNOcGIyNVVhVzFsYjNWMElqb3pNREFzSW5WelpYSlNiMnhsU1dRaU9pSmtaakJoWVROaU1DMWpZemc0TFRRM05UY3RZVGN5WlMwM05UaGhPV1F4TmpjellqUWlMQ0pvWVhORVpXWmxibVJsY2xCbGNtMXBjM05wYjI1eklqcDBjblZsTENKbGVIQWlPakUzTlRnd016Z3lNRElzSW1saGRDSTZNVGMxT0RBek56WXdNaXdpZFhObGNtNWhiV1VpT2lKcVlYTm9hVzVBY0dGc2IyRnNkRzl1WlhSM2IzSnJjeTVqYjIwaUxDSjFjMlZ5VW05c1pVNWhiV1VpT2lKVGVYTjBaVzBnUVdSdGFXNGlmUS5uZmlSRE1JVUZsUjZYcDd6Nm1wblNNX2w2UldtTXdoLXl5SnJIY1NUS1NrIiwiaXNzIjoidHdpc3Rsb2NrIiwiZXhwIjoxNzU4MDQxMjAyfQ.5DLKIBIXOitbs3a6dZ4MYR05CxGK8IkEmvQmA-7YN4I"
PRISMA_CLOUD_URL = "asia-southeast1.cloud.twistlock.com/aws-singapore-961149788"
PRISMA_CLOUD_VERSION = "v34.02"

def get_host_scan_results():
    """
    모든 호스트 스캔 보고서를 Prisma Cloud API에서 가져옵니다.

    Returns:
        list or None: 호스트 보고서 리스트, 또는 요청 실패 시 None.
    """
    url = f"https://{PRISMA_CLOUD_URL}/api/{PRISMA_CLOUD_VERSION}/hosts"

    headers = {
        "Authorization": f"Bearer {PRISMA_CLOUD_BEARER_TOKEN}",
        "Accept": "application/json"
    }

    print("모든 호스트 스캔 보고서를 가져오는 중...")

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API 호출 실패: {e}", file=sys.stderr)
        return None

def find_all_instances_of_package(package_name):
    """
    호스트 보고서를 검색하여 특정 패키지의 모든 인스턴스를 찾습니다.

    Args:
        package_name (str): 검색할 패키지의 이름.

    Returns:
        list: 해당 패키지 정보의 모든 인스턴스가 담긴 리스트.
    """
    all_found_packages = []
    host_reports = get_host_scan_results()

    if not host_reports:
        return []

    for host in host_reports:
        package_groups = host.get('packages')
        if package_groups:
            for pkg_group in package_groups:
                packages_in_group = pkg_group.get('pkgs')
                if packages_in_group:
                    for pkg in packages_in_group:
                        if pkg.get('name') == package_name:
                            all_found_packages.append({
                                "hostname": host.get("hostname"),
                                "distro": host.get("distro"),
                                "package_name": pkg.get("name"),
                                "package_version": pkg.get("version"),
                            })

    return all_found_packages

def main():
    """
    메인 스크립트 실행 함수.
    """
    if "YOUR_" in PRISMA_CLOUD_BEARER_TOKEN or "YOUR_" in PRISMA_CLOUD_URL:
        print("에러: 스크립트 내에 Prisma Cloud Bearer 토큰과 URL이 설정되지 않았습니다.", file=sys.stderr)
        sys.exit(1)

    search_package = input("검색할 패키지 이름을 입력하세요: ")
    if not search_package:
        print("패키지 이름이 입력되지 않았습니다. 스크립트를 종료합니다.", file=sys.stderr)
        sys.exit(1)

    all_packages = find_all_instances_of_package(search_package)

    if all_packages:
        print(f"\n✨ '{search_package}' 패키지의 모든 인스턴스 정보:")
        # 호스트별로 그룹화하여 출력
        hosts_with_package = {}
        for pkg_info in all_packages:
            hostname = pkg_info['hostname']
            if hostname not in hosts_with_package:
                hosts_with_package[hostname] = []
            hosts_with_package[hostname].append(pkg_info)
        
        for hostname, pkgs in hosts_with_package.items():
            print("-" * 20)
            print(f"  호스트 이름: {hostname}")
            print(f"  OS 배포판: {pkgs[0].get('distro', 'N/A')}")
            
            for pkg in pkgs:
                print(f"    - 이름: {pkg.get('package_name', 'N/A')}, 버전: {pkg.get('package_version', 'N/A')}")
    else:
        print(f"\n🔍 '{search_package}' 패키지를 포함하는 호스트를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()