if __name__ == "__main__":
    from database import DataBase
    from pathlib import Path

    db = DataBase(path=Path("app"), schema=Path("./app/database/schema.sql"))
    db.delete_all()

    db.insert("dictionary", {"title": "serbian", "background_image": ""})
    db.insert("content", {"id_dict": 1, "word": "zdravo", "meaning": "привет"})
    db.insert("content", {"id_dict": 1, "word": "druze", "meaning": "дружище"})
    # db.insert("content", {"id_dict": 0, "word": "hello", "meaning": "привет"})
    # db.insert("content", {"id_dict": 0, "word": "world", "meaning": "мир"})
    # db.insert("content", {"id_dict": 0, "word": "I", "meaning": "я"})
    # db.insert("content", {"id_dict": 0, "word": "am", "meaning": ""})
    # db.insert("content", {"id_dict": 0, "word": "in", "meaning": "в"})
    # db.insert("content", {"id_dict": 0, "word": "airport", "meaning": "аэропорт"})
    print(db.select_from(table="content"))
    print(db.select_from(table="statistics"))
    print(db.select_from(table="dictionary"))
    # print(db.search(pattern="h"))
    # print(db.search())
    # print(db.select_to_dicts("select card_id, word from content;"))
    print(db.search(pattern="и"))
    # print(db.search(pattern="a"))
    # db.update(
    #     card_id=3,
    #     values={
    #         "example": "I wrote few examples for future generation",
    #         "meaning": "Я",
    #     },
    # )
    #     # db.hard_delete(card_id=1)
    #     print(db.select_from(table="content"))

    # db.hard_delete("dictionary", 1)
