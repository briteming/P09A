# P09A
探测网络上的SOCKS5端口

<pre>
# 功能-探测网络上的SOCKS5端口 
# 配置文件 参数指定 config.json中 CheckURL 为检测socks5时需要的某个网站地址
# 启动 重启 run.sh
# 定时重启 15 5 * * * /root/P09A/run.sh 2>&1 >/dev/null
# 依赖 random requests json datetime time sqlite3
# 运行环境 Linux/Ubuntu python3
</pre>
