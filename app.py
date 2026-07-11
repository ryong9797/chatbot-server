from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    # 카카오 챗봇이 보낸 데이터 확인
    req = request.get_json()
    item = req['action']['parameters']['item']['value'] # '배추' 같은 단어
    
    # 깃허브 JSON 주소 (대표님 주소로 수정!)
    url = f"https://ryong9797.github.io/icb10proj2/weather-data/report/api/data_{item}.json"
    
    try:
        response = requests.get(url)
        data = response.json()
        price = data.get('price', '정보 없음')
        
        # 카카오톡에 보낼 답변 구성
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{"simpleText": {"text": f"{item}의 가격은 {price}원입니다."}}]
            }
        })
    except:
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "데이터를 불러오는 중 오류가 발생했습니다."}}]}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
