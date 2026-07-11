from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    # 1. 카카오에서 받은 파라미터를 로그로 출력 (Render Logs에서 확인 가능)
    print(f"카카오 요청 데이터: {req}")
    
    try:
        params = req.get('action', {}).get('parameters', {})
        # item 값을 가져옵니다
        item = params.get('item', {}).get('value')
        
        if not item:
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "파라미터 item을 찾을 수 없습니다."}}]}})
        
        url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/data_{item}.json"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            price = data.get('kpi', {}).get('가격', data.get('price', '정보 없음'))
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"{item}의 가격은 {price}원입니다."}}]}})
        else:
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"파일 data_{item}.json을 찾을 수 없습니다."}}]}})
    except Exception as e:
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"오류: {str(e)}"}}]} })

if __name__ == '__main__':
    app.run()
