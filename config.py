
def generate_yaml_doc_PyYaml(yaml_file, py_object):
    import yaml # pip install PyYaml
    # yaml.warnings({'YAMLLoadWarning':False}) # 不显示警告
    fs = open(yaml_file, 'r+', encoding='utf-8')
    yaml.dump(py_object, fs)  # 写

    datas = yaml.load(fs.read(), Loader=yaml.FullLoader) # 读
    print(datas)

    fs.close()

def generate_yaml_doc_ruamel(yaml_file, py_object):
    from ruamel import yaml # pip3 install ruamel.yaml
    fs = open(yaml_file, 'r+', encoding='utf-8')
    yaml.dump(py_object, fs, Dumper=yaml.RoundTripDumper) # 写

    data = yaml.load(fs.read(), Loader=yaml.Loader) # 读
    print(data)

    fs.close()