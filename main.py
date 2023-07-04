import PySimpleGUI as sg
import os


class Extrator:
    def __init__(self):
        self.version = "1.01"

    def py_gui(self):
        layout = [
            [sg.Text("Select a file:")],
            [sg.Input(key="-FILE-"), sg.FileBrowse()],
            [sg.Button("Submit")]
        ]

        window = sg.Window("File Browser", layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == "Submit":
                file_path = values["-FILE-"]
                self.sysinfo = file_path
                self.parse_sysinfo()
                self.get_policy()
                sg.popup(f"Files were extracted to '{os.getcwd()}'")
        window.close()

    def parse_sysinfo(self):
        with open(self.sysinfo, 'r', encoding="latin-1") as f:
            lines = f.readlines()
            for line in lines:  # Loop to get EOF marker
                if "inline exception" in line:
                    eof_marker = line.split('end-')[1].split('-')[0]
                    break
            index: list[int] = []
            search_for_start = "inline policy"
            search_for_end = f"end-{eof_marker}-inline"
            for line_number, line in enumerate(lines, 1): # Loop to find start and end of CPL policy files
                if search_for_start in line:
                    index.append(line_number)
                    new_start = line_number
                    for i, j in enumerate(lines[new_start:], start=new_start):
                        if search_for_end in j:
                            index.append(i + 1)
                            break
            search_vpm_xml_start = "<vpmapp>"
            search_vpm_xml_end = "</vpmapp>"
            for line_number, line in enumerate(lines, 1): # loop to find VPM XML
                if search_vpm_xml_start in line:
                    index.append(line_number)
                if search_vpm_xml_end in line:
                    index.append(line_number)
            self.index = index


    def get_policy(self):
        line_index = self.index
        with open(self.sysinfo, 'r', encoding="latin-1") as f:
            lines = [line.strip() for line in f.readlines()]  # Strip whitespace from each line
            policy_type = ["Central", "Local", "Forward", "VPM-CPL", "VPM-XML"]
            i, j = 0, 1
            start = line_index[i]
            end = line_index[j]
            try:
                for policy in policy_type:
                    content = lines[start:end - 1]
                    i += 2
                    j += 2
                    start, end = line_index[i], line_index[j]
                    content = '\n'.join(content)
                    try:
                        with open(f"{policy}.txt", "w") as file:
                            file.write(content)
                    except UnicodeEncodeError as e:
                        print(f"{e}")
                        with open(f"{policy}.txt", "w", encoding="latin-1") as file:
                            file.write(content)
                        continue
            except IndexError as e:
                print(f"No more objects to process. Calling {e}")
                with open(f"{policy}.txt", "w", encoding="latin-1") as file:
                    start, end = line_index[-2], line_index[-1]
                    content = lines[start:end - 1]
                    content = '\n'.join(content)
                    file.write(content)

object = Extrator()
object.py_gui()
