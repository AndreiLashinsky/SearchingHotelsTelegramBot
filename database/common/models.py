from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase('database.db')


class BaseModel(pw.Model):
    id = pw.PrimaryKeyField()
    tg_id = pw.IntegerField()
    created_at = pw.DateField(default=datetime.now())

    class Meta:
        database = db
        order_by = 'tg_id'


class HistorySearch(BaseModel):
    search_settings = pw.CharField()

    class Meta:
        db_table = 'Requests'


class HistorySummary(BaseModel):
    summary_id = pw.IntegerField()
    hotel_link = pw.CharField()

    class Meta:
        db_tabel = 'Summaries'




