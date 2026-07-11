from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    try:
        # 카카오가 보내는 단어(배추, 대파 등)를 가져옵니다.
        params = req.get('action', {}).get('parameters', {})
        item = params.get('item', {}).get('value')
        
        # 깃허브에 올린 파일 이름 규칙에 맞게 정확히 연결!
        url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/data_{item}.json"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            price = data.get('price', '정보 없음')
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"{item}의 가격은 {price}원입니다."}}]}})
        else:
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"{item}에 대한 데이터를 찾을 수 없습니다."}}]}})
    except Exception as e:
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "오류가 발생했습니다."}}]}})

if __name__ == '__main__':
    app.run()
