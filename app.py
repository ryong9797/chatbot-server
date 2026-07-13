"""
카카오톡 챗봇과 실시간 연동하여 농산물 가격 및 기상 요약 정보를 제공하는 Flask 서버입니다.
"""
from flask import Flask, request, jsonify
import requests
import os
import urllib.parse

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    try:
        action = req.get('action', {})
        detail_params = action.get('detailParams', {})
        params = action.get('params', {})
        
        item = None
        if 'item' in detail_params:
            item = detail_params.get('item', {}).get('value')
        elif 'item' in params:
            item = params.get('item')
        
        if not item:
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [{"simpleText": {"text": "조회할 품목을 선택하지 않았습니다."}}]
                }
            })
            
        # 품목명에서 "가격" 글자 정제
        item = item.replace("가격", "").strip()
            
        # 깃허브 JSON 파일 주소 생성
        encoded_item = urllib.parse.quote(item)
        url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/data_{encoded_item}.json"
        
        res = requests.get(url)
        
        if res.status_code == 200:
            data = res.json()
            
            # 1. 가격 트렌드에서 최신 가격 추출 (리스트의 가장 마지막 값)
            price_trends = data.get('price_trends', [])
            latest_price_str = "정보 없음"
            if price_trends and len(price_trends[0].get('data', [])) > 0:
                price_list = price_trends[0]['data']
                latest_price_str = f"{price_list[-1]:,}원"  # 숫자를 '30,295원' 형태로 변환
            
            # 2. KPI 딕셔너리에서 기상 및 변동률 정보 추출
            kpi = data.get('kpi', {})
            price_delta = kpi.get('price_delta', 0)
            avg_temp = kpi.get('avg_temp', '-')
            total_rain = kpi.get('total_rain', '-')
            
            # 가격 변동 방향 기호 처리
            if price_delta > 0:
                delta_str = f"▲{price_delta}% 상승"
            elif price_delta < 0:
                delta_str = f"▼{abs(price_delta)}% 하락"
            else:
                delta_str = "변동 없음"
            
            # 3. 조기 경보 메시지 추출
            warning_info = data.get('early_warning', {})
            warning_msg = ""
            if warning_info.get('active'):
                warning_msg = f"\n⚠️ [경보]: {warning_info.get('message', '')}"
                
            # 최종 예쁘게 정돈된 말풍선 메시지 조립
            response_text = (
                f"📊 [{item} 가격 및 기후 정보]\n\n"
                f"💵 최신 평균 가격: {latest_price_str} ({delta_str})\n"
                f"🌡️ 평균 기온: {avg_temp}℃\n"
                f"🌧️ 누적 강수량: {total_rain}mm\n"
                f"{warning_msg}"
            )
        else:
            response_text = f"'{item}' 가격 데이터를 찾을 수 없습니다. (URL 에러 코드: {res.status_code})"
            
    except Exception as e:
        response_text = f"가격 조회 중 오류가 발생했습니다: {str(e)}"

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": response_text
                    }
                }
            ]
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
