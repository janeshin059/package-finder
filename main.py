import requests
import json
import sys

# ==============================================================================
# 설정: API 키와 URL을 여기에 입력하세요.
# = Prisma Cloud API에 접근하기 위한 Bearer 토큰을 사용합니다.
# ==============================================================================
PRISMA_CLOUD_BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiamFzaGluQHBhbG9hbHRvbmV0d29ya3MuY29tIiwicm9sZSI6ImFkbWluIiwicm9sZVBlcm1zIjpbWzI1NSwyNTUsMjU1LDI1NSwyNTUsOTVdLFsyNTUsMjU1LDI1NSwyNTUsMjU1LDk1XV0sInNlc3Npb25UaW1lb3V0U2VjIjo2MDAsInNhYXNUb2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUo5LmV5SnpkV0lpT2lKcVlYTm9hVzVBY0dGc2IyRnNkRzl1WlhSM2IzSnJjeTVqYjIwaUxDSnpaWEoyYVdObFZYTmhaMlZQYm14NUlqcDBjblZsTENKbWFYSnpkRXh2WjJsdUlqcG1ZV3h6WlN3aWNISnBjMjFoU1dRaU9pSXhNak13T0RBeU56YzJPVFk1T1RRNU1UZzBJaXdpYVhCQlpHUnlaWE56SWpvaU16UXVPRGN1TVRNM0xqRTBNU0lzSW1semN5STZJbWgwZEhCek9pOHZZWEJwTG5ObkxuQnlhWE50WVdOc2IzVmtMbWx2SWl3aWNtVnpkSEpwWTNRaU9qQXNJblZ6WlhKU2IyeGxWSGx3WlVSbGRHRnBiSE1pT25zaWFHRnpUMjVzZVZKbFlXUkJZMk5sYzNNaU9tWmhiSE5sZlN3aWRYTmxjbEp2YkdWVWVYQmxUbUZ0WlNJNklsTjVjM1JsYlNCQlpHMXBiaUlzSW1selUxTlBVMlZ6YzJsdmJpSTZabUZzYzJVc0lteGhjM1JNYjJkcGJsUnBiV1VpT2pFM05UZ3dNamd4TVRNNE1ESXNJbUYxWkNJNkltaDBkSEJ6T2k4dllYQnBMbk5uTG5CeWFYTnRZV05zYjNWa0xtbHZJaXdpZFhObGNsSnZiR1ZVZVhCbFNXUWlPakVzSW1GMWRHZ3RiV1YwYUc5a0lqb2lVRUZUVTFkUFVrUWlMQ0p6Wld4bFkzUmxaRU4xYzNSdmJXVnlUbUZ0WlNJNklreGxaVWhoYms1VElFTnZjbkF1SUMwZ05qZzJOelE1TURZd09ERTNOVEExTmpJMk1pSXNJbk5sYzNOcGIyNVVhVzFsYjNWMElqb3pNREFzSW5WelpYSlNiMnhsU1dRaU9pSmtaakJoWVROaU1DMWpZemc0TFRRM05UY3RZVGN5WlMwM05UaGhPV1F4TmpjellqUWlMQ0pvWVhORVpXWmxibVJsY2xCbGNtMXBjM05wYjI1eklqcDBjblZsTENKbGVIQWlPakUzTlRnd016STJOVFVzSW1saGRDSTZNVGMxT0RBek1qQTFOU3dpZFhObGNtNWhiV1VpT2lKcVlYTm9hVzVBY0dGc2IyRnNkRzl1WlhSM2IzSnJjeTVqYjIwaUxDSjFjMlZ5VW05c1pVNWhiV1VpT2lKVGVYTjBaVzBnUVdSdGFXNGlmUS54WmZTMzdWUmtYbVdTTmVkZFRIdV9wRG9JMTFBVHR6QTk0Z1J3NkdwSUEwIiwiaXNzIjoidHdpc3Rsb2NrIiwiZXhwIjoxNzU4MDM1NjU1fQ.A25BZB5J0kj78Fgv_KnxGb0_MfddQHXSn3R4xD9qgzk"
PRISMA_CLOUD_URL = "asia-southeast1.cloud.twistlock.com/aws-singapore-961149788" # 예: console.paloaltonetworks.com
PRISMA_CLOUD_VERSION = "v34.02"

def get_package_info_by_name(package_name):
    """
    모든 이미지 보고서를 검색하여 특정 패키지 이름의 정보를 찾습니다.

    Args:
        package_name (str): 검색할 패키지의 이름.

    Returns:
        list: 검색된 패키지 정보가 담긴 딕셔너리 리스트.
    """
    found_packages = []
    limit = 50
    offset = 0
    headers = {
        "Authorization": f"Bearer {PRISMA_CLOUD_BEARER_TOKEN}",
        "Accept": "application/json"
    }

    print(f"'{package_name}' 패키지 정보를 검색 중...")

    try:
        while True:
            url = f"https://{PRISMA_CLOUD_URL}/api/{PRISMA_CLOUD_VERSION}/images"
            params = {"limit": limit, "offset": offset} # compact 옵션으로 필요한 정보만 요청

            response = requests.get(url, headers=headers, params=params, verify=False)
            response.raise_for_status()
            
            reports = response.json()
            # print(reports)
            if not reports:
                break
          
            for report in reports:
                if 'packages' in report and report['packages']:
                    #  print('YES')
                    for pkg_group in report['packages']:
                        if 'pkgs' in pkg_group:
                            # print('YES')
                            for pkg in pkg_group['pkgs']:
                                if pkg.get('name') == package_name:
                                    found_packages.append({
                                        "name": pkg.get("name"),
                                        "version": pkg.get("version"),
                                        "type": pkg_group.get("pkgsType"),
                                        "image_id": report.get("id"),
                                        "image_name": report.get("repoTag", {}).get("repo"),
                                        "registry": report.get("repoTag", {}).get("registry")
                                    })
            
            if len(reports) < limit:
                break
            
            offset += limit

    except requests.exceptions.RequestException as e:
        print(f"API 호출 중 오류 발생: {e}", file=sys.stderr)
        return []

    return found_packages

def main():
    """
    메인 스크립트 실행 함수.
    """
    if "YOUR_" in PRISMA_CLOUD_BEARER_TOKEN or "YOUR_" in PRISMA_CLOUD_URL:
        print("에러: Prisma Cloud Bearer 토큰과 URL을 올바르게 입력해주세요.", file=sys.stderr)
        sys.exit(1)

    # 검색하고 싶은 패키지 이름을 여기에 입력하세요.
    search_package_name = "init-system-helpers"
    # search_package_name = input("검색할 패키지 이름을 입력하세요: ")

    # 함수 호출
    packages = get_package_info_by_name(search_package_name)

    if packages:
        print(f"\n✨ '{search_package_name}' 패키지 정보:")
        for pkg in packages:
            print("-" * 20)
            print(f"  이름: {pkg['name']}")
            print(f"  버전: {pkg['version']}")
            print(f"  타입: {pkg['type']}")
            print(f"  포함된 이미지 ID: {pkg['image_id']}")
            print(f"  포함된 이미지 이름: {pkg['image_name']}")
            print(f"  레지스트리: {pkg['registry']}")
    else:
        print(f"\n '{search_package_name}' 패키지 정보를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()