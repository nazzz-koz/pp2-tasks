try:
    import psycopg2
    import psycopg2.extras
    _PSYCOPG2_AVAILABLE = True
except ImportError:
    _PSYCOPG2_AVAILABLE = False

DB_CONFIG = dict(
    host="localhost",
    port=5432,
    dbname="snake_game",
    user="postgres",
    password="1234",
)

_conn = None


def _get_conn():
    global _conn
    if not _PSYCOPG2_AVAILABLE:
        return None
    try:
        if _conn is None or _conn.closed:
            _conn = psycopg2.connect(**DB_CONFIG)
        return _conn
    except Exception as e:
        print(f"[DB] Connection failed: {e}")
        return None


def init_db():
    conn = _get_conn()
    if conn is None:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id       SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id            SERIAL PRIMARY KEY,
                    player_id     INTEGER REFERENCES players(id),
                    score         INTEGER   NOT NULL,
                    level_reached INTEGER   NOT NULL,
                    played_at     TIMESTAMP DEFAULT NOW()
                );
            """)
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB] init_db error: {e}")
        conn.rollback()
        return False


def get_or_create_player(username: str) -> int | None:
    conn = _get_conn()
    if conn is None:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM players WHERE username = %s", (username,))
            row = cur.fetchone()
            if row:
                return row[0]
            cur.execute(
                "INSERT INTO players (username) VALUES (%s) RETURNING id", (username,)
            )
            pid = cur.fetchone()[0]
        conn.commit()
        return pid
    except Exception as e:
        print(f"[DB] get_or_create_player error: {e}")
        conn.rollback()
        return None


def save_session(player_id: int, score: int, level_reached: int) -> bool:
    conn = _get_conn()
    if conn is None or player_id is None:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO game_sessions (player_id, score, level_reached) "
                "VALUES (%s, %s, %s)",
                (player_id, score, level_reached),
            )
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB] save_session error: {e}")
        conn.rollback()
        return False


def get_personal_best(player_id: int) -> int:
    conn = _get_conn()
    if conn is None or player_id is None:
        return 0
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COALESCE(MAX(score), 0) FROM game_sessions WHERE player_id = %s",
                (player_id,),
            )
            return cur.fetchone()[0]
    except Exception as e:
        print(f"[DB] get_personal_best error: {e}")
        return 0


def get_top10() -> list[dict]:
    conn = _get_conn()
    if conn is None:
        return []
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT p.username,
                       gs.score,
                       gs.level_reached,
                       gs.played_at::date AS date
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC
                LIMIT 10;
            """)
            return [dict(r) for r in cur.fetchall()]
    except Exception as e:
        print(f"[DB] get_top10 error: {e}")
        return []
