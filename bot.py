from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

import config


# ================= COMPANY INFO =================
COMPANY_INFO = """
KOMPANIYA HAQIDA:

Biz qurilish va dizayn sohasida xizmat ko‘rsatamiz.

XIZMATLAR:
1. Tayyor loyihalar
2. 3D dizayn xizmatlari
3. 2D va 3D dizayner xizmati
4. Individual loyiha ishlab chiqish

ALOQA:
Operator: Ayubalikhan
Telefon: +998 (90) 935 11 77
"""


# ================= TEXTS =================
TEXTS = {
    "uz": {
        "welcome": "🇺🇿 Tilni tanlang:",
        "contact": "📞 Telefon raqamingizni yuboring:",
        "contact_saved": "✅ Rahmat! Kontakt qabul qilindi.",
        "location": "📍 Lokatsiya yuboring:",
        "photo": "📸 Manzilni aniq topib borishimiz uchun iltimos, atrof muhitni ko‘rsatadigan rasm yuborib bera olasizmi?",
        "done": "✅ Ma'lumotlar qabul qilindi!",
        "menu": "💼 Xizmatni tanlang:",
        "final": "📩 So'rovingiz muvaffaqiyatli qabul qilindi!\n\n👨‍💼 Tez orada siz bilan operatorimiz bog‘lanadi.\n📞 Iltimos, aloqada bo‘ling.",
        "operator": "👨‍💼 Operator: Ayubalikhan\n📞 +998 (90) 935 11 77"
    },

    "ru": {
        "welcome": "🇷🇺 Выберите язык:",
        "contact": "📞 Отправьте номер телефона:",
        "contact_saved": "✅ Контакт сохранен.",
        "location": "📍 Отправьте локацию:",
        "photo": "📸 Чтобы мы могли точно найти ваш адрес, пожалуйста, отправьте фото окружающей местности.",
        "done": "✅ Данные получены!",
        "menu": "💼 Выберите услугу:",
        "final": "📩 Ваша заявка принята!\n\n👨‍💼 В ближайшее время с вами свяжется оператор.\n📞 Оставайтесь на связи.",
        "operator": "👨‍💼 Оператор: Ayubalikhan\n📞 +998 (90) 935 11 77"
    },

    "en": {
        "welcome": "🇬🇧 Choose language:",
        "contact": "📞 Send your phone number:",
        "contact_saved": "✅ Contact saved.",
        "location": "📍 Send location:",
        "photo": "📸 To help us find your location accurately, please send a photo of the surrounding area.",
        "done": "✅ Data received!",
        "menu": "💼 Choose service:",
        "final": "📩 Your request has been received!\n\n👨‍💼 Our operator will contact you soon.\n📞 Please stay available.",
        "operator": "👨‍💼 Operator: Ayubalikhan\n📞 +998 (90) 935 11 77"
    },

    "buttons": {
        "contact": {
            "uz": "📞 Telefon yuborish",
            "ru": "📞 Отправить номер",
            "en": "📞 Send phone"
        },
        "location": {
            "uz": "📍 Lokatsiya yuborish",
            "ru": "📍 Отправить локацию",
            "en": "📍 Send location"
        }
    },

    "menu_buttons": {
        "uz": [
            ["🏗 Menda tayyor loyiha bor"],
            ["🎨 Menda 3D dizayn bor"],
            ["🧑‍💻 Dizayner xizmati 2D/3D"],
            ["👨‍💼 Operator"]
        ],
        "ru": [
            ["🏗 У меня есть готовый проект"],
            ["🎨 У меня есть 3D дизайн"],
            ["🧑‍💻 Услуги дизайнера 2D/3D"],
            ["👨‍💼 Оператор"]
        ],
        "en": [
            ["🏗 I have a ready project"],
            ["🎨 I have a 3D design"],
            ["🧑‍💻 Designer service 2D/3D"],
            ["👨‍💼 Operator"]
        ]
    }
}


# ================= STATES =================
LANG, CONTACT, LOCATION, PHOTO, MENU = range(5)


# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🇬🇧 English", "🇷🇺 Русский", "🇺🇿 O'zbek"]]

    await update.message.reply_text(
        "🌐 Tilni tanlang / Choose language / Выберите язык",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return LANG


# ================= LANGUAGE =================
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "O'zbek" in text:
        lang = "uz"
    elif "Русский" in text:
        lang = "ru"
    else:
        lang = "en"

    context.user_data["lang"] = lang

    button = [[KeyboardButton(TEXTS["buttons"]["contact"][lang], request_contact=True)]]

    await update.message.reply_text(
        TEXTS[lang]["contact"],
        reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True)
    )

    return CONTACT


# ================= CONTACT =================
async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]

    if update.message.contact:
        phone = update.message.contact.phone_number
        context.user_data["contact"] = phone

    await update.message.reply_text(TEXTS[lang]["contact_saved"])

    button = [[KeyboardButton(TEXTS["buttons"]["location"][lang], request_location=True)]]

    await update.message.reply_text(
        TEXTS[lang]["location"],
        reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True)
    )

    return LOCATION


# ================= LOCATION =================
async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]

    loc = update.message.location
    context.user_data["lat"] = loc.latitude
    context.user_data["lon"] = loc.longitude

    await update.message.reply_text(TEXTS[lang]["photo"])

    return PHOTO


# ================= PHOTO =================
async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]

    await update.message.reply_text(TEXTS[lang]["done"])

    keyboard = TEXTS["menu_buttons"][lang]

    await update.message.reply_text(
        TEXTS[lang]["menu"],
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

    return MENU


# ================= MENU =================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data["lang"]
    text = update.message.text

    if "Operator" in text or "Оператор" in text:
        await update.message.reply_text(TEXTS[lang]["operator"])
        return MENU

    await update.message.reply_text(TEXTS[lang]["final"])
    return MENU

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    keyboard = [["🇬🇧 English", "🇷🇺 Русский", "🇺🇿 O'zbek"]]

    await update.message.reply_text(
        "🔄 \n\n🌐 Tilni tanlang / Choose language / Выберите язык",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

    return LANG


# ================= APP =================
def get_app():
    app = ApplicationBuilder().token(config.TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [MessageHandler(filters.TEXT, set_language)],
            CONTACT: [MessageHandler(filters.CONTACT | filters.TEXT, get_contact)],
            LOCATION: [MessageHandler(filters.LOCATION, get_location)],
            PHOTO: [MessageHandler(filters.PHOTO, get_photo)],
            MENU: [MessageHandler(filters.TEXT, menu)]
        },
        fallbacks=[CommandHandler("restart", restart)]
    )

    app.add_handler(CommandHandler("restart", restart))
    app.add_handler(conv)

    return app