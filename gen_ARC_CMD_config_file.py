#!/usr/bin/python

import sys
import argparse
import xml.etree.ElementTree as ET

def setupParser():
    parser = argparse.ArgumentParser(description='control the ARC_CMD raw conversion tool')
    # TODO: Force an explicit choice for --colorEncoding, --colorSpace, --EI
    parser.add_argument('--colorEncoding', choices=['logc', 'video', 'scenelinear'], default='logc',
                        help='the colorspace into which the raw file will be rendered')
    parser.add_argument('--colorSpace', choices=['ITU709', 'P3', 'CameraNative', 'WideGamut', 'ACES'],  default='WideGamut')
    parser.add_argument('--ND', action='store_true')
    # For these next three, if they aren't specified, then their value will be the Python reserved value None
    parser.add_argument('--CCT', type=int, choices=[2000, 2100, 2200, 2400, 2600, 2900, 3200, 3500, 3900, 4300, 4700, 5100, 5600, 6500, 7500, 9000, 11000])
    parser.add_argument('--tint', type=float)
    parser.add_argument('--EI', type=int, choices=[160, 200, 250, 320, 400, 500, 640, 800, 1000, 1280, 1600, 2000, 2560, 3200])
    parser.add_argument('--downscaleMode', choices=[ 'NATIVE_3414PX', 'NATIVE_2880PX', 'NATIVE_2868PX', 'NATIVE_2578PX', 'NATIVE_6560PX', 'NATIVE_5120PX', 'NATIVE_4320PX', 'NATIVE_3168PX', 'NATIVE_3424PX', 'NATIVE_2592PX', 'NATIVE_3200PX', 'NATIVE_1920PX', 'NATIVE_3840PX', 'NATIVE_4448PX', 'NATIVE_SCOPE_4448P ,SD_FROM_2880P', 'HD_1_78_FROM_3414PX', 'HD_1_85_FROM_3414PX', 'HD_2_39_FROM_3414PX', 'HD_1_78_FROM_2880PX', 'HD_2_39_FROM_2880PX', 'HD_2_39_FROM_2578PX', 'HD_FROM_2880PX', 'HD_FROM_6560PX', 'HD_2_39_FROM_6560PX', 'HD_1_85_FROM_6560PX', 'HD_1_78_FROM_6560PX', 'HD_FROM_5120PX', 'HD_2_39_FROM_5120PX', 'HD_1_85_FROM_5120PX', 'HD_1_78_FROM_5120PX', 'HD_FROM_4320PX', 'HD_2_39_FROM_4320PX', 'HD_1_85_FROM_4320PX', 'HD_1_78_FROM_4320PX', 'HD_FROM_3840PX', 'HD_FROM_4448PX', 'HD_FROM_SCOPE_4448PX', 'HD_1_78_FROM_3840PX', 'HD_1_78_FROM_4448PX', 'HD_1_85_FROM_4448P', 'HD_2_39_FROM_4448PX', 'TWO_K_1_78_FROM_3414PX', 'TWO_K_DCI_1_85_FROM_3414PX', 'TWO_K_1_85_FROM_3414PX', 'TWO_K_2_39_FROM_3414PX', 'TWO_K_FROM_2880PX', 'TWO_K_FROM_2868PX', 'TWO_K_1_78_FROM_2880PX', 'TWO_K_1_78_FROM_2868P', 'TWO_K_2_39_FROM_2880PX', 'TWO_K_DCI_1_85_FROM_2880PX', 'TWO_K_2_39_FROM_2578PX', 'TWO_K_FROM_6560P', 'TWO_K_2_39_FROM_6560PX', 'TWO_K_1_85_FROM_6560PX', 'TWO_K_DCI_1_85_FROM_6560PX', 'TWO_K_1_78_FROM_6560PX', 'TWO_K_FROM_5120PX', 'TWO_K_2_39_FROM_5120PX', 'TWO_K_1_85_FROM_5120PX', 'TWO_K_DCI_1_85_FROM_5120PX', 'TWO_K_1_78_FROM_5120PX', 'TWO_K_FROM_4320PX', 'TWO_K_2_39_FROM_4320PX', 'TWO_K_1_85_FROM_4320PX', 'TWO_K_DCI_1_85_FROM_4320PX', 'TWO_K_1_78_FROM_4320PX', 'TWO_K_FROM_3168PX', 'TWO_K_FROM_3200P', 'TWO_K_FROM_3840PX', 'TWO_K_FROM_4448PX', 'TWO_K_1_78_FROM_3840PX', 'TWO_K_DCI_1_85_FROM_3840P', 'TWO_K_DCI_1_85_FROM_4448PX', 'TWO_K_2_39_FROM_3840PX', 'TWO_K_2_39_FROM_SCOPE_4448PX', 'TWO_K_2_39_FROM_4448P', 'QUAD_HD_1_85_FROM_3414PX', 'QUAD_HD_2_39_FROM_3414PX', 'QUAD_HD_2_39_FROM_2880PX', 'QUAD_HD_2_39_FROM_2578PX', 'QUAD_HD_FROM_2880PX', 'QUAD_HD_FROM_6560PX', 'QUAD_HD_2_39_FROM_6560PX', 'QUAD_HD_1_85_FROM_6560PX', 'QUAD_HD_1_78_FROM_6560PX', 'QUAD_HD_FROM_5120PX', 'QUAD_HD_2_39_FROM_5120PX', 'QUAD_HD_1_85_FROM_5120PX', 'QUAD_HD_1_78_FROM_5120PX', 'QUAD_HD_FROM_4320PX', 'QUAD_HD_2_39_FROM_4320PX', 'QUAD_HD_1_85_FROM_4320PX', 'QUAD_HD_1_78_FROM_4320P', 'QUAD_HD_FROM_3168PX', 'QUAD_HD_FROM_3200P', 'QUAD_HD_FROM_3840PX', 'QUAD_HD_FROM_4448PX', 'QUAD_HD_1_78_FROM_3840PX', 'QUAD_HD_1_78_FROM_4448P', 'QUAD_HD_1_85_FROM_4448PX', 'QUAD_HD_2_39_FROM_4448P', 'FOUR_K_DCI_1_78_FROM_3414PX', 'FOUR_K_1_78_FROM_3414PX', 'FOUR_K_DCI_1_85_FROM_3414PX', 'FOUR_K_1_85_FROM_3414PX', 'FOUR_K_2_39_FROM_3414PX', 'FOUR_K_DCI_1_78_FROM_2880PX', 'FOUR_K_DCI_1_85_FROM_2880PX', 'FOUR_K_2_39_FROM_2880PX', 'FOUR_K_2_39_FROM_2578PX', 'FOUR_K_FROM_2880PX', 'FOUR_K_FROM_6560PX', 'FOUR_K_2_39_FROM_6560PX', 'FOUR_K_1_85_FROM_6560PX', 'FOUR_K_DCI_1_85_FROM_6560PX', 'FOUR_K_1_78_FROM_6560PX', 'FOUR_K_FROM_5120PX', 'FOUR_K_2_39_FROM_5120PX', 'FOUR_K_1_85_FROM_5120PX', 'FOUR_K_DCI_1_85_FROM_5120PX', 'FOUR_K_1_78_FROM_5120PX', 'FOUR_K_FROM_4320PX', 'FOUR_K_2_39_FROM_4320PX', 'FOUR_K_1_85_FROM_4320PX', 'FOUR_K_DCI_1_85_FROM_4320PX', 'FOUR_K_1_78_FROM_4320PX', 'FOUR_K_FROM_3168P', 'FOUR_K_FROM_3200PX', 'FOUR_K_FROM_4448PX', 'FOUR_K_DCI_1_85_FROM_3840PX', 'FOUR_K_DCI_1_85_FROM_4448P', 'FOUR_K_2_39_FROM_3840PX', 'FOUR_K_2_39_FROM_SCOPE_4448PX', 'FOUR_K_2_39_FROM_4448' ], default='NATIVE_3414PX')
    parser.add_argument('--anamorph', action='store_true')
    parser.add_argument('--sharpness', type=int, default=100)
    parser.add_argument('--cameraType', choices=['ALEXA', 'D21'], default='ALEXA')
    parser.add_argument('--inputContainer', choices=['FullOpenGate', 'OpenGateWith4by3', 'OpenGateWith6by5', 'OpenGateWith8by9', 'Classic16by9'], default='Classic16by9')
    parser.add_argument('--processing', type=float, choices=[1.0, 2.0, 3.0, 4.0, 5.0], default=5.0)
    parser.add_argument('--qualityMode', choices=['HQ', 'proxy2', 'proxy3'], default='HQ')
    parser.add_argument('--debayer', choices=['ADA-1 HW', 'ADA-3 SW', 'ADA-3 HW', 'ADA-5 SW', 'ADA-5 HW'], default='ADA-5 SW')
    parser.add_argument('--GPU', action='store_true', default=False)
    parser.add_argument('--inputDirectory', default='.')
    parser.add_argument('--inputFilenameBase')
    # parser.add_argument('--inputFilenameFrameNumberFormat', default='%d')
    # startFrame and endFrame can't be ints because we need to get the length if there are leading zeros
    parser.add_argument('--startFrame')
    parser.add_argument('--endFrame')
    parser.add_argument('--format', choices=['TIFF', 'DPX', 'DPX_16Bit', 'DPX_16Bit_BGR', 'EXR'], default='EXR')
    parser.add_argument('--outputDirectory', default='.')
    parser.add_argument('--outputFilenameBase')
    parser.add_argument('--processors', type=int, default=4)
    parser.add_argument('--configFilename')
    return parser

def checkArgs(args):
    # Now some checks that are a little too complicated to express with argparse
    if args.colorEncoding == 'LogC' :
        if not args.colorSpace in ['CameraNative', 'WideGamut'] :
            print('error: LogC as a color encoding requires either CameraNative (SUP 2.0 or earlier) or WideGamut (SUP 3.0 or later) as a color space')
            sys.exit(2)
    elif args.colorEncoding == 'Video' :
        if not args.colorSpace in ['ITU709', 'P3'] :
            print('error: Video as a color encoding requires either ITU709 or P3 as a color space')
            sys.exit(2)
    if args.tint != None and (args.tint < -12.0 or args.tint > 12.0) :
        print('error: tint outside range -12.0 .. 12.0')
        sys.exit(2)     
    if args.sharpness < 0 or args.sharpness > 300 :
        print('error: sharpness outside range of 0 .. 300')
        sys.exit(2)
    if args.inputFilenameBase == None :
        print('error: input filename base must be specified with --inputFilenameBase parameter')
        sys.exit(2)
    if args.outputFilenameBase == None :
        print('error: output filename base must be specified with --outputFilenameBase parameter')
        sys.exit(2)
    if args.startFrame == None :
        print('error: input start frame must be specified with --startFrame parameter')
        sys.exit(2)
    if args.endFrame == None :
        print('error: input end frame must be specified with --endFrame parameter')
        sys.exit(2)
    if args.configFilename == None :
        print('error: must specify file to which config information will be written with --configFilename')
        sys.exit(2)

def cleanInputFrameNumberFormat(args):
    startDigits = len(args.startFrame)
    endDigits = len(args.endFrame)
    if startDigits != endDigits :
        args.inputFilenameFrameNumberFormat = '%0' + ('%d' % max(startDigits, endDigits)) + 'd'

def attachParam(parent, name, value):
    if value != None :
        ET.SubElement(parent, "param", { "name" : name, "value" : value })

def colorHandlingParams(args):
    colorhandling = ET.Element("colorhandling")
    attachParam(colorhandling, "colorencoding", args.colorEncoding)
    attachParam(colorhandling, "colorspace", args.colorSpace)
    if args.CCT != None :
        attachParam(colorhandling, "cct", "%d" % args.CCT)
    if args.tint != None  and args.tint != 0.0:
        attachParam(colorhandling, "tint", "%0.4f" % args.tint)
    return colorhandling

def asalutParams(args):
    asalut = ET.Element("asalut")
    if args.EI != None :
        attachParam(asalut, "iso", "%d" % args.EI)
        return asalut
    else :
        return None

def downscaleParams(args):
    downscale = ET.Element("downscale")
    attachParam(downscale, "mode", args.downscaleMode)
    attachParam(downscale, "anamorph", "2.0" if args.anamorph else "1.0")
    attachParam(downscale, "crispness", "%0.2f" % (args.sharpness / 100.0))
    return downscale

def cameraParams(args):
    camera = ET.Element("camera")
    attachParam(camera, "cameratype", args.cameraType)
    attachParam(camera, "inputContainer", args.inputContainer)
    return camera

def studioParams(args):
    studio = ET.Element("studio")
    if args.ND :
        attachParam(studio, "ND-filter", 1 if args.ND else 0)
    return studio

def processingParams(args):
    processing = ET.Element("processing")
    attachParam(processing, "version", "%0.1f" % args.processing)
    return processing

def qualityParams(args):
    quality = ET.Element("quality")
    attachParam(quality, "mode", args.qualityMode)
    attachParam(quality, "debayer", args.debayer)
    return quality

def performanceParams(args):
    performance = ET.Element("performance")
    attachParam(performance, "processors", "%d" % args.processors)
    attachParam(performance, "rendermode", "GPU" if args.GPU else "CPU")
    return performance

def inputParams(args):
    # input and value seem to be reserved words
    inputVar = ET.Element("input")
    valueVar = args.inputDirectory + '/' + args.inputFilenameBase + '.'
    valueVar = valueVar + args.startFrame + '-'
    valueVar = valueVar + args.endFrame
    valueVar = valueVar + max(len(args.startFrame), len(args.endFrame)) * '#' + '.ari'
    attachParam(inputVar, "sequence", valueVar)
    return inputVar

def outputParams(args):
    output = ET.Element("output")
    attachParam(output, "directory", args.outputDirectory)
    attachParam(output, "filename", args.outputFilenameBase + '.' + max(len(args.startFrame), len(args.endFrame)) * '#')
    attachParam(output, "format", args.format.lower())
    # hardwire this
    attachParam(output, "startnumber", "-1")
    return output

def attachParamBlock(parent, child):
    if child != None and len(child) > 0 :
        parent.append(child)

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def topLevel(argv):
    parser = setupParser()
    args = parser.parse_args(argv[1:])
    args = parser.parse_args(argv[1:])
    # args = parser.parse_args('--colorEncoding logc --colorSpace WideGamut --inputFilenameBase foo --startFrame 100 --endFrame 100 --format DPX_16Bit_BGR --factor 1.0 --outputDirectory /tmp --outputFilenameBase bar --configFilename /tmp/test.xml'.split())
    checkArgs(args)
    cleanInputFrameNumberFormat(args)
    
    arri = ET.Element("arri")
    arriraw = ET.SubElement(arri, "arriraw")
    shortsettings = ET.SubElement(arriraw, "shortsettings", { "name" : "ARC", "version" : "2" })
    # if not args.CCT is None or not args.tint is None:
    #     attachParamBlock(shortsettings, colorHandlingParams(args))
    # if not args.EI:
    #     attachParamBlock(shortsettings, asalutParams(args))
    attachParamBlock(shortsettings, downscaleParams(args))
    # if not args.inputContainer is None:
    #     attachParamBlock(shortsettings, cameraParams(args))
    # if not args.ND is None:
    #     attachParamBlock(shortsettings, studioParams(args))
    # if not args.processing is None:
    #     attachParamBlock(shortsettings, processingParams(args))
    # if not args.qualityMode is None or not args.debayer is None:
    #     attachParamBlock(shortsettings, qualityParams(args))
    # if not args.processors is None or not args.GPU is None:
    #     attachParamBlock(shortsettings, performanceParams(args))
    attachParamBlock(shortsettings, inputParams(args))
    attachParamBlock(shortsettings, outputParams(args))
    
    tree = ET.ElementTree(arri)
    indent(tree.getroot())
    configFile = open(args.configFilename, 'w')
    tree.write(configFile, "utf-8")
    configFile.close()
    print("\n")
    
if __name__ == '__main__':
    topLevel(sys.argv)
