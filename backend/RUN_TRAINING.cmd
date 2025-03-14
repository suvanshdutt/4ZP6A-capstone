set PYTHONPATH=%PYTHONPATH%;/nfs/u20/<MacId>/
set CUDA_VISIBLE_DEVICES=0,1,2
nohup python train.py > output.log 2>&1 &

:: Do not run this cmd file. Run the commands above in your terminal on the grace server.