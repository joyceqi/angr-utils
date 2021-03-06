import networkx

from collections import defaultdict

from bingraphvis import *
from bingraphvis.angr import *
from bingraphvis.angr.x86 import *

def plot_common(graph, fname, format="png", type=True):
    vis = AngrVisFactory().default_common_graph_pipeline(type=type)
    vis.set_output(DotOutput(fname, format=format))
    vis.process(graph)

def plot_cfg(cfg, fname, format="png", path=None, asminst=False, vexinst=False, func_addr=None, remove_imports=True, remove_path_terminator=True, remove_simprocedures=False, debug_info=False, comments=True):
    vis = AngrVisFactory().default_cfg_pipeline(cfg, asminst=asminst, vexinst=vexinst, comments=comments)
    if remove_imports:
        vis.add_transformer(AngrRemoveImports(cfg.project))
    if remove_simprocedures:
        vis.add_transformer(AngrRemoveSimProcedures())
    if func_addr:
        vis.add_transformer(AngrFilterNodes(lambda node: node.obj.function_address in func_addr and func_addr[node.obj.function_address]))
    if debug_info:
        vis.add_content(AngrCFGDebugInfo())
    if path:
        vis.add_edge_annotator(AngrPathAnnotator(path))
        vis.add_node_annotator(AngrPathAnnotator(path))
    vis.set_output(DotOutput(fname, format=format))    
    vis.process(cfg.graph) 

def plot_cg(kb, fname, format="png", verbose=False):
    vis = AngrVisFactory().default_cg_pipeline(kb, verbose=verbose)
    vis.set_output(DotOutput(fname, format=format))    
    vis.process(kb) 
    
def plot_cdg(cfg, cdg, fname, format="png", pd_edges=False, cg_edges=True, remove_fakeret=True):
    vis = AngrVisFactory().default_cfg_pipeline(cfg, asminst=True, vexinst=False, color_edges=False)
    if remove_fakeret:
        vis.add_transformer(AngrRemoveFakeretEdges())
    if pd_edges:
        vis.add_transformer(AngrAddEdges(cdg.get_post_dominators(), color="green", reverse=True))
    if cg_edges:
        vis.add_transformer(AngrAddEdges(cdg.graph, color="purple", reverse=False))
    vis.set_output(DotOutput(fname, format=format))
    vis.process(cfg.graph)

def plot_dfg(dfg, fname, format="png"):
    vis = AngrVisFactory().default_common_graph_pipeline(type=True)
    vis.set_output(DotOutput(fname, format=format))
    vis.process(dfg)

#Note: method signature may change in the future
def plot_ddg_stmt(ddg_stmt, fname, format="png", project=None):
    vis = AngrVisFactory().default_common_graph_pipeline()
    if project:
        vis.add_content(AngrAsm(project))
        vis.add_content(AngrVex(project))
    vis.add_edge_annotator(AngrColorDDGStmtEdges(project))
    vis.set_output(DotOutput(fname, format=format))
    vis.process(ddg_stmt)

#Note: method signature may change in the future
def plot_ddg_data(ddg_data, fname, format="png", project=None, asminst=False, vexinst=True):
    vis = Vis()
    vis.set_source(AngrCommonSource())
    vis.add_content(AngrDDGLocationHead())
    vis.add_content(AngrDDGVariableHead(project=project))
    
    if project:
        if asminst:
            vis.add_content(AngrAsm(project))
        if vexinst:
            vis.add_content(AngrVex(project))
    acd = AngrColorDDGData(project, labels=True)
    vis.add_edge_annotator(acd)
    vis.add_node_annotator(acd)
    vis.set_output(DotOutput(fname, format=format))
    vis.process(ddg_data)
