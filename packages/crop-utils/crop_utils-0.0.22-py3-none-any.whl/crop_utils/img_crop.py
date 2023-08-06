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
            'expected_crop_result': False,
            # 上下padding 留了多少
            'top_padding_ratio': 0,
            'bottom_padding_ratio': 0,
            # 上下裁剪点是否存在
            'top_point': False,
            'bottom_point': False,
            # 图片背景
            'image_background': 0,
        }

    def expected_crop_result(self):
        if self.crop_indexing_dict['get_crop_point']['status']:
            self.crop_indexing_dict['expected_crop_result'] = True

    def top_and_bottom_crop_result(self, flag=False):
        """
        :param flag: flag为True,设置的上下裁剪点都可以满足
                     flag为False,设置的上下裁剪点只可以满足上
        :return:
        """

        # 裁剪后 上下裁剪点 是否存在
        if self.crop_indexing_dict['get_crop_point']['top_status']:
            self.crop_indexing_dict['top_point'] = True

        if self.crop_indexing_dict['get_crop_point']['bottom_status'] and flag:
            self.crop_indexing_dict['bottom_point'] = True

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
            'top_status': True if origin_crop_site[0] == crop_site[0] else False,
            'bottom_status': True if origin_crop_site[1] == crop_site[1] else False,
        }

    def get_top_and_bottom_padding(self, top, padding_top, bottom, padding_bottom):
        """获取 上下 padding占比 """
        if padding_top == 0:
            top_padding_ratio = 1
        elif top >= padding_top:  # 上裁剪点 距离图片顶部 大于 上padiing
            top_padding_ratio = 1
        else:
            top_padding_ratio = top / padding_top
        self.crop_indexing_dict['top_padding_ratio'] = top_padding_ratio

        if padding_bottom == 0:
            bottom_padding_ratio = 1
        elif bottom + padding_bottom <= 1:
            bottom_padding_ratio = 1
        else:
            bottom_padding_ratio = (1 - bottom) / padding_bottom

        self.crop_indexing_dict['bottom_padding_ratio'] = bottom_padding_ratio

    def crop_head(self):
        """裁剪头"""
        self.crop_indexing_dict['crop_head'] = {
            'status': True
        }


class ImageCrop:

    def __init__(self):
        self.si = ShouldIndex()
        # 裁剪点 向上向下兼容顺序顺序
        self.crop_sequence = ['pic_top', 'human_top', 'eye', 'nose', 'ear', 'mouth', 'mandible', 'shoulder',
                              'elbow',
                              'wrist', "waist", 'hip', 'knee', 'ankle', 'human_bottom', 'pic_bottom']
        self.garment_crop_sequence = ['pic_top', 'human_top', 'garment_top', 'garment_bottom', 'human_bottom',
                                      'pic_bottom']

        # 记录图片每一步的裁剪流程
        # 具体图片裁剪信息，在裁剪过程中不断计算，更新
        self.set_top_name = None
        self.set_bottom_name = None
        self.set_crop_parameter = None

        self.crop_top_site = None
        self.crop_top_name = None
        self.crop_bottom_site = None
        self.crop_bottom_name = None

        self.human_box = None
        self.cloth_box = None

    def crop(self, slot_config, img):
        """
        需求文档： https://www.teambition.com/task/619e01f619f251003f289802
        """
        slot_width = slot_config.get('width')
        slot_height = slot_config.get('height')
        crop_info = slot_config.get(CROP)
        crop_method = slot_config.get(STRETCH, 'fix')

        if img.img_crop_type == GIF:  # 如果分类为动图，特殊处理
            return self.__gif_crop(slot_width, slot_height, img)

        self.si.get_slot_and_img_ration(slot_width / slot_height, img.ratio)
        # 图片背景
        self.si.crop_indexing_dict['image_background'] = img.image_background

        # 是否需要裁剪
        need_crop = crop_info.get(NEED_CROP)
        if not need_crop:
            self.si.get_crop_site([None, None], [None, None])
            self.si.expected_crop_result()
            return self._need_center_crop(crop_method, slot_width, slot_height, img)

        # 槽是否设置对应图片类型的裁剪规则
        crop_parameter = crop_info.get(img.img_crop_type, {})
        if not crop_parameter:
            self.si.get_crop_site([None, None], [None, None])
            self.si.expected_crop_result()
            # print(f"居中裁剪： 未获取到裁剪参数，图片类型为 {img.image_classification}")
            return self._need_center_crop(crop_method, slot_width, slot_height, img)

        # 资质图裁剪
        # if img.img_crop_type == BRAND:
        #     self.si.get_crop_site([None, None], [None, None])
        #     return self.brand_crop(img, slot_config, slot_width, slot_height)

        # 是否配置裁剪主商品
        if crop_info.get(MAIN_PRODUCT_CROP) == 1:  # 需要裁剪主商品
            img.deal_crop_key_point(main_product_crop=True)

        # 左右居中方式  human_center human_and_cloth brand
        x_center_method = crop_info.get(X_CENTER_METHOD, "human_center")
        # 保留上下，还是保留左右，还是兴趣区域上下  human_center human_and_cloth brand
        retain_x_or_y = crop_info.get(RETAIN_X_OR_Y, "x")
        # 寻找上下裁剪点
        top, bottom, left, right = self._get_top_bottom_crop_point(crop_parameter, img, x_center_method, crop_method)

        # 计算 内边距
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

        x1 = max(left - padding_left, 0)
        x2 = min(right + padding_right, 1)
        y1 = max(top - padding_top, 0)
        y2 = min(bottom + padding_bottom, 1)

        self.si.get_top_and_bottom_padding(top, padding_top, bottom, padding_bottom)

        # 兴趣区域裁剪
        # https://thoughts.teambition.com/workspaces/5e37b6adf0f331001a9c172d/docs/625e7db4b587e60001e38a67
        interest_region_crop = crop_info.get("interest_region_crop", {})

        if interest_region_crop.get('need_crop'):  # 是否需要兴趣区域裁剪

            if interest_region_crop['size_paddingUnit'] == 'pixel':
                interest_width = interest_region_crop["width"]
                interest_height = interest_region_crop["height"]
            else:
                interest_width = interest_region_crop["width"] * slot_width
                interest_height = interest_region_crop["height"] * slot_height

            if interest_region_crop['origin_paddingUnit'] == 'pixel':
                interest_top = interest_region_crop["top"]
                interest_left = interest_region_crop["left"]
            else:
                interest_top = interest_region_crop["top"] * slot_width
                interest_left = interest_region_crop["left"] * slot_height

            height_scale = interest_height / ((y2 - y1) * img.height)
            transform_img_width = img.width * height_scale
            transform_img_height = img.height * height_scale

            x_center = left + (right - left) / 2  # x 轴的居中
            if transform_img_width >= slot_width and transform_img_height >= slot_height:  # 槽的上下左右都能被满足
                scale_x = scale_y = height_scale
                y = y1
                x = self._alternative_interest_center(x_center, slot_width, transform_img_width, interest_left,
                                                      interest_width)

                self.si.top_and_bottom_crop_result(True)  # 上下裁剪点都存在

            elif transform_img_height >= slot_height and transform_img_width < slot_width:
                width_scale = slot_width / img.width
                y = y1
                x = 0
                scale_x = scale_y = width_scale

                self.si.top_and_bottom_crop_result(False)  # 上裁剪点存在
            else:
                if retain_x_or_y == "x":

                    min_top_ratio = interest_top / (y1 * img.height)

                    min_bottom_ratio = (slot_height - interest_top) / ((1 - y1) * img.height)

                    if left == 0.5 and right == 0.5:  # 图片能放在slot位内 human 会被裁掉
                        min_img_left_ratio = (0.5 * img.width) / (interest_left + interest_width / 2)
                        min_img_right_ratio = (0.5 * img.width) / (slot_width - interest_left - interest_width / 2)

                        max_ratio = max(min_top_ratio, min_bottom_ratio, min_img_left_ratio, min_img_right_ratio)
                        # 换算 回 原图的x
                        x = ((interest_left + interest_width / 2) * max_ratio) / slot_width

                    else:  # human 放在 兴趣区域内
                        min_human_left_ratio = (interest_left / (left * img.width))
                        min_human_right_ratio = (slot_width - interest_left - interest_width) / (
                                    (1 - right) * img.width)
                        max_ratio = max(min_top_ratio, min_bottom_ratio, min_human_left_ratio, min_human_right_ratio)

                        # 换算 回 原图的x
                        x = ((interest_left + interest_width / 2) * max_ratio - (
                                    (right - left) / 2 * img.width)) / slot_width

                    y = y1
                    scale_x = scale_y = max_ratio
                    self.si.top_and_bottom_crop_result(False)  # 上裁剪点存在

                elif retain_x_or_y == "interest_y":

                    min_top_ratio = interest_top / (y1 * img.height)
                    min_bottom_ratio = (slot_height - interest_top) / ((1 - y1) * img.height)
                    max_ratio = max(min_top_ratio, min_bottom_ratio)

                    transform_img_width = img.width * max_ratio
                    if transform_img_width >= slot_width:
                        x_center = left + (right - left) / 2  # x 轴的居中

                        x = self._alternative_interest_center(x_center, slot_width, transform_img_width, interest_left,
                                                              interest_width)
                        scale_x = scale_y = max_ratio
                        if max_ratio == min_bottom_ratio:
                            self.si.top_and_bottom_crop_result(True)  # 上下裁剪点存在
                        else:
                            self.si.top_and_bottom_crop_result(False)  # 上裁剪点存在

                    else:
                        width_scale = slot_width / img.width
                        x = 0
                        scale_x = scale_y = width_scale
                        self.si.top_and_bottom_crop_result(False)  # 上裁剪点存在
                    y = y1

                else:
                    height_scale = slot_height / img.height

                    transform_img_width = img.width * height_scale

                    if transform_img_width >= slot_width:
                        x_center = left + (right - left) / 2  # x 轴的居中

                        x = self._alternative_interest_center(x_center, slot_width, transform_img_width, interest_left,
                                                              interest_width)
                        scale_x = scale_y = height_scale
                    else:
                        width_scale = slot_width / img.width
                        x = 0
                        scale_x = scale_y = width_scale
                    y = y1

                    self.si.top_and_bottom_crop_result(True)  # 上下裁剪点存在

            self.si.main_part_offset(x * img.width + interest_left / scale_x + interest_width / scale_x / 2,
                                     x_center * img.width, 'x')

            crop_x = x * img.width
            crop_y = y * img.height
            crop_width = slot_width / scale_x
            crop_height = slot_height / scale_x
            amend_layout_height = 0

        elif crop_method == 'w':  # 自适应裁剪，slot宽不变,高可以改变
            # 保留上下 y ，还是保留左右居中 x
            retain_x_or_y = crop_info.get(RETAIN_X_OR_Y, "y")
            if retain_x_or_y == 'y':
                # 旧版逻辑
                # 需要改变slot大小
                width_scale = slot_width / ((x2 - x1) * img.width)
                transform_img_height = width_scale * img.height
                scale_x = scale_y = width_scale
                x = x1
                y = y1
                crop_width = slot_width / scale_x
                crop_height = ((y2 - y1) * img.height)
                amend_layout_height = (y2 - y1) * transform_img_height - slot_height

            else:
                # 新逻辑
                height_scale = slot_height / ((y2 - y1) * img.height)
                transform_img_width = img.width * height_scale
                x_center = left + (right - left) / 2  # x 轴的居中
                center_ = x_center * transform_img_width

                # 在图片的范围内
                tag_1 = center_ - slot_width / 2
                tag_2 = center_ + slot_width / 2
                if tag_1 >= 0 and tag_2 <= transform_img_width:  # 两边都满足，直接居中裁剪
                    scale_x = scale_y = height_scale
                    y = y1
                    x = (center_ - slot_width / 2) / transform_img_width
                    crop_width = slot_width / scale_x
                    crop_height = slot_height / scale_x
                    amend_layout_height = 0
                else:
                    # 需要改变slot大小
                    min_x = min(x_center, 1 - x_center)
                    width_scale = slot_width / (2 * min_x * img.width)
                    transform_img_height = width_scale * img.height
                    scale_x = scale_y = width_scale
                    x = x_center - min_x
                    y = y1
                    crop_width = slot_width / scale_x
                    crop_height = ((y2 - y1) * img.height)
                    amend_layout_height = (y2 - y1) * transform_img_height - slot_height

            crop_x = x * img.width
            crop_y = y * img.height
            self.si.top_and_bottom_crop_result(True)  # 上下裁剪点都存在
        elif crop_method == 'e':  # 扩边裁剪，slot高不变,宽可以改变
            crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = self.__extension_crop(
                y1, y2, {'x1': x1, 'x2': x2}, [slot_width, slot_height], img
            )

        else:  # 固定裁剪, slot宽高不变
            # 裁剪高铺满的情况下,等比放缩 裁剪 宽

            height_scale = slot_height / ((y2 - y1) * img.height)
            transform_img_width = img.width * height_scale

            if transform_img_width >= slot_width:  # 图片宽度大于槽的宽度
                scale_x = scale_y = height_scale
                x_center = left + (right - left) / 2  # x 轴的居中
                y = y1
                x = self._alternative_center(x_center, slot_width, transform_img_width)

                self.si.main_part_offset(x * img.width + slot_width / scale_x / 2, x_center * img.width, 'x')
                self.si.expected_crop_result()
                self.si.top_and_bottom_crop_result(True)  # 上下裁剪点都存在

            else:
                width_scale = slot_width / img.width
                y = y1

                if retain_x_or_y == "y":
                    scale_x = scale_y = width_scale
                    x = x1

                    y_center = y1 + (y2 - y1) / 2
                    self.si.main_part_offset(y1 * img.height + slot_height / scale_x / 2, y_center * img.height, 'y')
                else:
                    left_ = left
                    right_ = 1 - right
                    bottom_ = 1 - y1
                    min_x = min(left_, right_, bottom_)  # 找到最小的距离
                    # 同比缩放图片，并计算裁剪点x 的数值
                    if bottom_ > min_x and left <= right:
                        width_scale = slot_width / ((right + min_x) * img.width)
                        x = 0
                    else:
                        width_scale = slot_width / ((1 - (left - min_x)) * img.width)
                        x = left - min_x
                    scale_x = scale_y = width_scale
                    self.si.extension()
                    self.si.crop_head()
                    self.si.main_part_offset(0.5, 0.5, 'y')

                self.si.top_and_bottom_crop_result(False)  # 上裁剪点都存在

            crop_x = x * img.width
            crop_y = y * img.height
            crop_width = slot_width / scale_x
            crop_height = slot_height / scale_x
            amend_layout_height = 0

        self.si.img_scale_ratio(scale_x, scale_y)

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
            crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = \
                self.self_adaption_height_crop(y1, y2, get_crop_point_result_dict, [slot_width, slot_height], img)
            if crop_dict.get('layout_self-adaption') == 'false':
                amend_layout_height = 0
        else:
            crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = self.img_crop_detail_crop(
                y1, y2, x1, x2, [slot_width, slot_height], img)

        return crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height, img.width, img.height

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

    def self_adaption_height_crop(self, top, bottom, crop_point_result_dict, origin_slot, img=None, img_width=None,
                                  img_height=None):
        # img_self-adaption: true,false     图片自适应
        # layout_self-adaption: true,false  画布自适应

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

    def _need_center_crop(self, crop_method, slot_width, slot_height, img):
        """裁剪所需信息不全，居中裁剪"""
        if crop_method == 'w':  # 宽固定，高自适应
            get_crop_point_result_dict = {'x1': 0, 'x2': 1}
            crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = self. \
                self_adaption_height_crop(0, 1, get_crop_point_result_dict, [slot_width, slot_height], img)
            amend_layout_height = 0  # 历史遗留问题，留着就行
            return crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height, img.width, img.height
        else:
            return self.center_crop(slot_width, slot_height, img.width, img.height)

    def __extension_crop(self, top, bottom, crop_point_result_dict, origin_slot, img):
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

        if not (tag_1 and tag_2):  # 一个不满足就需要扩边
            self.si.extension()
        self.si.expected_crop_result()

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

    def __gif_crop(self, slot_width, slot_height, img):
        """动图宽固定，高自适应 计算出 裁剪参数"""
        crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height = self. \
            self_adaption_height_crop(0, 1, {'x1': 0, 'x2': 1}, [slot_width, slot_height], img)
        amend_layout_height = 0
        return crop_x, crop_y, crop_width, crop_height, scale_x, scale_y, amend_layout_height, img.width, img.height

    def _get_top_bottom_crop_point(self, crop_parameter, img, x_center_method, crop_method):
        #  寻找 裁剪点

        if img.img_crop_type == BRAND:  # 资质图
            crop_top_site = img.brand_crop_point['brand_top']['top_site']
            crop_bottom_site = img.brand_crop_point['brand_bottom']['bottom_site']

            crop_top = crop_top_site[1]
            crop_bottom = crop_bottom_site[1]
            crop_left = crop_top_site[0]
            crop_right = crop_bottom_site[0]
            self.si.get_crop_site(['brand_top', 'brand_bottom'], ['brand_top', 'brand_bottom'])

        elif img.img_crop_type == TILE:  # 平铺图
            crop_top_site = img.crop_point.get('garment_top',
                                               {'top_site': [0, 0], 'bottom_site': [1, 1]})['top_site']
            crop_bottom_site = img.crop_point.get('garment_bottom',
                                                  {'top_site': [0, 0], 'bottom_site': [1, 1]})['bottom_site']

            crop_top = crop_top_site[1]
            crop_bottom = crop_bottom_site[1]
            crop_left = crop_top_site[0]
            crop_right = crop_bottom_site[0]
            self.si.get_crop_site(['garment_top', 'garment_bottom'], ['garment_top', 'garment_bottom'])
        else:  # 模特图
            top_site = crop_parameter.get(TOP_SITE)
            bottom_site = crop_parameter.get(BOTTOM_SITE)
            # 取裁剪点/兼容的裁剪点
            #  Todo 裁剪点 顺序

            crop_top_site, crop_top_name = self._from_img_get_top_site(img.crop_point, top_site)
            crop_bottom_site, crop_bottom_name = self._from_img_get_bottom_site(img.crop_point, bottom_site)

            self.si.get_crop_site([top_site, bottom_site], [crop_top_name, crop_bottom_name])

            crop_top = crop_top_site[1]
            crop_bottom = crop_bottom_site[1]

            # 根据设置居中类型，选择左右点. 左右居中方式  human_center human_and_cloth brand
            if x_center_method == "human_center":
                # 计算居中点
                human_center = img.humans.calculate_x_human_center(crop_top, crop_bottom)

                # 人体X轴中线未找到，则取人和衣服X轴最靠外的点
                if human_center is None:
                    crop_left, crop_right = self._get_x_human_and_cloth(img)
                else:
                    crop_left = crop_right = human_center

            elif x_center_method == "human_and_cloth":

                crop_left, crop_right = self._get_x_human_and_cloth(img)
            else:
                crop_left = crop_right = 0.5

        # 对上下左右点进行纠正
        top = min(crop_top, crop_bottom)
        bottom = max(crop_top, crop_bottom)
        left = min(crop_left, crop_right)
        right = max(crop_left, crop_right)

        return top, bottom, left, right

    @staticmethod
    def _get_x_human_and_cloth(img):
        """左右取人体和衣服最靠外的点"""
        # 衣服识别范围不存在,人的识别范围也不存在
        human_x_flag = False
        cloth_x_flag = False

        if 'garment_top' in img.crop_point:
            cloth_x_flag = True
            cloth_box_top = img.crop_point.get('garment_top',
                                               {'top_site': [0, 0], 'bottom_site': [1, 1]})['top_site']
            cloth_box_bottom = img.crop_point.get('garment_bottom',
                                                  {'top_site': [0, 0], 'bottom_site': [1, 1]})['bottom_site']

        if 'human_top' in img.crop_point:
            human_box_top = img.crop_point['human_top']['top_site']
            human_box_bottom = img.crop_point['human_top']['bottom_site']
            human_x_flag = True

        elif 'human_bottom' in img.crop_point:
            human_box_top = img.crop_point['human_bottom']['top_site']
            human_box_bottom = img.crop_point['human_bottom']['bottom_site']
            human_x_flag = True

        if human_x_flag and cloth_x_flag:
            crop_left = min(human_box_top[0], human_box_bottom[0], cloth_box_top[0], cloth_box_bottom[0])
            crop_right = max(human_box_top[0], human_box_bottom[0], cloth_box_top[0], cloth_box_bottom[0])
        elif human_x_flag and not cloth_x_flag:
            crop_left = min(human_box_top[0], human_box_bottom[0])
            crop_right = max(human_box_top[0], human_box_bottom[0])
        elif not human_x_flag and cloth_x_flag:
            crop_left = min(cloth_box_top[0], cloth_box_bottom[0])
            crop_right = max(cloth_box_top[0], cloth_box_bottom[0])
        else:
            crop_left = crop_right = 0.5

        return crop_left, crop_right

    def _from_img_get_top_site(self, crop_point, top_site):
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

    def _from_img_get_bottom_site(self, crop_point, bottom_site):
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

    def _alternative_interest_center(self, center, slot_height_or_width, transform_height_or_width,
                                     interest_left_or_top,
                                     interest_slot_height_or_width):
        center_ = center * transform_height_or_width
        # 在图片的范围内
        tag_1 = (center_ - interest_slot_height_or_width / 2 - interest_left_or_top) >= 0
        tag_2 = (center_ + interest_slot_height_or_width / 2 + (
                slot_height_or_width - interest_slot_height_or_width - interest_left_or_top)) <= transform_height_or_width

        if tag_1 and tag_2:  # 1 2 都有足够 预留范围
            x_or_y = center_ - interest_slot_height_or_width / 2 - interest_left_or_top
        elif tag_1 and not tag_2:  # 1范围够 2范围不够
            x_or_y = transform_height_or_width - interest_slot_height_or_width
        elif tag_2 and not tag_1:  # 1范围不够 2范围够
            x_or_y = 0
        else:  # 未知情况
            x_or_y = 0
        x_or_y = x_or_y / transform_height_or_width

        if not (tag_1 and tag_2):
            self.si.extension()

        return x_or_y

    def _alternative_center(self, center, slot_height_or_width, transform_height_or_width):
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
            x = self._alternative_center(center, origin_slot_width, transform_img_width)
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
            y = self._alternative_center(center, origin_slot_height, transform_img_height)
            self.si.main_part_offset(0.5, 0.5, 'y')
        self.si.img_scale_ratio(scale_x, scale_y)
        return x * img.width, y * img.height, origin_slot_width / scale_x, origin_slot_height / scale_x, scale_x, scale_y, 0
