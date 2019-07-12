# multiplayer server plugin getting started

## 测试服务器使用说明

测试服务器指在本地启动的游戏服务器，用于测试游戏的 Plugin 功能，可以用任意 APP ID 登录，但整个服务最多只能同时登录 20 个客户端。

为了能正常启动，请至少准备 512M 空余内存。

### 启动

1. [在 Releases](https://github.com/leancloud/multiplayer-server-plugin-getting-started/releases) 内找最新一次 Release 记录打开 Assets 下载 game-standalone.tar.gz 
1. 解压 game-standalone.tar.gz 后进入 game-standalone 目录
1. 执行 game-standalone 目录内 launch.sh 来启动 game 服务
1. game 服务启动后，launch.sh 会自动展示 game 服务的 STDOUT 输出，不关心其输出时可以 CTRL + C 退出，game 服务会在后台继续运行

### 关闭

1. 进入 game-standalone 目录内执行 shutdown.sh 来关闭后台运行的 game 服务

### 重启

1. 进入 game-standalone 目录内执行 restart.sh 来重启后台运行的 game 服务

### 日志

game 服务在后台运行时产生的日志记录会留在 `game-standlone/logs` 目录内。目前日志名称和用途如下：

文件 | 说明
---- | ---
gc-XXX.current | GC 日志
server.log | game 服务运行日志
stdout.log | 进程的 STDOUT 输出
plugin.log | 用户实现的 plugin 输出的日志
event.log | 事件日志，如用户登录登出等

### 启动过程常见错误处理

1. game-standalone 启动后 STDOUT 输出 ”java.net.BindException: Address already in use“

该错误为当前系统运行了多个 game-standalone 服务，请通过查找并杀死系统内已经存在的 game-standalone 进程，再尝试重新启动 game-standalone 服务。

## 示例 Game Plugin 打包与部署

1. 请先将游戏测试服务器运行起来
1. 进入 multiplayer-server-plugin-getting-started 工程，执行 `mvn clean package`
1. 拷贝生成的 `multiplayer-server-plugin-getting-started/target/multiplayer-server-plugin-getting-started-1.1-jar-with-dependencies.jar` 至 `game-standalone/extensions`
1. 执行 `multiplayer-server-plugin-getting-started/integration-test-scripts/run-tests.sh` 能正常运行完毕表示 Plugin 部署成功，并成功测试了作为示例的 `master_is_watching_you_plugin`


