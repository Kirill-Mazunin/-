class Drink:
    volume = 200 # Статический атрибут
# Создаем метод для инициализации объекта 
    def __init__ (self, name, price):
    # присваиваем значения динмичеким атрибутам
        self.name = name
        self.price = price
        # Устанавливаем начальное значение атрибута remains
        self.remains = self.volume
     # метод выведения информации о напитке
    def drink_info (self):
        print (f'Название: {self.name}. Стоимость: {self.price}. Начальный объем: {self.volume}. Осталось: {self.remains}.')
    def _is_enough (self, need):
        if self.remains >= need and self.remains > 0:
            return True
        print ('Осталось недостаточно напитка')
        return False  
     # Говорим другу сделать глоток
    def sip (self):
        if self._is_enough(20) == True:
            self.remains -= 20
            print('Друг сделал глоток')
    # Говорим другу сделать маленький глоток
    def small_sip (self):
        if self._is_enough(10) == True:
            self.remains -= 10
            print('Друг сделал маленький глоток')
    def drink_all (self):
        if self._is_enough(0) == True:
            self._remains = 0
            print ('Друг выпил напиток залпом')        


# Создаем объект    
coffee = Drink ('Кофе', 300)
coffee.remains = 20
coffee.sip()
coffee.drink_info()
print(coffee.remains) 
