from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    try:
        # 카카오에서 넘어오는 파라미터 값 추출
        action = req.get('action', {})
        params = action.get('parameters', {})
        item = params.get('item', {}).get('value')
        
        # 만약 item이 없다면, detailParams에서도 찾아봅니다.
        if not item:
            item = action.get('detailParams', {}).get('item', {}).get('value')

        if not item:
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "상품명을 인식하지 못했습니다."}}]}})

        url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/data_{item}.json"
        res = requests.get(url)
        
        if res.status_code == 200:
            data = res.json()
            price = data.get('kpi', {}).get('가격', '정보 없음')
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"{item}의 가격은 {price}원입니다."}}]}})
        else:
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"{item} 데이터를 찾을 수 없습니다."}}]}})
    except Exception as e:
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"Error: {str(e)}"}} ]}})

if __name__ == '__main__':
    app.run()
