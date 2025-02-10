import serial
import time
import threading

start_time = time.time() * 1000  
    
def elapsed_milliseconds():
    return round((time.time() * 1000) - start_time)

def read_serial(serial_port, buffer):
    while True:
        line = None
        try:
            line = serial_port.readline()
            serial_data = line.decode('utf-8').strip()
            timestamped_data = f"{elapsed_milliseconds()},{serial_data}"
            buffer.append(timestamped_data)
        except:
            print(line);

def write_to_file(buffer, output_file_path):
    while True:
        with open(output_file_path, 'a') as output_file:
            lines_to_write = buffer[:]
            buffer.clear()
            for line in lines_to_write:
                output_file.write(line + '\n')

if __name__ == "__main__":
    serial_port = serial.Serial('COM6', 1000000)  # Replace with your actual port and baud rate
    output_file_path = 'North.txt'
    data_buffer = []

    try:
        serial_thread = threading.Thread(target=read_serial, args=(serial_port, data_buffer), daemon=True)
        serial_thread.start()

        write_thread = threading.Thread(target=write_to_file, args=(data_buffer, output_file_path), daemon=True)
        write_thread.start()

        serial_thread.join()
        write_thread.join()

    except KeyboardInterrupt:
        serial_port.close()
        print('Serial port closed.')

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        serial_port.close()
