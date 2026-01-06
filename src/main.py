import os
import json
import google.generativeai as genai

# این تابع نقطه شروع اجرای فانکشن در اپ‌رایت است
def main(context):
    try:
        # 1. دریافت API Key از متغیرهای محیطی اپ‌رایت
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return context.res.json({
                "error": "GEMINI_API_KEY is not set in Appwrite Function variables."
            }, 500)

        # تنظیم جمینای
        genai.configure(api_key=api_key)

        # 2. بررسی متد درخواست (فقط POST قبول می‌کنیم)
        if context.req.method != "POST":
            return context.res.json({"error": "Only POST requests are allowed"}, 405)

        # 3. پارس کردن بادی درخواست (Payload)
        payload = context.req.body
        # اگر بادی به صورت رشته متنی آمده باشد، آن را به دیکشنری تبدیل می‌کنیم
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                 return context.res.json({"error": "Invalid JSON body"}, 400)

        text_to_embed = payload.get("text")
        
        if not text_to_embed:
            return context.res.json({"error": "Field 'text' is required"}, 400)

        # 4. درخواست به جمینای برای ساخت امبدینگ
        # مدل text-embedding-004 برای این کار عالی است
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text_to_embed,
            task_type="retrieval_document" # یا retrieval_query بسته به نیاز
        )

        embedding_vector = result['embedding']

        # 5. بازگرداندن نتیجه به کلاینت (بدون ذخیره در دیتابیس)
        return context.res.json({
            "status": "success",
            "text_preview": text_to_embed[:50], # 50 کاراکتر اول برای اطمینان
            "embedding": embedding_vector
        }, 200)

    except Exception as e:
        # ثبت خطا در لاگ‌های اپ‌رایت
        context.error(f"Error executing function: {str(e)}")
        return context.res.json({
            "error": "Internal Server Error",
            "details": str(e)
        }, 500)
