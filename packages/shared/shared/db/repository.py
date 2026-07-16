from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from datetime import datetime

import psycopg
from psycopg.rows import dict_row

from shared.config import DATABASE_URL

SENTIMENT_LABELS = {0: "positive", 1: "negative", 2: "neutral"}


@dataclass
class AnalysisRecord:
    platform: str
    platform_chat_id: str
    chat_name: str
    platform_user_id: str
    user_name: str
    platform_message_id: str
    raw_text: str
    cleaned_text: str | None = None
    is_useful: bool | None = None
    usefulness_confidence: float | None = None
    sentiment: str | None = None
    sentiment_confidence: float | None = None
    problem_category: str | None = None
    problem_confidence: float | None = None
    is_critical: bool = False


class StatsRepository:
    """Репозиторий PostgreSQL для сообщений и результатов анализа."""

    def __init__(self, database_url: str | None = None) -> None:
        self._database_url = database_url or DATABASE_URL
        self._connected = False

    def connect(self) -> None:
        with psycopg.connect(self._database_url) as conn:
            conn.execute("SELECT 1")
        self._connected = True

    def ping(self) -> bool:
        try:
            with psycopg.connect(self._database_url) as conn:
                conn.execute("SELECT 1")
            return True
        except psycopg.Error:
            return False

    def save_batch(self, records: list[AnalysisRecord]) -> None:
        if not records:
            return

        with psycopg.connect(self._database_url) as conn:
            for record in records:
                self._save_record(conn, record)
            conn.commit()

    def _save_record(self, conn: psycopg.Connection, record: AnalysisRecord) -> None:
        chat_id = self._upsert_chat(conn, record)
        user_id = self._upsert_user(conn, record)
        message_id = self._upsert_message(conn, record, chat_id, user_id)
        self._upsert_analysis(conn, record, message_id)

    def _upsert_chat(self, conn: psycopg.Connection, record: AnalysisRecord) -> int:
        row = conn.execute(
            """
            INSERT INTO chats (platform, platform_chat_id, chat_name)
            VALUES (%s, %s, %s)
            ON CONFLICT (platform, platform_chat_id)
            DO UPDATE SET chat_name = EXCLUDED.chat_name
            RETURNING id
            """,
            (record.platform, record.platform_chat_id, record.chat_name),
        ).fetchone()
        return row[0]

    def _upsert_user(self, conn: psycopg.Connection, record: AnalysisRecord) -> int:
        row = conn.execute(
            """
            INSERT INTO users (platform, platform_user_id, user_name, message_count)
            VALUES (%s, %s, %s, 1)
            ON CONFLICT (platform, platform_user_id)
            DO UPDATE SET
                user_name = EXCLUDED.user_name,
                message_count = users.message_count + 1
            RETURNING id
            """,
            (record.platform, record.platform_user_id, record.user_name),
        ).fetchone()
        return row[0]

    def _upsert_message(
        self,
        conn: psycopg.Connection,
        record: AnalysisRecord,
        chat_id: int,
        user_id: int,
    ) -> int:
        row = conn.execute(
            """
            INSERT INTO messages (chat_id, user_id, platform_message_id, raw_text, cleaned_text)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (chat_id, platform_message_id)
            DO UPDATE SET
                raw_text = EXCLUDED.raw_text,
                cleaned_text = EXCLUDED.cleaned_text
            RETURNING id
            """,
            (
                chat_id,
                user_id,
                record.platform_message_id,
                record.raw_text,
                record.cleaned_text,
            ),
        ).fetchone()
        return row[0]

    def _upsert_analysis(
        self,
        conn: psycopg.Connection,
        record: AnalysisRecord,
        message_id: int,
    ) -> None:
        conn.execute(
            """
            INSERT INTO analysis_results (
                message_id,
                is_useful,
                usefulness_confidence,
                sentiment,
                sentiment_confidence,
                problem_category,
                problem_confidence,
                is_critical
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (message_id)
            DO UPDATE SET
                is_useful = EXCLUDED.is_useful,
                usefulness_confidence = EXCLUDED.usefulness_confidence,
                sentiment = EXCLUDED.sentiment,
                sentiment_confidence = EXCLUDED.sentiment_confidence,
                problem_category = EXCLUDED.problem_category,
                problem_confidence = EXCLUDED.problem_confidence,
                is_critical = EXCLUDED.is_critical,
                analyzed_at = CURRENT_TIMESTAMP
            """,
            (
                message_id,
                record.is_useful,
                record.usefulness_confidence,
                record.sentiment,
                record.sentiment_confidence,
                record.problem_category,
                record.problem_confidence,
                record.is_critical,
            ),
        )


    def get_local_chat_id(self, chat_id: str) -> int:
            """
            Преобразование глобального чат айди в локальный
            
            Вызывать везде, где фигурирует локальный чат айди
            """
        
            query = """
            SELECT 
                id
                FROM chats
                WHERE platform_chat_id = %s
            """

            with psycopg.connect(self._database_url, row_factory=dict_row) as conn:
                try:
                    row = conn.execute(query, (chat_id,)).fetchone()
                    print(row)
                    print(type(row))
                    chat_id_local = row['id'] #Тут нужно при неправильном айди присылать соответствующий ответ

                    return chat_id_local

                except Exception as e:
                    print(f"Некорректный айди: {e}")
                    raise

                
    
    def _get_where_clause(self, chat_id: int, date_from: datetime, date_to: datetime) -> tuple[str, tuple]:
        """Вспомогательный метод для формирования условия WHERE"""
        return "m.chat_id = %s AND ar.analyzed_at BETWEEN %s AND %s" , (chat_id, date_from, date_to)
        

    def get_sentiment_distribution(self, chat_id_global: str, date_from: datetime, date_to: datetime) -> dict[str, float]:
        """Проценты настроений для Pie-диаграммы"""
        
        chat_id = self.get_local_chat_id(chat_id_global)
        where, params = self._get_where_clause(chat_id, date_from, date_to)
        query = f"""
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE ar.sentiment = 'positive') AS positive,
                COUNT(*) FILTER (WHERE ar.sentiment = 'negative') AS negative,
                COUNT(*) FILTER (WHERE ar.sentiment = 'neutral') AS neutral
            FROM messages m
            JOIN analysis_results ar ON ar.message_id = m.id
            WHERE {where}
        """

        with psycopg.connect(self._database_url, row_factory=dict_row) as conn:
            row = conn.execute(query, params).fetchone()

        if not row or row["total"] == 0:
            return {"positive": 0.0, "negative": 0.0, "neutral": 0.0}

        total = row["total"]
        return {
            "positive": row["positive"],
            "negative": row["negative"],
            "neutral": row["neutral"],
        }

    def get_sentiment_by_day(self, chat_id_global: str, date_from: datetime, date_to: datetime) -> list[dict[str, Any]]:
        """Массив настроений по дням для гистограммы"""
        
        chat_id = self.get_local_chat_id(chat_id_global)
        where, params = self._get_where_clause(chat_id, date_from, date_to)
        query = f"""
            SELECT
                DATE(m.created_at) AS stat_date,
                COUNT(*) FILTER (WHERE ar.sentiment = 'positive') AS positive,
                COUNT(*) FILTER (WHERE ar.sentiment = 'negative') AS negative,
                COUNT(*) FILTER (WHERE ar.sentiment = 'neutral') AS neutral
            FROM messages m
            JOIN analysis_results ar ON ar.message_id = m.id
            WHERE {where}
            GROUP BY DATE(m.created_at)
            ORDER BY stat_date
        """

        with psycopg.connect(self._database_url, row_factory=dict_row) as conn:
            rows = conn.execute(query, params).fetchall()

        # Конвертируем date в строку для корректной сериализации в JSON
        return [
            {
                "date": row["stat_date"].isoformat(),
                "positive": row["positive"],
                "negative": row["negative"],
                "neutral": row["neutral"]
            }
            for row in rows
        ]

    def get_problem_categories(self, chat_id_global: str, date_from: datetime, date_to: datetime) -> list[dict[str, Any]]:
        """Массив категорий проблем для диаграммы"""
        
        chat_id = self.get_local_chat_id(chat_id_global)
        # Если chat_id есть, фильтруем по нему. Если нет - берем все.
        where, params = self._get_where_clause(chat_id, date_from, date_to)
        query = f"""
            SELECT
                ar.problem_category,
                COUNT(*) AS count
            FROM messages m
            JOIN analysis_results ar ON ar.message_id = m.id
            WHERE {where} AND ar.problem_category IS NOT NULL
            GROUP BY ar.problem_category
            ORDER BY count DESC
        """

        with psycopg.connect(self._database_url, row_factory=dict_row) as conn:
            rows = conn.execute(query, params).fetchall()

        return [{"category": row["problem_category"], "count": row["count"]} for row in rows]

    def get_top_users(self, chat_id_global: str, date_from: datetime, date_to: datetime) -> dict[str, list[dict[str, Any]]]:
        """Топ пользователей: самые активные, позитивные и негативные"""
        
        chat_id = self.get_local_chat_id(chat_id_global)
        where, params = self._get_where_clause(chat_id, date_from, date_to)

        # 1. Самые активные (по общему кол-ву сообщений)
        q_active = f"""
            SELECT u.id AS user_id, u.user_name, COUNT(m.id) AS count
            FROM messages m
            JOIN users u ON u.id = m.user_id
            JOIN analysis_results ar ON m.id = ar.message_id
            WHERE {where}
            GROUP BY u.id, u.user_name
            ORDER BY count DESC LIMIT 10
        """

        # 2. Самые позитивные (по кол-ву сообщений с sentiment='positive')
        q_positive = f"""
            SELECT u.id AS user_id, u.user_name, COUNT(m.id) AS count
            FROM messages m
            JOIN users u ON u.id = m.user_id
            JOIN analysis_results ar ON ar.message_id = m.id
            WHERE {where} AND ar.sentiment = 'positive'
            GROUP BY u.id, u.user_name
            ORDER BY count DESC LIMIT 10
        """

        # 3. Самые негативные (по кол-ву сообщений с sentiment='negative')
        q_negative = f"""
            SELECT u.id AS user_id, u.user_name, COUNT(m.id) AS count
            FROM messages m
            JOIN users u ON u.id = m.user_id
            JOIN analysis_results ar ON ar.message_id = m.id
            WHERE {where} AND ar.sentiment = 'negative'
            GROUP BY u.id, u.user_name
            ORDER BY count DESC LIMIT 10
        """

        with psycopg.connect(self._database_url, row_factory=dict_row) as conn:
            active = conn.execute(q_active, params).fetchall()
            positive = conn.execute(q_positive, params).fetchall()
            negative = conn.execute(q_negative, params).fetchall()

        return {
            "most_active": [dict(row) for row in active],
            "most_positive": [dict(row) for row in positive],
            "most_negative": [dict(row) for row in negative],
        }
    
    def get_chat_stats(self, chat_global_id: str | None = None) -> dict[str, Any]:
        # Базовая часть запроса одинакова для обоих случаев
        
        chat_id = self.get_local_chat_id(chat_id=chat_global_id)
        base_query = """
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE ar.is_useful = true) AS useful_count,
                COUNT(*) FILTER (WHERE ar.is_useful = false) AS useless_count,
                COUNT(*) FILTER (WHERE ar.sentiment = 'positive') AS positive_count,
                COUNT(*) FILTER (WHERE ar.sentiment = 'negative') AS negative_count,
                COUNT(*) FILTER (WHERE ar.sentiment = 'neutral') AS neutral_count,
                COUNT(*) FILTER (WHERE ar.is_critical = true) AS critical_count,
                COUNT(DISTINCT m.user_id) AS unique_users
            FROM messages m
            JOIN analysis_results ar ON ar.message_id = m.id
            JOIN chats c ON c.id = m.chat_id
        """

        with psycopg.connect(self._database_url, row_factory=dict_row) as conn:
            try:
                if chat_id is None:
                    # Случай 1: Статистика по ВСЕМ чатам
                    query = base_query
                    params = ()
                    print("Executing query for ALL chats")
                else:
                    # Случай 2: Статистика по КОНКРЕТНОМУ чату.
                    # ВАЖНО: Мы сравниваем с c.id (BIGINT), так как chat_id у нас int!
                    query = base_query + "\nWHERE c.id = %s"
                    params = (chat_id,)
                    print(f"Executing query for chat_id={chat_id}")

                # --- ОТЛАДОЧНЫЙ ВЫВОД (поможет увидеть правду) ---
                print("\n[DEBUG] SQL Query:")
                print(query)
                print(f"[DEBUG] Params: {params}\n")
                # -------------------------------------------------

                row = conn.execute(query, params).fetchone()

                if row is None:
                    return self._empty_stats(chat_id)

                return {
                    "chat_id": chat_id,
                    "total": int(row["total"]),
                    "useful_count": int(row["useful_count"]),
                    "useless_count": int(row["useless_count"]),
                    "positive_count": int(row["positive_count"]),
                    "negative_count": int(row["negative_count"]),
                    "neutral_count": int(row["neutral_count"]),
                    "critical_count": int(row["critical_count"]),
                    "unique_users": int(row["unique_users"]),
                }

            except Exception as e:
                print(f"Database error in get_chat_stats: {e}")
                raise

    @staticmethod
    def _empty_stats(chat_id: int | None) -> dict[str, Any]:
        return {
            "chat_id": chat_id,
            "total": 0,
            "useful_count": 0,
            "useless_count": 0,
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0,
            "critical_count": 0,
            "unique_users": 0,
        }
