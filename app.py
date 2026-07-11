from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    try:
        # 카카오가 보내는 데이터 구조에서 item 값을 아주 끈질기게 찾아봅니다
        action = req.get('action', {})
        params = action.get('detailParams', {}).get('item', {}) # detailParams에서 찾아봅니다
        item = params.get('value')
        
        # 만약 여기서도 안 나오면 parameters에서 다시 시도
        if not item:
            item = req.get('action', {}).get('parameters', {}).get('item')

        if not item:
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "상품명을 인식하지 못했습니다. 설정(파라미터/엔티티)을 다시 확인해주세요."}}]}})
        
        # 데이터 호출
        url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/data_{item}.json"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            price = data.get('kpi', {}).get('가격', data.get('price', '정보 없음'))
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"{item}의 가격은 {price}원입니다."}}]}})
        else:
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"{item} 데이터를 찾을 수 없습니다."}}]}})
    except Exception as e:
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "오류가 발생했습니다."}}]}})

if __name__ == '__main__':
    app.run()
