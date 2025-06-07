import pandas as pd

class Scenario:
    def __init__(self, date_list, data):
        self.date_list = date_list  # 반드시 datetime 형식 리스트
        self.data = data
        self.rewrite_status = False

        self.scenarios = [
            {"num":1, "event": "코로나 발생", "start_date": "2019-06", "rewrite_date": "2019-12",
             "explain": "애플,구글,마이크로소프트,아마존,넷플릭스 등은 원격근무 및 스트리밍 서비스 수요 증가로 상승.\n모더나는 백신 개발 기대감으로 상승. 반면 GE는 전통 제조업 위축으로 하락."},
            {"num":1, "event": "코로나 발생 결과", "start_date": "2019-12", "rewrite_date": "2021-06",
             "explain": "애플,구글,마이크로소프트,아마존,넷플릭스 등은 원격근무 및 스트리밍 서비스 수요 증가로 상승.\n모더나는 백신 개발 기대감으로 상승. 반면 GE는 전통 제조업 위축으로 하락."},
            {"num":2, "event": "Chat GPT 상용화", "start_date": "2020-06", "rewrite_date": "2023-04",
             "dexplain": "Chat GPT 상용화로 AI 기술 발전을 실감하며 관련 주가 급등."},
            {"num":2, "event": "Chat GPT 상용화 결과", "start_date": "2020-06", "rewrite_date": "2024-02",
             "explain": "Chat GPT 상용화로 AI 기술 발전을 실감하며 관련 주가 급등."},
            {"num":3, "event": "러시아 우크라이나 전쟁 발발 및 장기화", "start_date": "2022-02", "rewrite_date": "2023-11",
             "explain": "전쟁 격화로 지정학적 불안과 에너지 공급 불안정성에 따른 금융시장 충격."},
            {"num":3, "event": "러시아 우크라이나 전쟁 발발 및 장기화 결과", "start_date": "2022-02", "rewrite_date": "2024-11",
             "explain": "전쟁 격화로 지정학적 불안과 에너지 공급 불안정성에 따른 금융시장 충격.\n 근데 의외로 큰 변동이 없다..?"},
            {"num":4, "event": "트럼프 당선", "start_date": "2024-10", "rewrite_date": "2024-11",
             "explain": "트럼프 대통령 당선으로 미국 성장 기대감 반영, 증시 상승."},
            {"num":4, "event": "트럼프 당선 결과", "start_date": "2024-11", "rewrite_date": "2025-01",
             "explain": "트럼프 대통령 당선으로 미국 성장 기대감 반영, 증시 상승."},
            {"num":5, "event": "트럼프 첫 관세 정책 시행", "start_date": "2025-01", "rewrite_date": "2025-04",
             "explain": "무역 관세 도입으로 시장 불확실성 증대, 증시 하락."},
            {"num":5, "event": "트럼프 첫 관세 정책 시행 결과", "start_date": "2025-01", "rewrite_date": "2025-05",
             "explain": "무역 관세 도입으로 시장 불확실성 증대, 증시 하락."},
        ]

        self.index = 0
    def apply_scenario(self, prices):
        if self.index >= len(self.scenarios):
            return

        scenario = self.scenarios[self.index]
        rewrite_date = pd.to_datetime(scenario["rewrite_date"]).date()

        rewrite_idx = next((i for i, d in enumerate(self.date_list) if d.date() == rewrite_date), None)
        if rewrite_idx is not None:
            rewrite_row = self.data.iloc[rewrite_idx]
            for stock in prices:
                prices[stock] = round(float(rewrite_row[stock]), 2) if not pd.isna(rewrite_row[stock]) else 0

    def next(self):
        if self.index < len(self.scenarios) - 1:
            self.index += 1
            self.ready = True
            self.rewrite_status = False
            self.timer_active = False
            self.timer_count = 0

    def get_current_explain(self):
        if self.index < len(self.scenarios):
            return self.scenarios[self.index].get("explain", "")
        return ""
