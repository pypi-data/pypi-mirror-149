为了区分3.0与4.0版本，同时资源图与详情页也共用的一套裁剪逻辑代码。

为了降低裁剪部分维护与开发难度，封装为裁剪工具包





# 包制作流程

环境：win

python版本: 3.9



# 自定义包

https://packaging.python.org/tutorials/packaging-projects/#



项目目录结构

~~~markdown
 ecpro-util/

 	|-- src/

 	|   |-- ecpro/

 	|   |  |-- init.py

 	|   |  |-- html_slot_config.py

 	|   |  |-- image.py

 	|   |  |-- img_crop.py

 	|--tests/

 	|   |--test.py

 	|--setup.py

 	|--LICENSE

 	|--MANIFEST.IN

 	|--pyproject.toml

 	|--READNE.md
~~~

# 打包
> python setup.py sdist bdist_wheel



# 发布到pypi

首先需要在pypi上注册并绑定邮箱才有权限上传

> twine upload dist/*



# 安装



pip install crop-utils==0.0.22 -i  https://pypi.python.org/simple/