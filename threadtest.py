from flask import Flask, render_template
import threading
import time

app = Flask(__name__)
finished = False

def func1():
    global finished
    finished = False
    time.sleep(1)
    print ("func1")
    return render_template('test1.html')
        

def func2():
    while True:
        time.sleep(3)
        print ("func2")
        return render_template('test2.html')

@app.route("/", methods=['GET', 'POST'])
def home():
    print ("HOME")
    t1 = threading.Thread(target=func1)
    #t2 = threading.Thread(target=func2)
    t1.start()
    #t2.start()

if __name__ == "__main__":
    app.run()