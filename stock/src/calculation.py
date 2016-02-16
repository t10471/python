from average import ichimoku
from t10471.model.db import Stock, StockDate
import t10471.model.register as register

def main():
    """main(銘柄コード)"""

    for stock in register.getStocks():
        date_stock = register.getStockDate(stock)
        data = [(stock.date, float(stock.end_price)) for stock in date_stock]
        st, ct, l, a1, a2 = ichimoku(data)

if __name__ == "__main__":
    main()
