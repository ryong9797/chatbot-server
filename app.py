from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    try:
        item = req['action']['parameters']['item']['value']
        url = f"https://ryong9797.github.io/icb10proj2/weather-data/report/api/data_{item}.json"
        response = requests.get(url)
        data = response.json()
        price = data.get('price', '정보 없음')
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"{item}의 가격은 {price}원입니다."}}]}})
    except:
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "데이터를 불러올 수 없습니다."}}]}})

if __name__ == '__main__':
    app.run()
