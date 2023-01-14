#!/usr/bin/python3
import utils.routes
import config.config
import utils.walt_handler as wh

wh.ssh_check()
config.config.main()
