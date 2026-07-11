from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    try:
        # 카카오 파라미터에서 item 값을 가져옵니다.
        item = req.get('action', {}).get('parameters', {}).get('item', {}).get('value')
        
        # 파일 주소
        url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/data_{item}.json"
        res = requests.get(url)
        
        if res.status_code == 200:
            data = res.json()
            
            # [최종 수정] kpi 안의 '가격'을 찾되, 없으면 데이터 전체를 출력하도록 디버깅
            price = data.get('kpi', {}).get('가격')
            
            if price is None:
                return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"데이터는 찾았으나 가격 항목이 없습니다. 전체 데이터: {data}"}}]}})
            
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"{item}의 가격은 {price}원입니다."}}]}})
        else:
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"파일을 찾을 수 없습니다."}}]}})
    except Exception as e:
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"에러: {str(e)}"}}]}})

if __name__ == '__main__':
    app.run()
