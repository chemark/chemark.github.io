# 终端 AI 编程助手配置指南：Claude Code & Codex

## 使用场景：
1. 在终端 terminal 和 warp 使用 claude code 和 codex cli
2. 在 IDE vscode 的终端使用claude code 和 codex
3. 在 IDE vscode 的插件 cline里直接使用模型 API
4. 放弃在 IDE vscode 使用 codex 和 claude code插件，因为需要订阅昂贵的会员
5. 在 cursor 使用插件 cline
## claude code

目前终端 claude code使用的是KAT-Coder,配置文件在/Users/xingshuhao/.secrets。
目前是免费使用 API 随时会挂掉，使用命令是 claude。配置方法见[官网指南](https://streamlake.com/document/WANQING/me6ymdjrqv8lp4iq0o9)

目前终端 codex 使用的是 minimax M2,没有每月续订，下个月12月19日到期，使用命令是codex --profile m2。配置方法是：
1. 修改配置文件/Users/xingshuhao/.codex/config.toml，清空 codex 关于 OpenAI 的设置，添加以下配置
```
[model_providers.minimax]
name = "MiniMax Chat Completions API"
base_url = "https://api.minimaxi.com/v1"
env_key = "MINIMAX_API_KEY"
wire_api = "chat"
requires_openai_auth = false
request_max_retries = 4
stream_max_retries = 10
stream_idle_timeout_ms = 300000

[profiles.m2]
model = "codex-MiniMax-M2"
model_provider = "minimax"
```
2. 导入环境变量，在文件 zshrc 里添加export MINIMAX_API_KEY="我的 minimax API"

### 现在发现有以下便捷方式使用：
1. 使用[GLM code](https://github.com/alchaincyf/glm-claude) ,可以在终端里使用命令claude 和glm同时使用 claude code 和GLM code ,不会互相影响，[这是教程](https://mp.weixin.qq.com/s/jXs_dnKRS-IYivopz1g9RA)。
2. 使用[阮一峰的方式](https://mp.weixin.qq.com/s?__biz=MzI4NjAxNjY4Nw==&mid=2650242330&idx=1&sn=24f19e9a16ab76e80ce2e5a16ca13c4a&chksm=f214807e350b2a9fbde9b0b492c6c425b682e7ec12a8a1e8e64b427951e28dd38c4afcdf12cf&scene=90&xtrack=1&sessionid=1762850864&subscene=93&clicktime=1762851247&enterid=1762851247&flutter_pos=4&biz_enter_id=4&ranksessionid=1762850964&jumppath=20020_1762850964623%2C1104_1762851031547%2C20020_1762851044787%2C1104_1762851245926&jumppathdepth=4&ascene=56&devicetype=iOS26.0.1&version=18004034&nettype=WIFI&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&countrycode=CN&fontScale=100&exportkey=n_ChQIAhIQJaohqQCma2zyp%2FEpJPw32hLhAQIE97dBBAEAAAAAAGatE1HGacoAAAAOpnltbLcz9gKNyK89dVj0jLpw9Q6OW%2BEBxJXMaQ1%2F%2F3WIjrA1uwHSsdD9lq9o8F%2Fwj3ioXcACb3N0dUaDh8jagkYrXplJNSQqekVCvtRFfkDRBvmcp7qUyaW0IiVaUPyZ6bqUHjgZE6aalRQZbc%2BTPtY1o9wE21XjnITOWggWPbOLNSdreSDr6wqJyej1Fpt4oPe%2BYo%2BFFRezbuL86QCjD0OS4BXScs59aHNTgTFRmVZmiO06UGmE2FB6yAVf77xRMiMkugpYWh3ubQ%3D%3D&pass_ticket=ERQeLy3p3BVr44phT2rdBG%2BBp13WWEQcpIcgyiLmVbLma004zVL3%2FCgu9Z7rjXid&wx_header=3)，将国产模型接入 claude code
3. [VS Code 使用国产大模型 MiniMax M2 教程](https://mp.weixin.qq.com/s?__biz=MzI4NjAxNjY4Nw==&mid=2650242455&idx=1&sn=9fd7914e0a13386489ad3c89a57746f9&chksm=f27b8678c048ec073dc53b02bbca671d6e10db7fe1f543327b612372166d06e1d703597bf447&scene=90&xtrack=1&req_id=1763524171814433&sessionid=1763524198&subscene=93&clicktime=1763524566&enterid=1763524566&flutter_pos=0&biz_enter_id=4&ranksessionid=1763524171&jumppath=1001_1763524196545%2C1104_1763524199350%2C20020_1763524214219%2C1104_1763524521402&jumppathdepth=4&ascene=56&devicetype=iOS26.0.1&version=1800412a&nettype=WIFI&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&countrycode=CN&fontScale=100&exportkey=n_ChQIAhIQbb3IZyjAuqHRO3AJsf%2BKmRLhAQIE97dBBAEAAAAAACchGeHqTgUAAAAOpnltbLcz9gKNyK89dVj0ABPQVqnI24hT9TIMJgUcasQ1r0m0ajbjXvfsNSJzdEyqMOdwyFXsiw3PXovPoZTGEopBzSIartieDJ3raS0wgBHASn38NSyVh4OWULWgjWLKACQcZ7w84bNTEZ%2FdKQOtMER4yXRn5YD1HPyS5IqxbxDRMEg%2Fi8iygosUZdL0JlVtC9m9tmKnk4zLYLDZ1NXw6jr56L2SXZII7xWM547jgBde%2Bl61%2BAnXDGdEkGmFp0SXFvBYZk33SVuEUA%3D%3D&pass_ticket=g4nkgUiFZ1aqyeP43LgR8fFRRbijC0vZ8mRglmYRxJntu9u52%2BQwPW7tVjnImg5B&wx_header=3)，不使用插件
4. 使用[CC switch](https://github.com/farion1231/cc-switch)和[CC mate](https://github.com/djyde/ccmate),

待办：KAT-Coder随时替换成便宜的模型，不再订阅 claude 和 ChatGPT。
有以下模型备选：
1. [kimi](https://platform.moonshot.ai/docs/overview)
2. [glm](https://bigmodel.cn/glm-coding?utm_source=bigModel&utm_medium=Frontend%20Model%20Group&utm_content=glm-code&utm_campaign=Platform_Ops&_channel_track_key=bW5juXcZ)
3. [qwen](https://github.com/QwenLM/qwen-code) 
4. [minimax ](https://platform.minimax.io/docs/coding-plan/intro)
5. [kat coder](https://www.streamlake.ai/product/kat-coder#packages)
6. [doubao seed code](https://www.volcengine.com/activity/codingplan)


## codex 
可以在 claude code 和 codex 中同时使用 minimax M2,[这是教程](https://mp.weixin.qq.com/s?__biz=MzkwMzE4NjU5NA==&mid=2247511736&idx=1&sn=9ca91fc44e9e3427212d6978472711f4&chksm=c15a328ce35a519f6bf42187fae828f92e965308db1a0f644286367ea49b702c7337ca9f0359&scene=90&xtrack=1&sessionid=1761644385&subscene=93&clicktime=1761644395&enterid=1761644395&flutter_pos=1&biz_enter_id=4&ranksessionid=1761644329&jumppath=1123_1761644379395%2C1003_1761644380810%2C1001_1761644381324%2C1104_1761644386501&jumppathdepth=4&ascene=56&devicetype=iOS26.0.1&version=1800402c&nettype=WIFI&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&countrycode=CN&fontScale=100&exportkey=n_ChQIAhIQQmqKgavWY%2FpOBbF6xDziHRLhAQIE97dBBAEAAAAAAM9wJPCsrHAAAAAOpnltbLcz9gKNyK89dVj09BP1Wax16KAZ0mcNMCEpy5Mog%2FcLCu2YPvMP0oz5ESyMtkcUkOCfHujyLQ9yAYm7MwGURAxWTP9ryVx8do%2FCMSHUurNN4AaxYort5AGc1KWI%2B3KFoWFdFw%2Bx%2FAsg%2FThQXxmzxGtcS1oBixPoyIsGU50Oa7sIQF7XBJ5yoxX0DspqMIbjF2uJONSbrNOjdpmVOBobG%2BsWC9iJyugvuhwwyCxsYpV1Zst9YkIouDPIF5%2BKS8OWkXSvaWE0fw%3D%3D&pass_ticket=7CooLa1XBAPveaQdly%2F3oGVm%2FGP8gllNJ%2BgbML2C4IhMbwnN8hpIQEavf%2FX8PMGo&wx_header=3)

