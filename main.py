import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

# بارگذاری متغیرهای محیطی از فایل امن .env
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# خواندن امن کلید از محیط سیستم (فایل .env)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class UserProfile(BaseModel):
    age: int
    gender: str
    weight: float
    height: float
    neck: float
    chest: float
    arm: float
    wrist: float
    waist: float
    hip: float
    thigh: float
    ankle: float
    goal: str
    days_per_week: int
    experience: str
    equipment: str
    duration: int
    activity_level: str
    injuries: str
    week_number: int = 1
    part: int = 1

class SubstitutionRequest(BaseModel):
    exercise_name: str
    goal: str
    equipment: str
    injuries: str

@app.post("/api/workout")
async def generate_workout(profile: UserProfile):
    try:
        total_days = profile.days_per_week
        if total_days > 3:
            if profile.part == 1:
                day_instruction = "فقط روز ۱، روز ۲ و روز ۳ را طراحی کن (بخش اول)."
            else:
                day_instruction = "بخش دوم: شمارش روزها حتماً از «روز ۴» به بعد شروع شود (تا انتهای روزهای تعیین شده)."
        else:
            day_instruction = f"روز ۱ تا روز {total_days} را دقیقاً طراحی کن و به هیچ وجه روز اضافی نساز."

        prompt = f"""
        تو یک سیستم هوشمند، حرفه‌ای و دقیق برنامه‌نویسی ورزشی و بدنسازی هستی. در ابتدای پاسخ، حتماً در حد دو خط به اهمیت گرم کردن پیش از تمرین و سرد کردن پس از تمرین اشاره کن. سپس جدول برنامه را بیاور.
        
        مشخصات کاربر: سن {profile.age} | وزن {profile.weight} | قد {profile.height} | هدف {profile.goal} | کل روزهای تمرین در هفته: {total_days}
        درخواست ویژه: برنامه تمرینی کاملاً اصولی، علمی و پیوسته مختص **«هفته {profile.week_number}»** (در راستای روند پیشرونده و پیوسته از هفته‌های پیشین تا پایان هفته چهارم با رعایت اصل اضافه بار) - {day_instruction} با رعایت کامل اصول و متدهای بدنسازی.
        
        الزامات بسیار مهم و غیرقابل‌تغییر:
        1. **تفکیک دقیق ستون‌ها و جلوگیری از تداخل:** نام هر حرکت را **فقط و فقط** در ستون «نام حرکت» بنویس و به هیچ وجه نام حرکت، وسایل یا کلمات اضافی را در ستون «تکرارها» قرار نده. ستون تکرارها **فقط و فقط** باید شامل اعداد تکرار هر ست (مثل ۱۲، ۱۰، ۱۰) باشد.
        2. **تقسیم متوازن فشار:** فشار تمرینی، حجم و شدت تمرین باید به صورت کاملاً متوازن و منطقی بین روزهای هفته تقسیم شود، به طوری که یک روز بسیار سبک و روز دیگر بیش از حد سنگین و فرساینده نباشد.
        3. **رعایت پیوستگی و اصول بدنسازی:** برنامه هفته جاری باید به صورت منطقی و پیشرونده در ادامه هفته‌های قبلی باشد.
        4. **قانون سخت‌گیرانه تعداد روزها:** تعداد روزهای تمرین در خروجی باید **دقیقاً و بدون کم و کاست برابر با {total_days} روز** باشد. به هیچ وجه روزهای اضافی تولید نکن.
        5. **فقط و فقط از زبان فارسی درست، روان و بدون غلط املایی استفاده کن.** به هیچ وجه از اسامی انگلیسی، کلمات لاتین یا فینگلیش استفاده نکن و تمام نام حرکات، بخش‌ها و اصطلاحات را به فارسی دقیق و پاکیزه برگردان.
        6. ستون‌ها دقیقاً و فقط شامل این ۴ مورد باشند:
           | روز | عضله هدف | نام حرکت | تکرارها (ست ۱، ست ۲، ست ۳...) |
        7. **قانون درج روز:** در ستون روزها، نام روز (مثلاً "روز ۱") را **فقط و فقط در اولین حرکتِ آن روز** بنویس و برای سایر حرکاتِ همان روز، آن خانه از جدول را خالی بگذار تا نام روز تکرار نشود.
        8. در بخش دوم، شروع روزها حتماً از «روز ۴» به بعد باشد.
        9. زمان استراحت بین ست‌ها را کاملاً حذف کن.
        10. به هیچ وجه از کلمه «تکرار» در جدول استفاده نکن و فقط اعداد تکرار هر ست را با ویرگول جدا کن (مثلاً ۱۲، ۱۰، ۱۰).
        """
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="qwen/qwen3.8-27b",
            max_tokens=1000,
        )
        
        return {"status": "success", "workout_plan": chat_completion.choices[0].message.content}
        
    except Exception as e:
        return {"status": "error", "workout_plan": f"خطا: {str(e)}"}

@app.post("/api/substitute")
async def substitute_exercise(req: SubstitutionRequest):
    try:
        prompt = f"""
        کاربر می‌خواهد حرکت «{req.exercise_name}» را در برنامه بدنسازی با هدف «{req.goal}»، تجهیزات در دسترس «{req.equipment}» و آسیب‌دیدگی «{req.injuries}» با یک حرکت جایگزین مناسب به زبان فارسی روان جایگزین کند.
        
        دستورالعمل بسیار سخت‌گیرانه برای خروجی:
        1. فقط و فقط نام حرکت جایگزین (به زبان فارسی روان و بدون کلمات انگلیسی) به همراه تکرارهای تفکیک‌شده‌ی ست‌ها (مثلاً: ۱۲، ۱۰، ۱۰) را بنویس.
        2. **به هیچ وجه** هیچ‌گونه توضیحات، مقدمه، حاشیه‌روی یا متن اضافی در خروجی قرار نده. فقط نام حرکت و تکرارها.
        3. اگر با توجه به شرایط کاربر، حرکت جایگزین مناسبی وجود نداشت، دقیقاً و فقط پاسخ بده: «حرکت جایگزین نیست».
        """
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="qwen/qwen3.8-27b",
            max_tokens=200,
        )
        return {"status": "success", "substitution": chat_completion.choices[0].message.content}
    except Exception as e:
        return {"status": "error", "substitution": f"خطا: {str(e)}"}