DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

-- the user store
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

-- the interest categories
CREATE TABLE category(
    cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cat_name VARCHAR(50) UNIQUE
);

-- the interest/ user

CREATE TABLE interests(
    int_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER FOREIGN KEY REFERENCES user(id),
    cat_id INTEGER FOREIGN KEY REFERENCES category(cat_id),
    interest_name VARCHAR(256),
    weight INTEGER DEFAULT 1
)


