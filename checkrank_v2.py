import time
import requests
import random
from urllib.parse import quote

def google_search(api_key, search_engine_id, keyword, target_url):
    found = False
    rank_info = None
    
    for start in range(1, 41, 10):  # Duyệt từ trang 1 đến trang 4 (40 kết quả)
        search_url = f"https://www.googleapis.com/customsearch/v1?q={quote(keyword)}&key={api_key}&cx={search_engine_id}&start={start}"
        
        try:
            response = requests.get(search_url, timeout=10)
            if response.status_code != 200:
                print(f"[ERROR] Không thể truy cập Google Custom Search API (Status Code: {response.status_code})")
                continue
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Lỗi kết nối API: {e}")
            continue
        
        data = response.json()
        results = data.get("items", [])
        
        rank = start
        for result in results:
            rank += 1
            real_url = result.get("link", "")
            if target_url in real_url:
                rank_info = f"Keyword: {keyword} | Rank: {rank} | URL: {real_url}"
                print(f"[SUCCESS] {rank_info}")
                found = True
                break
        if found:
            break
    
    if not found:
        rank_info = f"Keyword: {keyword} | Rank: Not Found | URL: None"
        print(f"[FAIL] Không tìm thấy {target_url}")
    
    return rank_info

def main():
    api_key = input("Nhập API Key của Google Custom Search: ").strip()
    search_engine_id = input("Nhập Search Engine ID: ").strip()
    keywords = input("Nhập danh sách từ khóa (cách nhau bằng dấu phẩy): ").split(",")
    target_url = input("Nhập URL mục tiêu: ").strip()
    
    all_ranks = []
    
    for keyword in keywords:
        keyword = keyword.strip()
        print(f"\n[INFO] Đang tìm kiếm từ khóa: {keyword}")
        rank_info = google_search(api_key, search_engine_id, keyword, target_url)
        all_ranks.append(rank_info)
        print("[INFO] Chờ 6 giây trước lần tìm kiếm tiếp theo...")
        time.sleep(6)
    
    print("\nChọn hành động sau khi kiểm tra xếp hạng:")
    print("1: Xuất kết quả xếp hạng ra file txt.")
    print("2: Thoát.")
    choice = input("Nhập lựa chọn (1/2): ").strip()
    
    if choice == "1":
        with open("rank_results.txt", "w", encoding="utf-8") as f:
            for line in all_ranks:
                f.write(line + "\n")
        print("[INFO] Kết quả đã được lưu vào rank_results.txt")
    
if __name__ == "__main__":
    main()
