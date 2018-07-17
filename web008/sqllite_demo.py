# coding: utf-8
import sqlite3


def create(conn):
    sql_create = '''
    CREATE TABLE `users` (
          `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
          `username` TEXT NOT NULL UNIQUE,
          `password` TEXT NOT NULL,
          email TEXT
    )
    '''
    conn.execute(sql_create)
    print('创建成功！')


def insert(conn, username, password, email):
    sql_insert = '''
    INSERT INTO
        users(username, password, email)
    VALUES
        (?, ?, ?)
    '''
    conn.execute(sql_insert, (username, password, email))
    print('插入数据成功')


def select(conn):
    sql = '''
    SELECT
        id
    FROM
        users
    WHERE
        id = 1
    '''
    cursor = conn.execute(sql)
    print('所有数据', list(cursor))
    # for row in cursor:
    #     print(row)


def delete(conn, user_id):
    sql_delete = '''
    DELETE FROM
        users
    WHERE 
        id=?
    '''
    conn.execute(sql_delete, (user_id))


def update(conn, user_id, email):
    sql_update = '''
    UPDATE
        `users`
    SET
        `email`=?
    WHERE
        `id`=?
    '''
    conn.execute(sql_update, (email, user_id))


def main():
    db_path = 'web8.sqlite'
    conn = sqlite3.connect(db_path)
    print('打开了数据库')

    create(conn)
    # insert(conn, 'sql4', '1234', 'a@b.c')
    # delete(conn, 1)
    # update(conn, 1, 'haha@163.com')
    # select(conn)

    # 用 commit 函数提交修改，否则将不会被写入到数据库中
    conn.commit()
    # 用完之后要关闭
    conn.close()


if __name__ == '__main__':
    main()
