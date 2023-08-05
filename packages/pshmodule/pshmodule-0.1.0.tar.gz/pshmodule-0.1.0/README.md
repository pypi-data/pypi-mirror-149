# 🤖 AI Module

### 👉🏻 데이터 수집, 전처리 관련 패키지 등록
<br>
<br>


## 👉🏻 tree
 * [src]
   * [pshmodule] 
     * [processing]
       * [__init__.py]
       * [processing.py]
     * [selenium]
       * [__init__.py]
       * [helper.py]
     * [__init__.py]
 * [test]
   * [selenium_test.py] 
 * [README.md]
 * [setup.py]


## 👉🏻 regist
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*


## 👉🏻 install
pip3 install shpark-module
