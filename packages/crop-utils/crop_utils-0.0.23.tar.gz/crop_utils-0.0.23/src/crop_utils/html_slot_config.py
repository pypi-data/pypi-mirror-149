# 标签  每个元素
ES = 'es'  # 每个元素
# 属性
T = 't'  # type 类型 image text table|  ms中的 标题 | ms-sub 中的 标题
SLOT = 's'  # slot配置
URL = 'u'  # 链接
WIDTH = 'w'  # 图片宽
HEIGHT = 'h'  # 图片高

# 匹配状态
MATCH_STATUS = 'm_s'  # 状态: f：未匹配成功 s：匹配成功

# 模块标签
MS = 'ms'  # 画布、模块  可以商量改一下 ，改为画布
MS_LOOP = 'ms-loop'
# 子模块标签
MS_SUB = 'ms-sub'  # 子画布
DATA_COLOR = 'data-color'  # 3.0版本不支持，4.0支持颜色排版
# 属性
LOOP = 'l'  # 循环的类型

#  Slot 配置的 mapping
VERSION = 'v'
SLOT_VERSION = '2020-12-12'
UUID = 'id'
MATCH_SLOT = 'ms'  # ai匹配
MS_IMAGE_BACKGROUND = 'ms_image_background'
NAME_SLOT = 'ns'  # 命名替换
MATCH_UUID = 'm_u'  # 匹配uuid
REPEAT_MATCH_UUID = 'r_m_u'  # 重复匹配uuid

DEFAULT_DISPLAY = 'd_d'  # 未替换时，默认展示的图片 0系统占位图  1模板图片 2空白图片

COLOR = 'c'  # 颜色
REPEAT_SLOT_IMG = 'r_s_i'  # 槽内图片是否被其他槽重复使用1次
REPEAT_SLOT_IMG_INFINITE = 'r_s_i_in'  # 槽内图片是否被其他槽重复使用N次
REPEAT = 'r'  # 重复替换
R_IMAGE_BACKGROUND = 'r_image_background'
STRETCH = 's'  # 是否自适应 fix固定不变  w自适应
CROP = 'cr'  # 裁剪
NEED_CROP = 'n_c'  # 0不裁剪  1 裁剪
X_CENTER_METHOD = "x_c_m"  # 左右居中方式  human_center human_and_cloth brand
RETAIN_X_OR_Y = "r_x_o_y"  # # 保留上下 y 保留左右居中 x  最大限度满足兴趣区域上下裁剪 interest_x
MAIN_PRODUCT_CROP = "m_p_c"  # 0不裁剪主商品  1 裁剪主商品
MODEL_TOP = 'm_t'
MODEL_BUST = 'm_bu'
MODEL_BOTTOM = 'm_bo'
MODEL_FULL = 'm_f'
TILE = 't'
BRAND = 'b'
CROP_DETAIL = 'c_d'
GIF = 'g'

TOP_SITE = 'ts'
BOTTOM_SITE = 'bs'
TOP = 't'
LEFT = 'l'
BOTTOM = 'b'
RIGHT = 'r'
PADDING_UNIT = 'pU'  # pe pi

DROP = 'd'
TYPE = 't'

DATA_SLOT_ID = 'data-slot-id'  # 元素新增uuid 与slots_json 绑定
DATA_TEMPLATE_COLOR = 'data-template-color'  # 模板背景色色块  3.0版本不支持，4.0支持颜色排版
