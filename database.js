const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('ideas.db');

db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS ideas (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      description TEXT,
      votes INTEGER DEFAULT 0
    )
  `);
});

module.exports = db;