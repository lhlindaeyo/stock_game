import pygame
import pandas as pd
from scenario import Scenario
from chart import draw_chart

STOCKS = [
    "AAPL", "GOOGL", "MSFT", "AMZN", "META",
    "TSLA", "NVDA", "AVGO", "GLDM", "NOW",
    "QQQM", "SPLG", "IONQ", "RGTI", "OKLO",
    "PLTR", "MRNA", "NFLX", "GE", "WMT"
]

class GameCore:
    def __init__(self, font):
        self.font=font
        self.money=10000 # 초기자산
        self.data=pd.read_csv("us_stock_monthly_close.csv")
        self.date_list=pd.to_datetime(self.data["Date"]).tolist() # 시뮬레이션 시간흐름 반영 위해
        self.scenario=Scenario(self.date_list, self.data)  # 시나리오에 전달
        self.show_explain=False
        self.time_index=0
        self.portfolio = {stock: 0 for stock in STOCKS}
        self.prices = self.get_prices_at_index(self.time_index) # 원하는 주식 날짜
        self.price_history = {stock: [] for stock in STOCKS} # 그 날짜의 가격 저장
        self.quantity=1 # 매수/매도 주식 양
        self.scroll=0
        self.max_visible=12  # 화면에 보일 최대 주식 수
        self.selected=0 # 원하는 주식 선택
        self.rewrite_status=False # 가격 다시 쓰기
        self.showing_chart = False # 차트 그리기 여부
        self.game_over = False  # 종료 여부

    def get_prices_at_index(self, idx): # 특정 날짜의 각 주식 종가 가져오기
        row = self.data.iloc[idx]
        return {stock: round(float(row[stock]), 2) if not pd.isna(row[stock]) else 0 for stock in STOCKS}

    def update(self):  # 시나리오 별 종료 가격 반영
        if self.scenario.index >= len(self.scenario.scenarios):
            return

        self.scenario.apply_scenario(self.prices)

        # 해당 시점 가격을 기록
        for stock in STOCKS:
            self.price_history[stock].append(self.prices[stock])

    def keyboard(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: # 주식 리스트 에서 종목 선택
                self.selected = (self.selected - 1) % len(STOCKS)
            elif event.key == pygame.K_DOWN: # 주식 리스트 에서 종목 선택
                self.selected = (self.selected + 1) % len(STOCKS)
            elif event.key == pygame.K_b: # 원하는 종목 매수
                self.buy(STOCKS[self.selected])
            elif event.key == pygame.K_s: # 원하는 종목 매도
                self.sell(STOCKS[self.selected])
            elif event.key == pygame.K_e: # 시나리오 설명글 보기
                self.show_explain = not self.show_explain
            elif event.key == pygame.K_n: # 다음 시나리오로 넘어가기
                self.scenario.next()
            elif event.key == pygame.K_f: # 게임 종료하기
                self.game_over = True
            elif event.key == pygame.K_PAGEUP:
                self.scroll= max(self.scroll - 1, 0)
            elif event.key == pygame.K_PAGEDOWN:
                max_offset = max(0, len(STOCKS) - self.max_visible)
                self.scroll= min(self.scroll + 1, max_offset)
            elif event.key == pygame.K_SPACE: # 원하는 종목의 주식 차트보기
                self.show_selected_stock_chart()


    def buy(self, stock): # 매수 함수
        cost = self.prices[stock] * self.quantity
        if self.money >= cost:
            self.money -= cost
            self.portfolio[stock] += self.quantity

    def sell(self, stock): # 매도 함수
        if self.portfolio[stock] >= self.quantity:
            self.portfolio[stock] -= self.quantity
            self.money += self.prices[stock] * self.quantity

    def show_selected_stock_chart(self):
        scenario = self.scenario.scenarios[self.scenario.index]
        start_date = scenario["start_date"]
        rewrite_date = scenario["rewrite_date"]
        ticker = STOCKS[self.selected]

        draw_chart(ticker, start_date, rewrite_date)

    def draw(self, screen):
        if self.game_over: # 종료화면 표시
            screen.fill((0, 0, 0))
            title = self.font.render("게임 종료", True, (255, 255, 255))

            total_stock_value = sum(self.prices[stock] * self.portfolio[stock] for stock in self.portfolio)

            total_asset = int(self.money + total_stock_value)
            total_asset_text = self.font.render(f"총 자산(현금 + 주식): ${total_asset}", True, (200, 200, 200))

            screen.blit(title, (350, 200))
            screen.blit(total_asset_text, (250, 250))
            return  # 종료화면 만 출력

        # 기본 게임 화면 표시
        y = 140
        start = self.scroll
        end = min(start + self.max_visible, len(STOCKS))

        for i in range(start, end):
            stock = STOCKS[i]
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = f"{stock} | 가격: ${self.prices[stock]} | 보유 수량: {self.portfolio[stock]}"
            render = self.font.render(text, True, color)
            screen.blit(render, (50, y))
            y += 40

        # 주식 리스트 스크롤 조정
        if self.selected < self.scroll:
            self.scroll = self.selected
        elif self.selected >= self.scroll + self.max_visible:
            self.scroll = self.selected - self.max_visible + 1

        # 시나리오 설명
        if self.show_explain:
            desc = self.scenario.get_current_explain()
            if desc:
                pygame.draw.rect(screen, (30, 30, 30), (50, 500, 700, 120))
                pygame.draw.rect(screen, (200, 200, 200), (50, 500, 700, 120), 2)

                render_multiline_text(
                    text=desc,
                    font=self.font,
                    color=(255, 255, 255),
                    x=60,
                    y=510,
                    max_width=680,
                    screen=screen
                )
                small_font = pygame.font.Font("BMDOHYEON_ttf.ttf", 16)
                hint = small_font.render("Close: E", True, (180, 180, 180))
                screen.blit(hint, (670, 590))

def draw_top(screen, game_core, font):
    cur_index = game_core.scenario.index
    current_scenario = game_core.scenario.scenarios[cur_index]
    scenario_num = current_scenario["num"]
    scenario_name = current_scenario["event"]
    scenario_show = f"Scenario {scenario_num}: {scenario_name}"

    cash_show = f"보유 현금: ${game_core.money:.2f}"

    total_asset = game_core.money
    for stock in STOCKS:
        quantity = game_core.portfolio.get(stock, 0)
        price = game_core.prices.get(stock, 0)
        total_asset += quantity * price
    asset_show = f"내 자산: ${total_asset:.2f}"

    scenario_surface = font.render(scenario_show, True, (255, 255, 255))
    cash_surface = font.render(cash_show, True, (255, 255, 255))
    asset_surface = font.render(asset_show, True, (255, 255, 255))

    screen.blit(scenario_surface, (20, 20))
    screen.blit(cash_surface, (20, 60))
    screen.blit(asset_surface, (20, 100))

def render_multiline_text(text, font, color, x, y, max_width, screen):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        text_width, _ = font.size(test_line)

        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        screen.blit(line_surface, (x, y + i * 30))
