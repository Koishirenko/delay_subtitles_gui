import os
import re
from datetime import timedelta
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import Tk

def delay_subtitles(input_file, output_file, delay):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.readlines()

    delayed_content = []
    time_regex = re.compile(r"(Dialogue: )(\d+),(\d+:\d+:\d+\.\d+),(\d+:\d+:\d+\.\d+)")

    def parse_time(time_str):
        hours, minutes, seconds = map(float, time_str.split(':'))
        return timedelta(hours=int(hours), minutes=int(minutes), seconds=seconds)

    def format_time(time_value):
        return f"{int(time_value.seconds // 3600)}:{int((time_value.seconds // 60) % 60):02d}:{time_value.seconds % 60 + time_value.microseconds / 1e6:05.2f}"

    for line in content:
        match = time_regex.search(line)
        if match:
            start_time = parse_time(match.group(3))
            end_time = parse_time(match.group(4))

            start_time += delay
            end_time += delay

            delayed_line = f"{match.group(1)}{match.group(2)},{format_time(start_time)},{format_time(end_time)},{line[match.end():]}"
            delayed_content.append(delayed_line)
        else:
            delayed_content.append(line)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(delayed_content)

def main():
    root = Tk()
    root.withdraw()

    input_file = filedialog.askopenfilename(title="Select input .ass file", filetypes=[("ASS files", "*.ass")])
    if not input_file:
        messagebox.showerror("Error", "No input file selected.")
        sys.exit(1)

    output_file = os.path.splitext(input_file)[0] + '_delayed.ass'

    delay_seconds = simpledialog.askfloat("Delay time", "Enter delay time in seconds:")
    if delay_seconds is None:
        messagebox.showerror("Error", "No delay time entered.")
        sys.exit(1)

    delay = timedelta(seconds=delay_seconds)

    delay_subtitles(input_file, output_file, delay)
    messagebox.showinfo("Success", "Subtitles have been delayed successfully.")

if __name__ == "__main__":
    main()
