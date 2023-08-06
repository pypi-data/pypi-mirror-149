import json

IMG_CLASSIFY = [['模特图', '模特上身图', '模特上身正面'], ['模特图', '模特上身图', '模特上身侧面'], ['模特图', '模特上身图', '模特上身背面'],
                ['模特图', '模特胸像图', '模特胸像正面'], ['模特图', '模特胸像图', '模特胸像侧面'], ['模特图', '模特胸像图', '模特胸像背面'],
                ['模特图', '模特下身图', '模特下身正面'], ['模特图', '模特下身图', '模特下身侧面'], ['模特图', '模特下身图', '模特下身背面'],
                ['模特图', '模特全身图', '模特全身正面'], ['模特图', '模特全身图', '模特全身侧面'], ['模特图', '模特全身图', '模特全身背面'],
                ['细节图', '面料'], ['细节图', '领部'], ['细节图', '肩部'], ['细节图', '腰部'], ['细节图', '衣袖'], ['细节图', '下摆'],
                ['细节图', '口袋'], ['细节图', '门襟'], ['细节图', '内衬'], ['细节图', '图案'], ['细节图', '裤脚'],
                ['平铺图', '平铺图背面'], ['平铺图', '平铺图正面'],
                ['资质图', '吊牌图'], ['资质图', '洗水唛'],
                ['动图']
                ]

CROP_TYPE = {
    'm_t': ['模特上身正面', '模特上身侧面', '模特上身背面'],
    'm_bu': ['模特胸像正面', '模特胸像侧面', '模特胸像背面'],
    'm_bo': ['模特下身正面', '模特下身侧面', '模特下身背面'],
    'm_f': ['模特全身正面', '模特全身侧面', '模特全身背面'],
    't': ['平铺图背面', '平铺图正面'],
    'b': ['资质图', '吊牌图', '洗水唛'],
    'g': ['动图'],
}


class Image:
    def __init__(self, data):
        #   1. 图片分类
        #   2. 颜色
        #   3. 裁剪范围
        #   4. 图片中人的数量，衣服的数量

        self.img_id = data.get('id')

        self.storage_key = data.get('storage_key')

        self.img_format = data.get('format')
        self.width = data.get('width')
        self.height = data.get('height')

        try:
            self.ratio = self.width / self.height
        except TypeError:
            raise TypeError(f"图片错误，请前往图片包页面将错误图片删除后再重试")
        except ZeroDivisionError:
            raise ZeroDivisionError(f"图片错误，请前往图片包页面将错误图片删除后再重试")
        except Exception:
            # logging.error("图片宽高信息错误", exc_info=True)
            raise Exception(f"图片错误，请前往图片包页面将错误图片删除后再重试")

        self.hot_area = None  # 自动生成热区
        self.hot_area_type = None  # 热区类型 url(链接) goods(货号)
        self.hand_hot_area_data(data.get('hot_area', {}))

        self.copy_writing = data['copy_writing'] if data.get('copy_writing') else ''
        self.name_slot = data.get('name_slot')
        self.name_slot_index = data.get('name_slot_index', 0)

        self.color = data.get('color', 1)  # 根据命名的颜色文件夹来划分 颜色 1 2 3 ·····
        self.color_name = data.get("color_name")  # 根据命名的颜色文件夹来划分 颜色 1 2 3 ·····
        self.filename = data.get("filename")  # 根据命名的颜色文件夹来划分 颜色 1 2 3 ·····

        image_analysis = data.get('image_analysis')
        if not image_analysis:
            image_analysis = {}

        self.ai_image_classification = '未识别'

        self.image_classification = self.amend_image_classification(data.get('image_classification'))  # 图片分类

        for i in IMG_CLASSIFY:
            if self.image_classification == i[-1]:
                self.image_classification_list = i
                break
        else:
            self.image_classification_list = [self.image_classification]  # 所属图片分类列表

        self.img_crop_type = None
        for t, img_class_list in CROP_TYPE.items():
            if self.image_classification in img_class_list:
                self.img_crop_type = t

        image_analysis['storage_key'] = self.storage_key
        self.humans = Human(image_analysis)
        self.cloths = Cloths(image_analysis)

        self.image_analysis = image_analysis
        # 获取主商品
        self.crop_point = self.deal_crop_key_point()
        # 获取图片背景图
        self.image_background = self.deal_image_background()

        self.image_detail = ImageDetail()
        self.detail_point = {}  # {'裁剪模特帽子':{},}

        if self.img_crop_type == 'b':
            self.brand = Brand(image_analysis)
            self.brand_crop_point = self.brand.deal_brand_crop_point()

        self.match_crop_detail = []

    def hand_hot_area_data(self, area_data):
        """
        自己根据 area content 添加 hot_area_type
        """
        if not area_data:
            return

        def is_url(hot_area):
            """判断热区是否为url"""
            return (hot_area and
                    (hot_area.get("hot_tb") or hot_area.get('hot_jd') or hot_area.get('hot_tm') or hot_area.get(
                        'hot_yz')))

        image_hot_area = area_data.get("content")
        if image_hot_area:
            hot_area = json.loads(image_hot_area)
            if is_url(hot_area):
                self.hot_area_type = "url"
            elif hot_area is not None and hot_area.get("code", None) is not None:
                self.hot_area_type = "goods"
            # Frontend need an object, loads string data into json object
            self.hot_area = hot_area

    def amend_image_classification(self, image_classification):
        '''ImageClassificationCategoryList = [
                    {
                        'name':
                            '模特上身图',
                        'value':
                            'model-top',
                        'sub_category': [
                            {
                                'name': '上身图正面',
                                'sub_category': None,
                                'value': 'model-top_positive',
                                'default': True,
                            },
                            {
                                'name': '上身图侧面',
                                'sub_category': None,
                                'value': 'model-top_side',
                            },
                            {
                                'name': '上身图背面',
                                'sub_category': None,
                                'value': 'model-top_back',
                            },
                        ]
                    },
                    {
                        'name':
                            '模特胸像图',
                        'value':
                            'model-up',
                        'sub_category': [
                            {
                                'name': '胸像图正面',
                                'sub_category': None,
                                'value': 'model-up_positive',
                                'default': True,
                            },
                            {
                                'name': '胸像图侧面',
                                'sub_category': None,
                                'value': 'model-up_side',
                            },
                            {
                                'name': '胸像图背面',
                                'sub_category': None,
                                'value': 'model-up_back',
                            },
                        ]
                    },
                    {
                        'name':
                            '模特下身图',
                        'value':
                            'model-down',
                        'sub_category': [
                            {
                                'name': '下身图正面',
                                'sub_category': None,
                                'value': 'model-down_positive',
                                'default': True,
                            },
                            {
                                'name': '下身图侧面',
                                'sub_category': None,
                                'value': 'model-down_side',
                            },
                            {
                                'name': '下身图背面',
                                'sub_category': None,
                                'value': 'model-down_back',
                            },
                        ]
                    },
                    {
                        'name':
                            '模特全身图',
                        'value':
                            'model-all',
                        'sub_category': [
                            {
                                'name': '全身图正面',
                                'sub_category': None,
                                'value': 'model-all_positive',
                                'default': True,
                            },
                            {
                                'name': '全身图侧面',
                                'sub_category': None,
                                'value': 'model-all_side',
                            },
                            {
                                'name': '全身图背面',
                                'sub_category': None,
                                'value': 'model-all_back',
                            },
                        ]
                    },
                    {
                        'name':
                            '平铺图',
                        'sub_category': [
                            {
                                'name': '正面',
                                'sub_category': None,
                                'value': 'tile_positive',
                                'default': True,
                            },
                            {
                                'name': '背面',
                                'sub_category': None,
                                'value': 'tile_back',
                            },
                        ],
                        'value':
                            'tile',
                    },
                    {
                        'name':
                            '细节图',
                        'sub_category': [
                            {
                                'name': '面料图',
                                'sub_category': None,
                                'value': 'detail_fabric',
                            },
                            {
                                'name': '其他',
                                'sub_category': None,
                                'value': 'detail_other',
                                'default': True,
                            },
                        ],
                        'value':
                            'detail',
                    },
                    {
                        'name':
                            '资质图',
                        'sub_category': [
                            {
                                'name': '吊牌',
                                'sub_category': None,
                                'value': 'intelligence_drop',
                                'default': True,
                            },
                            {
                                'name': '耐久性标签',
                                'sub_category': None,
                                'value': 'intelligence_tag',
                            },
                        ],
                        'value':
                            'intelligence',
                    },
                    {
                        'name':
                            '其他分类',
                        'sub_category': [
                            {
                                'name': '其他',
                                'sub_category': None,
                                'value': 'other',
                                'default': True,
                            },
                        ],
                        'value':
                            'other-category',
                    },
                ]'''
        cat_mapping = {'model': '模特', 'top': '上身', 'up': "胸像", "down": "下身", "all": "全身",
                       'tile': "平铺图",
                       "detail": "细节图", "fabric": "面料", "other": "其他",
                       "intelligence": "", 'drop': "吊牌图", 'tag': "洗水唛",
                       "positive": "正面", "side": "侧面", "back": "背面",
                       "sweep": "下摆", "lining": "内衬", "pocket": "口袋",
                       "pattern": "图案", "shoulder": "肩部", "waist": "腰部",
                       "sleeve": "衣袖", "leg": "裤脚", "stay": "门襟",
                       "collar": "领部",
                       "gif": "动图"
                       }
        try:
            # 素材中心，分类不存在 或 不存在识别分类，则按照ai识别结果的分类处理
            if not image_classification or ('no-watch' in image_classification):
                return '未识别'
            # 其他分类
            if '_' not in image_classification:
                return cat_mapping[image_classification]
            cat, sub_category = image_classification.split('_')
            if '-' not in cat:
                if sub_category != "other":
                    if cat == 'tile':
                        return cat_mapping[cat] + cat_mapping[sub_category]
                    return cat_mapping[sub_category]
                if cat == 'detail':
                    # 来个默认细节图
                    return "细节图"
                # 保持原有识别
                return self.ai_image_classification
            model, body = cat.split('-')
            return cat_mapping[model] + cat_mapping[body] + cat_mapping[sub_category]
        except Exception as e:
            # logging.error(f"图片{self.filename}, 分类解析失败: {e}", exc_info=True)
            return '未识别'

    def deal_image_background(self):
        """
        background : 0 不限 1 透明 2 白底 3 其他背景
        :return:
        """
        background_mapping = {
            "transparent": 1,
            "white": 2,
            "None": 3,
            "none": 3,
        }
        image_background = 0

        if self.image_analysis.get('recognition'):  # 新版本ai识别结果,存在主商品
            recognition = json.loads(self.image_analysis["recognition"])
            image_background = background_mapping.get(recognition.get("background"), 0)

        return image_background

    def deal_crop_key_point(self, cloth_classify=(1, 2, 3, 4, 5), main_product_crop=None):
        '''
        cloth_classify 当前详情页 图片分类是 上身 下身 全身

        >=1 人时如何裁剪 取最大值 或最小值
        每个裁剪点 均为： 矩形区域 top_site:left,top   bottom_site:right,bottom

        图片顶部：pic_top
        图片底部：pic_bottom

        头顶：human_top
        脚底：human_bottom

        衣服上边:garment_top
        衣服下边:garment_bottom

        眼睛：eye
        鼻子：nose
        耳朵：ear
        肩膀：shoulder
        肘部：elbow
        手腕：wrist
        臀部：hip
        膝盖：knee
        脚踝：ankle
        :return:
        '''

        if main_product_crop and self.image_analysis.get('recognition'):  # 新版本ai识别结果,存在主商品
            recognition = json.loads(self.image_analysis["recognition"])
            main_product_category_id = recognition.get("main_product", {}).get("category_id")
            if main_product_category_id:
                cloth_classify = [main_product_category_id]

        crop_point_dict = dict()
        crop_point_dict['pic_top'] = crop_point_dict['pic_bottom'] = {
            'top_site': [0, 0],
            'bottom_site': [1, 1]
        }
        crop_point_dict = self.humans.deal_human_crop_point(crop_point_dict)

        self.cloths.cloth_classify = cloth_classify  # 期望的衣服
        crop_point_dict = self.cloths.deal_cloth_crop_point(crop_point_dict)
        self.crop_point = crop_point_dict
        return crop_point_dict

    def deal_crop_detail_img(self, ai_result):
        """传入 ai 识别结果，获取到 各个裁剪细节"""

        crop_name = '裁剪'
        if '模特图' in self.image_classification_list:
            crop_name += '模特'
        elif '平铺图' in self.image_classification_list:
            crop_name += '平铺'
        elif '细节图' in self.image_classification_list:
            crop_name += '细节'
        detail = self.image_detail.seek_detail_img(ai_result)

        crop_point_mapping = {
            'shoulder': '肩部',
            'cuff': '袖口',
            'waistline': '腰部',
            'hemline': '下摆',
            'bottom': '裤脚',
            'hat': '帽子',
            'pocket': '口袋',
        }
        # 该图片存在哪些 裁剪细节点
        for k, v in detail.items():
            crop_detail = crop_point_mapping.get(k)
            if crop_detail:
                self.detail_point[crop_name + crop_detail] = v


class Human:
    '''人的ai数据处理'''
    # 17 个 人体关键点对应关系 旧版ai识别逻辑
    HUMAN_BODY_KEY_POINTS = [
        # face
        "nose",
        "left_eye", "right_eye",
        "left_ear", "right_ear",
        # upper body
        "left_shoulder", "right_shoulder",
        "left_elbow", "right_elbow",
        "left_wrist", "right_wrist",
        # middle body
        "left_hip", "right_hip",
        # lower body
        "left_knee", "right_knee",
        "left_ankle", "right_ankle"
    ]
    # 裁剪点 映射 ai 识别的 人体关键点  旧版ai识别逻辑
    mapping = {
        'eye': ["left_eye", "right_eye"],
        "nose": ["nose", "nose"],
        "ear": ["left_ear", "right_ear"],
        "shoulder": ["left_shoulder", "right_shoulder"],
        "elbow": ["left_elbow", "right_elbow"],
        "wrist": ["left_wrist", "right_wrist"],
        "hip": ["left_hip", "right_hip"],
        "knee": ["left_knee", "right_knee"],
        "ankle": ["left_ankle", "right_ankle"],
    }

    def __init__(self, image_analysis):
        self.threshold = 2.5  # 置信度 2.5
        self.image_analysis = image_analysis
        self.head = False  # 头是否存在，以此来判断 头顶是否存在
        if image_analysis.get('recognition'):  # 新版本ai识别结果
            self.threshold = 0.05
            image_analysis['human_pose'] = self.add_new_crop_point(image_analysis.get("recognition"),
                                                                   image_analysis.get("human_pose"))
        self.image_width = None
        self.image_height = None
        self.human_body_width = None
        self.human_bodies_list = self.ai_human_pose(image_analysis.get('human_pose'))


    def calculate_mouth(self, ai_crop_point_dict):
        """
        1.根据 眼镜 鼻子 计算嘴巴的位置
        2.根据眼睛鼻子判断 头顶是否要删除
        3.根据脚踝判断 脚底是否要删除
        """
        # y: 鼻子的y + (鼻子的y - 眼睛最低的y)
        # x: 鼻子的x
        if 'eye' in ai_crop_point_dict.keys() and 'nose' in ai_crop_point_dict.keys():
            eye_y = min(ai_crop_point_dict['eye']['top_site'][1], ai_crop_point_dict['eye']['bottom_site'][1])
            nose_y = ai_crop_point_dict['nose']['top_site'][1]
            mouth_y = nose_y + (nose_y - eye_y)
            nose_x = ai_crop_point_dict['nose']['top_site'][0]
            ai_crop_point_dict['mouth'] = {
                'top_site': (nose_x, mouth_y),
                'bottom_site': (nose_x, mouth_y)
            }

        if 'eye' not in ai_crop_point_dict.keys() and 'nose' not in ai_crop_point_dict.keys() \
                and not self.head and 'human_top' in ai_crop_point_dict.keys():
            ai_crop_point_dict.pop('human_top')

        if 'ankle' not in ai_crop_point_dict.keys() and 'human_bottom' in ai_crop_point_dict.keys():
            ai_crop_point_dict.pop('human_bottom')

        return ai_crop_point_dict

    def calculate_mandible_crop_point(self, face, human_keypoint_list):
        """
        在recognition face 内
        置信度小于0.8不可信
        嘴巴点 在 keypoints index 3 4
        下巴点 在 bbox index  2 3

        face 存在 使用 下巴+嘴巴 计算下颚
        face 不存在 使用 人体关键点肩部和颈部 来计算下颚

        :return: 下颚 的点
        """

        mandible_point = [-1, -1, 0]

        # ['右踝', '右膝', '右臀', '左臀', '左膝', '左踝', '腰', '脊柱', '颈', '头', '右腕', '右肘', '右肩', '左肩', '左肘', '左腕']
        r_ank, r_kne, r_hip, l_hip, l_kne, l_ank, pel, spi, nec, hea, r_wri, r_elb, r_sho, l_sho, l_elb, l_wri = human_keypoint_list

        # face 存在识别结果
        # 置信度小于0.8不可信
        if face and face.get('confidence', 0) >= 0.8:
            mandible_point[2] = face['confidence']
            # 下巴y点
            law_y = face['bbox'][3]  # 下巴纵轴
            left_mouth = face['landmarks'][3]  # 嘴的左边
            right_mouth = face['landmarks'][4]  # 嘴的右边
            # 嘴巴的中点
            mouth_x = min(left_mouth[0], right_mouth[0]) + abs(left_mouth[0] - right_mouth[0]) / 2
            mouth_y = max(left_mouth[1], right_mouth[1])
            # 下颚的点
            mandible_point[0] = mouth_x
            mandible_point[1] = min(law_y, mouth_y) + abs(mouth_y - law_y) / 2
            mandible_point[2] = 1
            # print(mandible_point)
        else:
            # print(r_sho, l_sho, pel, spi, nec)  # '右肩', '左肩' '腰', '脊柱', '颈'
            # 根据肩部和颈部计算下颚的点
            # 计算肩部点
            if r_sho[2] > 0.2 and l_sho[2] > 0.2:
                sho_y = min(r_sho[1], l_sho[1])
            elif r_sho[2] > 0.2:
                sho_y = r_sho[2]
            elif l_sho[2] > 0.2:
                sho_y = l_sho[2]
            else:
                # 无法判断肩膀位置，推出
                sho_y = None

            nec_y = None
            nec_x = None
            if nec[2] > 0.2:
                nec_y = nec[1]
                nec_x = nec[0]

            if nec_x is None or nec_y is None or sho_y is None:
                return mandible_point

            mandible_point[0] = nec_x
            mandible_point[1] = min(nec_y, sho_y) - abs(sho_y - nec_y) * 0.7
            mandible_point[2] = 1
        return mandible_point

    def calculate_x_human_center(self, crop_top, crop_bottom):

        """
        1.优先根据 左臀、右臀、腰、脊柱来计算，
        2.算不出来则 选择人体衣服外边框

        crop_top : 当前图片裁剪的上点
        crop_bottom： 当前图片裁剪的下点
        :return:
        """
        confidence = 0.4  # 人体主干关键点 置信度需要大于0.4

        if not self.image_analysis.get('recognition'):  # 新版本ai识别结果不存在
            return None

        recognition = json.loads(self.image_analysis.get('recognition'))  # 识别结果内不存在人体关键点
        human_bodies_list = recognition.get('human_bodies')
        if not human_bodies_list:
            return None

        all_human_center = []

        for i, human in enumerate(human_bodies_list):
            human_keypoint_list = human['keypoints']
            # ['右踝', '右膝', '右臀', '左臀', '左膝', '左踝', '腰', '脊柱', '颈', '头', '右腕', '右肘', '右肩', '左肩', '左肘', '左腕']
            r_ank, r_kne, r_hip, l_hip, l_kne, l_ank, pel, spi, nec, hea, r_wri, r_elb, r_sho, l_sho, l_elb, l_wri = human_keypoint_list

            # 有效的点
            valid_point_list = []

            # 不分左右的点 腰 pel、脊柱 spi
            # 1.置信度够
            # 2.在裁剪范围内
            pel_h = pel[1] / self.image_height
            pel_w = pel[0] / self.image_width
            if pel[2] >= confidence and crop_top <= pel_h <= crop_bottom:
                valid_point_list.append(pel_w)

            spi_h = spi[1] / self.image_height
            spi_w = spi[0] / self.image_width
            if spi[2] >= confidence and crop_top <= spi_h <= crop_bottom:
                valid_point_list.append(spi_w)

            # 分左右的点 左臀 l_hip、右臀 r_hip
            # 1. 左右点置信度都够
            # 2. 有一个点的 上下在裁剪范围内
            l_hip_h = l_hip[1] / self.image_height
            r_hip_h = r_hip[1] / self.image_height
            l_hip_w = l_hip[0] / self.image_width
            r_hip_w = r_hip[0] / self.image_width

            if l_hip[2] >= confidence and r_hip[2] >= confidence and \
                    (crop_top <= l_hip_h <= crop_bottom or crop_top <= r_hip_h <= crop_bottom):
                hip_w = l_hip_w + (r_hip_w - l_hip_w) / 2

                valid_point_list.append(hip_w)

            # 在有效点内计算人体中心点
            if valid_point_list:
                current_human_center = sum(valid_point_list) / len(valid_point_list)
                all_human_center.append(current_human_center)

        if not all_human_center:
            return None

        # 多人 取多人的中点
        return sum(all_human_center) / len(all_human_center)

    def add_new_crop_point(self, recognition, human_pose):
        """
        把 recognition 内的数据 添加到 旧版的17个人体关键点的数据结构中

        添加识别点
            腰部：waist
            下颚：mandible
        recognition 数据解释
        https://www.teambition.com/project/5e0dba42b2bba90021d9a872/app/5eba5fba6a92214d420a3219/workspaces/5fe40d962aa6d50046cc2bff/docs/60c1764beaa11900011f146e
        """
        if (human_pose is None) or (not human_pose):
            return human_pose
        human_pose_dict = json.loads(human_pose)
        human_pose_result = human_pose_dict["result"]

        recognition = json.loads(recognition)
        human_bodies_list = recognition.get('human_bodies')
        if (human_bodies_list is None) or (not human_bodies_list):
            return human_pose

        # 人的数量保持一致
        if len(human_bodies_list) != len(human_pose_result):
            return human_pose

        for i, human in enumerate(human_bodies_list):
            # ['右踝', '右膝', '右臀', '左臀', '左膝', '左踝', '腰', '脊柱', '颈', '头', '右腕', '右肘', '右肩', '左肩', '左肘', '左腕']
            r_ank, r_kne, r_hip, l_hip, l_kne, l_ank, pel, spi, nec, hea, r_wri, r_elb, r_sho, l_sho, l_elb, l_wri = human['keypoints']

            if hea[2] > 0:
                self.head = True
            if len(human_pose_result[i]['keypoints']) == 17:
                # 倒着insert 不会改变前面点的index
                # 在recognition keypoints 内 index 为6 的是腰部
                human_pose_result[i]['keypoints'].insert(self.HUMAN_BODY_KEY_POINTS.index('left_hip'),
                                                         human['keypoints'][6])

                # 在recognition face 内
                # 置信度小于0.8不可信
                # 嘴巴点 在 keypoints index 3 4
                # 下巴点 在 bbox index  2 3
                human_pose_result[i]['keypoints'].insert(self.HUMAN_BODY_KEY_POINTS.index('left_shoulder'),
                                                         self.calculate_mandible_crop_point(human['face'],
                                                                                            human['keypoints']))

        # 添加完裁剪点后，下面两个配置需要对应的改掉
        # 19 个 人体关键点对应关系
        self.HUMAN_BODY_KEY_POINTS = [
            # face
            "nose",
            "left_eye",
            "right_eye",
            "left_ear",
            "right_ear",
            "mandible",
            # upper body
            "left_shoulder",
            "right_shoulder",
            "left_elbow",
            "right_elbow",
            "left_wrist",
            "right_wrist",
            # middle body
            "waist",
            "left_hip",
            "right_hip",
            # lower body
            "left_knee",
            "right_knee",
            "left_ankle",
            "right_ankle",
        ]
        # 裁剪点 映射 ai 识别的 人体关键点
        self.mapping = {
            "eye": ["left_eye", "right_eye"],
            "nose": ["nose", "nose"],
            "ear": ["left_ear", "right_ear"],
            "mandible": ["mandible", "mandible"],
            "shoulder": ["left_shoulder", "right_shoulder"],
            "elbow": ["left_elbow", "right_elbow"],
            "wrist": ["left_wrist", "right_wrist"],
            "waist": ["waist", "waist"],
            "hip": ["left_hip", "right_hip"],
            "knee": ["left_knee", "right_knee"],
            "ankle": ["left_ankle", "right_ankle"],
        }

        human_pose_dict['result'] = human_pose_result

        human_pose = json.dumps(human_pose_dict)

        # except Exception:
        #     logging.error(f"ai识别结果-人体关键点-解析失败: {self.image_analysis} ", exc_info=True)
        return human_pose

    def deal_human_crop_point(self, crop_point_dict):
        '''
        处理人体的裁剪点，方便裁剪时取值
        '''
        for human in self.human_bodies_list:
            crop_point_dict = self.human_crop_point(human, crop_point_dict)

        # 计算嘴巴的位置
        crop_point_dict = self.calculate_mouth(crop_point_dict)

        return crop_point_dict

    def human_crop_point(self, human, crop_point_dict):
        '''
        眼睛：eye  矩形区域 top_site:left,top   bottom_site:right,bottom
        鼻子：nose
        耳朵：ear
        肩膀：shoulder
        肘部：elbow
        手腕：wrist
        臀部：hip
        膝盖：knee
        脚踝：ankle

        头顶：human_top
        脚底：human_bottom

        :return:
        '''

        human_body = human['human_key_point']
        # 关键点
        for point_k, point_v_list in self.mapping.items():

            # point_v_list 为 左点 右点  例如： ["left_eye", "right_eye"]
            # 关键点可见置信度阈值设置为 2.5
            # 左点
            x1, y1 = human_body[point_v_list[0]][0], human_body[point_v_list[0]][1]
            # 右点
            x2, y2 = human_body[point_v_list[1]][0], human_body[point_v_list[1]][1]

            # 人体识别点 分左右点 合并 左右点为一个矩形
            # 左右点 均存在
            point = {}
            if human_body[point_v_list[0]][2] > self.threshold and human_body[point_v_list[1]][2] > self.threshold:
                point['top_site'] = x1, y1
                point['bottom_site'] = x2, y2
            # 左点存在
            elif human_body[point_v_list[0]][2] > self.threshold:
                point['top_site'] = point['bottom_site'] = x1, y1
            # 右点存在
            elif human_body[point_v_list[1]][2] > self.threshold:
                point['top_site'] = point['bottom_site'] = x2, y2
            else:
                continue

            # 可能存在多个人 即存在多个相同分类 的人体关键点
            # 若不存在裁剪点
            if not crop_point_dict.get(point_k):
                crop_point_dict[point_k] = point
                continue
            human_top_site = crop_point_dict[point_k]['top_site']
            human_bottom_site = crop_point_dict[point_k]['bottom_site']
            # 存在裁剪点
            # 取最小
            crop_point_dict[point_k]['top_site'] = min(human_top_site[0], point['top_site'][0]), \
                                                   min(human_top_site[1], point['top_site'][1])
            # 取最大
            crop_point_dict[point_k]['bottom_site'] = max(human_bottom_site[0], point['bottom_site'][0]), \
                                                      max(human_bottom_site[1], point['bottom_site'][1])

        # 人的 头顶 脚底
        human_box = human['box']
        if not crop_point_dict.get('human_top'):
            point = dict()
            point['top_site'] = human_box[0], human_box[1]
            point['bottom_site'] = human_box[2], human_box[3]
            crop_point_dict['human_top'] = crop_point_dict['human_bottom'] = point
            return crop_point_dict

        human_top_site = crop_point_dict['human_top']['top_site']
        human_bottom_site = crop_point_dict['human_top']['bottom_site']
        # 取最小
        crop_point_dict['human_top']['top_site'] = min(human_top_site[0], human_box[0]), min(human_top_site[1],
                                                                                             human_box[1])
        # 取最大
        crop_point_dict['human_top']['bottom_site'] = max(human_bottom_site[0], human_box[2]), max(human_bottom_site[1],
                                                                                                   human_box[3])
        crop_point_dict['human_bottom'] = crop_point_dict['human_top']
        return crop_point_dict

    def ai_human_pose(self, human_pose):
        human_bodies = []
        if not human_pose:
            return human_bodies
        try:
            human_pose = json.loads(human_pose)
            self.image_width, self.image_height = human_pose['image']['width'], human_pose['image']['height']

            for one_human_data in human_pose['result']:
                human_body = self.deal_human(one_human_data)
                human_bodies.append(human_body)
        except Exception:
            raise Exception(f"ai识别结果-人体关键点-解析失败: {self.image_analysis} ")
            # logging.error(f"ai识别结果-人体关键点-解析失败: {self.image_analysis} ", exc_info=True)
        return human_bodies

    def deal_human(self, one_human_data):
        '''key: 各个人体关键点 value: x坐标，y坐标，置信度'''
        human_body = dict()  # box ; human_key_point
        human_body['box'] = [
            one_human_data['bbox'][0] / self.image_width,
            one_human_data['bbox'][1] / self.image_height,
            one_human_data['bbox'][2] / self.image_width,
            one_human_data['bbox'][3] / self.image_height
        ]

        if not len(self.HUMAN_BODY_KEY_POINTS) == len(one_human_data['keypoints']):
            return human_body

        key_points_list = one_human_data['keypoints']
        human_key_point = dict()
        for key_point_index, key_point in enumerate(self.HUMAN_BODY_KEY_POINTS):
            _key_point = [key_points_list[key_point_index][0] / self.image_width,
                          key_points_list[key_point_index][1] / self.image_height,
                          key_points_list[key_point_index][2]
                          ]
            human_key_point[key_point] = _key_point
        human_body['human_key_point'] = human_key_point
        return human_body


class Cloths:
    '''衣服的ai数据处理'''

    def __init__(self, image_analysis):
        self.image_analysis = image_analysis
        self.cloths_list = self.ai_cloth_1_info(image_analysis.get('cloth_1_info'))
        self.image_width = None
        self.image_height = None
        self.cloth_classify = None
        self.cloth_width = None
        self.cloth_height = None

    def deal_cloth_crop_point(self, crop_point_dict):

        for cloth in self.cloths_list:
            crop_point_dict = self.cloth_crop_point(cloth, crop_point_dict)
        return crop_point_dict

    def cloth_crop_point(self, cloth, crop_point_dict):
        #   衣服上边:garment_top
        #   衣服下边:garment_bottom
        #   衣服的范围

        # 该件衣服的分类 不在所需的范围
        if cloth['cat_id'] not in self.cloth_classify:
            return crop_point_dict

        cloth_box = cloth['box']
        if not crop_point_dict.get('garment_top'):
            point = dict()
            point['top_site'] = cloth_box[0], cloth_box[1]
            point['bottom_site'] = cloth_box[2], cloth_box[3]
            crop_point_dict['garment_top'] = crop_point_dict['garment_bottom'] = point
            return crop_point_dict

        garment_top_site = crop_point_dict['garment_top']['top_site']
        garment_bottom_site = crop_point_dict['garment_bottom']['bottom_site']
        # 取最小
        crop_point_dict['garment_top']['top_site'] = min(garment_top_site[0], cloth_box[0]), min(garment_top_site[1],
                                                                                                 cloth_box[1])
        # 取最大
        crop_point_dict['garment_top']['bottom_site'] = max(garment_bottom_site[0], cloth_box[2]), max(
            garment_bottom_site[1], cloth_box[3])
        crop_point_dict['garment_bottom'] = crop_point_dict['garment_top']
        return crop_point_dict

    def ai_cloth_1_info(self, cloth_1_info):
        '''计算各件衣服的分类 及box '''
        if not cloth_1_info:
            return []
        cloths_list = []
        try:
            cloth_1_info = json.loads(cloth_1_info)
            self.image_width, self.image_height = cloth_1_info['image']['width'], cloth_1_info['image']['height']
            for one_garment in cloth_1_info['result']:
                garment = self.deal_garment(one_garment)
                cloths_list.append(garment)
        except Exception:
            raise Exception(f"ai识别结果-衣服box-解析失败: {json.dumps(self.image_analysis)}")
            # logging.error(f"ai识别结果-衣服box-解析失败: {json.dumps(self.image_analysis)} ", exc_info=True)
        return cloths_list

    def deal_garment(self, one_garment):
        '''处理下 每件衣服的 box cat_id cat_name confidence'''
        garment = dict()

        #  服装的区域
        garment['box'] = [
            one_garment['bbox'][0] / self.image_width,
            one_garment['bbox'][1] / self.image_height,
            one_garment['bbox'][2] / self.image_width,
            one_garment['bbox'][3] / self.image_height
        ]

        garment['cat_id'] = one_garment['cat_id']  # 服装分类id
        garment['cat_name'] = one_garment['cat_name']  # 服装分类name
        return garment


class Brand:
    def __init__(self, image_analysis):
        self.image_analysis = image_analysis
        self.threshold = 0.6  # 小于0.6不可信
        self.brand_list = self.ai_brand_info(image_analysis.get("recognition"))

    def ai_brand_info(self, brand_json):
        '''计算各个资质图的分类 及box '''

        if not brand_json:
            return []

        brand_list = []
        try:
            brand_info = json.loads(brand_json)
            if not brand_info.get('labels'):
                return []
            self.image_width, self.image_height = brand_info['image']['width'], brand_info['image']['height']
            for one_brand in brand_info['labels']:
                if one_brand['confidence'] < self.threshold:  # 置信度过低
                    continue
                brand = self.deal_brand(one_brand)
                brand_list.append(brand)
        except Exception:
            raise Exception(f"ai识别结果-资质图box-解析失败: {json.dumps(self.image_analysis)}")
            # logging.error(f"ai识别结果-资质图box-解析失败: {json.dumps(self.image_analysis)} ", exc_info=True)
        return brand_list

    def deal_brand(self, one_brand):
        '''处理下 每个资质图的 box cat_id cat_name confidence'''

        brand = dict()

        #  服装的区域
        brand['box'] = [
            one_brand['bbox'][0] / self.image_width,
            one_brand['bbox'][1] / self.image_height,
            one_brand['bbox'][2] / self.image_width,
            one_brand['bbox'][3] / self.image_height
        ]

        brand['cat_id'] = one_brand['category_id']  # 服装分类id
        brand['cat_name'] = one_brand['category']  # 资质图分类name
        return brand

    def deal_brand_crop_point(self):
        if not self.brand_list:
            return {
                'brand_top': {
                    'top_site': [0, 0], 'bottom_site': [1, 1]
                },
                'brand_bottom': {
                    'top_site': [0, 0], 'bottom_site': [1, 1]
                }}

        brand_crop_point_dict = {}
        for brand in self.brand_list:
            brand_crop_point_dict = self.brand_crop_point(brand, brand_crop_point_dict)
        return brand_crop_point_dict

    def brand_crop_point(self, brand, crop_point_dict):
        # 资质图上边:brand_top
        # 资质图下边:brand_bottom

        brand_box = brand['box']
        if not crop_point_dict.get('brand_top'):
            point = dict()
            point['top_site'] = brand_box[0], brand_box[1]
            point['bottom_site'] = brand_box[2], brand_box[3]
            crop_point_dict['brand_top'] = crop_point_dict['brand_bottom'] = point
            return crop_point_dict

        brand_top_site = crop_point_dict['brand_top']['top_site']
        brand_bottom_site = crop_point_dict['brand_bottom']['bottom_site']
        # 取最小
        crop_point_dict['brand_top']['top_site'] = min(brand_top_site[0], brand_box[0]), min(brand_top_site[1],
                                                                                             brand_box[1])
        # 取最大
        crop_point_dict['brand_top']['bottom_site'] = max(brand_bottom_site[0], brand_box[2]), max(
            brand_bottom_site[1], brand_box[3])
        crop_point_dict['brand_bottom'] = crop_point_dict['brand_top']
        return crop_point_dict


class ImageDetail:
    """
    TB链接：https://thoughts.teambition.com/workspaces/5e37b6adf0f331001a9c172d/docs/607e874e4cc5830001d956c7

    从图片中，根据ai识别结果，标识出出细节图的位置
    帽子 hat
    袖口
    口袋 pocket
    腰部
    下摆
    裤脚
    鞋子 shoes
    包   bag
    """
    threshold = 0.1  # 置信度 0.1 看看效果
    # 衣服分类 及分类下关键点映射关系
    cloth_classify = {
        'blouse': [
            'neckline_left',
            'neckline_right',
            'center_front',
            'shoulder_left',
            'shoulder_right',
            'armpit_left',
            'armpit_right',
            'cuff_left_in',
            'cuff_left_out',
            'cuff_right_out',
            'top_hem_left',
            'top_hem_right'
        ],
        'skirt': [
            'waistband_left',
            'waistband_right',
            'hemline_left',
            'hemline_right'
        ],
        'outwear': [
            'neckline_left',
            'neckline_right',
            'center_front',
            'shoulder_left',
            'shoulder_right',
            'armpit_left',
            'armpit_right',
            'waistline_left',
            'waistline_right',
            'cuff_left_in',
            'cuff_left_out',
            'cuff_right_in',
            'cuff_right_out',
            'top_hem_left',
            'top_hem_right',
        ],
        'dress': [
            'neckline_left',
            'neckline_right',
            'center_front',
            'shoulder_left',
            'shoulder_right',
            'armpit_left',
            'armpit_right',
            'waistline_left',
            'waistline_right',
            'cuff_left_in',
            'cuff_left_out',
            'cuff_right_in',
            'cuff_right_out',
            'hemline_left',
            'hemline_right'
        ],

        'trousers': [
            'waistband_left',
            'waistband_right',
            'crotch',
            'bottom_left_in',
            'bottom_left_out',
            'bottom_right_in',
            'bottom_right_out',
        ]
    }
    # 关键点 3.0.7版本
    cloth_key_point = {
        'shoulder': ['shoulder_left',
                     'shoulder_right'],
        'cuff': ['cuff_left_out',
                 'cuff_left_in',
                 'cuff_right_in',
                 'cuff_right_out'],
        'waistline': ['waistline_left',
                      'waistline_right',
                      'waistband_left',
                      'waistband_right'
                      ],
        'hemline': ['hemline_left',
                    'hemline_right',
                    'top_hem_left',
                    'top_hem_right'
                    ],
        'bottom': ['bottom_left_out',
                   'bottom_left_in',
                   'bottom_right_in',
                   'bottom_right_out']
    }
    # 目标检测 3.0.7版本
    # cloth_object_detection = ['shoes', 'bag', 'hat', 'pocket']
    cloth_object_detection = ['hat', 'pocket']

    def __init__(self):
        self.image_width = None
        self.image_height = None

        self.detail = {}
        self.match_crop_detail = []

    def seek_detail_img(self, ai_predictions):
        """寻找 细节图 的坐标信息"""
        # ai_predictions = {"predictions": [
        #     {
        #         "image": {
        #             "width": 800,
        #             "height": 533
        #         },
        #         "result": [
        #             {
        #                 "bbox": [
        #                     "311.0",
        #                     "361.0",
        #                     "504.0",
        #                     "533.0"
        #                 ],
        #                 "cat_id": 5,
        #                 "cat_name": "trousers",
        #                 "confidence": 0.7771915793418884,
        #                 "keypoints": [
        #                     [
        #                         63.4375,
        #                         30.8125,
        #                         0.29523932933807373
        #                     ],
        #                     [
        #                         177.625,
        #                         25.375,
        #                         0.24510465562343597
        #                     ],
        #                     [
        #                         106.9375,
        #                         148.625,
        #                         0.36413368582725525
        #                     ],
        #                     [
        #                         54.375,
        #                         68.875,
        #                         0.013722038827836514
        #                     ],
        #                     [
        #                         45.3125,
        #                         134.125,
        #                         0.21816827356815338
        #                     ],
        #                     [
        #                         50.75,
        #                         67.0625,
        #                         0.008496182970702648
        #                     ],
        #                     [
        #                         195.75,
        #                         188.5,
        #                         0.019060151651501656
        #                     ]
        #                 ]
        #             },
        #             {
        #                 "bbox": [
        #                     "319.0",
        #                     "136.0",
        #                     "544.0",
        #                     "419.0"
        #                 ],
        #                 "cat_id": 1,
        #                 "cat_name": "blouse",
        #                 "confidence": 0.5724542140960693,
        #                 "keypoints": [
        #                     [
        #                         100.9375,
        #                         45.15625,
        #                         0.6377096176147461
        #                     ],
        #                     [
        #                         156.71875,
        #                         42.5,
        #                         0.626152515411377
        #                     ],
        #                     [
        #                         127.5,
        #                         53.125,
        #                         0.7923415899276733
        #                     ],
        #                     [
        #                         61.09375,
        #                         69.0625,
        #                         0.890479326248169
        #                     ],
        #                     [
        #                         196.5625,
        #                         71.71875,
        #                         0.8325190544128418
        #                     ],
        #                     [
        #                         77.03125,
        #                         132.8125,
        #                         0.4232546389102936
        #                     ],
        #                     [
        #                         183.28125,
        #                         135.46875,
        #                         0.3931943476200104
        #                     ],
        #                     [
        #                         63.75,
        #                         225.78125,
        #                         0.439550518989563
        #                     ],
        #                     [
        #                         39.84375,
        #                         228.4375,
        #                         0.37197989225387573
        #                     ],
        #                     [
        #                         106.25,
        #                         228.4375,
        #                         0.8018227815628052
        #                     ],
        #                     [
        #                         132.8125,
        #                         268.28125,
        #                         0.6333439350128174
        #                     ],
        #                     [
        #                         42.5,
        #                         289.53125,
        #                         0.2018098682165146
        #                     ],
        #                     [
        #                         185.9375,
        #                         276.25,
        #                         0.18934710323810577
        #                     ]
        #                 ]
        #             },
        #             {
        #                 "bbox": [
        #                     "452.0",
        #                     "387.0",
        #                     "483.0",
        #                     "451.0"
        #                 ],
        #                 "cat_id": 9,
        #                 "cat_name": "pocket",
        #                 "confidence": 0.6082484126091003,
        #                 "keypoints": [
        #
        #                 ]
        #             }
        #         ]
        #     }]}['predictions'][0]
        self.image_width = ai_predictions['image']['width']
        self.image_height = ai_predictions['image']['height']

        ai_prediction_results = ai_predictions['result']
        for predict_part in ai_prediction_results:
            cat_name = predict_part['cat_name']

            # 衣服关键点
            if cat_name in self.cloth_classify.keys():
                self.deal_cloth_key_point(predict_part)
            # 目标检测
            elif cat_name in self.cloth_object_detection:
                self.deal_cloth_obj_detection(predict_part)
        return self.detail
        # print(self.detail)

    def add_crop_detail(self, img_classify):
        """根据图片类型添加 裁剪细节图"""
        if '平铺图' in img_classify:
            self.match_crop_detail.append('裁剪平铺细节图')
        elif '模特图' in img_classify:
            self.match_crop_detail.append('裁剪模特细节图')

    def deal_cloth_key_point(self, predict_part):
        """根据衣服的key_point结果，找到细节位置"""
        cloth_bbox = predict_part['bbox']
        predict_key_points = predict_part['keypoints']  # ai识别的keypoint 数据列表
        key_point_list = self.cloth_classify.get(predict_part['cat_name'], [])  # keypoint 代表具体部位的列表

        for cat_name, keypoint_part_list in self.cloth_key_point.items():

            for i in range(0, len(keypoint_part_list), 2):
                # 识别点 在 ai 识别结果的下标

                if (keypoint_part_list[i] not in key_point_list) or (keypoint_part_list[i + 1] not in key_point_list):
                    continue

                predict_index_left = key_point_list.index(keypoint_part_list[i])
                predict_index_right = key_point_list.index(keypoint_part_list[i + 1])

                top_site = predict_key_points[predict_index_left]
                bottom_site = predict_key_points[predict_index_right]
                # 置信度过低，不使用该位置

                # if top_site[2] < self.threshold or bottom_site[2] < self.threshold:
                #     continue

                confidence = (top_site[2] + bottom_site[2]) * 0.5

                if cat_name in self.detail.keys() and confidence < self.detail[cat_name]['confidence']:
                    continue

                self.detail[cat_name] = {
                    'top_site': ((top_site[0] + cloth_bbox[0]) / self.image_width,
                                 (top_site[1] + cloth_bbox[1]) / self.image_height),
                    'bottom_site': ((bottom_site[0] + cloth_bbox[0]) / self.image_width,
                                    (bottom_site[1] + cloth_bbox[1]) / self.image_height),
                    'confidence': confidence,
                    'top_site_confidence': top_site[2],
                    'bottom_site_confidence': bottom_site[2]
                }

    def deal_cloth_obj_detection(self, predict_part):
        """根据目标检测的结果，找到细节位置"""
        confidence = predict_part['confidence']
        # 置信度过低，不使用该位置
        # if confidence < self.threshold:
        #     return

        bounding_box = [float(i) for i in predict_part['bbox']]
        cat_name = predict_part['cat_name']

        # part已经存在且  置信度低于 上一个 part 时
        if cat_name in self.detail and confidence < self.detail[cat_name]['confidence']:
            return

        self.detail[cat_name] = {
            'top_site': (bounding_box[0] / self.image_width, bounding_box[1] / self.image_height),
            'bottom_site': (bounding_box[2] / self.image_width, bounding_box[3] / self.image_height),
            'confidence': confidence
        }


if __name__ == '__main__':
    a = ImageDetail()
