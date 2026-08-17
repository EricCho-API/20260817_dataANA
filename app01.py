#這個是執行streamlit網頁板顯示的範例，必須要透過終端機將虛擬環境跑起來才會開啟網頁
# 終端機執行 uv run streamlit run (此程式的路徑(含檔名))

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title('視覺圖表顯示')

order = pd.read_csv('data/raw/orders.csv')
items = pd.read_csv('data/raw/order_items.csv')
df = order.merge(items, on='order_id')

#這邊不能用print, 要用streamlit的write
st.write('### 訂單明細筆') # 加上#作為標題文字大小的依據 # 代表大標 ~ ###### 最小標題大小
st.write(df.head())

# 增加一個欄位'amount'小計, 數量 x 單價 X 折扣
df['amount'] = df['quantity'] * df['unit_price'] * (1-df['discount_rate'])

# 增加一個order_date欄位，使用pandas將資料表的文字date轉成date值
df['order_date'] = pd.to_datetime(df['order_date'])

#取出訂單狀態
status_list = df['status'].unique() # 排除status欄的重複值後存到status_list
#加入下拉式選單
status = st.selectbox("XXXXX", status_list) # 前面式標題，後面是資料
# 篩選，將資料表'status' 與 status比對, 相同的才放進去data值
data = df[ df['status']== status ]  

#st.write(data.head())

chart_type = st.selectbox('次選單', 
                           ['每月銷售金額','付款-訂單數','訂單金額','不同付款方式小計'] )

if st.button("顯示圖表"):
    #st.info(chart_type)
    #線條圖
    if chart_type == '每月銷售金額':
        data = data.copy()  #複製一份資料表
        # 將資料表中的文字型態order_date欄位轉為date值後放進去新欄位
        data['month'] = data['order_date'].dt.to_period('M') 
        #把相同月份的amount加總
        m_sales = data.groupby('month')['amount'].sum()
        #index依照月份按照順序排序
        m_sales.index = m_sales.index.astype(str)

        #畫圖
        fig,ax = plt.subplots()
        ax.plot(
            m_sales.index,
            m_sales.values,
            marker = 'o'
        )
        ax.set_title("AAAA")
        ax.set_xlabel('month')
        ax.set_ylabel('$')
        st.pyplot(fig)

    #長條圖
    elif chart_type == '付款-訂單數':
        pay_count = data.groupby('payment_type')['order_id'].nunique() #nunique()是指不同值的數量

        fig,ax = plt.subplots()
        ax.bar(
            pay_count.index,
            pay_count.values
        )
        ax.set_title("AAAA")
        ax.set_xlabel('payment_type')
        ax.set_ylabel('$')
        st.pyplot(fig)



    #直方圖
    elif chart_type == '訂單金額':
        # 依照order_id分組並計算amount的總和
        order_amount = data.groupby('order_id')['amount'].sum()

        #繪圖
        fig,ax = plt.subplots()
        ax.hist(
            order_amount,
            bins = 40
        )
        ax.set_title("order_amount")
        ax.set_xlabel('order_amount')
        ax.set_ylabel('$')
        st.pyplot(fig)



    #箱形圖
    elif chart_type == '不同付款方式小計':
        order_amount = (
            data.groupby(["order_id",'payment_type'])['amount']  #分組多組，藥用dist包起來
            .sum()
            .reset_index()  #重設index值
        )
        pays = order_amount['payment_type'].unique()  #
        boxdata = []
        for i in pays:
            values = order_amount[ order_amount['payment_type'] == i ]['amount']
            boxdata.append(values)

        fig,ax = plt.subplots()
        ax.boxplot(boxdata)

        ax.set_title("payment_type")
        ax.set_xlabel('payment_type')
        ax.set_ylabel('$')
        ax.set_xticks([1,2,3,4],['atm','card','cod','wallet']) #把X軸的資料數列名稱改為這四個
        st.pyplot(fig)        


else:
    st.info("no selected")






