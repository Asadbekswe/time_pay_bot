import asyncio
import random
from datetime import datetime, timezone, timedelta

from aiogram import Bot
from inspirational_quotes import quote as get_quote

from database.models import Note

UZBEK_TZ = timezone(timedelta(hours=5))


async def reminder_worker(bot: Bot):
    while True:
        now = datetime.now(UZBEK_TZ)
        notes = await Note.filter()

        due_notes = [n for n in notes if n.note_time.replace(tzinfo=UZBEK_TZ) <= now]

        for note in due_notes:
            try:
                q = get_quote()
                quote_text = q["quote"]
                quote_author = q.get("author", "Noma’lum")

                messages = [
                    lambda note: (
                        f"⏰ Hey! Vaqt tugadi!\n\n"
                        f"📝 {note.description}\n"
                        f"📅 {note.note_time.strftime('%d.%m.%Y %H:%M')}\n\n"
                        f"🚀 Harakat qilish vaqti!\n\n"
                        f"💡 “{quote_text}” — {quote_author}"
                    ),
                    lambda note: (
                        f"🔔 Qo‘ng‘iroq chalinmoqda!\n\n"
                        f"Bugungi vazifangiz: <b>{note.description}</b>\n"
                        f"🕒 {note.note_time.strftime('%d.%m.%Y %H:%M')}\n\n"
                        f"💡 Yodingizda bo‘lsin: {quote_text} — {quote_author}"
                    ),
                    lambda note: (
                        f"🎯 Maqsad vaqti keldi!\n\n"
                        f"📝 {note.description}\n"
                        f"📅 {note.note_time.strftime('%d.%m.%Y %H:%M')}\n\n"
                        f"⚡ Orqaga surmang, hoziroq boshlang!\n\n"
                        f"💡 “{quote_text}” — {quote_author}"
                    ),
                ]

                message = random.choice(messages)(note)
                await bot.send_message(note.operator_id, message)
                await Note.delete(note.id)

            except Exception as e:
                print(f"Reminder error: {e}")

        await asyncio.sleep(60)
