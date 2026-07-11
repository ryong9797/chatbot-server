from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    try:
        # 카카오에서 파라미터 가져오기
        params = req.get('action', {}).get('parameters', {})
        item = params.get('item', {}).get('value')
        if not item:
            item = params.get('item') # 만약 value가 없다면 직접 접근

        url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/data_{item}.json"
        res = requests.get(url)
        
        if res.status_code == 200:
            data = res.json()
            # 데이터 파일의 kpi 안에 있는 "가격" 항목을 정확히 가져옵니다
            price = data.get('kpi', {}).get('가격', '정보 없음')
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [{"simpleText": {"text": f"{item}의 가격은 {price}원입니다."}}]
                }
            })
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "데이터 파일을 찾을 수 없습니다."}}]}})
    except Exception as e:
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "오류 발생"}}]}})

if __name__ == '__main__':
    app.run()
