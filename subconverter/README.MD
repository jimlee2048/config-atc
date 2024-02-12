subconverter-config
===

自用。

规则基于 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)。

## 本地自部署

使用`docker-compose`。
- 下载仓库中的文件到特定文件夹。
- `docker-compose up -d`

## 使用

### 处理单订阅

**本地部署：**

- 默认处理单订阅，懒的话直接参考官方文档用链接传参。
- 有心思就参考`profiles/example-profile.ini`建个配置档案Profile。
    - 调用链接：`/getprofile?name=profiles/xxx-profile.ini`
    - 配置档案Profile只能本地调用，用已有的在线服务参考下面直接链接传参。
- 常用参数
    - `target=`：要生成的目标配置文件
    - `rename=`：重命名规则
    - `filename=`：生成的文件名
    - `udp={true|false}`：是否开启upd
    - `rename=`：节点重命名规则，多条规则用 ` 分隔
    - `config=`：要用的配置文件（定义组与规则），自己看`custom/config`都有啥，也可以用在线的
    - `expand={true|false}`：规则写入详细内容 or 写入 `rule-provider`
    - `list={true|false}`：输出纯节点列表
    - `insert={true|false}`：是否对所有订阅插入本地配置文件的自定义节点信息，需在本地配置中设置`insert_url`。常用于插入私有节点配置，本配置开启后会自动显示“私有节点”策略组。
    - `online=(true|false)`：导入其他规则时，是否使用线上配置文件。在非本地自建服务使用本外部规则时使用。
    - `ad={full|lite|false}`：广告过滤启用程度，如不配置，默认只开启[隐私保护](https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Clash/Privacy)+[反劫持](https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Clash/Hijacking)规则
    - `region.size={full|lite}`：输出配置使用的自动地区分组，`full`为完整地区分组，`lite`为精简地区分组
    - `region.mode={select|url-test|fallback|load-balance}`：地区节点分组的模式，`select`为手动选择，`url-test`为URL测试，`fallback`为故障转移，`load-balance`为负载均衡
    - `ipv6={true|false}`：是否开启IPv6, 默认为`false`
    - `tun={true|false}`：是否开启TUN模式, 默认为`false`
    - `clash_type={meta|stash}`：Clash配置文件类型，如不配置默认为原版Clash格式
    - `clash_dns={redir-host|fake-ip}`：Clash DNS模式，默认为`redir-host`
    - `include_private={true|false}`：是否包含私有节点，默认为 false。启用后将会添加单独的策略组`私有节点`，用于显示私有节点。
    - `include_info={true|false}`：是否用节点展示订阅信息，默认为 false。启用后将会添加单独的策略组`订阅信息`，用于显示订阅信息。

- **注意：** 参数需要进行URLEncode，参数间用`&`分隔

## 常用正则小记

- `(?i:\\bSG[P]?\\b)`匹配地域代码

## 参考文档
[subconverter 中文文档](https://github.com/tindy2013/subconverter/blob/master/README-cn.md)