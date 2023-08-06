from ovos_PHAL import PHAL, on_ready, on_error, on_stopping


def main(ready_hook=on_ready, error_hook=on_error, stopping_hook=on_stopping):
    # config read from mycroft.conf
    # "PHAL": {
    #     "ovos-PHAL-plugin-display-manager-ipc": {"enabled": true},
    #     "ovos-PHAL-plugin-mk1": {"enabled": True}
    # }
    phal = PHAL(on_error=error_hook, on_ready=ready_hook, on_stopping=stopping_hook)
    phal.start()
    
    
if __name__ == "__main__":
    main()
