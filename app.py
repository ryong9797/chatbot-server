from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    try:
        # 카카오에서 item 파라미터 추출
        params = req.get('action', {}).get('parameters', {})
        item = params.get('item', {}).get('value')
        
        # 파일 주소
        url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/data_{item}.json"
        res = requests.get(url)
        
        if res.status_code == 200:
            data = res.json()
            # 데이터 파일의 kpi 안에 있는 "가격"을 가져옵니다.
            # 만약 이게 안되면, 단순히 data['kpi']['가격']으로 직접 접근합니다.
            price = data['kpi']['가격'] 
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [{"simpleText": {"text": f"{item}의 가격은 {price}원입니다."}}]
                }
            })
        else:
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "파일을 찾을 수 없습니다."}}]}})
    except Exception as e:
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"오류 발생: {str(e)}"}}]}})

if __name__ == '__main__':
    app.run()
