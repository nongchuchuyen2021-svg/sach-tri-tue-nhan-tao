import urllib.request
import urllib.error

BASE_URL = "https://sach-tri-tue-nhan-tao.vercel.app"

test_urls = [
    f"{BASE_URL}/",
    f"{BASE_URL}/reader.html?book=lop-10&lesson=bai-1-tri-tue-nhan-tao",
    f"{BASE_URL}/reader.html?book=lop-10&lesson=bai-2-ai-tao-sinh",
    f"{BASE_URL}/reader.html?book=lop-10&lesson=bai-11-moi-truong-phat-trien-san-pham-ai",
    f"{BASE_URL}/assets/images/lop-10/bai-1/hinh-1-1-nhan-dang-sinh-trac.webp",
    f"{BASE_URL}/assets/images/lop-10/bai-2/hinh-2-1.webp",
    f"{BASE_URL}/assets/images/lop-10/bai-2/hinh-2-9.webp",
    f"{BASE_URL}/assets/images/lop-10/bai-4/hinh-4-1.webp",
    f"{BASE_URL}/assets/images/lop-10/bai-9/hinh-9-1.webp",
    f"{BASE_URL}/assets/images/lop-10/bai-11/hinh-11-2.webp",
    f"{BASE_URL}/assets/images/lop-10/bai-12/hinh-12-3.webp"
]

all_ok = True
for url in test_urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            code = resp.getcode()
            clen = resp.headers.get("Content-Length", len(resp.read()))
            print(f"✓ [{code}] {url} ({int(clen)/1024:.1f} KB)")
    except urllib.error.HTTPError as e:
        print(f"✗ [{e.code}] {url}: {e.reason}")
        all_ok = False
    except Exception as e:
        print(f"✗ ERROR {url}: {e}")
        all_ok = False

if all_ok:
    print("\nALL LIVE PRODUCTION ASSETS VERIFIED 200 OK!")
