#import libraries
import serial
import matplotlib.pyplot as plt, mpld3
import numpy as np
import time
from threading import Thread
import http.server
import socketserver
from datetime import datetime
from matplotlib.dates import DateFormatter

def update_line(l, ax, x, y, max_len):
    # Plot updating function
    if x.size > max_len:
        x = x[-max_len:-1]
        y = y[-max_len:-1]

    l.set_ydata(y)
    l.set_xdata(x)
    ax.relim()
    ax.autoscale_view()

def plot_data():
    #initialize serial connection    
    s = serial.Serial('COM6',9600)

    # Initialize empty plots
    plt.ion()
    fig = plt.figure()
    axt1 = fig.add_subplot(221)
    axt2 = fig.add_subplot(222)
    axh1 = fig.add_subplot(223)
    axh2 = fig.add_subplot(224)

    t1, = axt1.plot([],[],'r-')
    t2, = axt2.plot([],[],'r-')
    h1, = axh1.plot([],[],'b-')
    h2, = axh2.plot([],[],'b-')

    # Add plot labels
    axt1.set_ylabel("Temperature [C]")
    axh1.set_ylabel("Humidity [%]")
    axh1.set_xlabel("Seconds Ago")
    axh2.set_xlabel("Seconds Ago")
    # Initialize 'time'
    t = np.array([0])

    # Initialize Data Arrays
    temp1 = np.array([])
    temp2 = np.array([])
    humidity1 = np.array([])
    humidity2 = np.array([])
    soilMoisture = np.array([])
    while True:

        #read data from serial port
        res_b = s.readline()
        res = res_b.decode("utf-8")

        # split string into arrays of data
        rawData = res.split(' ')
        temp1 = np.append(temp1, float(rawData[0]))
        humidity1 = np.append(humidity1,float(rawData[1]))
        temp2 = np.append(temp2,float(rawData[2]))
        humidity2 = np.append(humidity2,float(rawData[3]))

        # update 'time'
        t_label = np.append(t, datetime.now())
        t = np.append(t, t[-1]+1)

        # update plots
        max_plot_len = 50
        update_line(t1,axt1,t[0:-1],temp1,max_plot_len)
        update_line(t2,axt2,t[0:-1],temp2,max_plot_len)
        update_line(h1,axh1,t[0:-1],humidity1,max_plot_len)
        update_line(h2,axh2,t[0:-1],humidity2,max_plot_len)

        #plt.draw()
        plt.savefig('data.png')
        plt.pause(1)
        #mpld3.save_html(fig,'test.html')
        #f=open("test.html", "w")
        #f.write("\n<meta http-equiv=\"refresh\" content=\"2\">")
        #f.write("<IMG SRC=\"data.png\" ALT=\"some text\" WIDTH=32 HEIGHT=32>")
        #f.close()
        #time.sleep(1)

def web_server():
    #set up web server
    PORT = 8000

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

if __name__ == "__main__":
    Thread(target = plot_data).start()
    Thread(target = web_server).start()