from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    try:
        # 카카오에서 넘어온 값을 가져옵니다
        params = req.get('action', {}).get('parameters', {})
        item = params.get('item', {}).get('value')
        
        # 깃허브 주소 (파일 이름이 '감귤.json', '감자.json' 형태라고 가정)
        url =# 기존 주소에서 {item}.json 부분을 data_{item}.json으로 수정합니다.
url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/data_{item}.json"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # [수정된 부분] 
            # 1. 감귤처럼 kpi 안에 price가 있는 경우
            # 2. 혹은 그냥 price가 있는 경우를 모두 처리합니다.
            price = None
            if 'kpi' in data and 'price' in data['kpi']:
                price = data['kpi']['price']
            elif 'price' in data:
                price = data['price']
            else:
                price = '정보 없음'
            
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [{"simpleText": {"text": f"{item}의 현재 가격은 {price}원입니다."}}]
                }
            })
        else:
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"{item} 데이터를 찾을 수 없습니다."}}]}})
    except Exception as e:
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "데이터 처리 중 오류가 발생했습니다."}}]}})

if __name__ == '__main__':
    app.run()
