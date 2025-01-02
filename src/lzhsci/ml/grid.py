# -*- coding: UTF-8 -*-
# Public package
import itertools
# Private package
# Internal package

################################################################################
# parameters.json 目录结构
# config['paras'] = ['para1', 'para2', 'para3']                 <= 所有进行扫描的参数
# config['group'] = {'preload': ['para1', 'para2'],             <= 不同项目需要扫描的参数名字
#                    'replay': ['para1', 'para2', 'para3']}
# config['value'] = {'para1': {'key1_1': value1_1,              <= 不同参数对应的选项名和选项值
#                              'key1_2': value1_2},
#                    'para2': {'key2_1': value2_1,
#                              'key2_2': value2_2},
#                    'para3': {'key3_1': value3_1,
#                              'key3_2': value3_2}}
# config['fixed'] = {'fpara1': fvalue1,                         <= 固定参数对应的选项名和选项值
#                    'fpara2': fvalue2}
################################################################################
# node 结构
# node['name'] = 'key1_1_key2_1_key3_1'                         <= 结点名
# node['name_preload'] = 'key1_1_key2_1'                        <= 子项目结点名，仅对all项目节点存在
# node['para1'] = value1_1                                      <= 扫描参数
# node['para2'] = value2_1
# node['para3'] = value3_1
# node['fpara1'] = fvalue1                                      <= 固定参数
# node['fpara2'] = fvalue2
################################################################################


class Grid:
    def __init__(self, config):
        self.config = config.copy()
        self.paras = self.config['paras'].copy()
        self.group = self.config['group'].copy()
        self.value = self.config['value'].copy()
        self.fixed = self.config['fixed'].copy()
        self.group['all'] = self.paras
        self.__build_combines()
        self.__build_nodes()

    def __build_combine(self, proj):
        keys = [self.value[para].keys() for para in self.group[proj]]
        return list(itertools.product(*keys))

    def __build_combines(self):
        self.combines = {proj: self.__build_combine(proj) for proj in self.group}

    def __build_node(self, proj):
        nodes = []
        for combine in self.combines[proj]:
            node = {}
            node['name'] = '_'.join(combine)
            if (proj == 'all'):
                for subproj in self.group:
                    if (subproj != 'all'):
                        node['name_%s' % (subproj)] = '_'.join([combine[ipara] for ipara, para in enumerate(self.group[subproj])])
            for ipara, para in enumerate(self.group[proj]):
                node[para] = self.value[para][combine[ipara]]
            for key in self.fixed:
                node[key] = self.fixed[key]
            nodes.append(node)
        return nodes

    def __build_nodes(self):
        self.nodes = {proj: self.__build_node(proj) for proj in self.group}

    def get_nodes(self, proj):
        '获得某个项目的所有节点'
        return self.nodes[proj]

    def search(self, name, proj='all'):
        '根据名称搜寻某个节点'
        for node in self.nodes[proj]:
            if (node['name'] == name):
                return node
        return None
