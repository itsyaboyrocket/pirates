# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.shader.Blur
import math, random
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from otp.otpbase import OTPRender

class DependencyArray:
    __module__ = __name__

    def __init__(self, createCallback):
        self.state = False
        self.createCallback = createCallback
        self.array = []

    def enable(self, enable):
        self.state = enable

    def addDependency(self, item):
        self.array.append(item)

    def removeDependency(self, item):
        if item and item in self.array:
            self.array.remove(item)

    def checkDependencies(self):
        state = False
        if self.array:
            state = True
            length = len(self.array)
            for i in range(length):
                item = self.array[i]
                if item.created == False:
                    state = False
                    break

            if (state and self).state:
                self.createCallback()
        return state

    def delete(self):
        if self.array:
            length = len(self.array)
            for i in range(length):
                item = self.array[i]
                if item:
                    self.array[i] = None
                    item = None

            self.array = None
        return


class RenderToTexture(DirectObject):
    __module__ = __name__

    def __init__(self, rtt_name, width=512, height=512, order=0, format=0, clear_color=Vec4(0.0, 0.0, 0.0, 1.0), dependency_array=None):
        self.rtt_name = rtt_name
        self.width = width
        self.height = height
        self.order = order
        self.format = format
        self.clear_color = clear_color
        self.texture_buffer = None
        self.camera_node_path = None
        self.card = None
        self.card_parent = None
        self.card_shader = None
        self.created = False
        self.dependency_arrays = []
        if dependency_array:
            self.dependency_arrays.append(dependency_array)
            dependency_array.addDependency(self)
        if self.__createBuffer():
            self.accept('close_main_window', self.__destroyBuffer)
            self.accept('open_main_window', self.__createBuffer)
        return

    def addDependencyArray(self, array):
        if array:
            self.dependency_arrays.append(array)

    def removeDependencyArray(self, array):
        if array and array in self.dependency_arrays:
            self.dependency_arrays.remove(array)

    def enable(self, enable):
        if enable:
            if self.texture_buffer:
                self.texture_buffer.setActive(1)
        else:
            if self.texture_buffer:
                self.texture_buffer.setActive(0)

    def getTextureBuffer(self):
        return self.texture_buffer

    def saveCamera(self, camera):
        self.camera_node_path = camera

    def saveCard(self, card):
        self.card = card

    def __destroyBuffer(self):
        if self.camera_node_path:
            self.camera_node_path.removeNode()
            self.camera_node_path = None
        if self.card:
            self.card.removeNode()
            self.card = None
        if self.texture_buffer:
            self.texture_buffer.setActive(False)
            base.graphicsEngine.removeWindow(self.texture_buffer)
        self.texture_buffer = None
        self.created = False
        return

    def __createBuffer(self):
        state = False
        self.__destroyBuffer()
        texture_buffer = base.win.makeTextureBuffer(self.rtt_name, self.width, self.height)
        if texture_buffer:
            texture_buffer.setClearColor(self.clear_color)
            texture_buffer.setSort(self.order)
            if self.format:
                texture = texture_buffer.getTexture()
                if texture:
                    texture.setMatchFramebufferFormat(0)
                    texture.setFormat(self.format)
            state = True
        self.texture_buffer = texture_buffer
        self.created = state
        length = len(self.dependency_arrays)
        for i in range(length):
            dependency_array = self.dependency_arrays[i]
            if dependency_array:
                dependency_array.checkDependencies()

        return state

    def delete(self):
        if self.texture_buffer:
            self.created = False
            self.__destroyBuffer()
            self.ignore('close_main_window')
            self.ignore('open_main_window')
            if self.dependency_arrays:
                length = len(self.dependency_arrays)
                for i in range(length):
                    dependency_array = self.dependency_arrays[i]
                    if dependency_array:
                        dependency_array.delete()
                        self.dependency_arrays[i] = None

            self.dependency_arrays = None
        return


class Glow(DirectObject):
    __module__ = __name__

    def createCallback(self):
        self.success = False
        glow_rtt = self.glow_rtt
        if glow_rtt:
            gbuffer = glow_rtt.getTextureBuffer()
            if gbuffer:
                self.success = True
                self.glow_camera = Camera('glow_camera')
                self.glow_camera_node_path = self.scene.attachNewNode(self.glow_camera)
                self.glow_camera_node_path.node().setScene(self.scene)
                camera_parent = self.camera.getParent()
                self.glow_camera_node_path.reparentTo(camera_parent)
                self.scene.hide(OTPRender.GlowCameraBitmask)
                self.glow_camera.setCameraMask(OTPRender.GlowCameraBitmask)
                self.updateCamera(self.camera)
                self.card = gbuffer.getTextureCard()
                display_region = gbuffer.makeDisplayRegion()
                display_region.setCamera(self.glow_camera_node_path)
                if gbuffer.shareDepthBuffer(self.source_rtt.getTextureBuffer()):
                    gbuffer.setClearColorActive(1)
                    gbuffer.setClearDepthActive(0)
                    gbuffer.setClearStencilActive(0)
                else:
                    self.success = False
                glow_rtt.saveCamera(self.glow_camera_node_path)
                glow_rtt.saveCard(self.card)
                if self.add:
                    self.card and self.card.reparentTo(render2d)
                    self.card.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))

    def __init__(self, width, height, source_rtt, scene, camera, add=0, order=0, format=0, glitter=1):
        self.first_tick = True
        dependency_array = DependencyArray(self.createCallback)
        self.dependency_array = dependency_array
        source_rtt.addDependencyArray(dependency_array)
        self.source_rtt = source_rtt
        dependency_array.addDependency(source_rtt)
        self.success = False
        self.hdr = None
        self.card = None
        self.glow_camera = None
        self.glow_camera_node_path = None
        self.add = add
        self.scene = scene
        self.camera = camera
        self.glitter = glitter
        glow_rtt = RenderToTexture('glow', width, height, order, format, dependency_array=dependency_array)
        self.glow_rtt = glow_rtt
        dependency_array.enable(True)
        dependency_array.checkDependencies()
        self.updateCamera(self.camera)
        taskMgr.add(self.camTask, 'glowCamTask-' + str(id(self)), priority=49)
        return

    def camTask--- This code section failed: ---

 268       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             1  'updateCamera'
           6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             2  'camera'
          12  CALL_FUNCTION_1       1  None
          15  POP_TOP          

 270      16  LOAD_FAST             1  'task'
          19  LOAD_ATTR             4  'time'
          22  STORE_FAST            6  'time'

 271      25  LOAD_FAST             0  'self'
          28  LOAD_ATTR             5  'first_tick'
          31  JUMP_IF_FALSE        19  'to 53'
          34  POP_TOP          

 272      35  LOAD_CONST            1  0.0
          38  STORE_FAST            5  'elapsed_time'

 273      41  LOAD_GLOBAL           7  'False'
          44  LOAD_FAST             0  'self'
          47  STORE_ATTR            5  'first_tick'
          50  JUMP_FORWARD         14  'to 67'
        53_0  COME_FROM            31  '31'
          53  POP_TOP          

 275      54  LOAD_FAST             6  'time'
          57  LOAD_FAST             0  'self'
          60  LOAD_ATTR             8  'current_time'
          63  BINARY_SUBTRACT  
          64  STORE_FAST            5  'elapsed_time'
        67_0  COME_FROM            50  '50'

 277      67  LOAD_FAST             6  'time'
          70  LOAD_FAST             0  'self'
          73  STORE_ATTR            8  'current_time'

 278      76  LOAD_FAST             5  'elapsed_time'
          79  LOAD_FAST             0  'self'
          82  STORE_ATTR            6  'elapsed_time'

 280      85  LOAD_CONST            2  180.0
          88  LOAD_FAST             0  'self'
          91  STORE_ATTR            9  'speed'

 282      94  LOAD_FAST             0  'self'
          97  LOAD_ATTR             8  'current_time'
         100  LOAD_FAST             0  'self'
         103  LOAD_ATTR             9  'speed'
         106  BINARY_MULTIPLY  
         107  STORE_FAST            2  'distance'

 284     110  LOAD_FAST             0  'self'
         113  LOAD_ATTR            11  'hdr'
         116  JUMP_IF_FALSE       132  'to 251'
       119_0  THEN                     252
         119  POP_TOP          

 285     120  LOAD_FAST             0  'self'
         123  LOAD_ATTR            12  'glitter'
         126  JUMP_IF_FALSE        96  'to 225'
         129  POP_TOP          

 286     130  LOAD_CONST            3  0.14
         133  STORE_FAST            3  'maximum_range'

 288     136  LOAD_CONST            5  1.0
         139  LOAD_GLOBAL          14  'random'
         142  LOAD_ATTR            14  'random'
         145  CALL_FUNCTION_0       0  None
         148  LOAD_FAST             3  'maximum_range'
         151  BINARY_MULTIPLY  
         152  LOAD_FAST             3  'maximum_range'
         155  LOAD_CONST            6  2.0
         158  BINARY_DIVIDE    
         159  BINARY_SUBTRACT  
         160  BINARY_ADD       
         161  STORE_FAST            4  'factor'
         164  JUMP_ABSOLUTE       232  'to 232'
         167  POP_TOP          

 290     168  LOAD_FAST             2  'distance'
         171  LOAD_CONST            7  360.0
         174  BINARY_MODULO    
         175  STORE_FAST            7  'angle'

 291     178  LOAD_FAST             7  'angle'
         181  LOAD_GLOBAL          17  'math'
         184  LOAD_ATTR            18  'pi'
         187  LOAD_CONST            2  180.0
         190  BINARY_DIVIDE    
         191  INPLACE_MULTIPLY 
         192  STORE_FAST            7  'angle'

 292     195  LOAD_CONST            5  1.0
         198  LOAD_GLOBAL          17  'math'
         201  LOAD_ATTR            19  'sin'
         204  LOAD_FAST             7  'angle'
         207  CALL_FUNCTION_1       1  None
         210  LOAD_FAST             3  'maximum_range'
         213  LOAD_CONST            6  2.0
         216  BINARY_DIVIDE    
         217  BINARY_MULTIPLY  
         218  BINARY_ADD       
         219  STORE_FAST            4  'factor'
         222  JUMP_FORWARD          7  'to 232'
       225_0  COME_FROM           126  '126'
         225  POP_TOP          

 294     226  LOAD_CONST            5  1.0
         229  STORE_FAST            4  'factor'
       232_0  COME_FROM           222  '222'

 295     232  LOAD_FAST             0  'self'
         235  LOAD_ATTR            11  'hdr'
         238  LOAD_ATTR            20  'setGlowFactor'
         241  LOAD_FAST             4  'factor'
         244  CALL_FUNCTION_1       1  None
         247  POP_TOP          
         248  JUMP_FORWARD          1  'to 252'
       251_0  COME_FROM           116  '116'
         251  POP_TOP          
       252_0  COME_FROM           248  '248'

 299     252  LOAD_GLOBAL          21  'Task'
         255  LOAD_ATTR            22  'cont'
         258  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 167

    def updateCamera(self, camera):
        if camera:
            if self.glow_camera:
                lens = camera.node().getLens()
                self.glow_camera_node_path.node().setLens(lens)

    def getGlowBuffer(self):
        glow_buffer = None
        if self.glow_rtt:
            glow_buffer = self.glow_rtt.getTextureBuffer()
        return glow_buffer

    def delete(self):
        if self.source_rtt:
            self.source_rtt.removeDependencyArray(self.dependency_array)
        self.source_rtt = None
        if self.dependency_array:
            self.dependency_array.delete()
        self.dependency_array = None
        self.card = None
        self.scene = None
        self.camera = None
        if self.glow_camera:
            self.glow_camera = None
        if self.glow_camera_node_path:
            self.glow_camera_node_path.removeNode()
            self.glow_camera_node_path = None
        if self.glow_rtt:
            self.glow_rtt.delete()
            self.glow_rtt = None
        taskMgr.remove('glowCamTask-' + str(id(self)))
        return


class Blur(DirectObject):
    __module__ = __name__

    def createCallback(self):
        if self.luminance:
            if self.luminance_rtt == None:
                return
        tonemap = self.hdr
        source = self.source_rtt.getTextureBuffer()
        original = source
        if self.average:
            parameters = Vec4(0.0, 0.0, 0.0, 0.0)
            source_size = 1024.0
            parameters.set(1.0 / source_size, 1.0 / source_size, 0.0, 0.0)
            sbuffer = original
            a = 'a256'
            a_rtt = self.a256_rtt
            abuffer = a_rtt.getTextureBuffer()
            acamera = base.makeCamera2d(abuffer, cameraName=a)
            ascene = NodePath(a + '_scene')
            acamera.node().setScene(ascene)
            acard = source.getTextureCard()
            acard.setShader(self.average_shader)
            acard.reparentTo(ascene)
            a_rtt.saveCamera(acamera)
            acard.setShaderInput(self.parameters_name, parameters)
            acard.setShaderInput(self.original_name, sbuffer.getTexture())
            self.cameraClearOff(acamera)
            source_size = 256.0
            parameters.set(1.0 / source_size, 1.0 / source_size, 0.0, 0.0)
            sbuffer = a_rtt.getTextureBuffer()
            a = 'a64'
            a_rtt = self.a64_rtt
            abuffer = a_rtt.getTextureBuffer()
            acamera = base.makeCamera2d(abuffer, cameraName=a)
            ascene = NodePath(a + '_scene')
            acamera.node().setScene(ascene)
            acard = sbuffer.getTextureCard()
            acard.setShader(self.average_shader)
            acard.reparentTo(ascene)
            a_rtt.saveCamera(acamera)
            acard.setShaderInput(self.parameters_name, parameters)
            acard.setShaderInput(self.original_name, sbuffer.getTexture())
            self.cameraClearOff(acamera)
            source_size = 64.0
            parameters.set(1.0 / source_size, 1.0 / source_size, 0.0, 0.0)
            sbuffer = a_rtt.getTextureBuffer()
            a = 'a16'
            a_rtt = self.a16_rtt
            abuffer = a_rtt.getTextureBuffer()
            acamera = base.makeCamera2d(abuffer, cameraName=a)
            ascene = NodePath(a + '_scene')
            acamera.node().setScene(ascene)
            acard = sbuffer.getTextureCard()
            acard.setShader(self.average_shader)
            acard.reparentTo(ascene)
            a_rtt.saveCamera(acamera)
            acard.setShaderInput(self.parameters_name, parameters)
            acard.setShaderInput(self.original_name, sbuffer.getTexture())
            self.cameraClearOff(acamera)
            source_size = 16.0
            parameters.set(1.0 / source_size, 1.0 / source_size, 0.0, 0.0)
            sbuffer = a_rtt.getTextureBuffer()
            a = 'a4'
            a_rtt = self.a4_rtt
            abuffer = a_rtt.getTextureBuffer()
            acamera = base.makeCamera2d(abuffer, cameraName=a)
            ascene = NodePath(a + '_scene')
            acamera.node().setScene(ascene)
            acard = sbuffer.getTextureCard()
            acard.setShader(self.average_shader)
            acard.reparentTo(ascene)
            a_rtt.saveCamera(acamera)
            acard.setShaderInput(self.parameters_name, parameters)
            acard.setShaderInput(self.original_name, sbuffer.getTexture())
            self.cameraClearOff(acamera)
            source_size = 4.0
            parameters.set(1.0 / source_size, 1.0 / source_size, 0.0, 0.0)
            sbuffer = a_rtt.getTextureBuffer()
            sbuffer.getTexture().setWrapU(Texture.WMRepeat)
            sbuffer.getTexture().setWrapV(Texture.WMRepeat)
            a = 'a1'
            a_rtt = self.a1_rtt
            abuffer = a_rtt.getTextureBuffer()
            acamera = base.makeCamera2d(abuffer, cameraName=a)
            ascene = NodePath(a + '_scene')
            acamera.node().setScene(ascene)
            acard = sbuffer.getTextureCard()
            acard.setShader(self.average_shader)
            acard.reparentTo(ascene)
            a_rtt.saveCamera(acamera)
            acard.setShaderInput(self.parameters_name, parameters)
            acard.setShaderInput(self.original_name, sbuffer.getTexture())
            self.cameraClearOff(acamera)
        if self.luminance:
            luminance_rtt = self.luminance_rtt
            lbuffer = luminance_rtt.getTextureBuffer()
            if lbuffer:
                lcamera = base.makeCamera2d(lbuffer, cameraName='luminance')
                lscene = NodePath('l_scene')
                lcamera.node().setScene(lscene)
                lcard = source.getTextureCard()
                lcard.setShader(self.luminance_shader)
                lcard.reparentTo(lscene)
                if self.add_glow:
                    if self.glow_rtt:
                        lcard.setShaderInput(self.glow_name, self.glow_rtt.getTextureBuffer().getTexture())
                        self.lcard = lcard
                        self.setGlowFactor(self.glow_factor)
                    luminance_rtt.saveCamera(lcamera)
                    luminance_rtt.saveCard(lcard)
                    source = lbuffer
            x_rtt = self.x_rtt
            xbuffer = x_rtt.getTextureBuffer()
            xcamera = base.makeCamera2d(xbuffer, cameraName='x_blur')
            xscene = NodePath('x_scene')
            xcamera.node().setScene(xscene)
            xcard = source.getTextureCard()
            xcard.setShader(self.blur_x_shader)
            xcard.reparentTo(xscene)
            x_rtt.saveCamera(xcamera)
            x_rtt.saveCard(xcard)
            b_rtt = self.b_rtt
            bbuffer = b_rtt.getTextureBuffer()
            ycamera = base.makeCamera2d(bbuffer, cameraName='y_blur')
            yscene = NodePath('y_scene')
            ycamera.node().setScene(yscene)
            ycard = xbuffer.getTextureCard()
            ycard.setShader(self.blur_y_shader)
            ycard.reparentTo(yscene)
            b_rtt.saveCamera(ycamera)
            b_rtt.saveCard(ycard)
            t_rtt = (tonemap and self).t_rtt
            tbuffer = t_rtt.getTextureBuffer()
            tcamera = base.makeCamera2d(tbuffer, cameraName='tonemap')
            tscene = NodePath('t_scene')
            tcamera.node().setScene(tscene)
            tcard = bbuffer.getTextureCard()
            tcard.setShader(self.tonemap_shader)
            tcard.reparentTo(tscene)
            self.tcard = tcard
            t_rtt.saveCamera(tcamera)
            t_rtt.saveCard(tcard)
            self.deleteSliders()
            tcard.setShaderInput(self.parameters_name, self.parameters)
            tcard.setShaderInput(self.parameters2_name, self.parameters2)
            tcard.setShaderInput(self.factors_name, self.factors)
            tcard.setShaderInput(self.original_name, original.getTexture())
            if self.average:
                tcard.setShaderInput(self.average_name, self.a1_rtt.getTextureBuffer().getTexture())
            if self.hdr_output:
                tcard.reparentTo(render2d)
            if self.debug_keys:
                self.accept('shift-8', self.toggleSliders)
                self.accept('shift-9', self.toggleDisplay)

            def update_slider(slider, update_function):
                string = slider.label + ' %.5f' % (slider['value'] * slider.parameter_scale)
                slider['text'] = string
                update_function(slider['value'])

            def create_slider(update_function, default_value, x, y, resolution, label):
                slider = DirectSlider(parent=None, command=update_slider, thumb_relief=DGG.FLAT, pos=(x, 0.0, y), text_align=TextNode.ARight, text_scale=(0.1,
                                                                                                                                                          0.1), text_pos=(0.5,
                                                                                                                                                                          0.1), scale=0.5, pageSize=resolution, text='default', value=default_value)
                slider.label = label
                slider['extraArgs'] = [slider, update_function]
                slider.parameter_scale = 1.0
                return slider

            x = -0.8
            y = 0.8
            x_increment = 1.1
            y_increment = -0.15
            resolution = 0.02
            slider = create_slider(self.updateExposure, self.exposure, x, y, resolution, 'exposure')
            slider.parameter_scale = self.exposure_scale
            self.slider_array.append(slider)
            y += y_increment
            slider = create_slider(self.updateExposure2, self.exposure2, x, y, resolution, 'blurred exposure')
            slider.parameter_scale = self.exposure_scale
            self.slider_array.append(slider)
            y += y_increment
            slider = create_slider(self.updateGamma, self.gamma, x, y, resolution, 'gamma')
            slider.parameter_scale = self.gamma_scale
            self.slider_array.append(slider)
            y += y_increment
            slider = create_slider(self.updateFactor, self.factor, x, y, resolution, 'factor')
            slider.parameter_scale = self.factor_scale
            self.slider_array.append(slider)
            y += y_increment
            slider = create_slider(self.updateFactor2, self.factor2, x, y, resolution, 'blurred factor')
            slider.parameter_scale = self.factor_scale
            self.slider_array.append(slider)
            y += y_increment
            slider = create_slider(self.updateMinimumExposure, self.minimum_exposure, x, y, resolution, 'minimum exposure')
            slider.parameter_scale = self.minimum_exposure_scale
            self.slider_array.append(slider)
            y += y_increment
            slider = create_slider(self.updateMaximumExposure, self.maximum_exposure, x, y, resolution, 'maximum exposure')
            slider.parameter_scale = self.maximum_exposure_scale
            self.slider_array.append(slider)
            y += y_increment
            slider = create_slider(self.updateHdrFactor, self.hdr_factor, x, y, resolution, 'hdr factor')
            slider.parameter_scale = self.hdr_factor_scale
            self.slider_array.append(slider)
            y += y_increment
        self.card = None
        if self.add and b_rtt:
            card = b_rtt.getTextureBuffer().getTextureCard()
            self.card = card
            card.reparentTo(render2d)
            card.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.displaySliders(self.display_sliders)
        return

    def __init__(self, width, height, source_rtt, luminance=1, add=0, order=-1, format=0, hdr=1, hdr_output=1, add_glow=0, glow_rtt=0, average=0):
        DirectObject.__init__(self)
        self.debug_keys = base.config.GetInt('want-hdr-development', 0)
        self.display = 1
        self.display_sliders = 0
        dependency_array = DependencyArray(self.createCallback)
        self.dependency_array = dependency_array
        source_rtt.addDependencyArray(dependency_array)
        dependency_array.addDependency(source_rtt)
        self.hdr = None
        self.deleted = False
        self.width = width
        self.height = height
        self.source_rtt = source_rtt
        self.luminance = luminance
        self.add = add
        self.order = order
        self.format = format
        self.hdr = hdr
        self.hdr_output = hdr_output
        self.add_glow = add_glow
        self.glow_rtt = glow_rtt
        self.glow_factor = 1.0
        self.rtt_array = []
        self.shader_array = []
        if glow_rtt:
            dependency_array.addDependency(glow_rtt)
        self.parameters_name = InternalName.make('parameters')
        self.parameters2_name = InternalName.make('parameters2')
        self.factors_name = InternalName.make('factors')
        self.original_name = InternalName.make('original')
        self.average_name = InternalName.make('average')
        self.glow_name = InternalName.make('glow')
        self.glowfactor_name = InternalName.make('glowfactor')
        parameters = Vec4(0.0, 0.0, 0.0, 0.0)
        parameters2 = Vec4(1.0, 0.0, 0.0, 0.0)
        factors = Vec4(0.0, 0.0, 0.0, 0.0)
        self.exposure_scale = 5.0
        self.gamma_scale = 2.0
        self.factor_scale = 2.0
        self.hdr_factor_scale = 1.0
        self.minimum_exposure_scale = 2.0
        self.maximum_exposure_scale = 2.0
        exposure = 1.5 / self.exposure_scale
        exposure2 = 1.5 / self.exposure_scale
        gamma = 1.0 / self.gamma_scale
        average_parameter = average
        parameters.set(exposure, gamma, exposure2, average_parameter)
        hdr_factor = 1.0
        parameters2.set(hdr_factor, 0.0, 0.0, 0.0)
        factor = 0.5 / self.factor_scale
        factor2 = 0.6 / self.factor_scale
        minimum_exposure = 1.0 / self.minimum_exposure_scale
        maximum_exposure = 1.5 / self.maximum_exposure_scale
        factors.set(factor, factor2, minimum_exposure, maximum_exposure)
        self.exposure = exposure
        self.exposure2 = exposure2
        self.gamma = gamma
        self.average_parameter = average_parameter
        self.hdr_factor = hdr_factor
        self.factor = factor
        self.factor2 = factor2
        self.minimum_exposure = minimum_exposure
        self.maximum_exposure = maximum_exposure
        self.parameters = parameters
        self.parameters2 = parameters2
        self.factors = factors
        self.average = average
        self.luminance_rtt = None
        self.x_rtt = None
        self.b_rtt = None
        self.t_rtt = None
        self.a256_rtt = None
        self.a64_rtt = None
        self.a16_rtt = None
        self.a4_rtt = None
        self.a1_rtt = None
        self.lcard = None
        self.tcard = None
        self.slider_array = []
        self.luminance_shader = None
        if luminance:
            if add_glow:
                self.luminance_shader = self.loadShader('luminance_plus_glow.cg')
            else:
                self.luminance_shader = self.loadShader('luminance.cg')
            self.shader_array.append(self.luminance_shader)
        self.blur_x_shader = self.loadShader('blur_x.cg')
        self.shader_array.append(self.blur_x_shader)
        self.blur_y_shader = self.loadShader('blur_y.cg')
        self.shader_array.append(self.blur_y_shader)
        if base.config.GetInt('want-half-hdr', 0):
            self.tonemap_shader = self.loadShader('half_tonemap.cg')
        else:
            self.tonemap_shader = self.loadShader('tonemap.cg')
        self.shader_array.append(self.tonemap_shader)
        self.average_shader = self.loadShader('average.cg')
        self.shader_array.append(self.average_shader)
        if luminance:
            self.luminance_rtt = RenderToTexture('luminance', width, height, order - 3, format, dependency_array=dependency_array)
            self.rtt_array.append(self.luminance_rtt)
        self.x_rtt = RenderToTexture('xblur', width, height, order - 2, format, dependency_array=dependency_array)
        self.rtt_array.append(self.x_rtt)
        self.b_rtt = RenderToTexture('yblur', width, height, order - 1, format, dependency_array=dependency_array)
        self.rtt_array.append(self.b_rtt)
        if hdr:
            self.t_rtt = RenderToTexture('tonemap', width, height, order, format, dependency_array=dependency_array)
            self.rtt_array.append(self.t_rtt)
        if self.average:
            order -= 5
            self.a256_rtt = RenderToTexture('a256x256', 256, 256, order - 4, format, dependency_array=dependency_array)
            self.rtt_array.append(self.a256_rtt)
            self.a64_rtt = RenderToTexture('a64x64', 64, 64, order - 3, format, dependency_array=dependency_array)
            self.rtt_array.append(self.a64_rtt)
            self.a16_rtt = RenderToTexture('a16x16', 16, 16, order - 2, format, dependency_array=dependency_array)
            self.rtt_array.append(self.a16_rtt)
            self.a4_rtt = RenderToTexture('a4x4', 4, 4, order - 1, format, dependency_array=dependency_array)
            self.rtt_array.append(self.a4_rtt)
            self.a1_rtt = RenderToTexture('a1x1', 1, 1, order - 0, format, dependency_array=dependency_array)
            self.rtt_array.append(self.a1_rtt)
        dependency_array.enable(True)
        dependency_array.checkDependencies()
        self.displaySliders(self.display_sliders)
        self.enable(0)
        self.enable(1)
        self.success = self.checkArray(self.shader_array, self.checkShader) and self.checkArray(self.rtt_array, self.checkRtt)
        return

    def setGlowFactor(self, factor):
        self.glow_factor = factor
        if self.lcard:
            parameters = Vec4(self.glow_factor, 0.0, 0.0, 0.0)
            self.lcard.setShaderInput(self.glowfactor_name, parameters)

    def checkShader(self, shader):
        if shader:
            return True
        else:
            return False

    def checkRtt(self, rtt):
        if rtt:
            return rtt.created
        else:
            return False

    def enableRtt(self, rtt):
        if rtt:
            rtt.enable(1)

    def disableRtt(self, rtt):
        if rtt:
            rtt.enable(0)

    def deleteRtt(self, rtt):
        if rtt:
            rtt.delete()

    def clearArray(self, array, function=None):
        if array:
            length = len(array)
            for i in range(length):
                if array[i]:
                    if function:
                        function(array[i])
                    array[i] = None

        return

    def processArray(self, array, function=None):
        if array:
            length = len(array)
            for i in range(length):
                if array[i]:
                    if function:
                        function(array[i])

    def checkArray(self, array, function=None):
        state = False
        if array:
            state = True
            length = len(array)
            for i in range(length):
                state = False
                if array[i]:
                    if function:
                        state = function(array[i])
                    else:
                        state = True
                if state == False:
                    break

        return state

    def cameraClearOff(self, camera_node):
        if camera_node:
            camera = camera_node.node()
            if camera:
                dr = camera.getDisplayRegion(0)
                if dr:
                    dr.disableClears()

    def update_parameters(self):
        self.parameters.set(self.exposure * self.exposure_scale, self.gamma * self.gamma_scale, self.exposure2 * self.exposure_scale, self.average_parameter)
        if self.tcard:
            self.tcard.setShaderInput(self.parameters_name, self.parameters)

    def update_parameters2(self):
        self.parameters2.set(self.hdr_factor * self.hdr_factor_scale, 0.0, 0.0, 0.0)
        if self.tcard:
            self.tcard.setShaderInput(self.parameters2_name, self.parameters2)

    def update_factors(self):
        self.factors.set(self.factor * self.factor_scale, self.factor2 * self.factor_scale, self.minimum_exposure * self.minimum_exposure_scale, self.maximum_exposure * self.maximum_exposure_scale)
        if self.tcard:
            self.tcard.setShaderInput(self.factors_name, self.factors)

    def updateExposure(self, value):
        self.exposure = value
        self.update_parameters()

    def updateGamma(self, value):
        self.gamma = value
        self.update_parameters()

    def updateExposure2(self, value):
        self.exposure2 = value
        self.update_parameters()

    def updateHdrFactor(self, value):
        self.hdr_factor = value
        self.update_parameters2()

    def updateFactor(self, value):
        self.factor = value
        self.update_factors()

    def updateFactor2(self, value):
        self.factor2 = value
        self.update_factors()

    def updateMinimumExposure(self, value):
        self.minimum_exposure = value
        self.update_factors()

    def updateMaximumExposure(self, value):
        self.maximum_exposure = value
        self.update_factors()

    def loadShader(self, filepath):
        shader = loader.loadShader('models/shaders/' + filepath)
        if shader:
            pass
        else:
            shader = loader.loadShader('../shader/' + filepath)
            if shader:
                pass
            else:
                shader = loader.loadShader('src/shader/' + filepath)
                if shader:
                    pass
                else:
                    shader = loader.loadShader(filepath)
                    if shader:
                        pass
        return shader

    def unloadShader(self, shader):
        if shader:
            pass

    def enable(self, enable):
        if self.deleted == False:
            self.display = enable
            if enable:
                if self.card:
                    self.card.show()
                self.processArray(self.rtt_array, self.enableRtt)
            else:
                if self.card:
                    self.card.hide()
                self.processArray(self.rtt_array, self.disableRtt)

    def toggleDisplay(self):
        if self.display:
            self.enable(0)
        else:
            self.enable(1)

    def displaySliders(self, enable):
        if self.slider_array:
            length = len(self.slider_array)
            for i in range(length):
                slider = self.slider_array[i]
                if enable:
                    slider.show()
                    self.display_sliders = 1
                else:
                    slider.hide()
                    self.display_sliders = 0

    def toggleSliders(self):
        if self.display_sliders:
            self.displaySliders(0)
        else:
            self.displaySliders(1)

    def deleteSliders(self):
        if self.slider_array:
            length = len(self.slider_array)
            for i in range(length):
                slider = self.slider_array[i]
                self.slider_array[i] = None
                slider.destroy()
                slider = None

        self.slider_array = []
        return

    def delete(self):
        if self.deleted == False:
            self.enable(0)
            self.ignoreAll()
            if self.card:
                self.card.removeNode()
                self.card = None
            if self.source_rtt:
                self.source_rtt.removeDependencyArray(self.dependency_array)
            self.source_rtt = None
            if self.dependency_array:
                self.dependency_array.delete()
            self.dependency_array = None
            self.clearArray(self.rtt_array, self.deleteRtt)
            self.rtt_array = None
            self.luminance_rtt = None
            self.x_rtt = None
            self.b_rtt = None
            self.t_rtt = None
            self.a256_rtt = None
            self.a64_rtt = None
            self.a16_rtt = None
            self.a4_rtt = None
            self.a1_rtt = None
            self.deleteSliders()
            self.slider_array = None
            self.clearArray(self.shader_array)
            self.shader_array = None
            self.unloadShader(self.luminance_shader)
            self.luminance_shader = None
            self.unloadShader(self.blur_x_shader)
            self.blur_x_shader = None
            self.unloadShader(self.blur_y_shader)
            self.blur_y_shader = None
            self.unloadShader(self.tonemap_shader)
            self.tonemap_shader = None
            self.unloadShader(self.average_shader)
            self.average_shader = None
            self.parameters_name = None
            self.parameters2_name = None
            self.factors_name = None
            self.original_name = None
            self.average_name = None
            self.glow_name = None
            self.glowfactor_name = None
            self.lcard = None
            self.tcard = None
            self.deleted = True
        return