# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['annofab_3dpc']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json', 'numpy']

setup_kwargs = {
    'name': 'annofabapi-3dpc-extensions',
    'version': '0.2.0',
    'description': 'annofabapiの3DPC Editor用の拡張機能です。',
    'long_description': '# annofabapi-3dpc-extensions\n[![Build Status](https://travis-ci.com/kurusugawa-computer/annofabapi-3dpc-extensions.svg?branch=master)](https://travis-ci.com/kurusugawa-computer/annofabapi-3dpc-extensions)\n[![PyPI version](https://badge.fury.io/py/annofabapi-3dpc-extensions.svg)](https://badge.fury.io/py/annofabapi-3dpc-extensions)\n[![Python Versions](https://img.shields.io/pypi/pyversions/annofabapi-3dpc-extensions.svg)](https://pypi.org/project/annofabapi-3dpc-extensions/)\n[![Documentation Status](https://readthedocs.org/projects/annofabapi-3dpc-extensions/badge/?version=latest)](https://annofabapi-3dpc-extensions.readthedocs.io/en/latest/?badge=latest)\n\n\n\n[annofabapi](https://github.com/kurusugawa-computer/annofab-api-python-client)の3DPC（3D Point Cloud） Editor用の拡張機能です。\n\n# Install\n\n* Python 3.7+\n\n# Install\n\n```\n$ pip install annofabapi-3dpc-extensions\n```\n\n\n# Usage\n\ncuboidアノテーションやセグメントアノテーションに対応したデータクラスを利用できます。\n\n```python\nfrom annofabapi.parser import SimpleAnnotationDirParser\n\nfrom annofab_3dpc.annotation import (\n    CuboidAnnotationDetailDataV2,\n    EulerAnglesZXY,\n    SegmentAnnotationDetailData,\n    SegmentData,\n    convert_annotation_detail_data,\n)\n\nparser = SimpleAnnotationDirParser("tests/data/task1/input1.json")\nresult = parser.parse(convert_annotation_detail_data)\n\nsegment_annotation_data = result.details[0].data\ncuboid_annotation_data = result.details[1].data\nassert type(segment_annotation_data) == SegmentAnnotationDetailData\nassert type(cuboid_annotation_data) == CuboidAnnotationDetailDataV2\n\n\n### cuboid annotation\n\nprint(cuboid_annotation_data)\n# => CuboidAnnotationDetailDataV2(shape=CuboidShapeV2(dimensions=Size(width=6.853874863204751, height=0.2929844409227371, depth=4.092537841193188), location=Location(x=-11.896872014598989, y=-3.0571381239812996, z=0.3601047024130821), rotation=EulerAnglesZXY(x=0, y=0, z=0), direction=CuboidDirection(front=Vector3(x=1, y=0, z=0), up=Vector3(x=0, y=0, z=1))), kind=\'CUBOID\', version=\'2\')\n\n# オイラー角をクォータニオンに変換\nprint(cuboid_annotation_data.shape.rotation.to_quaternion())\n# => [1.0, 0.0, 0.0, 0.0]\n\n# クォータニオンからオイラー角に変換\nprint(EulerAnglesZXY.from([1.0, 0.0, 0.0, 0.0]))\n# => EulerAnglesZXY(x=-0.0, y=0.0, z=0.0)\n\n\n### segment annotation\nprint(segment_annotation_data)\n# => SegmentAnnotationDetailData(data_uri=\'./input1/7ba51c15-f07a-4e29-8584-a4eaf3a6812a\')\n\n# セグメント情報が格納されたファイルを読み込む\nwith parser.open_outer_file(Path(segment_annotation_data.data_uri).name) as f:\n    dict_segmenta_data = json.load(f)\n    segment_data = SegmentData.from_dict(dict_segmenta_data)\n    assert type(segment_data) == SegmentData\n    assert len(segment_data.points) > 0\n\n```\n',
    'author': 'yuji38kwmt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kurusugawa-computer/annofabapi-3dpc-extensions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
