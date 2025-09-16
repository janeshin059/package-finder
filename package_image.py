import requests
import json
import sys

# ==============================================================================
# 설정: API 키와 URL을 여기에 입력하세요.
# ==============================================================================
PRISMA_CLOUD_BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiamFzaGluQHBhbG9hbHRvbmV0d29ya3MuY29tIiwicm9sZSI6ImFkbWluIiwicm9sZVBlcm1zIjpbWzI1NSwyNTUsMjU1LDI1NSwyNTUsOTVdLFsyNTUsMjU1LDI1NSwyNTUsMjU1LDk1XV0sInNlc3Npb25UaW1lb3V0U2VjIjo2MDAsInNhYXNUb2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUo5LmV5SnpkV0lpT2lKcVlYTm9hVzVBY0dGc2IyRnNkRzl1WlhSM2IzSnJjeTVqYjIwaUxDSnpaWEoyYVdObFZYTmhaMlZQYm14NUlqcDBjblZsTENKbWFYSnpkRXh2WjJsdUlqcG1ZV3h6WlN3aWNISnBjMjFoU1dRaU9pSXhNRGM0TXpVeE16WTFOVGswTURNeE1UQTBJaXdpYVhCQlpHUnlaWE56SWpvaU1UQTBMakU1T0M0eE1Ea3VOek1pTENKcGMzTWlPaUpvZEhSd2N6b3ZMMkZ3YVRRdWNISnBjMjFoWTJ4dmRXUXVhVzhpTENKeVpYTjBjbWxqZENJNk1Dd2lkWE5sY2xKdmJHVlVlWEJsUkdWMFlXbHNjeUk2ZXlKb1lYTlBibXg1VW1WaFpFRmpZMlZ6Y3lJNlptRnNjMlY5TENKMWMyVnlVbTlzWlZSNWNHVk9ZVzFsSWpvaVUzbHpkR1Z0SUVGa2JXbHVJaXdpYVhOVFUwOVRaWE56YVc5dUlqcDBjblZsTENKc1lYTjBURzluYVc1VWFXMWxJam94TnpVNE1ETTNNekl3TnpZMUxDSmhkV1FpT2lKb2RIUndjem92TDJGd2FUUXVjSEpwYzIxaFkyeHZkV1F1YVc4aUxDSjFjMlZ5VW05c1pWUjVjR1ZKWkNJNk1Td2lZWFYwYUMxdFpYUm9iMlFpT2lKVFFVMU1NaUlzSW5ObGJHVmpkR1ZrUTNWemRHOXRaWEpPWVcxbElqb2lVMEVnWkdWdGJ5QndjbTlrSUMwZ05UUTFOalUxTURZME1EZ3lPVEE0TkRJd05TSXNJbk5sYzNOcGIyNVVhVzFsYjNWMElqb3pNREFzSW5WelpYSlNiMnhsU1dRaU9pSTFNekZsT0dOaFlTMWlPVEJtTFRSbVpUZ3RZalZsT0MwNFpHTTRNMkl4TW1VeU1tUWlMQ0pvWVhORVpXWmxibVJsY2xCbGNtMXBjM05wYjI1eklqcDBjblZsTENKbGVIQWlPakUzTlRnd016Z3hORFlzSW1saGRDSTZNVGMxT0RBek56VTBOaXdpZFhObGNtNWhiV1VpT2lKcVlYTm9hVzVBY0dGc2IyRnNkRzl1WlhSM2IzSnJjeTVqYjIwaUxDSjFjMlZ5VW05c1pVNWhiV1VpT2lKVGVYTjBaVzBnUVdSdGFXNGlmUS5ySmdhMXVkUFcxNV85QW5OS3pPN19mcXpuREFZTHFORmxhRVhWZHZWUzgwIiwiaXNzIjoidHdpc3Rsb2NrIiwiZXhwIjoxNzU4MDQxMTQ2fQ.PyzHgTmT51nOsqzilpZRgiKvxtxmtxrOzUAT24cHQwg"
PRISMA_CLOUD_URL = "asia-southeast1.cloud.twistlock.com/aws-singapore-961149788"
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
    headers = {
        "Authorization": f"Bearer {PRISMA_CLOUD_BEARER_TOKEN}",
        "Accept": "application/json"
    }

    print(f"'{package_name}' 패키지 정보를 검색 중...")

    try:
        url = f"https://{PRISMA_CLOUD_URL}/api/{PRISMA_CLOUD_VERSION}/images"
        
        # offset, limit 없이 한 번의 요청으로 모든 데이터를 가져옴
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        
        reports = response.json()
        
        if not reports:
            print("더 이상 이미지 보고서가 없습니다.", file=sys.stderr)
            return []
      
        for report in reports:
            package_groups = report.get('packages')
            if package_groups:
                for pkg_group in package_groups:
                    packages_in_group = pkg_group.get('pkgs')
                    if packages_in_group:
                        for pkg in packages_in_group:
                            if pkg.get('name') == package_name:
                                found_packages.append({
                                    "name": pkg.get("name"),
                                    "version": pkg.get("version"),
                                    "type": pkg_group.get("pkgsType"),
                                    "image_id": report.get("id"),
                                    "image_name": report.get("repoTag", {}).get("repo"),
                                    "registry": report.get("repoTag", {}).get("registry")
                                })

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

    search_package_name = input("검색할 패키지 이름을 입력하세요: ")
    if not search_package_name:
        print("패키지 이름이 입력되지 않았습니다. 스크립트를 종료합니다.", file=sys.stderr)
        sys.exit(1)

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