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
    PRIMARY KEY ("word_id", "translation_id"),
    FOREIGN KEY("word_id") REFERENCES "words"("id")
    ON DELETE CASCADE,
    FOREIGN KEY("translation_id") REFERENCES "translations"("id") 
    ON DELETE CASCADE
);

-- 'foreign' words next to their translation, i.e. dictionary itself
CREATE VIEW IF NOT EXISTS "dictionary" AS 
SELECT "name" AS 'word', "meaning" FROM "words"
JOIN "translate" ON "words"."id" = "translate"."word_id"
JOIN "translations" ON "translate"."translation_id" = "translations"."id";

-- auto-insert values into all tables only by given word and it's translation 
CREATE TRIGGER IF NOT EXISTS "insert"
INSTEAD OF INSERT ON "dictionary"
FOR EACH ROW 
BEGIN
    --insert word
    INSERT INTO "words"("name")
    VALUES (NEW."word")
    ON CONFLICT ("name") DO NOTHING;
    -- insert meaning
    INSERT INTO "translations"("meaning")
    VALUES (NEW."meaning")
    ON CONFLICT ("meaning") DO NOTHING;
    -- insert bindings
    INSERT INTO "translate"("word_id", "translation_id")
    VALUES ((
        SELECT "id" FROM "words"
        WHERE "name" = (NEW."word")
        ), (
        SELECT "id" FROM "translations"
        WHERE "meaning" = (NEW."meaning")
        )
    )
    ON CONFLICT ("word_id", "translation_id") DO NOTHING;

END;



