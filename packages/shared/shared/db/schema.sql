-- 1. Таблица ЧАТОВ
CREATE TABLE chats (
    id BIGSERIAL PRIMARY KEY,
    platform VARCHAR(10) NOT NULL CHECK (platform IN ('tg', 'max')),
    platform_chat_id VARCHAR(100) NOT NULL,
    chat_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_platform_chat UNIQUE (platform, platform_chat_id)
);

-- 2. Таблица ПОЛЬЗОВАТЕЛЕЙ
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    platform VARCHAR(10) NOT NULL CHECK (platform IN ('tg', 'max')),
    platform_user_id VARCHAR(100) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    message_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_platform_user UNIQUE (platform, platform_user_id)
);

-- 3. Таблица СООБЩЕНИЙ (без лемматизации)
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    platform_message_id VARCHAR(100) NOT NULL,
    raw_text TEXT NOT NULL,          -- Сырой текст
    cleaned_text TEXT,               -- Очищенный текст (без эмодзи, ссылок и т.д.)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_chat_platform_message UNIQUE (chat_id, platform_message_id)
);

-- 4. Таблица РЕЗУЛЬТАТОВ АНАЛИЗА (с учетом, что проблема может быть NULL)
CREATE TABLE analysis_results (
    id BIGSERIAL PRIMARY KEY,
    message_id BIGINT UNIQUE NOT NULL REFERENCES messages(id) ON DELETE CASCADE,

    -- Модель 1: Полезность (работает всегда)
    is_useful BOOLEAN,
    usefulness_confidence FLOAT,
    usefulness_model_version VARCHAR(20) DEFAULT '1.0.0',

    -- Модель 2: Настроение (работает всегда)
    sentiment VARCHAR(10) CHECK (sentiment IN ('positive', 'negative', 'neutral')),
    sentiment_confidence FLOAT,
    sentiment_model_version VARCHAR(20) DEFAULT '1.0.0',

    -- Модель 3: Проблема (работает НЕ всегда)
    problem_category VARCHAR(50),    -- Может быть NULL
    problem_confidence FLOAT,        -- Может быть NULL
    problem_model_version VARCHAR(20) DEFAULT '1.0.0',

    -- Общие поля
    is_critical BOOLEAN DEFAULT FALSE,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE daily_chat_stats (
    id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT REFERENCES chats(id) ON DELETE CASCADE,
    stat_date DATE NOT NULL,

    -- === БАЗОВЫЕ МЕТРИКИ ===
    total_messages INTEGER DEFAULT 0,
    unique_users INTEGER DEFAULT 0,
    messages_per_user FLOAT DEFAULT 0,

    -- === МЕТРИКИ ПОЛЕЗНОСТИ ===
    useful_messages INTEGER DEFAULT 0,
    not_useful_messages INTEGER DEFAULT 0,
    usefulness_rate FLOAT DEFAULT 0,  -- % полезных сообщений

    -- === МЕТРИКИ НАСТРОЕНИЯ ===
    positive_messages INTEGER DEFAULT 0,
    negative_messages INTEGER DEFAULT 0,
    neutral_messages INTEGER DEFAULT 0,
    sentiment_score FLOAT DEFAULT 0,  -- от -1 до 1

    -- === МЕТРИКИ ПРОБЛЕМ ===
    critical_messages INTEGER DEFAULT 0,
    messages_with_problem INTEGER DEFAULT 0,
    top_problems JSONB,  --  Храним топ-3 проблемы за день

    -- === ДОПОЛНИТЕЛЬНО ===
    peak_hour INTEGER,  -- час пик активности
    night_messages INTEGER DEFAULT 0,  -- сообщения ночью

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_chat_date UNIQUE (chat_id, stat_date)
);

-- Индексы
CREATE INDEX idx_messages_chat_id ON messages(chat_id);
CREATE INDEX idx_messages_created_at ON messages(created_at DESC);
CREATE INDEX idx_analysis_message_id ON analysis_results(message_id);
CREATE INDEX idx_analysis_is_useful ON analysis_results(is_useful) WHERE is_useful = true;
CREATE INDEX idx_analysis_sentiment ON analysis_results(sentiment) WHERE sentiment IS NOT NULL;
CREATE INDEX idx_analysis_problem ON analysis_results(problem_category) WHERE problem_category IS NOT NULL; --Индекс только для не-NULL
CREATE INDEX idx_analysis_critical ON analysis_results(is_critical) WHERE is_critical = true;