import time
import autopilot
import messages
import router
import definitions as vars

def elimination_process(stop_command):
    while autopilot.state['connection'] == False and not stop_command.is_set():
        try:
            time.sleep(7)
            messages.display(messages.terminator_process_connecting, [vars.mavlink_url])
        except Exception as e:
            messages.display(messages.fatal_error, [e])
            pass
    
    if not stop_command.is_set():
        messages.display(messages.terminator_process_connected, [vars.mavlink_url])

    while not stop_command.is_set():
        try:
            if autopilot.state['bee_state'] in ['KILL', 'DESTROY']:
                if autopilot.state['ruined'] == False:
                    if int(autopilot.state['altitude']) != 0:
                        router.put_command(router.Command(1,'DESTROY',{}))
            time.sleep(2)
        except:
            pass

    stopped_time = time.strftime("%H:%M:%S, %Y, %d %B", time.localtime())
    messages.display(messages.terminator_process_done, [stopped_time])
