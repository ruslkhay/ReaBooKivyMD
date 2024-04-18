-- creates table for 'foreign' words
CREATE TABLE IF NOT EXISTS "words"(
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id")
);

-- creates table for word's translations 
CREATE TABLE IF NOT EXISTS "translations"(
    "id" INTEGER,
    "meaning" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id")
);

-- binding between previous tables
CREATE TABLE IF NOT EXISTS "translate"(
    "word_id" INTEGER,
    "translation_id" INTEGER,
    -- PRIMARY KEY ("word_id", "translation_id"),
    FOREIGN KEY("word_id") REFERENCES "words"("id")
    ON DELETE CASCADE,
    FOREIGN KEY("translation_id") REFERENCES "translations"("id") 
    ON DELETE CASCADE
);



-- CREATE TRIGGER "auto_translate_fill"
-- AFTER INSERT ON translations
-- BEGIN
--     INSERT INTO "translate"("word_id","translation_id")
--     VALUES ('')