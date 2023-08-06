import os
import random
import json
import codecs
from collections import defaultdict

from qtpy.QtCore import Qt
from qtpy.QtCore import QPointF
from qtpy.QtGui import QColor
from qtpy.QtGui import QFont
from qtpy.QtGui import QImage
from qtpy.QtGui import QPainter


from nezzle.graphics import NodeClassFactory
from nezzle.graphics import EdgeClassFactory
from nezzle.graphics import LabelClassFactory
from nezzle.graphics import ArrowClassFactory
from nezzle.graphics import Network
from nezzle.constants import DEFAULT_SCENE_WIDTH, DEFAULT_SCENE_HEIGHT
from nezzle.utils import extract_name_and_ext

import math
from nezzle.utils.math import rotate, dist, internal_division


def read_metadata_from_sif(fpath):
    metadata = {}
    interactions = defaultdict(int)
    with codecs.open(fpath, "r", encoding="utf-8-sig") as fin:
        for i, line in enumerate(fin):
            if line.isspace():
                continue

            items = line.split()
            str_src, str_edge_type, str_tgt = items[:3]
            interactions[str_edge_type.strip()] += 1

    metadata["NETWORK_NAME"] = os.path.basename(fpath)
    metadata["INTERACTIONS"] = interactions
    return metadata


def read_metadata_from_nzj(fpath):
    metadata = {}
    interactions = defaultdict(int)
    with codecs.open(fpath, "r", encoding="utf-8") as fin:
        dict_net = json.loads(fin.read())

    for edge in dict_net["EDGES"]:
        str_head_type = edge["HEAD"]["ITEM_TYPE"].title()
        interactions[str_head_type] += 1

    metadata["NETWORK_NAME"] = dict_net["NAME"]
    metadata["INTERACTIONS"] = interactions
    return metadata

def read_metadata(fpath):
    if not fpath:
        raise ValueError("Invalid file path: %s"%(fpath))

    file_name_ext = os.path.basename(fpath)
    fname, fext = os.path.splitext(file_name_ext)

    if file_name_ext.endswith('.sif'):
        return read_metadata_from_sif(fpath)
    elif file_name_ext.endswith('.json'):
        return read_metadata_from_nzj(fpath)

    else:
        raise ValueError("Unsupported file type: %s"%(fext))


def read_network(fpath, edge_map=None):
    if not fpath:
        raise ValueError("Invalid file path: %s"%(fpath))
    file_name_ext = os.path.basename(fpath)
    fname, fext = os.path.splitext(file_name_ext)

    if file_name_ext.endswith('.sif'):
        return read_sif(fpath, edge_map)
    elif file_name_ext.endswith('.json'):
        return read_nzj(fpath, edge_map)

    else:
        raise ValueError("Unsupported file type: %s"%(fext))
# end of read_network


def read_sif(fpath, edge_map=None):

    scene_width = DEFAULT_SCENE_WIDTH
    scene_height = DEFAULT_SCENE_HEIGHT

    fname = os.path.basename(fpath)
    net = Network(fname)
    #net.scene.setBackgroundBrush(QColor(0, 0, 0, 0))
    net.scene.setBackgroundBrush(Qt.white)  #(Qt.transparent)

    with codecs.open(fpath, "r", encoding="utf-8-sig") as fin:
        NodeClass = NodeClassFactory.create("ELLIPSE_NODE")
        nodes = {}
        counter_node = 0
        counter_edge = 0
        for i, line in enumerate(fin):
            if line.isspace():
                continue

            items = line.split()
            str_src, str_edge_type, str_tgt = items[:3]

            if edge_map and (str_edge_type not in edge_map):
                raise ValueError("Undefined edge type: %s"%(str_edge_type))

            color = Qt.white
            half_width = scene_width/2
            half_height = scene_height/2

            range_x = (-scene_width/4, scene_width/4)
            range_y = (-scene_height/4, scene_height/4)

            sx = half_width + random.uniform(*range_x)
            sy = half_height + random.uniform(*range_y)

            tx = half_width + random.uniform(*range_x)
            ty = half_height + random.uniform(*range_y)

            width = 50
            height = 35

            if str_src in nodes:
                src = nodes[str_src]
            else:
                counter_node += 1
                src = NodeClass(str_src, width=width, height=height,
                                pos=QPointF(sx, sy))

                src["FILL_COLOR"] = color
                src['BORDER_COLOR'] = Qt.darkGray
                nodes[str_src] = src
            # end of else

            if str_tgt in nodes:
                trg = nodes[str_tgt]
            else:
                counter_node += 1
                trg = NodeClass(str_tgt, width=width, height=height,
                                pos=QPointF(tx, ty))

                trg["FILL_COLOR"] = color
                trg['BORDER_COLOR'] = Qt.darkGray
                nodes[str_tgt] = trg
            # end of else

            counter_edge += 1

            head = None
            ArrowClass = None

            if edge_map:
                head_type = edge_map[str_edge_type]
                ArrowClass = ArrowClassFactory.create(head_type)

            if ArrowClass:
                head = ArrowClass()

            if str_src == str_tgt: # Self-loop edge
                EdgeClass = EdgeClassFactory.create('SELFLOOP_EDGE')
                iden = "%s%s%s" % (str_src, str_edge_type, str_src)
                edge = EdgeClass(iden=iden,
                                 name=str_edge_type,
                                 node=src,
                                 head=head)

                edge["FILL_COLOR"] = QColor(100, 100, 100, 100)

            else:
                EdgeClass = EdgeClassFactory.create('CURVED_EDGE')
                iden = "%s%s%s" % (str_src, str_edge_type, str_tgt)
                edge = EdgeClass(iden=iden,
                                 name= str_edge_type,
                                 source=src, target=trg,
                                 head=head)

                edge["FILL_COLOR"] = Qt.black

            src.add_edge(edge)
            trg.add_edge(edge)
            net.add_edge(edge)
        # end of for: reading each line of SIF file

        # Add nodes and labels in network
        # font = QFont()
        # font.setFamily("Tahoma")
        # font.setPointSize(10)
        LabelClass = LabelClassFactory.create("TEXT_LABEL")
        for str_name, node in nodes.items():
            net.add_node(node)
            label = LabelClass(node, str_name)
            #label.font = font
            label["FONT_FAMILY"] = "Tahoma"
            label["FONT_SIZE"] = 10
            rect = label.boundingRect()
            label.setPos(-rect.width()/2, -rect.height()/2)
            net.add_label(label)
            nodes[str_name] = node

    # end of with

    for src, trg, attr in net.nxgraph.edges(data=True):
        if net.nxgraph.has_edge(trg, src):
            if src == trg:  # Skip selfloops
                continue

            edge = attr['GRAPHICS']
            mid = internal_division(edge.pos_src, edge.pos_tgt, 0.5, 0.5)
            d = dist(edge.pos_src, mid)/math.cos(math.pi/4)
            cp = rotate(edge.pos_src, mid, -30, d)
            edge.ctrl_point.setPos(cp)

    return net
# end of def


def read_nzj(fpath, edge_map):
    with codecs.open(fpath, "r", encoding="utf-8") as fin:
        dict_net = json.loads(fin.read())

        for edge in dict_net["EDGES"]:
            head_type_ori = edge["HEAD"]["ITEM_TYPE"].title()
            head_type_new = edge_map[head_type_ori]
            edge["HEAD"]["ITEM_TYPE"] = head_type_new.upper()

    return Network.from_dict(dict_net)


def write_network(net, fpath):
    file_name_ext = os.path.basename(fpath)
    file_name_ext = file_name_ext.casefold()

    if file_name_ext.endswith('.sif'):
        write_sif(net, fpath)
    elif file_name_ext.endswith('.json'):
        write_nzj(net, fpath)
    else:
        raise ValueError("Unsupported file type: %s" % (file_name_ext))


def write_sif(net, fpath):
    with codecs.open(fpath, "w", encoding="utf-8") as fout:
        for iden, edge in net.edges.items():
            if 'SELFLOOP' in edge.ITEM_TYPE:
                args = (edge.node.iden, edge.name, edge.node.iden)
            else:
                args = (edge.source.iden, edge.name, edge.target.iden)
            fout.write("%s\t%s\t%s\n"%args)


def write_nzj(net, fpath):
    with codecs.open(fpath, "w", encoding="utf-8") as fout:
        fout.write(json.dumps(net.to_dict()))


def write_image(net,
                fpath,
                transparent=True,
                quality=100,
                scale_width=100, scale_height=100,
                dpi_width=350, dpi_height=350,
                pad_width=10, pad_height=10):

    fname, fext = extract_name_and_ext(fpath)

    scene = net.scene
    scene.clearSelection()
    scene.clearFocus()
    brect = scene.itemsBoundingRect()
    brect.adjust(-pad_width, -pad_height, +2*pad_width, +2*pad_height)

    image = QImage((scale_width/100.0) * brect.width(),
                   (scale_height/100.0) * brect.height(),
                   QImage.Format_ARGB32_Premultiplied)

    # [REF] http://stackoverflow.com/a/13425280/4136588
    # dpm = 300 / 0.0254 # ~300 DPI
    dpm_width = dpi_width / 0.0254
    dpm_height = dpi_height / 0.0254
    image.setDotsPerMeterX(dpm_width)
    image.setDotsPerMeterY(dpm_height)

    bbrush = scene.backgroundBrush()

    painter = QPainter(image)
    if not transparent or fext in ["jpeg", "jpg"]:
        image.fill(Qt.white)
        painter.setPen(Qt.NoPen)
        painter.setBrush(bbrush.color())
        painter.drawRect(0, 0, image.width(), image.height())
    elif fext in ['png']:
        image.fill(bbrush.color())

    painter.setRenderHints(QPainter.TextAntialiasing
                           | QPainter.Antialiasing
                           | QPainter.SmoothPixmapTransform
                           | QPainter.HighQualityAntialiasing)

    scene.render(painter)
    image.save(fpath, fext.upper(), quality)
    painter.end()


