# main.py
import telebot
from telebot import types
from config import BOT_TOKEN, CHANNELS, DB_CHANNEL, ADMIN_IDS
from database import Database

bot = telebot.TeleBot(BOT_TOKEN)
db = Database()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    
    db.add_user(user_id, username)
    
    if check_all_subscriptions(user_id):
        bot.reply_to(message, "Selamat datang! Kirimkan video untuk diunggah ke channel database.")
    else:
        markup = types.InlineKeyboardMarkup()
        for channel_id in CHANNELS:
            chat = bot.get_chat(channel_id)
            channel_name = chat.title
            markup.add(types.InlineKeyboardButton(f"Join {channel_name}", url=f"https://t.me/c/{str(channel_id)[4:]}"))
        markup.add(types.InlineKeyboardButton("Sudah Join, Cek Sekarang", callback_data="check_subscription"))
        bot.reply_to(message, "Silakan bergabung ke channel berikut untuk melanjutkan:", reply_markup=markup)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    user_id = message.from_user.id
    
    if not check_all_subscriptions(user_id):
        markup = types.InlineKeyboardMarkup()
        for channel_id in CHANNELS:
            chat = bot.get_chat(channel_id)
            channel_name = chat.title
            markup.add(types.InlineKeyboardButton(f"Join {channel_name}", url=f"https://t.me/c/{str(channel_id)[4:]}"))
        markup.add(types.InlineKeyboardButton("Sudah Join, Cek Sekarang", callback_data="check_subscription"))
        bot.reply_to(message, "Anda harus bergabung ke semua channel terlebih dahulu:", reply_markup=markup)
        return
    
    video = message.video.file_id
    sent_message = bot.send_video(DB_CHANNEL, video, caption=f"Uploaded by @{message.from_user.username or 'Unknown'}")
    
    db.add_file(video, user_id, sent_message.message_id)
    
    link = f"https://t.me/c/{str(DB_CHANNEL)[4:]}/{sent_message.message_id}"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Lihat Video", url=link))
    bot.reply_to(message, "Video Anda telah diunggah. Klik tombol di bawah untuk melihatnya:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription_callback(call):
    user_id = call.from_user.id
    if check_all_subscriptions(user_id):
        db.update_subscription(user_id, 1)
        bot.edit_message_text("Terima kasih! Anda sekarang dapat mengunggah video.", 
                              chat_id=call.message.chat.id, 
                              message_id=call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "Anda belum bergabung ke semua channel. Silakan join terlebih dahulu.")

def check_all_subscriptions(user_id):
    for channel_id in CHANNELS:
        try:
            member = bot.get_chat_member(channel_id, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception:
            return False
    return True

@bot.message_handler(commands=['stats'], func=lambda message: message.from_user.id in ADMIN_IDS)
def send_stats(message):
    db.cursor.execute("SELECT COUNT(*) FROM users")
    total_users = db.cursor.fetchone()[0]
    db.cursor.execute("SELECT COUNT(*) FROM users WHERE is_subscribed = 1")
    subscribed_users = db.cursor.fetchone()[0]
    db.cursor.execute("SELECT COUNT(*) FROM files")
    total_files = db.cursor.fetchone()[0]
    bot.reply_to(message, f"Total Pengguna: {total_users}\nPengguna Tersubscribe: {subscribed_users}\nTotal File: {total_files}")

if __name__ == "__main__":
    print("Bot berjalan...")
    bot.polling(none_stop=True)
