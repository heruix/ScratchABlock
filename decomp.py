from graph import Graph
from core import *


class Seq(BBlock):
    def __init__(self, b1, b2):
        self.addr = b1.addr
        self.items = [b1, b2]

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.items[0], self.items[1])

    def dump(self, stream, indent=0):
        for b in self.items:
            b.dump(stream, indent)


def match_seq(cfg):
    for v, _ in cfg.iter_nodes():
        if cfg.degree_out(v) == 1:
            succ = cfg.succ(v)[0]
            if cfg.degree_in(succ) == 1:
                print("seq:", v, succ)
                newb = Seq(cfg.node(v), cfg.node(succ))
                cfg.add_node(v, newb)
                cfg.move_succ(succ, v)
                cfg.remove_node(succ)
                return True


class If(BBlock):
    def __init__(self, header, t_block, false_cond):
        self.addr = header.addr
        self.cond = false_cond
        self.items = [header, t_block]

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.items[0], self.items[1])

    def dump(self, stream, indent=0):
        self.write(stream, indent, "if %s {" % self.cond.neg())
        self.items[1].dump(stream, indent + 1)
        self.write(stream, indent, "}")


def match_if(cfg):
    for v, _ in cfg.iter_nodes():
        if cfg.degree_out(v) == 2:
            a, b = cfg.sorted_succ(v)
            if cfg.degree_in(a) >= 2 and cfg.degree_in(b) == 1 and cfg.degree_out(b) == 1:
                c = cfg.succ(b)[0]
                if c == a:
                    print("if:", v, b, c)
                    if_header = cfg.node(v)
                    t_block = cfg.node(b)
                    newb = If(if_header, t_block, cfg.edge(v, a))
                    cfg.add_node(v, newb)
                    cfg.remove_node(b)
                    cfg.set_edge(v, a, None)
                    return True
