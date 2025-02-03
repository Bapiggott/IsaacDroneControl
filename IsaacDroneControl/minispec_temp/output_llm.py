import time
from functions_gps import *
import asyncio
import datetime
import json
import os

original_code = """?_1=s('bench');->True{tc(180);->True}->False;"""
START_SAVING_URL = "http://localhost:5000/start_saving"
STOP_SAVING_URL = "http://localhost:5000/stop_saving"

async def main():
    mission_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    mission_description = "output_llm.py"
    if mission_description == "":
        n = ""
    else:
        n = '_'
    mission_directory = f"mission_{mission_description}{n}{mission_timestamp}"
    with open(__file__, 'r') as f_in:
        translated_code = f_in.read()
    start_data = {
        "mission_directory": mission_directory,
        "original_code": original_code,
        "translated_code": translated_code
    }

    # Notify the server to start saving images to the mission directory
    requests.post(START_SAVING_URL, json=start_data)

    await connect_drone()
    await ensure_armed_and_taken_off()
    # await return_to_start_position()
    # Start the print_status_text task
    # status_task = asyncio.create_task(print_status_text(drone))

    try:
        if _1=await scan('bench'):
        return True
            await turn_cw(180)
            return True
        return False

    except:
        print("")
    await land_drone()
    requests.post(STOP_SAVING_URL)
    print("STOP_SAVING_URL")

if __name__ == '__main__':
    result = asyncio.run(main())
    current_datetime = datetime.datetime.now().isoformat()
    with open(__file__, 'r') as f_in:
        translated_code = f_in.read()
    log_data = {
        'date': current_datetime,
        'original_code': original_code,
        'translated_code': translated_code,
        'output': result
    }
    with open('execution_log.json', 'a') as log_file:
        log_file.write(json.dumps(log_data) + '\n')
    destination_folder = "./saved_logs"
    print("end")
    time.sleep(15)
    os._exit(0)
