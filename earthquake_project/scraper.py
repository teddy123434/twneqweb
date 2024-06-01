# 自AjaxHandler中抓取資料，自json提取資料存入sqlite中
import requests, json, sqlite3

params = {
    'draw': 14,
    'columns[0][data]': 0,
    'columns[0][name]': 'EventNo',
    'columns[0][searchable]': False,
    'columns[0][orderable]': True,
    'columns[0][search][value]': '',
    'columns[0][search][regex]': False,
    'columns[1][data]': 1,
    'columns[1][name]': 'MaxIntensity',
    'columns[1][searchable]': True,
    'columns[1][orderable]': True,
    'columns[1][search][value]': '',
    'columns[1][search][regex]': False,
    'columns[2][data]': 2,
    'columns[2][name]': 'OriginTime',
    'columns[2][searchable]': True,
    'columns[2][orderable]': True,
    'columns[2][search][value]': '',
    'columns[2][search][regex]': False,
    'columns[3][data]': 3,
    'columns[3][name]': 'MagnitudeValue',
    'columns[3][searchable]': True,
    'columns[3][orderable]': True,
    'columns[3][search][value]': '',
    'columns[3][search][regex]': False,
    'columns[4][data]': 4,
    'columns[4][name]': 'Depth',
    'columns[4][searchable]': True,
    'columns[4][orderable]': True,
    'columns[4][search][value]': '',
    'columns[4][search][regex]': False,
    'columns[5][data]': 5,
    'columns[5][name]': 'Description',
    'columns[5][searchable]': True,
    'columns[5][orderable]': True,
    'columns[5][search][value]': '',
    'columns[5][search][regex]': False,
    'columns[6][data]': 6,
    'columns[6][name]': 'Description',
    'columns[6][searchable]': True,
    'columns[6][orderable]': True,
    'columns[6][search][value]': '',
    'columns[6][search][regex]': False,
    'order[0][column]': 2,
    'order[0][dir]': 'desc',
    'start': 0,
    'length': -1,
    'search[value]': '',
    'search[regex]': False,
    'Search': '',
    'txtSDate': '2024-4-1',
    'txtEDate': '2024-5-31',
    'txtSscale': '',
    'txtEscale': '',
    'txtSdepth': '',
    'txtEdepth': '',
    'txtLonS': '',
    'txtLonE': '',
    'txtLatS': '',
    'txtLatE': '',
    'ddlCity': '',
    'ddlTown': '',
    'ddlCitySta': '',
    'ddlStation': '',
    'txtIntensityB': '',
    'txtIntensityE': '',
    'txtLon': '',
    'txtLat': '',
    'txtKM': '',
    'ddlStationName': '------',
    'cblEventNo': '',
    'txtSDatePWS': '',
    'txtEDatePWS': '',
    'txtSscalePWS': '',
    'txtEscalePWS': '',
    'ddlMark': ''
}

# 發送 POST 請求
url = "https://scweb.cwa.gov.tw/zh-tw/earthquake/ajaxhandler"  # 替換為實際的 URL
response = requests.post(url, data=params)

# 解析回應
data = response.json()  # 假設回應是 JSON 格式
json_data = json.dumps(data, indent=2, ensure_ascii=False)
db_path = '/workspaces/twneqweb/earthquake_project/data/earthquakes.db'

def test():
    print(type(data))
    print(data['data'])

def check_db_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        print("Database connection successful.")
    except sqlite3.Error as e:
        print(f"Database connection failed. Error: {e}")
    finally:
        if conn:
            conn.close()

def save_to_db(data):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS earthquakes 
              (id TEXT PRIMARY KEY,
              eq_id TEXT,
              date TEXT,
              magnitude REAL,
              depth REAL,
              location TEXT,
              MaxIntensity TEXT,
              Lon REAL,
              Lat REAL
              )''')

    for eq in data['data']:
        id = eq[0] if eq[0] else None
        eq_id = eq[1] if eq[1] else "小區域有感地震"
        date = eq[2]
        magnitude = float(eq[3])
        depth = float(eq[4])
        location = eq[5]
        MaxIntensity = eq[6]
        Lon = float(eq[7])
        Lat = float(eq[8])

        c.execute('''
                  INSERT OR IGNORE INTO earthquakes 
                  (id, eq_id, date, magnitude, depth, location, MaxIntensity, Lon, Lat) VALUES (?,?,?,?,?,?,?,?,?)''',
                    (id,eq_id,date, magnitude, depth, location, MaxIntensity, Lon, Lat))
    
    conn.commit()
    conn.close()

check_db_connection(db_path)
#test()
save_to_db(data)
