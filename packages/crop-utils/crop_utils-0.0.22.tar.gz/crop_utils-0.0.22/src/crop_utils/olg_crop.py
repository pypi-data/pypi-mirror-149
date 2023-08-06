from .html_slot_config import *


class ShouldIndex:
    def __init__(self):
        # 裁剪指标
        self.crop_indexing_dict = {
            'extension': {'status': False},
            'main_part_offset': {'coordinates': 'x', 'offset': 0},
            'crop_head': {'status': False},
            'get_crop_point': {'status': False},
            'slot_and_img_ration': {'offset': 1},
        }

    def extension(self):
        self.crop_indexing_dict['extension'] = {
            'status': True
        }

    def main_part_offset(self, pic_center, main_part_center, coordinates):
        """
        图片主体内容 偏移 图片中心的比率
        :param pic_center:  裁剪后中点
        :param main_part_center: 主题中点
        :param coordinates:  x 轴 或 y轴 ,原点在左上方处
        :return:
        """

        if pic_center < main_part_center:
            offset = - (main_part_center - pic_center) / pic_center
        elif pic_center == main_part_center:
            offset = 0
        else:
            offset = (pic_center - main_part_center) / pic_center

        self.crop_indexing_dict['main_part_offset'] = {
            'coordinates': coordinates,
            'offset': offset
        }

        return offset

    def img_scale_ratio(self, width_scale, height_scale):
        """
        图片缩放比率 ,目前图片都是等比放缩。所以 宽高缩放率是一样的
        小于1  为缩放
        大于1  为放大
        :param width_scale:
        :param height_scale:
        :return:
        """
        self.crop_indexing_dict['img_scale_ratio'] = {
            'width_scale': width_scale,
            'height_scale': height_scale,
        }

        return width_scale

    def get_slot_and_img_ration(self, slot_ratio, crop_main_part_ratio):
        """
        slot宽高比 / 裁剪主题宽高比
        :param slot_ratio:
        :param crop_main_part_ratio:
        :return:
        """
        self.crop_indexing_dict['slot_and_img_ration'] = {
            'slot_ratio': slot_ratio,
            'img_ratio': crop_main_part_ratio,
            'offset': abs(crop_main_part_ratio - slot_ratio) / slot_ratio
        }
        return None

    def get_crop_site(self, origin_crop_site, crop_site):
        """预设裁剪点是否取到 或 兼容取到"""

        self.crop_indexing_dict['get_crop_point'] = {
            'origin_crop_site': origin_crop_site,
            'crop_site': crop_site,
            'status': True if origin_crop_site == crop_site else False,
        }

    def crop_head(self):
        """裁剪头"""
        self.crop_indexing_dict['crop_head'] = {
            'status': True
        }


class ImageCrop:
    def __init__(self):
        self.si = ShouldIndex()
        #  Todo 裁剪点 顺序
        self.crop_sequence = ['pic_top', 'human_top', 'eye', 'nose', 'ear', 'mouth', 'mandible', 'shoulder', 'elbow',
                              'wrist',"waist", 'hip', 'knee', 'ankle', 'human_bottom', 'pic_bottom']
        self.garment_crop_sequence = ['pic_top', 'human_top', 'garment_top', 'garment_bottom', 'human_bottom',
                                      'pic_bottom']

    def gif_crop(self, slot_width, slot_height, img):
        """动图宽固定，高自适应 计算出 裁剪参数"""
        crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = self. \
            self_adaption_height_crop(0, 1, {'x1': 0, 'x2': 1}, [slot_width, slot_height], img)
        amend_layout_height = 0
        return crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height, img.width, img.height

    def brand_crop(self, img, slot_config, slot_width, slot_height):
        """资质图裁剪"""
        top_site = img.brand_crop_point['brand_top']['top_site']
        bottom_site = img.brand_crop_point['brand_bottom']['bottom_site']

        crop_info = slot_config.get(CROP)
        crop_dict = {
            "need_crop": crop_info.get(NEED_CROP),
            "img_self-adaption": slot_config.get(STRETCH, 'fix'),
            "layout_self-adaption": 'false',
            "crop_method": crop_info.get(BRAND, {})
        }

        # 每个槽设置的裁剪参数
        crop_parameter = crop_dict.get('crop_method')

        crop_top_site = min(top_site[1], bottom_site[1])
        crop_bottom_site = max(top_site[1], bottom_site[1])
        left = min(top_site[0], bottom_site[0])
        right = max(top_site[0], bottom_site[0])

        # 需要裁剪、加上 内边距
        # 计算 高的内边距
        padding_unit = crop_parameter.get(PADDING_UNIT, 'pi')  # 'percent pe' 'pixel pi'
        if padding_unit == 'pe':  # 简写
            padding_left, padding_right = float(crop_parameter.get(LEFT, 0)) * 0.01, float(
                crop_parameter.get(RIGHT, 0)) * 0.01
            padding_top, padding_bottom = float(crop_parameter.get(TOP, 0)) * 0.01, float(
                crop_parameter.get(BOTTOM, 0)) * 0.01
        else:
            padding_left, padding_right = float(crop_parameter.get(LEFT, 0)) / slot_width, float(
                crop_parameter.get(RIGHT, 0)) / slot_width
            padding_top, padding_bottom = float(crop_parameter.get(TOP, 0)) / slot_height, float(
                crop_parameter.get(BOTTOM, 0)) / slot_height
        # 加上内边界后 裁剪点 x1,y1,x2,y2
        x1 = max(left - padding_left, 0)
        x2 = min(right + padding_right, 1)

        y1 = max(crop_top_site - padding_top, 0)
        y2 = min(crop_bottom_site + padding_bottom, 1)

        get_crop_point_result_dict = dict()
        get_crop_point_result_dict['x1'] = x1
        get_crop_point_result_dict['x2'] = x2

        if crop_dict['img_self-adaption'] == 'w':
            crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = self.self_adaption_height_crop(
                y1, y2, get_crop_point_result_dict, [slot_width, slot_height], img)
            if crop_dict.get('layout_self-adaption') == 'false':
                amend_layout_height = 0
        else:
            crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = self.img_crop_detail_crop(
                y1, y2, x1, x2, [slot_width, slot_height], img)

        return crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height, img.width, img.height

    def crop(self, slot_config, img):
        """
        裁剪逻辑 需求文档
        https://thoughts.teambition.com/workspaces/5e37b6adf0f331001a9c172d/docs/5f2e438de6eed50001359150
        """
        slot_width = slot_config.get('width')
        slot_height = slot_config.get('height')

        if img.image_classification == '动图':  # 如果分类为动图，特殊处理
            return self.gif_crop(slot_width, slot_height, img)

        crop_dict = self.get_crop_dict(slot_config, img)
        img_crop_type = crop_dict['img_crop_type']

        # if 'asset/1000175/47178d5e-6db6-4f7e-b7f8-f1b284476e26.jpg' in img.storage_key:
        #     print(12312323)

        self.si.get_slot_and_img_ration(slot_width / slot_height, img.ratio)

        # 是否需要裁剪
        need_crop = crop_dict['need_crop']
        if not need_crop:
            # print("居中裁剪, 图片设置为不裁剪，")
            self.si.get_crop_site([None, None], [None, None])
            return self.need_center_crop(crop_dict, slot_width, slot_height, img)

        # 每个槽设置的裁剪参数
        crop_parameter = crop_dict.get('crop_method')
        if not crop_parameter:
            self.si.get_crop_site([None, None], [None, None])
            # print(f"居中裁剪： 未获取到裁剪参数，图片类型为 {img.image_classification}")
            return self.need_center_crop(crop_dict, slot_width, slot_height, img)

        # 资质图裁剪
        if img_crop_type == BRAND:
            self.si.get_crop_site([None, None], [None, None])
            return self.brand_crop(img, slot_config, slot_width, slot_height)

        # 找到裁剪点
        get_crop_point_result_dict = self.get_crop_point(crop_parameter, img, img_crop_type)
        if not get_crop_point_result_dict:
            return self.need_center_crop(crop_dict, slot_width, slot_height, img)

        crop_top_site, crop_bottom_site = get_crop_point_result_dict['crop_top_site'], get_crop_point_result_dict[
            'crop_bottom_site']

        if get_crop_point_result_dict['crop_top_name'] == 'pic_top' and get_crop_point_result_dict[
            'crop_bottom_name'] == 'pic_bottom' and crop_dict['img_self-adaption'] != 'e':
            # 居中裁剪 并往上移动
            # print(123123123123)
            return self.need_pic_top_and_pic_bottom_crop(crop_dict, slot_width, slot_height, img,
                                                         get_crop_point_result_dict)

        left = get_crop_point_result_dict['crop_left']
        right = get_crop_point_result_dict['crop_right']

        # 计算 高的内边距
        padding_unit = crop_parameter[PADDING_UNIT]  # 'percent pe' 'pixel pi'
        if padding_unit == 'pe':  # 简写
            padding_left, padding_right = float(crop_parameter.get(LEFT, 0)) * 0.01, float(
                crop_parameter.get(RIGHT, 0)) * 0.01
            padding_top, padding_bottom = float(crop_parameter[TOP]) * 0.01, float(crop_parameter[BOTTOM]) * 0.01
        else:
            padding_left, padding_right = float(crop_parameter.get(LEFT, 0)) / slot_width, float(
                crop_parameter.get(RIGHT, 0)) / slot_width
            padding_top, padding_bottom = float(crop_parameter[TOP]) / slot_height, float(
                crop_parameter[BOTTOM]) / slot_height
        # 加上内边界后 裁剪点 x1,y1,x2,y2
        x1 = max(left - padding_left, 0)
        x2 = min(right + padding_right, 1)
        get_crop_point_result_dict['x1'] = x1
        get_crop_point_result_dict['x2'] = x2
        y1 = max(crop_top_site[1] - padding_top, 0)
        y2 = min(crop_bottom_site[1] + padding_bottom, 1)

        if crop_dict['img_self-adaption'] == 'w':
            crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = self.self_adaption_height_crop(
                y1, y2, get_crop_point_result_dict, [slot_width, slot_height], img)
            if crop_dict.get('layout_self-adaption') == 'false':
                amend_layout_height = 0
        elif crop_dict['img_self-adaption'] == 'e':
            crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = self.extension_crop(
                y1, y2, get_crop_point_result_dict, [slot_width, slot_height], img, img_crop_type
            )
        else:
            crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = self.height_crop(
                y1, y2, get_crop_point_result_dict, [slot_width, slot_height], img, img_crop_type
            )

        return crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height, img.width, img.height

    def crop_details(self, img, slot_config, slot_width, slot_height, best_image_dict):
        """
        裁剪细节图 需求文档
        https://thoughts.teambition.com/workspaces/5e37b6adf0f331001a9c172d/docs/607e874e4cc5830001d956c7
        """
        top_site = best_image_dict['top_site']
        bottom_site = best_image_dict['bottom_site']

        crop_info = slot_config.get(CROP)
        crop_dict = {
            "need_crop": crop_info.get(NEED_CROP),
            "img_self-adaption": slot_config.get(STRETCH, 'fix'),
            "layout_self-adaption": 'false',
            "crop_method": crop_info.get(CROP_DETAIL, {}),
            "match_slot": best_image_dict['match_s']
        }

        # 每个槽设置的裁剪参数
        crop_parameter = crop_dict.get('crop_method')

        crop_top_site = min(top_site[1], bottom_site[1])
        crop_bottom_site = max(top_site[1], bottom_site[1])
        left = min(top_site[0], bottom_site[0])
        right = max(top_site[0], bottom_site[0])

        # 需要裁剪、加上 内边距
        # 计算 高的内边距
        padding_unit = crop_parameter.get(PADDING_UNIT, 'pi')  # 'percent pe' 'pixel pi'
        if padding_unit == 'pe':  # 简写
            padding_left, padding_right = float(crop_parameter.get(LEFT, 0)) * 0.01, float(
                crop_parameter.get(RIGHT, 0)) * 0.01
            padding_top, padding_bottom = float(crop_parameter.get(TOP, 0)) * 0.01, float(
                crop_parameter.get(BOTTOM, 0)) * 0.01
        else:
            padding_left, padding_right = float(crop_parameter.get(LEFT, 0)) / slot_width, float(
                crop_parameter.get(RIGHT, 0)) / slot_width
            padding_top, padding_bottom = float(crop_parameter.get(TOP, 0)) / slot_height, float(
                crop_parameter.get(BOTTOM, 0)) / slot_height
        # 加上内边界后 裁剪点 x1,y1,x2,y2
        x1 = max(left - padding_left, 0)
        x2 = min(right + padding_right, 1)

        y1 = max(crop_top_site - padding_top, 0)
        y2 = min(crop_bottom_site + padding_bottom, 1)
        print(f"{crop_dict['match_slot']} {x1},{y1},{x2},{y2} {img.name_slot}{img.name_slot_index}")
        get_crop_point_result_dict = dict()
        get_crop_point_result_dict['x1'] = x1
        get_crop_point_result_dict['x2'] = x2

        if crop_dict['img_self-adaption'] == 'w':
            crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = self.self_adaption_height_crop(
                y1, y2, get_crop_point_result_dict, [slot_width, slot_height], img)
            if crop_dict.get('layout_self-adaption') == 'false':
                amend_layout_height = 0
        else:
            crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = self.img_crop_detail_crop(
                y1, y2, x1, x2, [slot_width, slot_height], img)

        return crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height, img.width, img.height

    def self_adaption_height_crop(self, top, bottom, crop_point_result_dict, origin_slot, img=None, img_width=None,
                                  img_height=None):
        ''' img_self-adaption: true,flase     图片自适应
            layout_self-adaption: true,flase  画布自适应
        '''
        if img:
            img_width = img.width
            img_height = img.height
        # 宽铺满的情况下,等比放缩 计算 高  裁剪高
        origin_slot_width, origin_slot_height = origin_slot
        # 加上内边界后 裁剪点 x1,x2
        x1 = crop_point_result_dict['x1']
        x2 = crop_point_result_dict['x2']
        width_scale = origin_slot_width / ((x2 - x1) * img_width)
        transform_img_height = width_scale * img_height
        scale_x = scale_y = width_scale
        x = x1
        y = top
        crop_width = origin_slot_width / scale_x
        crop_height = ((bottom - top) * img_height)

        amend_layout_height = (bottom - top) * transform_img_height - origin_slot_height

        self.si.img_scale_ratio(scale_x, scale_y)
        # print(f'自适应裁剪: slot高度{origin_slot_height} -> {amend_layout_height}')
        return x * img_width, y * img_height, crop_width, crop_height, scale_x, scale_y, amend_layout_height

    @staticmethod
    def get_crop_dict(slot_config, img):
        # print(slot_config)
        crop_info = slot_config.get(CROP)
        crop_dict = {
            "img_crop_type": img.img_crop_type,
            "need_crop": crop_info.get(NEED_CROP),
            "img_self-adaption": slot_config.get(STRETCH, 'fix'),
            "layout_self-adaption": 'false',
            "crop_method": crop_info.get(img.img_crop_type, {})
        }

        if crop_info.get(MAIN_PRODUCT_CROP) == 1:  # 需要裁剪主商品
            img.deal_crop_key_point(main_product_crop=True)

        return crop_dict

    def height_crop(self, top, bottom, crop_point_result_dict, origin_slot, img, img_crop_type):
        # 一定要考虑图片放缩 后 相关点的变化
        cloth_x1, cloth_y1, cloth_x2, cloth_y2 = crop_point_result_dict['cloth_box']

        origin_slot_width, origin_slot_height = origin_slot

        # 裁剪高铺满的情况下,等比放缩 裁剪 宽
        height_scale = origin_slot_height / ((bottom - top) * img.height)
        transform_img_width = img.width * height_scale

        if transform_img_width >= origin_slot_width:  # 图片宽度大于槽的宽度
            # print('x轴裁剪: 高铺满的slot,原图等比放缩后, 裁剪宽')
            scale_x = scale_y = height_scale
            y = top
            center = cloth_x1 + (cloth_x2 - cloth_x1) / 2
            # 模特图
            crop_left, crop_right = crop_point_result_dict['crop_left'], crop_point_result_dict['crop_right']

            if img_crop_type in ['m_t', 'm_bu', 'm_bo', 'm_f']:
                # 衣服模特最靠外的 左点 右点 不包含内间距
                if (crop_right - crop_left) * transform_img_width <= origin_slot_width:
                    center = crop_left + (crop_right - crop_left) / 2

            x = self.alternative_center_crop(center, origin_slot_width, transform_img_width, [crop_left, crop_right])

            self.si.main_part_offset(x * img.width + origin_slot_width / scale_x / 2, center * img.width, 'x')

        else:
            # print('y轴裁剪: 宽铺满,原图等比放缩后 裁剪高')
            # 宽铺满的情况下,等比放缩 计算 高  裁剪高

            # 加上内边界后 裁剪点 x1,x2
            x1 = crop_point_result_dict['x1']
            x2 = crop_point_result_dict['x2']

            width_scale = origin_slot_width / ((x2 - x1) * img.width)
            # width_scale = origin_slot_width / img.width
            transform_img_height = width_scale * img.height
            scale_x = scale_y = width_scale
            x = x1  # 左位置为  加上内边界后 的左
            # x = 0  # 左位置为  加上内边界后 的左
            center = cloth_y1 + (cloth_y2 - cloth_y1) / 2
            if img_crop_type in ['m_t', 'm_bu', 'm_bo', 'm_f', 't']:
                if (bottom - top) * transform_img_height >= origin_slot_height:  # 图片放不进 slot内

                    y = top  # 默认向上移动,优先显示主体, 距上边的距离
                    # 未添加padding 裁剪主体的 left right 位置  # 加了padding的 是x1 x2 看要用哪个
                    crop_left, crop_right = crop_point_result_dict['crop_left'], crop_point_result_dict['crop_right']

                    left = crop_left  # 距左边的距离
                    right = 1 - crop_right  # 距右边的距离
                    bottom_ = 1 - y  # 距下边的距离
                    min_x = min(left, right, bottom_)  # 找到最小的距离
                    # 同比缩放图片，并计算裁剪点x 的数值
                    if bottom_ > min_x and left <= right:
                        width_scale = origin_slot_width / ((crop_right + min_x) * img.width)
                        x = 0
                    else:
                        width_scale = origin_slot_width / ((1 - (crop_left - min_x)) * img.width)
                        x = crop_left - min_x

                    scale_x = scale_y = width_scale

                    self.si.extension()
                    self.si.crop_head()
                    self.si.img_scale_ratio(scale_x, scale_y)
                    self.si.main_part_offset(0.5, 0.5, 'y')

                    return x * img.width, y * img.height, origin_slot_width / scale_x, origin_slot_height / scale_x, \
                           scale_x, scale_y, 0
                else:
                    center = top + (bottom - top) / 2
            crop_top, crop_bottom = crop_point_result_dict['crop_top_site'][1], \
                                    crop_point_result_dict['crop_bottom_site'][1]
            y = self.alternative_center_crop(center, origin_slot_height, transform_img_height, [crop_top, crop_bottom])

            self.si.main_part_offset(y * img.height + origin_slot_height / scale_x / 2, center * img.height, 'y')

        self.si.img_scale_ratio(scale_x, scale_y)

        return x * img.width, y * img.height, origin_slot_width / scale_x, origin_slot_height / scale_x, scale_x, scale_y, 0

    def alternative_center_crop(self, center, slot_height_or_width, transform_height_or_width, x_or_y):
        center_ = center * transform_height_or_width
        # 在图片的范围内
        tag_1 = (center_ - slot_height_or_width / 2) >= 0
        tag_2 = (center_ + slot_height_or_width / 2) <= transform_height_or_width

        if tag_1 and tag_2:  # 上下 都有足够 预留范围
            x_or_y = center_ - slot_height_or_width / 2
        elif tag_1 and not tag_2:  # 1范围够 2范围不够
            x_or_y = transform_height_or_width - slot_height_or_width
        elif tag_2 and not tag_1:  # 1范围不够 2范围够
            x_or_y = 0
        else:  # 未知情况
            x_or_y = 0.5 * transform_height_or_width - slot_height_or_width / 2
        x_or_y = x_or_y / transform_height_or_width

        if not (tag_1 and tag_2):
            self.si.extension()

        return x_or_y

    def get_crop_point(self, crop_parameter, img, img_crop_type):
        #  寻找 裁剪点 并兼容

        top_site = crop_parameter.get(TOP_SITE, 'garment_top')
        if top_site == 'null':
            top_site = 'garment_top'

        # if 'mandible' == top_site:
        #     print(top_site)

        bottom_site = crop_parameter.get(BOTTOM_SITE, 'garment_bottom')
        if bottom_site == 'null':
            bottom_site = 'garment_bottom'
        # 裁剪 上下 点
        # Todo 取上下裁剪点时，取出 2组 x1,y1 x2,y2  找最靠外的 x与y
        crop_top_site, crop_top_name = self.from_img_get_top_site(img.crop_point, top_site)
        crop_bottom_site, crop_bottom_name = self.from_img_get_bottom_site(img.crop_point, bottom_site)

        # 裁剪范围不存在
        if not (crop_top_site and crop_bottom_site):
            # print(f'居中裁剪,{top_site},{bottom_site} 裁剪点不存在')
            return False
        # 裁剪 左右 点
        human_box_top = list(img.crop_point.get('human_top', {}).get('top_site', [None, None]))
        human_box_bottom = list(img.crop_point.get('human_bottom', {}).get('bottom_site', [None, None]))
        human_box_top.extend(human_box_bottom)
        human_box = human_box_top

        cloth_box_top = list(img.crop_point.get('garment_top', {}).get('top_site', [None, None]))
        cloth_box_bottom = list(img.crop_point.get('garment_bottom', {}).get('bottom_site', [None, None]))
        cloth_box_top.extend(cloth_box_bottom)
        cloth_box = cloth_box_top

        human_x1, human_y1, human_x2, human_y2 = human_box
        cloth_x1, cloth_y1, cloth_x2, cloth_y2 = cloth_box

        # 左点 # 右点 人体识别点 可能为 0 ；当为None 时 证明 不存在数据ai数据
        if (human_x1 is None) and (cloth_x1 is None):
            # 左点 右点 不存在 识别结果
            left = 0
            right = 1
            human_box = [0, 0, 1, 1]
            cloth_box = [0, 0, 1, 1]

        elif cloth_x1 is None and human_x1 is not None:
            left = human_x1
            right = human_x2
            cloth_box = [0, 0, 1, 1]
        elif human_x1 is None and cloth_x1 is not None:
            left = cloth_x1
            right = cloth_x2
            human_box = [0, 0, 1, 1]
        else:
            left = min(human_x1, cloth_x1)
            right = max(human_x2, cloth_x2)

        if img_crop_type == 't':
            left = cloth_box[0]
            right = cloth_box[2]

        self.si.get_crop_site([top_site, bottom_site], [crop_top_name, crop_bottom_name])

        return {
            'crop_top_site': crop_top_site,
            'crop_top_name': crop_top_name,
            'crop_bottom_site': crop_bottom_site,
            'crop_bottom_name': crop_bottom_name,
            'crop_left': left,
            'crop_right': right,
            'human_box': human_box,
            'cloth_box': cloth_box,
            'set_top_site': top_site,
            'set_bottom_site': bottom_site,
        }

    def from_img_get_top_site(self, crop_point, top_site):
        if top_site not in self.crop_sequence:
            flag_index = self.garment_crop_sequence.index(top_site)
            crop_top, crop_top_name = None, None
            while flag_index >= 0:
                crop_top, crop_top_name = crop_point.get(self.garment_crop_sequence[flag_index]), \
                                          self.garment_crop_sequence[flag_index]
                if crop_top:
                    break
                flag_index -= 1
            return crop_top['top_site'], crop_top_name

        flag_index = self.crop_sequence.index(top_site)
        crop_top, crop_top_name = None, None
        while flag_index >= 0:
            crop_top, crop_top_name = crop_point.get(self.crop_sequence[flag_index]), self.crop_sequence[flag_index]
            if crop_top:
                break
            flag_index -= 1
        return crop_top['top_site'], crop_top_name

    def from_img_get_bottom_site(self, crop_point, bottom_site):
        if bottom_site not in self.crop_sequence:
            flag_index = self.garment_crop_sequence.index(bottom_site)
            crop_bottom, crop_bottom_name = None, None
            while flag_index < len(self.crop_sequence):
                crop_bottom, crop_bottom_name = crop_point.get(self.garment_crop_sequence[flag_index]), \
                                                self.garment_crop_sequence[
                                                    flag_index]
                if crop_bottom:
                    break
                flag_index += 1
            return crop_bottom['bottom_site'], crop_bottom_name

        flag_index = self.crop_sequence.index(bottom_site)
        crop_bottom, crop_bottom_name = None, None
        while flag_index < len(self.crop_sequence):
            crop_bottom, crop_bottom_name = crop_point.get(self.crop_sequence[flag_index]), self.crop_sequence[
                flag_index]
            if crop_bottom:
                break
            flag_index += 1
        return crop_bottom['bottom_site'], crop_bottom_name

    def need_center_crop(self, crop_dict, slot_width, slot_height, img):
        """裁剪所需信息不全，居中裁剪"""
        if crop_dict['img_self-adaption'] == 'w':  # 宽固定，高自适应
            get_crop_point_result_dict = {'x1': 0, 'x2': 1}
            crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = self. \
                self_adaption_height_crop(0, 1, get_crop_point_result_dict, [slot_width, slot_height], img)
            if crop_dict.get('layout_self-adaption') == 'false':
                amend_layout_height = 0
            return crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height, img.width, img.height
        else:
            return self.center_crop(slot_width, slot_height, img.width, img.height)

    def need_pic_top_and_pic_bottom_crop(self, crop_dict, slot_width, slot_height, img, crop_point_result_dict):
        """用户设的裁剪点:图片顶端到图片底端,做特殊处理"""
        if crop_dict['img_self-adaption'] == 'w':  # 宽固定，高自适应
            get_crop_point_result_dict = {'x1': 0, 'x2': 1}
            crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = self. \
                self_adaption_height_crop(0, 1, get_crop_point_result_dict, [slot_width, slot_height], img)
            if crop_dict.get('layout_self-adaption') == 'false':
                amend_layout_height = 0
            return crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height, img.width, img.height
        else:
            return self.pic_top_and_pic_bottom_crop(slot_width, slot_height, img, crop_point_result_dict)

    def pic_top_and_pic_bottom_crop(self, origin_slot_width, origin_slot_height, img, crop_point_result_dict):
        """
        特殊处理
        1.高铺满时，尽量人体居中
        2.宽铺满时，往上移动裁剪框
        """
        img_width = img.width
        img_height = img.height
        cloth_x1, cloth_y1, cloth_x2, cloth_y2 = crop_point_result_dict['cloth_box']

        height_scale = origin_slot_height / img_height
        transform_img_width = img_width * height_scale
        if transform_img_width >= origin_slot_width:  # 图片宽度大于槽的宽度
            scale_x = scale_y = height_scale
            y = 0
            center = cloth_x1 + (cloth_x2 - cloth_x1) / 2
            # 模特图
            crop_left, crop_right = crop_point_result_dict['crop_left'], crop_point_result_dict['crop_right']

            if img.img_crop_type in ['m_t', 'm_bu', 'm_bo', 'm_f']:
                # 衣服模特最靠外的 左点 右点 不包含内间距
                if (crop_right - crop_left) * transform_img_width <= origin_slot_width:
                    center = crop_left + (crop_right - crop_left) / 2

            x = self.alternative_center_crop(center, origin_slot_width, transform_img_width, [crop_left, crop_right])
            self.si.main_part_offset(x * img.width + origin_slot_width / scale_x / 2, center * img.width, 'x')
        else:
            # 宽铺满的情况下,等比放缩高  裁剪高，往上移动裁剪框
            width_scale = origin_slot_width / img_width
            scale_x = scale_y = width_scale
            x = 0
            y = 0
            self.si.main_part_offset(0.5, 0.5, 'y')

        self.si.img_scale_ratio(scale_x, scale_y)
        return x * img.width, y * img.height, origin_slot_width / scale_x, origin_slot_height / scale_x, scale_x, scale_y, 0, img_width, img_height

    def center_crop(self, origin_slot_width, origin_slot_height, img_width, img_height):
        # 裁剪高铺满的情况下,等比放缩 裁剪 宽
        height_scale = origin_slot_height / img_height
        transform_img_width = img_width * height_scale
        if transform_img_width >= origin_slot_width:  # 图片宽度大于槽的宽度

            scale_x = scale_y = height_scale
            y = 0
            x = 0.5 * transform_img_width - origin_slot_width / 2
            self.si.main_part_offset(0.5, 0.5, 'x')
        else:
            # 宽铺满的情况下,等比放缩高  裁剪高
            width_scale = origin_slot_width / img_width
            scale_x = scale_y = width_scale
            transform_img_height = width_scale * img_height
            x = 0
            y = 0.5 * transform_img_height - origin_slot_height / 2
            self.si.main_part_offset(0.5, 0.5, 'y')

        self.si.img_scale_ratio(scale_x, scale_y)
        return x / scale_x, y / scale_x, origin_slot_width / scale_x, origin_slot_height / scale_x, scale_x, scale_y, 0, img_width, img_height

    def extension_crop(self, top, bottom, crop_point_result_dict, origin_slot, img, img_crop_type):
        # 一定要考虑图片放缩 后 相关点的变化

        origin_slot_width, origin_slot_height = origin_slot
        # 裁剪高铺满的情况下,等比放缩 裁剪 宽
        height_scale = origin_slot_height / ((bottom - top) * img.height)
        transform_img_width = img.width * height_scale

        scale_x = scale_y = height_scale
        y = top
        # 加上padding的 左右点
        x1 = crop_point_result_dict['x1']
        x2 = crop_point_result_dict['x2']
        center = x1 + (x2 - x1) / 2

        left = center * transform_img_width - origin_slot_width / 2  # slot左边 距离 原点的位置
        right = center * transform_img_width + origin_slot_width / 2  # slot右边 距离 原点的位置

        tag_1 = (left >= 0)
        tag_2 = (right <= transform_img_width)

        if not (tag_1 and tag_2):
            self.si.extension()
        x = (center * transform_img_width - origin_slot_width / 2)
        # 调整 左右 扩边留白相等
        if tag_1 and tag_2:  # 左右 都有足够 预留范围 不用调整
            pass
        elif tag_1 and not tag_2:  # 左范围够 右范围不够 # 尝试 向 左移动
            if (right - transform_img_width) <= left:  # 右扩边 小于 左距离
                x = left - (right - transform_img_width)
            else:
                x = -((right - transform_img_width - left) / 2)
        elif not tag_1 and tag_2:  # 左范围不够 右范围够
            if -left <= (transform_img_width - right):
                x = 0
            else:
                x = (left + (transform_img_width - right)) / 2
        else:  # 左右范围都不够
            # 左右白边相加 求平均值
            x = -((right - transform_img_width) - left) / 2
        x = x / transform_img_width

        self.si.main_part_offset(x * img.width + origin_slot_width / scale_x / 2, center * img.width, 'x')

        self.si.img_scale_ratio(scale_x, scale_y)
        return x * img.width, y * img.height, origin_slot_width / scale_x, origin_slot_height / scale_x, scale_x, scale_y, 0

    def img_crop_detail_crop(self, top, bottom, left, right, origin_slot, img):
        """图片裁剪出 细节图"""

        origin_slot_width, origin_slot_height = origin_slot

        # 裁剪高铺满的情况下,等比放缩 裁剪 宽
        height_scale = origin_slot_height / ((bottom - top) * img.height)
        transform_img_width = img.width * height_scale

        if transform_img_width >= origin_slot_width:  # 图片宽度大于槽的宽度
            scale_x = scale_y = height_scale
            center = left + (right - left) / 2
            y = top
            x = self.alternative_center_crop(center, origin_slot_width, transform_img_width, [left, right])
            self.si.main_part_offset(0.5, 0.5, 'x')
        else:
            # 宽铺满的情况下,等比放缩 计算 高  裁剪高

            # 加上内边界后 裁剪点 x1,x2
            x1 = left
            x2 = right

            width_scale = origin_slot_width / ((x2 - x1) * img.width)
            # width_scale = origin_slot_width / img.width
            transform_img_height = width_scale * img.height
            scale_x = scale_y = width_scale
            x = x1  # 左位置为  加上内边界后 的左
            # x = 0  # 左位置为  加上内边界后 的左
            center = top + (bottom - top) / 2
            y = self.alternative_center_crop(center, origin_slot_height, transform_img_height, [top, bottom])
            self.si.main_part_offset(0.5, 0.5, 'y')
        self.si.img_scale_ratio(scale_x, scale_y)
        return x * img.width, y * img.height, origin_slot_width / scale_x, origin_slot_height / scale_x, scale_x, scale_y, 0


if __name__ == '__main__':
    slot_config = {
        "cr": {
            "n_c": 1,
            "m_t": {
                "ts": "human_top",
                "bs": "hip",
                "pU": "pi",
                "t": 20,
                "r": 0,
                "b": 30,
                "l": 0
            },
            "m_bu": {
                "ts": "human_top",
                "bs": "hip",
                "pU": "pi",
                "t": 20,
                "r": 0,
                "b": 30,
                "l": 0
            },
            "m_bo": {
                "ts": "garment_top",
                "bs": "human_bottom",
                "pU": "pi",
                "t": 0,
                "r": 0,
                "b": 0,
                "l": 0
            },
            "m_f": {
                "ts": "human_top",
                "bs": "hip",
                "pU": "pi",
                "t": 20,
                "r": 0,
                "b": 30,
                "l": 0
            },
            "t": {
                "ts": "garment_top",
                "bs": "garment_bottom",
                "pU": "pi",
                "t": 30,
                "r": 0,
                "b": 30,
                "l": 0
            }
        },
        # "s": "fix",
        "s": "e",
        "v": "2020-12-12",
        "width": 1280,
        "height": 1280,
        # "width": 750,
        # "height": 1000,
    }

    img_dict = {'id': '684245', 'filename': '2020-12-27 谜底LOOKBOOK82970.jpg',
                'storage_key': 'asset/1000189/dc2a1421-1c67-407a-b910-3e8088c55cdf.jpg',
                'image_classification': 'model-all_side', 'width': 3121, 'height': 4681, 'file_id': '723519',
                'recognition': '{"image": {"width": 533, "height": 800}, "image_category": "模特", "confidence": 0.9999964237213135, "human_bodies": [{"bbox": [115, 94, 371, 750], "confidence": 0.9444527626037598, "keypoints": [[205, 708, 0.3948015868663788], [151, 504, 0.32096853852272034], [169, 360, 0.5516449213027954], [231, 354, 0.5299614071846008], [231, 522, 0.25429943203926086], [295, 673, 0.36741459369659424], [197, 339, 0.406144917011261], [218, 258, 0.5439403653144836], [226, 188, 0.7137809991836548], [218, 125, 0.5797253251075745], [204, 309, 0.3430940508842468], [150, 316, 0.3954583406448364], [154, 208, 0.7125232219696045], [293, 210, 0.7758114337921143], [313, 299, 0.6915827393531799], [346, 390, 0.6816549301147461]], "keypoints_coco": [[370, 209, 0.19185090065002441], [-1, -1, 0.07802201807498932], [370, 191, 0.4209941327571869], [-1, -1, 0.015631435438990593], [370, 215, 0.5712090730667114], [-1, -1, 0.0031422432512044907], [370, 362, 0.4440481960773468], [-1, -1, 0.0031390266958624125], [263, 322, 0.9416176080703735], [-1, -1, 0.003667104057967663], [370, 239, 0.5986910462379456], [-1, -1, 0.04587884619832039], [370, 694, 0.7474750876426697], [-1, -1, 0.01830916479229927], [-1, -1, 0.0008104267180897295], [-1, -1, 0.013747957535088062], [-1, -1, 0.013147641904652119]], "orientation": 150, "face": {"bbox": [198, 117, 242, 178], "confidence": 0.9833429455757141, "landmarks": [[205, 140], [225, 134], [216, 150], [213, 164], [228, 160]]}}], "clothes": [{"bbox": [146, 691, 239, 754], "category_id": 6, "category": "shoes", "confidence": 0.8420706391334534, "keypoints": null}, {"bbox": [278, 665, 344, 750], "category_id": 6, "category": "shoes", "confidence": 0.8294224739074707, "keypoints": null}, {"bbox": [321, 448, 403, 598], "category_id": 7, "category": "bag", "confidence": 0.6695075631141663, "keypoints": null}, {"bbox": [103, 324, 302, 619], "category_id": 2, "category": "skirt", "confidence": 0.633188009262085, "keypoints": null}, {"bbox": [110, 131, 379, 434], "category_id": 1, "category": "blouse", "confidence": 0.5361945033073425, "keypoints": null}]}',
                'image_analysis': {
                    'human_pose': '{"image": {"width": 533, "height": 800}, "result": [{"bbox": [115, 94, 371, 750], "confidence": 0.9444527626037598, "keypoints": [[216, 150, 0.9833429455757141], [205, 140, 0.9833429455757141], [225, 134, 0.9833429455757141], [205, 140, 0.9833429455757141], [225, 134, 0.9833429455757141], [293, 210, 0.7758114337921143], [154, 208, 0.7125232219696045], [313, 299, 0.6915827393531799], [150, 316, 0.3954583406448364], [346, 390, 0.6816549301147461], [204, 309, 0.3430940508842468], [231, 354, 0.5299614071846008], [169, 360, 0.5516449213027954], [231, 522, 0.25429943203926086], [151, 504, 0.32096853852272034], [295, 673, 0.36741459369659424], [205, 708, 0.3948015868663788]]}]}',
                    'cloth_1_classification': '{"image": {"width": 533, "height": 800}, "result": [{"cat_id": 3, "cat_name": "模特（侧面）", "confidence": 0.9999964237213135}]}',
                    'cloth_1_info': '{"image": {"width": 533, "height": 800}, "result": [{"bbox": [146, 691, 239, 754], "cat_id": 6, "cat_name": "shoes", "confidence": 0.8420706391334534}, {"bbox": [278, 665, 344, 750], "cat_id": 6, "cat_name": "shoes", "confidence": 0.8294224739074707}, {"bbox": [321, 448, 403, 598], "cat_id": 7, "cat_name": "bag", "confidence": 0.6695075631141663}, {"bbox": [103, 324, 302, 619], "cat_id": 2, "cat_name": "skirt", "confidence": 0.633188009262085}, {"bbox": [110, 131, 379, 434], "cat_id": 1, "cat_name": "blouse", "confidence": 0.5361945033073425}]}',
                    'storage_key': 'asset/1000189/dc2a1421-1c67-407a-b910-3e8088c55cdf.jpg',
                    'recognition': '123123',
                }}

    # print('-------------开始裁剪--------------')
    image_crop = ImageCrop()
    result = image_crop.crop(slot_config, img_dict)
    # print('-------------结束裁剪--------------')

    # print('评价指标：', image_crop.si.crop_indexing_dict)
    # print('裁剪结果：', result)
