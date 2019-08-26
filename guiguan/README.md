## Project changqing

#### 工程简介
本工程开发背景是基于常青嵌入式系统测试的自动化需求，希望通过本工程实现对系统测试基本功能用例的快速回归，从而达到有效提高测试效率的目的。

工程开发和运行解释器环境为python3.5，操作系统环境为ubuntu的16.04 LTS。

整个工程基于pytest搭建了测试框架，目录结构主要由common、configs、data、email、log、report、services、testcases、testsuite几个目录构成，各目录的说明详见下节的目录结构描述。

#### 目录结构描述
```
changqing/                      # 父目录
├── common                      # 公共目录，目录中的模块文件定义了业务层运行时所需的各类常量、类和函数
│   ├── check_result.py         # 结果校验模块，抽象和封装了测试结果的校验和分析动作
│   ├── command.py              # 命令模块，定义了常用的linux命令常量
│   ├── comm_paras.py           # 公共参数模块，定义了常用的本地工程目录常量和远程host目录常量、以及ssh连接对象常量
│   ├── host_visitor.py         # 远程host访问模块，定义了ssh访问类HostVisitor（用于执行linux命令和sftp文件传输）和ftp操作类FtpHandler(用于普通ftp文件传输)。
│   ├── manip_case_table.py     # 用例表操作模块，抽象和封装了针对测试用例excel表的读写动作
│   ├── manip_cfg_file.py       # ini配置文件操作模块，抽象和封装了针对ini文件的读写动作
│   ├── manip_report.py         # 测试报告操作模块，抽象和封装了修改和更新测试报告的动作
│   ├── operate_os.py           # 系统操作模块，针对常青os系统的操作动作进行了抽象和封装
│   ├── parse_str.py            # 字符串解析模块，模块中定义的函数用于对测试结果返回的字符串进行结果提取，提取动作基于正则表达式
│   └── record_time_log.py      # 日志记录模块，抽象和封装了日志文件生成和日志句柄对象生成两个功能
├── configs                     # 配置目录，用于存放配置文件
│   ├── config.ini              # 主配置文件，包含硬件类型、host信息、邮件信息等几个方面配置
│   └── module.ini              # 模块选择文件，用于选择测试模块
├── data                        # 数据目录，存放各类测试使用数据
│   ├── os_version              # os版本目录，用于存放os版本文件
│   ├── ota                     # ota目录，用于存放ota所需的地图文件和配置文件
│   ├── shell                   # shell脚本目录，用于存放测试所需的shell脚本
│   └── uos_version             # uos版本目录，用于存放uos版本文件
├── Email                       # 邮件目录，存放了邮件操作模块文件
│   └── send_mail.py            # 邮件模块，封装了邮件发送的功能函数，实现测试报告的邮件发送
├── log                         # 测试日志目录，存放所有的历史日志文件
├── report                      # 测试报告目录，存放测试执行完成后生成的测试报告文件
│   └── report.html             # 测试报告html文件
├── services                    # 业务层目录，存放各个测试模块文件
│   ├── APU.py                  # APU业务模块，对应测试模块APU中各测试用例的业务流程和测试结果校验都以函数的形式进行了抽象和封装
│   ├── FPGA.py                 # FPGA业务模块，对应测试模块FPGA中各测试用例的业务流程和测试结果校验都以函数的形式进行了抽象和封装
│   ├── IO_External.py          # IO_External业务模块，对应测试模块IO_External中各测试用例的业务流程和测试结果校验都以函数的形式进行了抽象和封装
│   ├── IO_Internal.py          # IO_Internal业务模块，对应测试模块IO_Internal中各测试用例的业务流程和测试结果校验都以函数的形式进行了抽象和封装
│   ├── Network.py              # Network业务模块，对应测试模块Network中各测试用例的业务流程和测试结果校验都以函数的形式进行了抽象和封装
│   ├── OTA.py                  # OTA业务模块，对应测试模块OTA中各测试用例的业务流程和测试结果校验都以函数的形式进行了抽象和封装
│   └── TX2.py                  # TX2业务模块，对应测试模块TX2中各测试用例的业务流程和测试结果校验都以函数的形式进行了抽象和封装
├── testcases                   # 用例表目录
│   └── case_cq.xlsx            # 常青测试用例excel表
├── testsuite                   # 测试套件目录，存放了对应各测试模块的测试套件文件
│   ├── test_a_TX2.py           # TX2测试套件模块，基于pytest实现对业务层TX2模块中所有用例的执行
│   ├── test_b_APU.py           # APU测试套件模块，基于pytest实现对业务层APU模块中所有用例的执行
│   ├── test_c_Network.py       # Network测试套件模块，基于pytest实现对业务层Network模块中所有用例的执行
│   ├── test_d_FPGA.py          # FPGA测试套件模块，基于pytest实现对业务层FPGA模块中所有用例的执行
│   ├── test_e_IO_Internal.py   # TX2测试套件模块，基于pytest实现对业务层TX2模块中所有用例的执行
│   ├── test_f_IO_External.py   # IO_External测试套件模块，基于pytest实现对业务层IO_External模块中所有用例的执行
│   └── test_g_OTA.py           # OTA测试套件模块，基于pytest实现对业务层OTA模块中所有用例的执行
├── conftest.py                 # pytest测试配置文件，重写了pytest所定义的部分钩子函数，实现对测试结果和报告呈现的个性定制
├── run.py                      # 测试启动文件，用于启动测试和执行测试报告邮件发送
├── venv                        # python虚拟环境文件目录，存放了虚拟环境中的各种配置文件、python解释器和已安装的模块库
└── README.md                   # 工程说明文件
```

#### 功能模块简介
整个工程按照逻辑功能可以划分为测试模块选择、用例读取、用例执行、结果校验、日志记录、结果写入、测试报告生成、邮件发送，下面对各个功能模块依次介绍：
1. 测试模块选择  
测试模块的选择通过`pytest.main`函数中的`-k keys`参数来对测试模块进行筛选，其中`keys`是pytest用来收集用例的关键字字符串，使用`or`来连接各模块名。在指定pytest收集测试套件目录为testsuite后，pytest会按照`keys`中的模块名查找并执行testsuite目录下的对应套件。
2. 用例读取  
在确定测试的模块后，我们会将excel表中的用例信息读取出来，传入pytest的装饰器`@pytest.mark.parametrize`参数`case_params`。为了按照选定模块来完成excel表用例信息的读取，我们封装了`get_selected_case_param`函数，它通过选择的模块名映射到具体excel表sheet页，然后根据excel表中switch列中的勾选情况来选择将置on的用例信息读取到二维列表中。
3. 用例执行  
在上个功能模块中已经提到，excel表中的用例信息读取出来之后，会传入pytest的装饰器`@pytest.mark.parametrize`参数`case_params`，被该装饰器装饰的测试函数会按照遍历用例信息列表的方式完成用例的依次执行。例如TX2模块的测试执行代码入口：
    ```python
    @pytest.mark.parametrize(
        'case_name, case_input, case_expect',
        case_params,
        ids=[case_param[0] for case_param in case_params]
    )
    def test_TX2(case_name, case_input, case_expect):
        assert run_case(case_name, case_input, case_expect)
    ```
上面代码中`run_case`函数在services目录中的业务模块（例如TX2.py）定义，当`run_case`被调用时，最终会执行语句`dict_func[case_name]()`，其中`dict_func`是在业务模块中定义的用例名字符串与业务函数间的映射字典，该语句根据用例名索引到对应的业务函数并执行。`dict_func`如下所示：
    ```python
    dict_func = {
        'check version': check_version,
        'degrade os verision': degrade_os_ver,
        'upgrade os verision': upgrade_os_ver,
        'set product type cq': set_prod_type_cq,
        'set product type gg': set_prod_type_gg,
    }
    ```
4. 结果校验  
用例业务函数执行到最后阶段时，针对返回的业务结果，通过调用`check_result.py`中定义的函数对业务结果进行了分析与校验，如果用例执行失败，则使用`assert False`去断言，之所以使用assert断言机制，是基于pytest的结果收集机制来考虑的，pytest会将assert为False的用例判定为fail并将assert处的异常记录下来，并最终呈现在总的测试结果summary中。
5. 日志记录  
在通过`run.py`启动时，程序就会调用`record_time_log.py`中的`get_logger`函数，该函数会在log目录中建立本次测试的log文件，并返回日志句柄对象`logger`并保存到全局变量`g_logger`中，`logger`按级别划分为`debug`、`info`、`warning`、`error`几个级别，测试业务执行过程中遇到需要记录的打印，可以按照级别直接调用`g_logger`,例如要打印告警就调用`g_logger.warning`，此时打印会同时输出到终端界面和log文件中。
6. 结果写入  
考虑到可能出现的测试中断场景，我们在每条测试用例执行完后都立即将结果写入用例excel表中。测试过程中用例结果的获取是通过`conftest.py`中的钩子函数`pytest_runtest_makereport`来实现，其中通过`yield`生成的`report`对象包含了每条用例的执行结果，可以提取出来并写入对应的用例excel表result列，用例结果写入的过程封装在函数`write_rst_to_xls`中。
7. 测试报告生成  
测试报告生成使用了pytest的插件pytest-html，这个插件可以将pytest的用例结果以html形式生成一份简单的测试报告。报告功能启用是在入口函数`pytest.main`中加入`'--html', report_path, '--self-contained-html'`三个参数即可，其中变量`report_path`指定了报告生成的路径，`--self-contained-html`使得报告在发送邮件时能够保留网页的格式。
8. 邮件发送  
在测试报告report.html生成后，通过模块`send_mail.py`中定义的`mail_report`函数，将html报告邮件发送给指定邮箱。`mail_report`函数会去读取`config.ini`中的邮件配置，以获取发件人、收件人等信息，典型的邮件配置信息如下所示：
    ```
    [mail]
    sender = user@uisee.com
    receivers = user1@uisee.com,user2@uisee.com
    smtpserver = smtp.uisee.com
    username = user@uisee.com
    password = password
    ```

#### 工程涉及的第三方库
* paramiko 2.4.2  
该模块用来实现和系统master和slave建立ssh连接、sftp连接，并通过ssh连接执行linux命令，通过sftp连接进行文件的上传、下载等操作。
* pexpect 4.6.0  
该模块是对paramiko进行系统操作的补充，因为部分用例的业务流程涉及图形用户界面权限，而paramiko是非图形界面权限下工作的，因此有时需要通过pexpect直接模拟linux终端命令交互的过程，进而规避paramiko库没有图形界面权限的问题。
* pytest 4.2.1  
如前面介绍功能模块所提到的，pytest模块作为python的流行测试插件实现了用例的收集，用例的遍历执行以及用例结果的记录。
* pytest-html 1.20.0  
这个模块是依赖pytest开发的插件，用来提取pytest的用例执行结果并生成html格式的测试报告。
* xlrd 1.2.0  
该模块用来读取excel表中的内容，在读取excel用例表中的用例信息时使用。

#### 使用说明
工程的运行可以参照以下步骤进行：
1. 配置工程  
工程的相关配置在configs目录下的config.ini，主要包含硬件类型、host信息、ftp服务器信息、邮件配置信息三个部分。硬件类型是为了日后对gg的支持扩展，目前默认为cq；host信息就是配置的master和slave的ssh登录信息，一般情况下不需要修改；ftp服务器信息是ftp访问时的必需信息，改动频率也不大；邮件配置指定了发件人和收件人，可以按实际情况进行修改。
2. 选择测试模块  
模块选择目前可以在文件configs目录下的module.ini文件中进行，模块名开头如果没有#，表示改模块用例将被执行，否则不执行，例如我要执行TX2和APU两个模块的用例，可以将module.ini文件内容修改如下：
    ```
    test_TX2
    #test_Network
    test_APU
    #test_FPGA
    #test_IO_Internal
    #test_IO_External
    #test_OTA
    #test_Pressure
    ```
3. 测试用例准备  
前面提到，工程会到用例表中读取用例信息，实际执行时，当config.ini中的硬件类型为cq时，用例表对应了testcases目录下的case_cq.xlsx，如果硬件类型为gg，则对应case_gg.xlsx。一般情况下，只要对用例表进行用例勾选的操作，此时如果要执行某个用例，将该用例对应的switch列置为on即可。  另外，关于用例准备，有几个地方需要特别关注，一个是某些用例和版本强相关，需要注意在版本有更新时针对用例输入和预期结果做对应更新；一个是某些用例需要准备数据，例如版本文件等等，目前固定是放在data目录下的，data目录下的说明可以参考本文档第二段的目录结构描述；最后执行用例前应关注用例的预置条件，例如一些外设（摄像头、外置路由等）是否在位等等。
4. 启动工程  
工程的启动文件为run.py，为保证工程的可移植性，如果在命令终端中执行，在工程changqing目录下，应使用`./venv/bin/python3 run.py`来执行脚本；如果在pycharm中执行run.py，需要先将工程使用的解释器引用为venv目录中的python解释器。对于邮件发送功能，如果需要使用，请将run.py中最后代码行的邮件发送代码去掉注释。
5. 查看用例结果与日志    
用例结果的查看有两种方式，一个是直接查看report目录中的测试报告report.html，里面包含了用例的执行结果以及失败原因，另外一种方式是打开testcases目录下的用例表，在result列也保存了每条用例的结果。  对于日志的查看，直接查看log目录下的log文件即可，日志文件按本次执行开始的时间命名。 
