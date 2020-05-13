# SimpleUI settings
# https://github.com/newpanjing/simpleui/blob/master/QUICK.md
# SIMPLEUI_FAVICON_ICON = "/static/bistu/img/logo.png"
# SIMPLEUI_LOGIN_LOGO = "/static/bistu/img/caiselogo.png"
# SIMPLEUI_INDEX_LOGO = "/static/bistu/img/logo.png"
# SIMPLEUI_HOME_TITLE = '工作台'
# SIMPLEUI_HOME_ICON = 'fas fa-tachometer-alt'

# 站点域名
DOMAIN_NAME = 'http://127.0.0.1:'
# 站点应用端口
PORT = '8000'

# 开启/关闭登录页粒子动画（默认为开启）
SIMPLEUI_LOGIN_PARTICLES = True

# 首页配置
# SIMPLEUI_HOME_PAGE = 'https://www.baidu.com'

# 首页标题
# SIMPLEUI_HOME_TITLE = '百度一下你就知道'

# 首页图标,
# 支持element-ui和fontawesome的图标，
# 参考https://fontawesome.com/icons图标
# SIMPLEUI_HOME_ICON = 'fa fa-user'

# 设置simpleui 点击首页图标跳转的地址
SIMPLEUI_INDEX = DOMAIN_NAME + PORT + '/admin'

"""
首页-模块
首页默认展示3个模块，服务器信息、快速操作、最近动作，大家可以根据需要来显示或者隐藏某些模块。
"""

# 修改LOGO(左上角图标)
SIMPLEUI_LOGO = '/static/admin/img/simpleui_logo.png'

# 显示/隐藏服务器信息（默认显示）
SIMPLEUI_HOME_INFO = False

# 显示/隐藏快速操作（默认显示）
SIMPLEUI_HOME_QUICK = True

# 显示/隐藏最近动作（默认显示）
SIMPLEUI_HOME_ACTION = True

# 使用分析
# 默认开启，统计分析信息只是为了更好的帮助simpleui改进，
# 并不会读取敏感信息。并且分析数据不会分享至任何第三方。
SIMPLEUI_ANALYSIS = False

# 是/否离线模式(默认为否)（不加载任何第三方资源）
# 指定simpleui 是否以脱机模式加载静态资源，
# 为True的时候将默认从本地读取所有资源，即使没有联网一样可以。
SIMPLEUI_STATIC_OFFLINE = True

# 关闭/开启Loading遮罩层
SIMPLEUI_LOADING = True

SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menus': [
        {
            'app': 'users',
            'name': '用户管理',
            'icon': 'fas fa-user-shield',
            'models': [
                {
                    'name': '用户',
                    'icon': 'fa fa-user',
                    'url': 'auth/user/'
                },
                {
                    'name': '用户组',
                    'icon': 'fa fa-users-cog',
                    'url': 'auth/group/'
                }
            ]
        },
        {
            'app': 'recipe',
            'name': '减肥食谱管理',
            'icon': 'fas fa-user-shield',
            'models': [
                {
                    'name': '食物分类',
                    'icon': 'fa fa-user',
                    'url': 'recipe/classfoodmodel/'
                },
                {
                    'name': '食物',
                    'icon': 'fa fa-users-cog',
                    'url': 'recipe/foodmodel/'
                },
                {
                    'name': '食谱',
                    'icon': 'fa fa-users-cog',
                    'url': 'recipe/recipemodel/'
                }
            ]
        },
        {
            'app': 'meal',
            'name': '每日一餐管理',
            'icon': 'fas fa-user-shield',
            'models': [
                {
                    'name': '每日一餐记录',
                    'icon': 'fa fa-user',
                    'url': 'meal/mealmodel/'
                },
            ]
        },
        # {
        #     'app': 'auth',
        #     'name': '账户管理',
        #     'icon': 'fas fa-user-shield',
        #     'models': [
        #         {
        #             'name': '用户',
        #             'icon': 'fa fa-user',
        #             'url': 'auth/user/'
        #         },
        #         {
        #             'name': '用户组',
        #             'icon': 'fa fa-users-cog',
        #             'url': 'auth/group/'
        #         }
        #     ]
        # },
        # {
        #     'app': 'blog',
        #     'name': '博客管理',
        #     'icon': 'fas fa-user-shield',
        #     'models': [
        #         {
        #             'name': '用户',
        #             'icon': 'fa fa-user',
        #             'url': 'blog/user/'
        #         },
        #         {
        #             'name': '分类列表',
        #             'icon': 'fa fa-users-cog',
        #             'url': 'blog/category/ '
        #         },
        #         {
        #             'name': '文章列表',
        #             'icon': 'fa fa-user',
        #             'url': 'blog/article/'
        #         },
        #         {
        #             'name': '标签列表',
        #             'icon': 'fa fa-user',
        #             'url': 'blog/tag/'
        #         },
        #         {
        #             'name': '评论列表',
        #             'icon': 'fa fa-user',
        #             'url': 'blog/articlecomment/'
        #         },
        #     ]
        # },
        {
            'app': 'epidemic',
            'name': '疫情',
            'models': [
                {
                    'name': '疫情数据分析',
                    'url': '/epidemic/'
                },
                {
                    'name': '疫情大数据可视化',
                    'url': '/DA_epidemic/'
                },
            ]
        },
        # {
        #     'app': 'accounts',
        #     'name': '学生管理',
        #     'icon': 'fa fa-graduation-cap',
        #     'url': 'accounts/student/'
        # },
        # {
        #     'app': 'accounts',
        #     'name': '教师管理',
        #     'icon': 'fa fa-id-card',
        #     'url': 'accounts/tutor/'
        # },
        # {
        #     'app': 'colleges',
        #     'name': '学院管理',
        #     'icon': 'fa fa-university',
        #     'models': [
        #         {
        #             'name': '学院',
        #             'icon': 'fa fa-university',
        #             'url': 'colleges/academy/'
        #         },
        #         {
        #             'name': '专业',
        #             'icon': 'fa fa-university',
        #             'url': 'colleges/major/'
        #         },
        #         {
        #             'name': '班级',
        #             'icon': 'fa fa-university',
        #             'url': 'colleges/class/'
        #         },
        #         {
        #             'name': '教改',
        #             'icon': 'fa fa-university',
        #             'url': 'colleges/reform/'
        #         },
        #         {
        #             'name': '统计',
        #             'icon': 'fa fa-university',
        #             'url': 'colleges/reformresults/'
        #         }
        #     ]
        # },
        # {
        #     'app': 'education',
        #     'name': '教学管理',
        #     'icon': 'fas fa-book',
        #     'models': [
        #         {
        #             'name': '论文',
        #             'icon': 'fa fa-book',
        #             'url': 'education/thesis/'
        #         },
        #         {
        #             'name': '论文查重',
        #             'icon': 'fa fa-book',
        #             'url': 'education/thesisplacheck/'
        #         },
        #         {
        #             'name': '论文盲审',
        #             'icon': 'fa fa-book',
        #             'url': 'education/thesisblindreview/'
        #         },
        #     ]
        # }
    ]
}
