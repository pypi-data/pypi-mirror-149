*** Settings ***
Library        SeleniumLibrary
Library        RuirenyunLibrary.PublicLibrary

*** Keywords ***
equal
    [Arguments]    ${object}
    [Return]    ${object}

ilog
    [Arguments]    @{msgs}
    log    ${msgs}    console=True

public_check_texts
    [Arguments]    @{text_list}    ${timeout}=10s
    [Documentation]    公共检查点方法：判断页面是否存在指定的字符串，如果超时不存在则报错
    should be true    ${text_list}
    FOR    ${text}    IN    @{text_list}
        wait until page contains    ${text}    ${timeout}
        info    检查目标字符串存在：${text}
    END

public_check_texts_not_exist
    [Arguments]    @{text_list}    ${timeout}=0.1s
    [Documentation]    共有检查点方法：判断页面是否不存在指定的字符串，如果超时存在则报错
    should be true    ${text_list}
    FOR    ${text}    IN    @{text_list}
        Wait Until Page Does Not Contain    ${text}    ${timeout}
        info    检查目标字符串不存在：${text}
    END

public_check_abnormal
    [Arguments]    @{text_list}    ${loglevel}=TRACE
    [Documentation]    共有检查点方法：判断页面是否存在指定字符串的异常
    ${abnormal}    create list    系统异常    异常
    ${text_list}    Set Variable If    ${text_list}    ${text_list}    ${abnormal}
    debug    全局异常检查点:${text_list}
    FOR    ${text}    IN    @{text_list}
        Page Should Not Contain    ${text}    loglevel=${loglevel}
    END

public_check_expression_true
    [Arguments]    ${expression}    ${msg}=${None}    ${filename}=selenium-screenshot-{index}.png
    [Documentation]    公共断言函数，断言为False时截图保存并嵌入日志
    ${condition}    evaluate    ${expression}
    Run Keyword If    not ${condition}    Capture Page Screenshot    ${filename}
    info    表达式[${expression}]结果：${condition}
    ${msg}    Set Variable If    $msg    ${msg}    预期结果:True|==|实际结果:${condition}
    should be true    ${condition}    msg=${msg}

public_check_expression_false
    [Arguments]    ${expression}    ${msg}=${None}    ${filename}=selenium-screenshot-{index}.png
    [Documentation]    公共断言函数，断言为False时截图保存并嵌入日志
    ${condition}    evaluate    ${expression}
    Run Keyword If    ${condition}    Capture Page Screenshot    ${filename}
    info    表达式[${expression}]结果：${condition}
    Should Not Be True    ${condition}    msg=预期结果:False|==|实际结果:${condition}

public_assert_true
    [Arguments]    ${condition}    ${msg}=${None}    ${filename}=selenium-screenshot-{index}.png
    [Documentation]    公共断言函数，断言为False时截图保存并嵌入日志
    Run Keyword If    not ${condition}    Capture Page Screenshot    ${filename}
    ${msg}    Set Variable If    $msg    ${msg}    预期结果:True|==|实际结果:${condition}
    should be true    ${condition}    msg=${msg}

public_assert_false
    [Arguments]    ${condition}    ${msg}=${None}    ${filename}=selenium-screenshot-{index}.png
    [Documentation]    公共断言函数，断言为False时截图保存并嵌入日志
    Run Keyword If    ${condition}    Capture Page Screenshot    ${filename}
    Should Not Be True    ${condition}    msg=预期结果:False|==|实际结果:${condition}

public_check_equal
    [Arguments]    ${expect_text}    ${actual_text}    ${msg}=${None}    ${filename}=selenium-screenshot-{index}.png
    [Documentation]    判断两个字符串相等,不等时截图报错
    ${condition}    evaluate    "${expect_text}".strip()=="${actual_text}".strip()
    Run Keyword If    not $condition    Capture Page Screenshot    ${filename}
    Should Be True    ${condition}    msg=预期结果:${expect_text}|==|实际结果:${actual_text}

public_check_unequal
    [Arguments]    ${expect_text}    ${actual_text}    ${msg}=${None}    ${filename}=selenium-screenshot-{index}.png
    [Documentation]    判断两个字符串不相等,相等时截图报错
    ${condition}    evaluate    "${expect_text}".strip()!="${actual_text}".strip()
    Run Keyword If    not $condition    Capture Page Screenshot    ${filename}
    Should Be True    ${condition}    msg=预期结果:${expect_text}|!=|实际结果:${actual_text}

public_load_test_suit_model
    [Arguments]    ${work_dir}=""    ${model_path}=""    ${time}=0.1s
    [Documentation]    导入工程配置，生成测试套模型
    set selenium speed    ${time}
    ${suite_model_path}    evaluate    os.path.join($work_dir,$model_path)    os
    ${local_model}    load_yml    ${suite_model_path}
    Set Suite Variable    ${suite_model_path}    ${suite_model_path}
    Set Suite Variable    ${suite_model}    ${local_model}
    Set Suite Variable    ${work_dir}    ${work_dir}

    Set Log Level    ${suite_model}[loglevel]

public_load_test_case_model
    [Documentation]    导入工程配置，生成测试用例模型
    ${local_model}    load_yml    ${suite_model_path}
    Set Test Variable    ${test_model}    ${local_model}
    ${local_suffix}    create_random_string    6
    Set Test Variable    ${suffix}    ${local_suffix}

public_open_browser
    [Arguments]    ${url}=http://dev-fwx.ruirenyun.tech/login_smsVerificationCode    ${browser}=chrome
    [Documentation]    携带命令行参数启动web浏览器
    ${option}    init_chrome_option_for_web    userdata=UserDataForTest
    ${index}    open browser    ${url}    ${browser}    options=${option}
    Set Suite Variable    ${browser}    ${index}
    [Return]    ${browser}

public_open_browser_en
    [Arguments]    ${url}=http://dev-fwx.ruirenyun.tech/login_smsVerificationCode    ${browser}=chrome
    [Documentation]    携带命令行参数启动web浏览器
    ${option}    init_chrome_option_for_web    userdata=UserDataForEnTest
    ${index}    open browser    ${url}    ${browser}    options=${option}
    Set Suite Variable    ${browser_en}    ${index}
    [Return]    ${browser_en}

public_open_browser_with_option
    [Arguments]    ${url}=http://dev-fwx.ruirenyun.tech/login_smsVerificationCode    ${browser}=chrome
    [Documentation]    携带命令行参数启动模拟微信浏览器
    ${option}    init_chrome_option_for_wx
    ${index}    open browser    ${url}    ${browser}    options=${option}
    Set Suite Variable    ${browser_wx}    ${index}
    [Return]    ${browser_wx}

public_open_browser_for_pay
    [Arguments]    ${url}=http://dev-fwx.ruirenyun.tech/login_smsVerificationCode    ${browser}=chrome
    [Documentation]    携带命令行参数启动在线支付浏览器
    ${option}    init_chrome_option_pay
    ${index}    open browser    ${url}    ${browser}    options=${option}
    [Return]    ${index}

public_switch_browser_web
    [Documentation]    切换到平台端浏览器
    switch browser    ${browser}
    info    切换浏览器:平台端浏览器

public_switch_browser_en
    [Documentation]    切换到平台端浏览器
    switch browser    ${browser_en}
    info    切换浏览器:企业端浏览器

public_switch_browser_wechat
    [Documentation]    切换到微信端浏览器
    switch browser    ${browser_wx}
    info    切换浏览器:微信端浏览器

public_move_scroll_bar
    [Arguments]    ${scroll_arg}=10000
    [Documentation]    移动滚动条到指定的位置
    execute javascript    document.documentElement.scrollTop=${scroll_arg}

public_move_scroll_bar_to_element
    [Arguments]    ${locator}    ${offset}=0
    [Documentation]    移动滚动条到指定元素的位置
    wait until element is visible     ${locator}
    ${vertical_position}    get vertical position    ${locator}
    ${scroll_arg}   evaluate    ${vertical_position}-${offset}
    public_move_scroll_bar    ${scroll_arg}

public_scroll_element_into_view
    [Arguments]    ${locator}
    [Documentation]    滚动元素到可视界面
    wait until element is enabled    ${locator}
    scroll element into view    ${locator}

public_set_logcalstorage_editable
    [Documentation]    设置localstorage为可编辑状态
    execute javascript    window.addEventListener("storage",(function(e){localStorage.setItem(e.key,e.newValue),sessionStorage.setItem(e.key,e.newValue)}))

public_set_local_storage
    [Arguments]    ${key}    ${value}
    [Documentation]    设置localstorage的指定键值
    Execute Javascript    window.localStorage.setItem("${key}", "${value}")

public_get_local_storage
    [Arguments]    ${key}
    [Documentation]    获取logcalstorage的指定键值
    ${value}    Execute Javascript    window.localStorage.getItem("${key}")
    [Return]    ${value}

public_set_session_storage
    [Arguments]    ${key}    ${value}=
    [Documentation]    设置sessionstorage的指定键值
    Execute Javascript    window.sessionStorage.setItem("${key}", "${value}")

public_get_session_storage
    [Arguments]    ${key}
    [Documentation]    获取sessionstorage的指定键值
    Execute Javascript    window.sessionStorage.getItem("${key}")

public_wait_and_click_element
    [Arguments]    ${locator}    ${modifier}=False    ${action_chain}=False    ${timeout}=30s    ${error}=${None}
    [Documentation]     公共关键字，等待指定元素可见后再执行点击动作
    [Timeout]           # 关键字执行超时时间
    Wait Until Element Is Visible    ${locator}    ${timeout}    ${error}
    Click Element    ${locator}    ${modifier}    ${action_chain}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_and_click_text
    [Arguments]    ${text}=    ${prefix}=     ${suffix}=    ${modifier}=False    ${action_chain}=False    ${timeout}=10s    ${error}=${None}
    [Documentation]     公共关键字，根据text点击元素
    [Timeout]           # 关键字执行超时时间
    Wait Until Element Is Visible    xpath=//*[text()="${prefix}${text}${suffix}"]    ${timeout}    ${error}
    Click Element    xpath=//*[text()="${prefix}${text}${suffix}"]    ${modifier}    ${action_chain}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_click_text
    [Arguments]    ${text}=    @{xpath_list}    ${modifier}=False    ${action_chain}=False    ${timeout}=30s    ${error}=${None}
    [Documentation]     公共关键字，根据text点击元素，针对text前后有空格进行了专项处理
    [Timeout]           # 关键字执行超时时间
    Wait Until Page Contains    ${text}    ${timeout}    ${error}
    # 存在空格的text
    ${text_space}    Get WebElements    xpath=//*[text()=" ${text} "]
    IF    $text_space
        Click Element    xpath=//*[text()=" ${text} "]    ${modifier}    ${action_chain}
        Return From Keyword
    END
    # 没有空格的text
    ${text_nospace}    Get WebElements    xpath=//*[text()="${text}"]
    IF    $text_nospace
        Click Element    xpath=//*[text()="${text}"]    ${modifier}    ${action_chain}
        Return From Keyword
    END
    # 针对非标准text属性通过扩展属性定位处理
    FOR    ${xpath}    IN    @{xpath_list}
        ${assert}    public_asssert_element_is_exist    xpath=${xpath}
        IF    $assert
            Click Element    xpath=${xpath}    ${modifier}    ${action_chain}
            Return From Keyword
        ELSE
            Continue For Loop
        END
    END
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_until_text_visible
    [Arguments]    ${text}=    ${prefix}=     ${suffix}=
    [Documentation]     公共关键字，根据text点击元素
    [Timeout]           # 关键字执行超时时间
    wait until element is visible     xpath=//*[text()="${prefix}${text}${suffix}"]
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_and_input_text
    [Arguments]    ${locator}    ${text}=    ${clear}=True    ${timeout}=10s    ${error}=${None}
    [Documentation]     公共关键字，等待指定元素可见后再输入文本
    [Timeout]           # 关键字执行超时时间
    Wait Until Element Is Visible    ${locator}     ${timeout}    ${error}
    set focus to element    ${locator}
    input text    ${locator}    ${text}    clear=${clear}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_and_get_text
    [Arguments]    ${locator}    ${timeout}=10s    ${error}=${None}
    [Documentation]     公共关键字，等待指定元素可见后获取并返回文本值
    [Timeout]           # 关键字执行超时时间
    Wait Until Element Is Visible    ${locator}     ${timeout}    ${error}
    ${text}    get text    ${locator}
    [Teardown]          # 关键字的teardown
    [Return]     ${text}       # 关键字返回值

public_click_element_checked
    [Arguments]    ${locator}    ${attribute}    ${timeout}=10s
    [Documentation]    根据指定属性点选指定元素，如果初始为非选中状态，则点击成选中状态
    [Timeout]           # 关键字执行超时时间
    # 判断元素如果没有选中就点击选中
    wait until element is enabled    ${locator}    ${timeout}
    ${ischecked}    SeleniumLibrary.get element attribute    ${locator}    ${attribute}
    IF    "${ischecked}" == "false" or "checked" not in "${ischecked}"
        click element    ${locator}
    END
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_click_element_unchecked
    [Arguments]    ${locator}    ${attribute}
    [Documentation]    根据指定属性点选指定元素，如果初始为选中状态，则点击成非选中状态
    [Timeout]           # 关键字执行超时时间
    # 判断元素如果选中就点击取消选中
    ${ischecked}    SeleniumLibrary.get element attribute    ${locator}    ${attribute}
    IF    "${ischecked}" == "true" or "checked" in "${ischecked}"
        click element    ${locator}
    END
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_and_upload_file
    [Arguments]    ${locator}   ${filepath}=${None}    ${timeout}=10s    ${error}=${None}
    [Documentation]     公共关键字，等待指定元素可见后再执行点击动作
    [Timeout]           # 关键字执行超时时间
    wait until element is enabled    ${locator}     ${timeout}    ${error}
    Choose File    ${locator}    ${filepath}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_and_get_attribute
    [Arguments]    ${locator}   ${attribute}    ${timeout}=10s    ${error}=${None}
    [Documentation]     公共关键字，等待指定元素可见后获取指定属性值
    [Timeout]           # 关键字执行超时时间
    wait until element is enabled    ${locator}     ${timeout}    ${error}
    ${value}    SeleniumLibrary.get element attribute    ${locator}    ${attribute}
    [Teardown]          # 关键字的teardown
    [Return]    ${value}

public_set_attribute
    [Arguments]    ${loactor}    ${key}    ${value}
    [Documentation]    给指定属性的元素设置属性
    [Timeout]           # 关键字执行超时时间
    ${id}    create_random_string    6
    # 分配临时ID属性给元素
    Wait Until Element Is Visible    ${loactor}
    Assign Id To Element   ${loactor}    ${id}
    # 调用原生的JS语法清除input的内容
    Execute Javascript    document.getElementById("${id}").setAttribute("${key}","${value}")
    [Teardown]          # 关键字的teardown
    [Return]    ${id}

public_run_keyword_if_text_exist
    [Arguments]    ${text}    ${keyword}    @{args}
    [Documentation]    判断页面是否存在指定文本字符串，如果存在运行关键字keyword
    [Timeout]           # 关键字执行超时时间
    ${actual}    Run Keyword And Return Status    page should contain    ${text}
    IF    ${actual}
        run keyword    ${keyword}    @{args}
    END
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_run_keyword_if_text_no_exist
    [Arguments]    ${text}    ${keyword}    @{args}
    [Documentation]    判断页面是否存在指定文本字符串，如果不存在运行关键字keyword
    [Timeout]           # 关键字执行超时时间
    ${actual}    Run Keyword And Return Status    page should contain    ${text}
    IF    not $actual
        run keyword    ${keyword}    @{args}
    END
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_pay_with_cookie_for_alipay
    [Arguments]    ${url}    ${payment_password}
    [Documentation]    利用浏览器缓存，保存有支付账号缓存信息，指定支付宝的支付链接，完成在线付款。
    [Timeout]           # 关键字执行超时时间
    ${password_decode}    base64_decode    ${payment_password}
    ${current_browser_ids}    get browser ids
    ${current_browser_id}    set variable    ${current_browser_ids}[0]
    ${pay_browser}    public_open_browser_for_pay    ${url}
    switch browser    ${pay_browser}
    public_wait_and_click_Element    xpath=//*[text()="继续浏览器付款"]
    public_wait_and_click_Element    xpath=//button[@type="submit"]    timeout=30s
    public_wait_and_input_text    id=pwd_unencrypt    ${password_decode}
    public_check_texts    支付成功    完成
    public_wait_and_click_Element    xpath=//*[text()="完成"]
    close browser
    switch browser    ${current_browser_id}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_asssert_element_is_exist
    [Arguments]    ${locator}
    [Documentation]    判断元素是否存在
    [Timeout]           # 关键字执行超时时间
    ${count}    SeleniumLibrary.get element count    ${locator}
    ${result}    evaluate    ${count}>0
    [Return]    ${result}
    [Teardown]          # 关键字的teardown

public_analyze_dictionary_args
    [Arguments]    ${dic_string}    @{keys_list}
    [Documentation]    解析字典参数
    ...    eg:    ${dict_str}    set variable    {"one":"1","two":"2"}
    ...           &{dict_dic}    create dictionary    one    value1    two    value2
    ...           ${one}    ${two}    public_analyze_dictionary_args    ${dict_dic}    one    two
    ...           info    ${one}    ${two}
    [Timeout]           # 关键字执行超时时间
    ${values_list}   analyze_dictionary    ${dic_string}    ${keys_list}
    [Return]    ${values_list}

public_create_dict
    [Arguments]    ${dic_string}
    [Documentation]    利用json格式的字符串创建字典
    [Timeout]           # 关键字执行超时时间
    ${dict}   create_dict    ${dic_string}
    [Return]    ${dict}

public_set_dict
    [Arguments]    ${dic}    ${key}    ${value}
    [Documentation]    更新字典的键值
    [Timeout]           # 关键字执行超时时间
    set_dict    ${dic}    ${key}    ${value}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_del_list_by_index
    [Arguments]    ${target_list}    ${start}=    ${end}=
    [Documentation]    删除列表元素
    [Timeout]           # 关键字执行超时时间
    del_list_by_index    ${target_list}    ${start}    ${end}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_until_keyword_succeeds
    [Arguments]    ${keyword}    @{args}    ${counts}=30x    ${interval}=2s
    [Documentation]    公共装饰器函数
    [Timeout]           # 关键字执行超时时间
    Wait Until Keyword Succeeds    ${counts}    ${interval}    ${keyword}     @{args}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_run_keyword_until_except
    [Arguments]    ${keyword}    @{args}    ${except_result}=    ${counts}=5    ${interval}=2
    [Documentation]    公共装饰器函数
    ...    1.轮询等待关键字执行返回除except_result以外的值，超过轮询的次数和时间后报错；
    [Timeout]           # 关键字执行超时时间
    ${default_except_result}    create list    ${None}   no_target_element_index
    ${except_result}    set variable if     $except_result    ${except_result}    ${default_except_result}
    ${return_value}    Run Keyword    ${keyword}    @{args}
    ${return_value}    evaluate    str($return_value)
    info    除外条件:${except_result}
    FOR    ${count}    IN RANGE    0    ${counts}
        # 返回值还在除外条件内则继续轮询
        IF    $return_value in $except_result
            sleep    ${interval}
            ${return_value}    Run Keyword    ${keyword}    @{args}
            info    第${count}次轮询：${return_value}
        ELSE
            Exit For Loop
        END
    END
    ${assert}    evaluate    $return_value not in $except_result
    public_assert_true    ${assert}
    [Return]    ${return_value}

public_run_keyword_until_include
    [Arguments]    ${keyword}    @{args}    ${include_result}=    ${counts}=5    ${interval}=2
    [Documentation]    公共装饰器函数
    ...    1.轮询等待关键字执行返回包含include_result的值，超过轮询的次数和时间后报错；
    [Timeout]           # 关键字执行超时时间
    ${default_include_result}    create list    ${None}   no_target_element_index
    ${include_result}    set variable if     $include_result    ${include_result}    ${default_include_result}
    ${return_value}    Run Keyword    ${keyword}    @{args}
    ${return_value}    evaluate    str($return_value)
    info    预期条件:${include_result}
    FOR    ${count}    IN RANGE    0    ${counts}
        # 返回值不在期望范围内则继续轮询
        IF    $return_value not in $include_result
            sleep    ${interval}
            ${return_value}    Run Keyword    ${keyword}    @{args}
            info    第${count}次轮询：${return_value}
        ELSE
            Exit For Loop
        END
    END
    ${assert}    evaluate    $return_value in $include_result
    public_assert_true    ${assert}
    [Return]    ${return_value}

public_clear_input_text
    [Arguments]    ${loactor}
    [Documentation]    清除输入框，当public_wait_and_input_text关键字的clear参数无效时，使用该方法
    [Timeout]           # 关键字执行超时时间
    ${id}    create_random_string    6
    # 分配临时ID属性给元素
    Wait Until Element Is Visible    ${loactor}
    Assign Id To Element   ${loactor}    ${id}
    # 调用原生的JS语法清除input的内容
    Execute Javascript    document.getElementById("${id}").value=""
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_set_bgcolor
    [Arguments]    ${loactor}    ${color}=red
    [Documentation]    给元素背景色着色
    [Timeout]           # 关键字执行超时时间
    ${id}    create_random_string    6
    # 分配临时ID属性给元素
    Wait Until Element Is Visible    ${loactor}
    Assign Id To Element   ${loactor}    ${id}
    # 调用原生的JS语法修改元素背景色
    Execute Javascript    document.getElementById("${id}").style.background="${color}"
    [Return]    ${id}

public_check_element_count
    [Arguments]    ${loactor}    ${expect_count}
    [Documentation]    检查指定属性的元素的个数是否符合预期
    [Timeout]           # 关键字执行超时时间
    ${target_element_list}    get webelements    ${loactor}
    ${actual_count}    evaluate    len($target_element_list)
    public_check_equal    ${expect_count}    ${actual_count}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_until_page_contains
    [Arguments]    ${text}    ${timeout}=30s    ${error}=${None}    ${laoding_text}=正在加载
    [Documentation]    等待直到界面包含指定的文本，同时不包含排外文本
    [Timeout]           # 关键字执行超时时间
    Wait Until Page Contains    ${text}    ${timeout}    ${error}
    public_wait_until_page_does_not_contain    ${laoding_text}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_until_page_does_not_contain
    [Arguments]    ${text}=正在加载    ${timeout}=30s    ${error}=${None}
    [Documentation]    等待直到界面包不含指定的文本
    [Timeout]           # 关键字执行超时时间
    Wait Until Page Does Not Contain    ${text}    ${timeout}    ${error}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_get_len
    [Arguments]    ${variable}
    [Documentation]    打印并返回变量的长度
    [Timeout]           # 关键字执行超时时间
    ${actual}    evaluate    len($variable)
    debug    目标变量长度：${actual}
    [Return]    ${actual}

public_click_element_in_table
    [Arguments]    ${keyword}    @{args}    ${table_num}=3    ${text}=${empty}    ${specify_xpath}=${empty}    ${timeout}=10s    ${error}=${None}
    [Documentation]    公共关键字，通过接口查询目标元素的索引后，再通过索引确认页面元素集的目标元素实现点击操作
    ...    keyword    str|接口函数名，根据入参确定目标数据唯一的索引并返回该索引
    ...    args       list|接口的参数
    ...    table_num  str|表格个数
    ...    text       str|待点击目标元素的text
    ...    timeout    str|页面查找text的超时时间
    ...    error      str|页面找不到text的报错消息
    ...    e.g:  调用接口inter_get_enterprise_account_index，并根据name属性确定唯一索引，然后获取text=详情的页面元素列表，利用索引定位列表中的目标元素对象
    ...          #public_click_element_in_table    inter_get_enterprise_account_index    ${name}    table_num=2    text=详情
    [Timeout]           # 关键字执行超时时间
    # 确认页面目标字符串可见
    Wait Until Page Contains    ${text}    ${timeout}    ${error}
    # 针对text属性前后有空格进行容错处理
    ${text_space}    Get WebElements    xpath=//*[text()=" ${text} "]
    ${text_nospace}    Get WebElements    xpath=//*[text()="${text}"]
    # 针对text动态变化的元素(如：启用/禁用)利用其他xpath来定位处理
    ${element_specify_xpath}    Run Keyword If    $specify_xpath    Get WebElements    xpath=${specify_xpath}
    ...    ELSE    Set Variable    ${empty}

    # 判断确定最终的目标元素
    ${target_text}    Set Variable If
    ...    $text and $text_space    ${text_space}
    ...    $text and $text_nospace    ${text_nospace}
    ...    $specify_xpath and $element_specify_xpath    ${element_specify_xpath}
    
    Should Not Be Empty    ${target_text}    msg=目标元素未找到：${text}|${specify_xpath}
    
    ${target_text_len}    public_get_len    ${target_text}
    debug    目标元素个数: ${target_text_len}

    # 运行接口查找包含目标元素的数据所在数据集的索引
    ${element_index}    Run Keyword    ${keyword}    @{args}
    debug    目标元素接口索引:${element_index}
    ${actual}    evaluate    "${element_index}"=="0" or $element_index
    public_assert_true    ${actual}    msg=接口未查询到目标数据：${actual}

    # 根据页面元素堆叠逻辑计算元素页面索引
    ${target_element_index}    evaluate    int($target_text_len/int($table_num)*(int($table_num)-1)+int($element_index))
    info    目标元素页面索引:${target_element_index}

    public_wait_and_click_Element    ${target_text}[${target_element_index}]
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_and_mouse_over
    [Arguments]    ${locator}    ${timeout}=30s    ${error}=${None}
    [Documentation]     公共关键字，等待指定元素可见后再执行鼠标悬浮动作
    [Timeout]           # 关键字执行超时时间
    Wait Until Element Is Visible    ${locator}    ${timeout}    ${error}
    Mouse Over    ${locator}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_and_mouse_out
    [Arguments]    ${locator}    ${timeout}=30s    ${error}=${None}
    [Documentation]     公共关键字，等待指定元素可见后再执行鼠标移出动作
    [Timeout]           # 关键字执行超时时间
    Wait Until Element Is Visible    ${locator}    ${timeout}    ${error}
    Mouse Out    ${locator}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_and_mouse_down
    [Arguments]    ${locator}    ${timeout}=30s    ${error}=${None}
    [Documentation]     公共关键字，等待指定元素可见后再执行鼠标左键点击动作
    [Timeout]           # 关键字执行超时时间
    Wait Until Element Is Visible    ${locator}    ${timeout}    ${error}
    Mouse Down    ${locator}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_and_mouse_up
    [Arguments]    ${locator}    ${timeout}=30s    ${error}=${None}
    [Documentation]     公共关键字，等待指定元素可见后再执行鼠标左键释放动作
    [Timeout]           # 关键字执行超时时间
    Wait Until Element Is Visible    ${locator}    ${timeout}    ${error}
    Mouse Up    ${locator}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_and_drag_and_drop
    [Arguments]    ${locator}    ${target}    ${timeout}=30s    ${error}=${None}
    [Documentation]     公共关键字，等待指定元素可见后再执行点击动作
    [Timeout]           # 关键字执行超时时间
    Wait Until Element Is Visible    ${locator}    ${timeout}    ${error}
    Wait Until Element Is Visible    ${target}    ${timeout}    ${error}
    Drag And Drop    ${locator}    ${target}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_wait_and_drag_and_drop_by_offset
    [Arguments]    ${locator}    ${xoffset}    ${yoffset}    ${timeout}=30s    ${error}=${None}
    [Documentation]     公共关键字，等待指定元素可见后再执行点击动作
    [Timeout]           # 关键字执行超时时间
    Wait Until Element Is Visible    ${locator}    ${timeout}    ${error}
    Drag And Drop By Offset    ${locator}     ${xoffset}    ${yoffset}
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值

public_run_keyword_with_variable
    [Arguments]    ${variable}    ${keyword}
    [Documentation]     公共关键字，判断指定变量存在的时候运行关键字
    [Timeout]           # 关键字执行超时时间
    ${variables}    Get Variables    no_decoration=True
    ${actual}    evaluate    "${variable}" in $variables
    Run Keyword If    $actual    ${keyword}   ${variables}[${variable}]
    [Teardown]          # 关键字的teardown
    [Return]            # 关键字返回值