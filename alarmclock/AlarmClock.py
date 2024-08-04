from tkinter import *
import datetime
import pygame


class Clock:

    def __init__(self):
        self.main_clock = Tk()
        self.main_clock.title("Clock")
        self.main_clock.geometry("500x500")
        self.alarms = []
        self.setup_clock_window()

        pygame.mixer.init()

        self.sound = "signal-elektronnogo-budilnika-33304.mp3"

        self.on_image = PhotoImage(width=48, height=24)
        self.off_image = PhotoImage(width=48, height=24)
        self.on_image.put(("green",), to=(0, 0, 23, 23))
        self.off_image.put(("red",), to=(24, 0, 47, 23))

        self.check_alarms()

    def setup_clock_window(self):
        self.time_label = Label(self.main_clock, text="", font=("Helvetica", 48, "bold"))
        self.time_label.pack(pady=20)
        self.update_time()

        bottom_frame = Frame(self.main_clock)
        bottom_frame.pack(side=BOTTOM, pady=10, fill=X)

        self.set_alarm_btn = Button(bottom_frame, text="Add alarm", command=self.create_alarm_window)
        self.set_alarm_btn.pack(pady=5)

        self.alarms_frame1 = Frame(self.main_clock)
        self.alarms_frame1.pack(side=LEFT, padx=50, fill=Y)

        self.alarms_frame2 = Frame(self.main_clock)
        self.alarms_frame2.pack(side=RIGHT, padx=50, fill=Y)

    def update_time(self):
        time_now = datetime.datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=time_now)

        self.main_clock.after(1000, self.update_time)

    def check_alarms(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        for alarm_time in self.alarms:
            if current_time == alarm_time:
                self.sound_alarm()
        self.main_clock.after(1000, self.check_alarms)

    def sound_alarm(self):
        pygame.mixer.music.load(self.sound)
        pygame.mixer.music.play(loops=-1)

        self.alarm_message()

    def off_sound(self):
        pygame.mixer.quit()

    def alarm_message(self):
        window = Toplevel(self.main_clock)
        message = MessageWindow(window, self)

    def onoff_alarm(self, state, set_time):
        if state:
            self.alarms.append(set_time)
        else:
            self.alarms.remove(set_time)

    def add_button(self, parent_frame, alarm):
        var1 = IntVar(value=1)

        del_btn = Button(parent_frame, text="Delete", command=lambda: self.delete_alarm(alarm))
        del_btn.pack(side="right", padx=5)

        cb1 = Checkbutton(parent_frame, image=self.off_image, selectimage=self.on_image, indicatoron=False,
                          onvalue=1, offvalue=0, variable=var1,
                          command=lambda: self.onoff_alarm(var1.get(), alarm))
        cb1.pack(side="right", padx=5)

    def delete_alarm(self, alarm):
        if alarm in self.alarms:
            self.alarms.remove(alarm)
            self.display_alarms()

    def add_alarm(self, alarm_time):
        self.alarms.append(alarm_time)
        self.display_alarms()

    def display_alarms(self):
        for widget in self.alarms_frame1.winfo_children():
            widget.destroy()
        for widget in self.alarms_frame2.winfo_children():
            widget.destroy()

        for i, alarm in enumerate(self.alarms):
            alarm_frame = Frame(self.alarms_frame1 if i < 8 else self.alarms_frame2)
            alarm_frame.pack(fill=X, pady=5)

            alarm_label = Label(alarm_frame, text=alarm, font=("Helvetica", 15, "bold"))
            alarm_label.pack(side="left")

            self.add_button(alarm_frame, alarm)

    def create_alarm_window(self):
        window = Toplevel(self.main_clock)
        AlarmWindow(window, self)


class AlarmWindow:
    def __init__(self, root, clock_instance):
        self.root = root
        self.clock = clock_instance
        self.root.title("New alarm")
        self.root.geometry("235x175")
        self.setup_alarm_page()

    def setup_alarm_page(self):
        set_time_label = Label(self.root, text="Set Time", font=("Helvetica", 18, "bold"), fg="red")
        set_time_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.hour = StringVar(self.root)
        hours = ('00', '01', '02', '03', '04', '05', '06', '07',
                 '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17', '18', '19', '20', '21', '22', '23', '24'
                 )
        self.hour.set(hours[0])
        hrs = OptionMenu(self.root, self.hour, *hours)
        hrs.grid(row=1, column=0, padx=10)

        self.minute = StringVar(self.root)
        minutes = ('00', '01', '02', '03', '04', '05', '06', '07',
                   '08', '09', '10', '11', '12', '13', '14', '15',
                   '16', '17', '18', '19', '20', '21', '22', '23',
                   '24', '25', '26', '27', '28', '29', '30', '31',
                   '32', '33', '34', '35', '36', '37', '38', '39',
                   '40', '41', '42', '43', '44', '45', '46', '47',
                   '48', '49', '50', '51', '52', '53', '54', '55',
                   '56', '57', '58', '59', '60')
        self.minute.set(minutes[0])
        mins = OptionMenu(self.root, self.minute, *minutes)
        mins.grid(row=1, column=1, padx=10)

        self.second = StringVar(self.root)
        seconds = ('00', '01', '02', '03', '04', '05', '06', '07',
                   '08', '09', '10', '11', '12', '13', '14', '15',
                   '16', '17', '18', '19', '20', '21', '22', '23',
                   '24', '25', '26', '27', '28', '29', '30', '31',
                   '32', '33', '34', '35', '36', '37', '38', '39',
                   '40', '41', '42', '43', '44', '45', '46', '47',
                   '48', '49', '50', '51', '52', '53', '54', '55',
                   '56', '57', '58', '59', '60')
        self.second.set(seconds[0])
        secs = OptionMenu(self.root, self.second, *seconds)
        secs.grid(row=1, column=2, padx=10)

        save_alarm = Button(self.root, text="Save", font=("Helvetica", 10, "bold"), command=self.save_alarm)
        save_alarm.grid(row=2, column=0, columnspan=3, pady=5)

        cancel = Button(self.root, text="Cancel", font=("Helvetica", 10, "bold"), command=self.cancel)
        cancel.grid(row=3, column=0, columnspan=3, pady=5)

    def save_alarm(self):
        set_hour = self.hour.get()
        set_min = self.minute.get()
        set_sec = self.second.get()

        alarm_time = f"{set_hour}:{set_min}:{set_sec}"
        self.clock.add_alarm(alarm_time)
        print(self.clock.alarms)

        self.root.destroy()

    def cancel(self):
        self.root.destroy()


class MessageWindow:
    def __init__(self, message, clock_instance):
        self.msg_window = message
        self.clock = clock_instance

        self.setup_message_window()

    def setup_message_window(self):
        message = Message(self.msg_window, text="IT'S TIME!", font=("Helvetica", 13, "bold"),
                             width=300)
        message.pack(padx=20, pady=20)

        off_btn = Button(self.msg_window, text="OFF", bg="red", command=self.turn_off_alarm)
        off_btn.pack(padx=5, pady=5)

    def turn_off_alarm(self):
        self.clock.off_sound()
        self.msg_window.destroy()


if __name__ == "__main__":
    clock = Clock()
    clock.main_clock.mainloop()

