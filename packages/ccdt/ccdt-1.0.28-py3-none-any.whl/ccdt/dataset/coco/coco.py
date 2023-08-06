# -*- coding: utf-8 -*-
# @Time : 2022/3/25 14:11
# @Author : Zhan Yong
from ccdt.dataset.base_labelme.base_labelme import BaseLabelme, PathTest, Encoder, json, collections, np
from pycocotools.coco import COCO
from tqdm import *
import os


class Coco(BaseLabelme):
    """
    coco实现类，主要实现coco转labelme，labelme转coco，同时继承BaseLabelme
    子类就可以访问到基类（父类）的属性和方法了，它提高了代码的可扩展性和重用行。
    """

    def __init__(self, *args, **kwargs):
        # 注释ID
        self.cur_ann_id = 0
        # 图片ID
        self.cur_image_id = 0
        # 图片对象列表
        self.images = list()
        # 注释对象列表
        self.annotations = list()
        # 类别对象列表
        self.categories = list()
        # 所有标注属性对象列表
        self.coco_shapes = list()
        # 目标检测类别对象列表
        self.categories_name = list()
        # 自定义coco文件名称
        self.coco_file_name = 'coco.json'
        self.coco_file = kwargs.get('coco_file')
        self.coco = None
        if self.coco_file:
            self.coco = COCO(self.coco_file)  # 加载coco文件数据
        super().__init__(*args, **kwargs)

    def self2labelme(self):
        """
        coco转labelme实现
        """
        # 如果self.coco为空，则实现labelme转coco
        if self.coco is None:
            return
        # 获取每一张图片的id
        img_ids = self.coco.getImgIds()
        # 循环遍历每一个id
        i = 0
        for img_id in tqdm(img_ids):
            img_info = self.coco.loadImgs(img_id)[0]
            obj_dir = PathTest.initialize(img_info['file_name'])
            relative_path = os.path.join('..', '00.images', img_info['file_name'])
            # 通过注释id寻找到同一帧图片下的多个注释属性
            labelme_data = self.single_coco2labelme(img_id)
            labelme_data['imageHeight'] = img_info['height']
            labelme_data['imageWidth'] = img_info['width']
            labelme_data['imagePath'] = relative_path
            data_info = dict(image_dir=self.images_dir,
                             image_file=img_info['file_name'],
                             labelme_dir=self.labelme_dir,
                             labelme_file=obj_dir.stem + '.json',
                             labelme_info=labelme_data,
                             data_type=self.data_type,
                             input_dir=self.input_dir,
                             output_dir=self.output_dir,
                             only_annotation=self.only_annotation)
            self.data_infos.append(data_info)
            i += 1
        print("coco转labelme结束,一共%d" % i)

    def single_coco2labelme(self, img_id):
        """
        实现每一个coco注释合成labelme注释
        @param img_id:
        @return:
        """
        ann_ids = self.coco.getAnnIds(imgIds=img_id)
        labelme_data = dict(
            version='4.5.9',
            flags={},
            shapes=[],
            imagePath=None,
            imageData=None,
            imageHeight=None,
            imageWidth=None
        )
        if ann_ids:
            shapes = []
            anns = self.coco.loadAnns(ann_ids)
            for ann in anns:
                # 取到同一张图片的多个注释属性
                category_id = ann['category_id']
                # 获取坐标框
                bbox = ann['bbox']
                # 坐标切割
                bbox = [bbox[0:2], bbox[2:4]]
                # 左上角的坐标(x,y)右上角的坐标(x,y+h)左下角的坐标(x+w,y)右下角的坐标(x+w,y+h)
                points = [bbox[0], [bbox[0][0] + bbox[1][0], bbox[0][1] + bbox[1][1]]]
                # 通过类别id获取类别名称
                cats = self.coco.loadCats(category_id)[0]
                # 取到类别名称
                name = cats['name']
                shape = {"label": name, "points": points, "group_id": None, "shape_type": "rectangle", "flags": {}}
                shapes.append(shape)
            labelme_data['shapes'] = shapes
        return labelme_data

    def self2coco(self):
        """
        labelme转coco实现
        """
        # 如果self.coco不为空，则实现coco转labelme
        if self.coco:
            return
        self.get_data_paths()
        self.load_labelme()
        self.update_property()
        if self.data_infos:
            # 定义coco数据格式
            coco_data = dict(
                images=self.images,
                annotations=self.annotations,
                categories=self.categories,
            )
            for labelme_info in self.data_infos:
                # 针对背景类直接跳过、有json文件没有图片文件直接跳过，不写入图片属性
                if labelme_info['labelme_info'] is None or labelme_info['labelme_info']['shapes'] == [] \
                        or labelme_info['image_file'] is None:
                    continue
                self.cur_image_id += 1
                images = dict(
                    file_name=labelme_info['image_file'],
                    height=labelme_info['labelme_info']['imageHeight'],
                    width=labelme_info['labelme_info']['imageWidth'],
                    id=self.cur_image_id,
                )
                self.images.append(images)
                self.coco_shapes = labelme_info['labelme_info']['shapes']
                # 标签属性处理
                one_img_ann_list = self.labelme_shapes2coco_ann()
                self.annotations.extend(one_img_ann_list)
            for category_id, category_name in enumerate(self.categories_name, 1):
                category = dict(
                    supercategory='object',
                    id=category_id,
                    name=category_name,
                )
                self.categories.append(category)
            obj_dir = PathTest.initialize(self.images_dir)
            # self.save_labelme()
            out_put_coco_file = obj_dir.joinpath(self.input_dir, obj_dir.parent, self.coco_file_name)
            with open(out_put_coco_file, 'w', encoding='utf-8') as coco_fp:
                json.dump(coco_data, coco_fp, ensure_ascii=False, indent=4, cls=Encoder)
        return

    def labelme_shapes2coco_ann(self):
        """
        把labeme标签转成coco标签
        @return:
        """
        shapes_type = collections.defaultdict(list)
        for shape in self.coco_shapes:
            if shape['shape_type'] == 'rectangle':
                if shape['label'] not in self.categories_name:
                    self.categories_name.append(shape['label'])
                shapes_type[shape['shape_type']].append(shape)
            elif shape['shape_type'] == 'polygon':
                continue
            elif shape['shape_type'] == 'line':
                continue
            elif shape['shape_type'] == 'linestrip':
                continue
            elif shape['shape_type'] == 'circle':
                continue
        one_img_ann_list = list()
        for shape_type, shapes_type_ann in shapes_type.items():
            if shape_type == 'rectangle':
                ann_list = self.rectangle_shapes2coco(shapes_type.get(shape_type))
                one_img_ann_list.extend(ann_list)
            elif shape_type == 'polygon':
                continue
            elif shape_type == 'line':
                continue
            elif shape_type == 'linestrip':
                continue
            elif shape_type == 'circle':
                continue
        return one_img_ann_list

    def rectangle_shapes2coco(self, shapes):
        """
        实现矩形框转换计算
        @param shapes:
        @return:
        """
        ann_list = []
        for shape in shapes:
            ann = self.get_default_ann()
            category_id = shapes.index(shape) + 1
            ann['category_id'] = category_id
            points = np.array(shape['points'])
            point_min, point_max = points.min(axis=0), points.max(axis=0)
            w, h = point_max - point_min
            ann['bbox'] = [point_min[0], point_min[1], w, h]
            ann['area'] = w * h
            ann_list.append(ann)
        return ann_list

    def get_default_ann(self):
        """
        标签属性定义，并id自增
        @return:
        """
        self.cur_ann_id += 1
        annotation = dict(
            segmentation=[],
            area=0,
            iscrowd=0,
            image_id=self.cur_image_id,
            bbox=[],
            category_id=0,
            id=self.cur_ann_id,
        )
        return annotation
