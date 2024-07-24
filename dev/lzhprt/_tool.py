# -*- coding: UTF-8 -*-
# Public package
# Private package
# Internal package

################################################################################
# 填充字符串的工具
################################################################################

class Filler:
    def __init__(self, **argv):
        '''
        Args:
            fill_block (str): 填充字符
            fill_loc (str): 填充位置 ['left', 'l', 'center', 'c', 'right', 'r']
            fill_length (int): 填充长度 [None:不填充, -1:动态填充, >=0:固定填充]
        '''
        # block
        if ('fill_block' in argv):
            self.block = argv['fill_block']
        else:
            self.block = ' '
        assert (len(self.block) == 1), 'block length must be 1'
        # loc
        if ('fill_loc' in argv):
            if (argv['fill_loc'] in ['center', 'c']):
                self.loc = 'c'
            elif (argv['fill_loc'] in ['left', 'l']):
                self.loc = 'l'
            elif (argv['fill_loc'] in ['right', 'r']):
                self.loc = 'r'
            else:
                raise ValueError("loc must be in ['left', 'l', 'center', 'c', 'right', 'r']")
        else:
            self.loc = 'c'
        # length
        if ('fill_length' in argv):
            self.length = argv['fill_length']
        else:
            self.length = None

    def fill(self, value):
        output = value
        if (self.length is not None):
            if (self.loc in ['left', 'l']):
                while (len(output) < self.length):
                    output = output + self.block
            elif (self.loc in ['right', 'r']):
                while (len(output) < self.length):
                    output = self.block + output
            else:
                while (len(output) < self.length):
                    if (len(output) % 2 == 0):
                        output = self.block + output
                    else:
                        output = output + self.block
            if (self.length < len(output)):
                output = output[:self.length]
        return output

################################################################################
# 改变字符串样式的工具
################################################################################


class Styler:
    def __init__(self, **argv):
        '''
        Args:
            style_effect (str): 样式效果 ['bold', 'b', 'underline', 'u', 'blink', 'l', 'reverse', 'r', 'invisible', 'i']
            style_front (str): 前景色 ['black', 'd', 'red', 'r', 'green', 'g', 'yellow', 'y', 'blue', 'b', 'purple', 'p', 'cyan', 'c', 'white', 'w']
            style_back (str): 背景色 ['black', 'd', 'red', 'r', 'green', 'g', 'yellow', 'y', 'blue', 'b', 'purple', 'p', 'cyan', 'c', 'white', 'w']
        '''
        if ('style_effect' in argv):
            self.set_effect(argv['style_effect'])
        else:
            self.effect = '0'
        if ('style_front' in argv):
            self.set_front(argv['style_front'])
        else:
            self.front = None
        if ('style_back' in argv):
            self.set_back(argv['style_back'])
        else:
            self.back = None

    def set_effect(self, effect):
        if (effect in ['bold', 'b']):
            self.effect = '1'
        elif (effect in ['underline', 'u']):
            self.effect = '4'
        elif (effect in ['blink', 'l']):
            self.effect = '5'
        elif (effect in ['reverse', 'r']):
            self.effect = '7'
        elif (effect in ['invisible', 'i']):
            self.effect = '8'
        else:
            self.effect = '0'

    def set_front(self, color):
        if (color in ['black', 'd']):
            self.front = '30'
        elif (color in ['red', 'r']):
            self.front = '31'
        elif (color in ['green', 'g']):
            self.front = '32'
        elif (color in ['yellow', 'y']):
            self.front = '33'
        elif (color in ['blue', 'b']):
            self.front = '34'
        elif (color in ['purple', 'p']):
            self.front = '35'
        elif (color in ['cyan', 'c']):
            self.front = '36'
        elif (color in ['white', 'w']):
            self.front = '37'
        else:
            self.front = None

    def set_back(self, color):
        if (color in ['black', 'd']):
            self.back = '40'
        elif (color in ['red', 'r']):
            self.back = '41'
        elif (color in ['green', 'g']):
            self.back = '42'
        elif (color in ['yellow', 'y']):
            self.back = '43'
        elif (color in ['blue', 'b']):
            self.back = '44'
        elif (color in ['purple', 'p']):
            self.back = '45'
        elif (color in ['cyan', 'c']):
            self.back = '46'
        elif (color in ['white', 'w']):
            self.back = '47'
        else:
            self.back = None

    def __call__(self, value):
        output = [code for code in [self.effect, self.front, self.back] if code is not None]
        output = ';'.join(output)
        output = '\033[%sm%s\033[0m' % (output, value)
        return output
