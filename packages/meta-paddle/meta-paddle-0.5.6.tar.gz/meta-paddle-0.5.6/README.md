# cvpaddle
paddle识别通用框架

# 安装 paddlepaddle
## CPU
python -m pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple

## CUDA 11.1
python -m pip install paddlepaddle-gpu==2.2.2.post111 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html

## Check
import paddle
paddle.utils.run_check()