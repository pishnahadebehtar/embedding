import requests
import json
import sys

# تنظیم انکودینگ برای نمایش صحیح فارسی در ویندوز
sys.stdout.reconfigure(encoding='utf-8')

# آدرس وب‌سرویس شما
API_URL = "https://695d7f950038a6b59759.fra.appwrite.run/"

def main():
    print("--- Start Program ---")
    
    # دریافت ورودی
    try:
        user_text = input("Matn ra vared konid (Enter bezanid): ").strip()
    except Exception as e:
        print(f"Error dar daryaft voroodi: {e}")
        return

    if not user_text:
        print("Error: Matn khali ast.")
        return

    print(f"Matn daryaft shod: {user_text}")
    print("Dar hale ersal be server (lotfan sabr konid)...")

    # آماده‌سازی داده‌ها
    payload = {"text": user_text}
    headers = {"Content-Type": "application/json"}

    try:
        # ارسال درخواست با تایم‌اوت 30 ثانیه
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        
        print(f"Pasokh az server daryaft shod. Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            
            if "embedding" in data:
                embedding_vector = data["embedding"]
                
                # ذخیره در فایل
                filename = "embedding.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(json.dumps(embedding_vector))
                
                print("Mofaghaghiat! File 'embedding.txt' zakhire shod.")
                print(f"Tool vector: {len(embedding_vector)}")
            else:
                print("Key 'embedding' dar pasokh nist.")
                print("Pasokh: ", data)
        else:
            print(f"Khata dar server: {response.text}")

    except requests.exceptions.Timeout:
        print("Khata: Zamane ersal toolani shod (Timeout). Server kond ast.")
    except requests.exceptions.ConnectionError:
        print("Khata: Moshkel dar etesal be internet.")
    except Exception as e:
        print(f"Yek khataye nashenakhte: {e}")

    input("\nBaraye khorooj Enter bezanid...")

if __name__ == "__main__":
    main()
