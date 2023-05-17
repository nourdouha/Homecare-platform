import datetime

class DailySchedule:
    
    def __init__(self, date):
        self.date = date
        self.appointments = []

    def add_appointment(self, time):
        self.appointments.append(time)

    def display_schedule(self):
        print(f"Schedule for {self.date.strftime('%Y-%m-%d')}:")
        print("Appointments:")
        for appointment in self.appointments:
            print(f"- {appointment}")

# Create schedules for a week
week_schedules = []
start_date = datetime.date(2023, 5, 17)

for i in range(5):
    date = start_date + datetime.timedelta(days=i)
    schedule = DailySchedule(date)
    schedule.add_appointment("9:00 AM")
    schedule.add_appointment("11:00 AM")
    schedule.add_appointment("2:00 PM")
    week_schedules.append(schedule)

# Display schedules
for schedule in week_schedules:
    schedule.display_schedule()
    print()
