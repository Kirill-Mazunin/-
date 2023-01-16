import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import tkinter

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

root = tkinter.Tk()

frame = tkinter.Frame(root)
frame.grid()

label = tkinter.Label(frame, text="Приветствие").grid(row=1,column=1)

canvas = tkinter.Canvas(root, height=1000, width=1800)
img = tkinter.PhotoImage(file = 'HelloCode3.png') 
image = canvas.create_image(0, 0, anchor='nw',image=img)
canvas.grid(row=2,column=1)
root.mainloop()

# Загрузка данных из таблицы fact
fact = pd.read_excel('AHD_Fact.xlsx')
fact = fact.fillna(0)
fact

# Суммирование фактических затрат в колонку fact_costs
fact['fact_costs'] = fact.loc[:, 'fact_salary':'fact_overhead_costs'].sum(axis=1)

# Вычисление маржинальной прибыли 
fact ['fact_margin_profit'] = fact ['fact_sales'] - fact ['fact_costs']

# Вычисление маржинальной рентабельности 
fact ['fact_margin_r'] = fact ['fact_margin_profit'] / fact ['fact_sales'] * 100
fact

# Итоговые данные
print ('Общая сумма выручки по филиалу: ', fact['fact_sales'].sum())
print ('Общая сумма затрат по филиалу: ', fact['fact_costs'].sum())
print ('Общая сумма маржинальной прибыли по филиалу: ', round(fact['fact_margin_r'].sum(),2))

# вывод объектов с их рентабельностью
fact[['facility', 'fact_margin_r']] 

# три объекта с максимальной рентабельностью
facility_max_r = fact.nlargest(3, ['fact_margin_r'])
facility_max_r[['facility', 'fact_margin_r']]

# Общая фактическая рентабельность по объектам филиала
def r_total ():
    return round(fact ['fact_margin_profit'].sum() / fact ['fact_sales'].sum() * 100,1)
print ('Общая фактическая маржинальная рентабельность по всем объектам филиала: ',r_total(),'%')

# Объекты с отрицательной рентабельностью)
bad_r = fact.loc[fact['fact_margin_r'] < 0]
bad_r[['facility', 'fact_margin_r']]

# + датафрейм с данными экономического отдела

plan = pd.read_excel('AHD_Plan.xlsx')
plan = plan.fillna(0)
plan

# Вычисление в таблице Plan 
# Сумму расходов, маржинальную прибыль, маржинальную рентабельность

plan ['plan_costs'] = plan.loc[:, 'plan_salary':'plan_overhead_costs'].sum(axis=1)
plan ['plan_margin_profit'] = plan ['plan_sales'] - plan ['plan_costs']
plan ['plan_margin_r'] = plan ['plan_margin_profit'] / plan ['plan_sales'] * 100
plan = plan.fillna(0)
plan

# Объединение таблиц план и факт
diff = plan.merge(fact)
diff = diff.fillna(0)
diff

# Вычисление отклоненения от плана продаж
diff ['diff_sales'] =  diff ['fact_sales'] - diff ['plan_sales'] 
diff [['facility', 'diff_sales']]

facility_very_bad_sales = diff.nsmallest(3, ['diff_sales'])
facility_very_bad_sales[['facility', 'diff_sales']]

# объекты с невыполненным планом по выручке
bad_fact_sales  = diff.loc[diff['diff_sales'] < 0]
bad_fact_sales[['facility', 'diff_sales']]

print ('План по выручке не выполнен общую сумму: ', round(bad_fact_sales['diff_sales'].sum(),2))

# Отклонение фактической прибыли от плановой
diff ['diff_margin_profit'] = diff ['fact_margin_profit'] - diff ['plan_margin_profit']
diff = diff.fillna(0)
# Объекты с невыполненным планом по прибыли
bad_fact_profit  = diff.loc[diff['diff_margin_profit'] < 0]
bad_fact_profit[['facility', 'diff_margin_profit']]

very_bad_fact_profit = bad_fact_profit.nsmallest(3, ['diff_margin_profit'])
very_bad_fact_profit[['facility', 'diff_margin_profit']]

print ('Недополученная прибыль: ', round(bad_fact_profit['diff_margin_profit'].sum(),2))

# Отклонение от плана по расходам 
diff ['diff_costs'] = diff['fact_costs'] - diff ['plan_costs']
# объекты где не выполнен план по рентабельности и првышены расходы
bad_fact_big_costs = diff.loc[(diff['diff_margin_profit'] < 0) & (diff['plan_costs'] > 0)]
bad_fact_big_costs

# Три объекта с максимальными 
very_bad_fact_big_costs = bad_fact_big_costs.nsmallest(3, ['diff_margin_profit'])
very_bad_fact_big_costs[['facility', 'diff_margin_profit']]

import matplotlib.pyplot as plt

fact_facility_manager1 = fact.loc[fact['cluster_manager'] == 'manager_1']
plan_facility_manager1 = plan.loc[fact['cluster_manager'] == 'manager_1']
facility_series = fact_facility_manager1 ['facility'].tolist()    
plan_margin_profit_series = plan_facility_manager1 ['plan_margin_profit'].tolist() 
fact_margin_profit_series = fact_facility_manager1 ['fact_margin_profit'].tolist()
count = fact_facility_manager1 ['facility'].count()

# Диаграмма отклонения прибыли (факт/план) 

def diagram(): 
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot()
    x = np.arange(count) 
    y1 = plan_margin_profit_series               
    y2 = fact_margin_profit_series             
    w = 0.3
    plt.title('Отклонение фактической прибыли от плана', fontsize=20)
    ax.bar(x - w/2, y1, width=w)
    ax.bar(x + w/2, y2, width=w)
    plt.xticks(x,)#FacilitySeries)
    plt.show()

diagram() 

# Поиск объекта по индексу
def print_facility_by_index(index1):
    print(fact_facility_manager1['facility'].loc[fact_facility_manager1.index[index1]])


print('Введите индекс искомого объекта: ')
index1 = int(input())
print_facility_by_index (index1)

# круговая диаграмма доля менеджера в прибыли 

def sum_profit_manager_1():
    facility_manager_1 = fact.loc[fact['cluster_manager'] == 'manager_1'] 
    return facility_manager_1['fact_margin_profit'].round().sum()

def sum_profit_manager_2():
    facility_manager_2 = fact.loc[fact['cluster_manager'] == 'manager_2'] 
    return facility_manager_2['fact_margin_profit'].round().sum()    

def sum_profit_manager_3():
    facility_manager_3 = fact.loc[fact['cluster_manager'] == 'manager_3'] 
    return facility_manager_3['fact_margin_profit'].round().sum()    

def sum_profit_manager_4():
    facility_manager_4 = fact.loc[fact['cluster_manager'] == 'manager_4'] 
    return facility_manager_4['fact_margin_profit'].round().sum() 

def pie_chart():
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot()
    vals = [sum_profit_manager_1(), sum_profit_manager_2(), sum_profit_manager_3(), sum_profit_manager_4()]
    labels = ['manager_1', 'manager_2', 'manager_3','manager_4']
    exp = (0, 0, 0, 0.2)
    ax.pie(vals, labels=labels, autopct='%.2f', explode=exp, shadow=True)
    plt.show()

pie_chart()


