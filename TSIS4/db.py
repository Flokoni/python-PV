import psycopg2
from config import DB_CONFIG

def get_conn(): return psycopg2.connect(**DB_CONFIG)

def init_db():
    conn = get_conn(); cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS players (id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL);")
    cur.execute("""CREATE TABLE IF NOT EXISTS game_sessions (
        id SERIAL PRIMARY KEY, player_id INTEGER REFERENCES players(id),
        score INTEGER, level_reached INTEGER, played_at TIMESTAMP DEFAULT NOW());""")
    conn.commit(); cur.close(); conn.close()

def save_res(user, score, lvl):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (user,))
    cur.execute("SELECT id FROM players WHERE username = %s", (user,))
    pid = cur.fetchone()[0]
    cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", (pid, score, lvl))
    conn.commit(); cur.close(); conn.close()

def get_top():
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""SELECT p.username, s.score, s.level_reached FROM game_sessions s 
                   JOIN players p ON s.player_id = p.id ORDER BY s.score DESC LIMIT 10""")
    res = cur.fetchall(); cur.close(); conn.close()
    return res

def get_pb(user):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT MAX(score) FROM game_sessions s JOIN players p ON s.player_id = p.id WHERE p.username = %s", (user,))
    res = cur.fetchone()[0]
    cur.close(); conn.close()
    return res if res else 0