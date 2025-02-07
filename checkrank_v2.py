import time
import requests
import random
from urllib.parse import quote

def google_search(keyword, target_url, api_key):
    found = False
    rank_info = None
    
    for start in range(0, 50, 10):  # Duyệt từ trang 1 đến trang 5 (50 kết quả)
        search_url = f"https://serpapi.com/search.json?q={quote(keyword)}&engine=google&start={start}&api_key={api_key}"
        
        try:
            response = requests.get(search_url, timeout=10)
            if response.status_code != 200:
                print(f"[ERROR] Không thể truy cập SerpAPI (Status Code: {response.status_code})")
                continue
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Lỗi kết nối SerpAPI: {e}")
            continue
        
        data = response.json()
        results = data.get("organic_results", [])
        
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
    api_key = input("Nhập API Key của SerpAPI: ").strip()
    keywords = input("Nhập danh sách từ khóa (cách nhau bằng dấu phẩy): ").split(",")
    target_url = input("Nhập URL mục tiêu: ").strip()
    
    all_ranks = []
    
    for keyword in keywords:
        keyword = keyword.strip()
        print(f"\n[INFO] Đang tìm kiếm từ khóa: {keyword}")
        rank_info = google_search(keyword, target_url, api_key)
        all_ranks.append(rank_info)
        print("[INFO] Chờ 6 giây trước lần tìm kiếm tiếp theo...")
        time.sleep(6)  # Delay 1 phút
    
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
