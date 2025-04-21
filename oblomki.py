#обломки кода, которые могут быть полезны
name_months = {31: 'jan', 28: 'feb_f', 29: 'feb_t', 31: 'mar', 30: 'apr', 31: 'may', 30: 'jun', 31: 'jul', 31: 'aug', 30: 'sep', 31: 'oct', 30: 'nov', 31: 'dec'}
def date(q, speed):
    global now_date
    start_date = datetime.strptime("00:00:00/01/01/2000", "%H:%M:%S/%d/%m/%Y")  # Начальная дата
    current_date = start_date
    while True:
        # Обновляем дату
        current_date += timedelta(seconds=speed)
        now_date = current_date.strftime("%H:%M:%S/%d/%m/%Y")  # Форматируем дату
        q.put(now_date)  # Отправляем дату в очередь
manag_thread = Thread(target=managment)
def managment_initiator(q):
    global bodies
    global now_date
    global manag_thread
    manag_thread.start()
    while True:
        inputs = []
        while not q.empty():
            inputs.append(q.get())
        bodies_in = inputs[1]
        print(bodies_in)
        for i in range(len(bodies_in)):
            bodies.append(Body(bodies_in[i][0], bodies_in[i][1], bodies_in[i][2], bodies_in[i][3], bodies_in[i][4],
                               bodies_in[i][5], bodies_in[i][6], bodies_in[i][7], bodies_in[i][8], bodies_in[i][9],
                               bodies_in[i][10], bodies_in[i][11]))
        now_date = inputs[0]
def integ_initiator():
    global speed
    lasttime = time()
    while True:
        if time()-lasttime > 1/speed:
            num_integr(3600)
            lasttime = time()