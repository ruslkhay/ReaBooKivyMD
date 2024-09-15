from new_database import DataBase


if __name__ == "__main__":
    db = DataBase(path="app", schema="app/database/new_schema.sql")
    db.insert("dictionary", {"title": "serbian", "background_image": ""})
    db.insert("content", {"id_dict": 1, "word": "hello", "meaning": "привет"})
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
    # print(db.search(pattern="и"))
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
    db.delete_all()
