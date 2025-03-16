from flask import render_template
from datetime import datetime


def setup_routes(app):
    # while True:
    #     try:
    #         conn = psycopg2.connect(database="postgresdb", user="postgres", password=os.environ.get("POSTGRES_PASSWORD"), host="postgres", port="5432")
    #         print("Opened database successfully", flush=True)
    #         break
    #     except Exception as e:
    #         print(e, flush=True)
    #         time.sleep(5)

    # cur = conn.cursor()

    # cur.execute("CREATE TABLE IF NOT EXISTS actuals (ts TIMESTAMP, value float);")
    # conn.commit()

    # cur.execute("SELECT * FROM actuals;")
    # if (cur.rowcount == 0):
    #     cur.execute("INSERT INTO actuals(ts, value) VALUES ('%s', 55) RETURNING *;" % datetime.now())
    #     conn.commit()

    @app.route("/")
    def index():
        # cur.execute("SELECT * FROM actuals;")
        # data = [{"date": d[0], "value": d[1]} for d in cur.fetchall()]
        data = [{"date": datetime.now(), "value": 55}]
        return render_template("table.html", title="Actuals", data=data)
