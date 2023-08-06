from setuptools import setup, find_packages
setup(
    name = "kcevan",      #这里是pip项目发布的名称
    version = "1.1",  #版本号，数值大的会优先被pip
    keywords = ["pip", "kcevan"],			# 关键字
    description = "evan's private utils.",	# 描述
    long_description = "evan's private utils.",
    license = "MIT Licence",		# 许可证
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["docopt","hdfs","livy"]          #这个项目依赖的第三方库
)