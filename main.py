from tg_API.core import bot
from database.common.models import db, HistorySummary, HistorySearch


if __name__ == "__main__":
    db.create_tables([HistorySearch, HistorySummary])
    bot.infinity_polling()

