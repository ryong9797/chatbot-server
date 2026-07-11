from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    try:
        # 카카오 파라미터에서 값을 가져옵니다
        params = req.get('action', {}).get('parameters', {})
        item = params.get('item', {}).get('value')
        
        # [핵심] 주소를 refs/heads/를 뺀 표준 주소로 바꿉니다.
        # 이게 진짜 데이터가 있는 경로입니다.
        url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/data_{item}.json"
        
        res = requests.get(url)
        
        if res.status_code == 200:
            data = res.json()
            # 파일 구조에 맞게 '가격' 추출
            price = data.get('kpi', {}).get('가격', '정보 없음')
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [{"simpleText": {"text": f"{item}의 가격은 {price}원입니다."}}]
                }
            })
        else:
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"파일을 찾을 수 없습니다. (URL: {url})"}}]} })
    except Exception as e:
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"오류: {str(e)}"}}]}})

if __name__ == '__main__':
    app.run()
