@REM Launch windows terminal, split pane vertically, ssh to rpi1 and rpi2, run htop on both
@REM this expects that you have ssh setup for passwordless login using key pairs
@echo off
wt -M nt --commandline "ssh" -t rpi1 htop ; split-pane -V --commandline "ssh" -t rpi2 htop; mf --direction left
