-- table represented specific card set
CREATE TABLE IF NOT EXISTS "dictionary"(
    "id" INTEGER PRIMARY KEY,
    "title" TEXT NOT NULL UNIQUE,
    "background_image" TEXT
);

-- table for storing flashcard
CREATE TABLE IF NOT EXISTS "content"(
    "card_id" INTEGER PRIMARY KEY,
    "id_dict" INTEGER,  -- GUI filled.
    "word" TEXT NOT NULL,
    "meaning" TEXT NOT NULL,
    "example" TEXT DEFAULT NULL,
    "image" TEXT DEFAULT NULL,
    -- "deleted" INTEGER DEFAULT 0,
    FOREIGN KEY("id_dict") REFERENCES "dictionary"("id")
    ON DELETE CASCADE,
    UNIQUE("word", "meaning")
);

-- table for storing statistic of the specific card
-- Insert values only when new card is being learned first time on 
-- study screen.
CREATE TABLE IF NOT EXISTS "statistics"(
    "card_id" INTEGER,
    "date_added" TEXT DEFAULT CURRENT_TIMESTAMP,
    "right_guesses" INTEGER DEFAULT 0,
    "wrong_guesses" INTEGER DEFAULT 0,
    FOREIGN KEY("id") REFERENCES "content"("id")
    ON DELETE CASCADE
);