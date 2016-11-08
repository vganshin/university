
# coding: utf-8

# In[27]:

first = lambda l: l[0]
second = lambda l: l[1]
rest = lambda l: l[1:]

data = [("Мат. Анализ", [("Иванов", 15), ("Петров", 13), ("Сидоров", 2), ("Васильев", 10), ("Жуков", 6)]), 
("Алгебра", [("Петров", 24), ( "Иванов", 20),( "Васильев", 11),( "Жуков", 12)]), 
("Логика", [("Иванов", 10), ("Петров", 15), ("Сидоров", 6), ("Жуков", 15)])]


# In[51]:

def transform_to_list(data):
    return data[0][1] + transform_to_list(data[1:]) if data else []


# In[57]:

get_names = lambda transformed_data: list(set(map(first, transformed_data)))

score_of_person = lambda transformed_data: lambda name: sum(map(second, list(filter(lambda d: name == d[0], transformed_data))))

scores = lambda transformed_data: ((name, score_of_person(transformed_data)(name)) for name in get_names(transformed_data))

max_score = lambda transformed_data: max(map(second, transformed_data))

to_mark = lambda persent: 5 if persent >= 0.8 else 4 if 0.6 <= persent < 0.8 else 3 if persent >= 0.4 else 2


# In[58]:

def do_it(transformed_data):
    return list(map(lambda d: (first(d), to_mark(second(d) / max_score(transformed_data))), scores(transformed_data)))
    
print(do_it(transform_to_list(data)))


# In[ ]:



