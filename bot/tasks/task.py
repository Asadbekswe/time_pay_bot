import asyncio
import random
from datetime import datetime, timezone, timedelta

from aiogram import Bot
from inspirational_quotes import quote as get_quote
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database.base import db
from database.models import Comment

UZBEK_TZ = timezone(timedelta(hours=5))


async def reminder_worker(bot: Bot):
    while True:
        now = datetime.now(UZBEK_TZ)

        # bitta so'rovda comment + lead ni yuklaymiz (joined eager load)
        result = await db.execute(select(Comment).options(joinedload(Comment.lead)))
        comments = result.scalars().all()

        due_comments = []
        for c in comments:
            # agar sana yoki vaqt bo'lmasa — o'tkazib yubor
            if not c.reminder_date or not c.reminder_time:
                continue

            # reminder_date may be datetime or date
            rd = c.reminder_date
            if isinstance(rd, datetime):
                rd_date = rd.date()
            else:
                rd_date = rd

            rt = c.reminder_time
            # rt expected to be datetime.time (or time-like)
            # birlashtiramiz va timezone qo'shamiz
            try:
                reminder_dt = datetime.combine(rd_date, rt)
            except Exception:
                # noto'g'ri format bo'lsa, o'tkazib yubor
                continue

            if reminder_dt.tzinfo is None:
                reminder_dt = reminder_dt.replace(tzinfo=UZBEK_TZ)
            else:
                reminder_dt = reminder_dt.astimezone(UZBEK_TZ)

            if reminder_dt <= now:
                due_comments.append((c, reminder_dt))

        for comment, reminder_dt in due_comments:
            try:
                # operator idni olamiz (lead orqali)
                operator_id = getattr(comment.lead, "operator_id", None)
                if not operator_id:
                    # operator yo'q bo'lsa, yuborilmadi
                    await Comment.delete(comment.id)
                    continue

                q = get_quote()
                quote_text = q.get("quote", "")
                quote_author = q.get("author", "Noma’lum")

                messages = [
                    (
                        f"⏰ Hey! Vaqt tugadi!\n\n"
                        f"📝 {comment.description}\n"
                        f"📅 {reminder_dt.strftime('%d.%m.%Y %H:%M')}\n\n"
                        f"🚀 Harakat qilish vaqti!\n\n"
                        f"💡 “{quote_text}” — {quote_author}"
                    ),
                    (
                        f"🔔 Qo‘ng‘iroq chalinmoqda!\n\n"
                        f"Bugungi vazifangiz: <b>{comment.description}</b>\n"
                        f"🕒 {reminder_dt.strftime('%d.%m.%Y %H:%M')}\n\n"
                        f"💡 Yodingizda bo‘lsin: {quote_text} — {quote_author}"
                    ),
                    (
                        f"🎯 Maqsad vaqti keldi!\n\n"
                        f"📝 {comment.description}\n"
                        f"📅 {reminder_dt.strftime('%d.%m.%Y %H:%M')}\n\n"
                        f"⚡ Orqaga surmang, hoziroq boshlang!\n\n"
                        f"💡 “{quote_text}” — {quote_author}"
                    ),
                ]

                await bot.send_message(operator_id, random.choice(messages), parse_mode="HTML")

                # yuborilgach commentni o'chiramiz
                await Comment.delete(comment.id)

            except Exception as e:
                # loglash uchun print; kerak bo'lsa logger bilan almashtiring
                print(f"Reminder error: {e}")

        await asyncio.sleep(60)
