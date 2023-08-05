# TCCM Python SDK

## Tccm Client python + Tccm Agent 接入
https://iwiki.woa.com/pages/viewpage.action?pageId=1132770611

## 用法
1. 创建并初始化TccmClient客户端对象
2. 创建CustomMetric用于上报自定义监控指标数据
3. ModuleMetric可用于上报模调监控指标数据
4. 关闭TccmClient对象

### 初始化
TccmClient全局仅支持创建一个单例对象,close后才可以重新init。
ClientOption对象是配置 TccmClient 所需的 Option

```python
//初始化 tccm-client, 通过 tccm-agent 上报监控数据，完全使用内部默认配置,默认使用HTTP协议上报到127.0.0.1:8126
def init_client(self, business_app_id, business_name, report_region)
//初始化 tccm-client, 通过 tccm-agent 上报监控数据，支持指定客户端配置ClientOption,未设置则会使用内部默认配置
def init_client(self, business_app_id, business_name, report_region, option)
```

初始化后就可以上报指标了，示例：
### 示例1—上报到本地agent(默认)

```python
# coding:utf-8
# -*- coding:utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")
from tccm.api.tccm_client import TccmClient, Measurement
from tccm.api.client_option import ClientOption
import random

if __name__ == "__main__":
    tccm = TccmClient().init_client(1258344699, "Coding-trpc-nodejs", "gz2")
    m = Measurement().new_measurement("custom_metric", "ziana_test_measurement")
    m.set_app_id(1258344699)
    m.set_namespace("Coding-trpc-nodejs")
    m.add_tags({"env": "dev", "region": "bj"})
    m.add_sum_field(name="my_sum_metric", value=random.randint(0, 100))
    m.add_max_field(name="my_max_metric", value=random.randint(0, 100))
    m.add_min_field(name="my_min_metric", value=random.randint(0, 100))
    m.add_first_field(name="my_first_metric", value=random.randint(0, 100))
    m.add_last_field(name="my_last_metric", value=random.randint(0, 100))
    m.add_counter_field(name="my_counter_metric", value=random.randint(0, 100))
    m.add_gauge_field(name="my_gauge_metric", value=random.randint(0, 100))
    m.add_histogram_field(name="my_histogram_metric", value=random.randint(0, 100), buckets=[])
    m.add_summary_field(name="my_summary_metric", value=random.randint(0, 100), quantiles=[])
    m.add_set_field(name="my_set_metric", value="set_value")

    tccm.write(m)
    tccm.close()
```
### 示例2—上报到其他地址(中台)
```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")
from tccm.api.tccm_client import TccmClient, Measurement
from tccm.api.client_option import ClientOption
import random

if __name__ == "__main__":
    option = ClientOption()
    option.set_tccm_agent_addr("地址")
    tccm = TccmClient().init_client(1258344699, "Coding-trpc-nodejs", "gz2", option)
    //后面上报的部分同示例1
```