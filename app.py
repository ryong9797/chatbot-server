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
        
        # 깃허브의 파일 주소
        url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/data_{item}.json"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            # 파일 안에 price만 있으니 그것만 가져옵니다!
            price = data.get('price', '정보 없음')
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [{"simpleText": {"text": f"{item}의 가격은 {price}원입니다."}}]
                }
            })
        else:
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "해당 농산물 데이터를 찾을 수 없습니다."}}]}})
    except Exception as e:
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "데이터 처리 중 오류가 발생했습니다."}}]}})

if __name__ == '__main__':
    app.run()
