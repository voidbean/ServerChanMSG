# ServerChanMSG

## 简介

基于ServerChan的消息推送

### 功能单

| 功能        | 描述                         | 路径                         |
| ----------- | ---------------------------- | ---------------------------- |
| B站直播订阅 | 跟踪直播状态, 开播时进行推送 | ./livewatcher/livewatcher.py |
|直播订阅-函数计算|用于阿里云函数计算的直播监听, 支持b站/ytb|./livewatcher-ali/livewatcher-ali|

上述功能基于ServerChan实现消息推送, 如果使用hoshino作为qq bot, 可以使用[该项目](https://github.com/voidbean/livewatcher)

