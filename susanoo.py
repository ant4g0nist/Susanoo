# @ant4g0nist

import os
import sys
import gzip
import time
import argparse
from app.helpers.utils import TerminalColors
from app.controllers import api as APIController
from app.controllers import smoke as SmokeController

def banner():
    ban ="""
                                                             ,--.    ,----..       ,----..    
  .--.--.                  .--.--.      ,---,              ,--.'|   /   /   \     /   /   \   
 /  /    '.          ,--, /  /    '.   '  .' \         ,--,:  : |  /   .     :   /   .     :  
|  :  /`. /        ,'_ /||  :  /`. /  /  ;    '.    ,`--.'`|  ' : .   /   ;.  \ .   /   ;.  \ 
;  |  |--`    .--. |  | :;  |  |--`  :  :       \   |   :  :  | |.   ;   /  ` ;.   ;   /  ` ; 
|  :  ;_    ,'_ /| :  . ||  :  ;_    :  |   /\   \  :   |   \ | :;   |  ; \ ; |;   |  ; \ ; | 
 \  \    `. |  ' | |  . . \  \    `. |  :  ' ;.   : |   : '  '; ||   :  | ; | '|   :  | ; | ' 
  `----.   \|  | ' |  | |  `----.   \|  |  ;/  \   \'   ' ;.    ;.   |  ' ' ' :.   |  ' ' ' : 
  __ \  \  |:  | | :  ' ;  __ \  \  |'  :  | \  \ ,'|   | | \   |'   ;  \; /  |'   ;  \; /  | 
 /  /`--'  /|  ; ' |  | ' /  /`--'  /|  |  '  '--'  '   : |  ; .' \   \  ',  /  \   \  ',  /  
'--'.     / :  | : ;  ; |'--'.     / |  :  :        |   | '`--'    ;   :    /    ;   :    /   
  `--'---'  '  :  `--'   \ `--'---'  |  | ,'        '   : |         \   \ .'      \   \ .'    
            :  ,      .-./           `--''          ;   |.'          `---`         `---`      
             `--`----'                              '---'                                     
                                                                                                
    """
    print ban


if __name__ == '__main__':

	banner()
	parser = argparse.ArgumentParser()
	parser.add_argument("-c","--config", help="run api security scan on given config file", required=True)
	parser.add_argument("-s","--smoke", help="run smoke scan on the given config file?True/False", action='store_true', default=False)
	args = parser.parse_args()

	tty_colors = TerminalColors(True)

	if not os.path.exists(args.config):
		print tty_colors.red()+'Make sure config file exists'+tty_colors.default()
		sys.exit(0)

	if args.smoke:
		smokeSusanoo = SmokeController.SusanooConfig(args.config)
		apis  = smokeSusanoo.get_apis()

		for api in apis:
			print tty_colors.cyan()+"testing %s"%(api)+tty_colors.default()

			
			scan 	= SmokeController.Scans(apis[api], smokeSusanoo)
			scan.run()

			print tty_colors.cyan()+"*"*100+tty_colors.default()

	if not args.smoke:
		susanoo = APIController.SusanooConfig(args.config)
		apis 	= susanoo.get_apis()

		for api in apis:
			
			name 	= api
			scan 	= APIController.Scans(apis[api], susanoo)

			print tty_colors.cyan()+"*"*100+tty_colors.default()
			
			scan.authentication_check()

			scan.authorization_check()

			scan.sqlinjection_heuristic_check()

			if apis[api].raw_url:
				scan.url_param_fuzz()

			scan.fuzz()
			# scan.ratelimit_check()
			print tty_colors.cyan()+"*"*100+tty_colors.default()
