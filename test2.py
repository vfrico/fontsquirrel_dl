import threading, time, random
def worker(count, callback):
    """funcion que realiza el trabajo en el thread"""
    tim = int(random.random() * 90) % 5
    time.sleep(tim)
    print "Este es el %s trabajo que hago hoy para Genbeta Dev" % count

    callback("realizado: %s en %s" % (count, tim))
    return

texto = []
def integration(text):
    texto.append(text)
tasks = range(10)
threads = list()
for i in tasks:
    t = threading.Thread(target=worker, args=(i,integration,))
    threads.append(t)
    t.start()
    # time.sleep(1)
for i in threads:
    i.join()
print texto
