@REM Launch windows terminal, split pane into quarters, ssh into 4 different machines, run htop on each
@echo off
wt -M nt --commandline "ssh" -t rpi1 htop ; split-pane -V --commandline "ssh" -t rpi2 htop; mf --direction left ; split-pane -H --commandline "ssh" -t rpi3 htop; mf --direction right ; split-pane -H --commandline "ssh" -t rpi4 htop
 