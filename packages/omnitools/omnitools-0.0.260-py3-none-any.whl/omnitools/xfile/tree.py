from .path import join_path
import os


def create_cascade(files, key=-1, sep=os.path.sep):
    fps = [_[key] for _ in files]
    fps = sorted(fps, key=lambda file: [sep.join(file.split(sep)[:-1]), file.split(sep)[-1]])
    ordered = []
    def loop_dir(dir):
        nonlocal ordered
        ordered.append([(dir, 1)])
        _dir = [fp.split(sep) for fp in fps if fp.startswith(dir+sep)]
        done = []
        pend = []
        # print("\t"*(dir.count(sep)), dir, len(_dir))
        for __dir in _dir:
            if dir.count(sep) + 2 < len(__dir):
                __dir = __dir[dir.count(sep) + 1]
                if __dir in done:
                    continue
                done.append(__dir)
                loop_dir(sep.join(dir.split(sep) + [__dir]))
            else:
                pend.append(__dir)
        # print("\t"*(dir.count(sep)+1), "files", len(pend))
        for __dir in pend:
            i = 99999
            found = False
            for i in range(len(files) - 1, -1, -1):
                if files[i][key] == sep.join(__dir):
                    found = True
                    break
            if found:
                ordered.append(files.pop(i))
                ordered[key].append((sep.join(__dir), 0))
    loop_dir(fps[0].split(sep)[0])
    return ordered


def format_cascade(cascade, key=-1, sep=os.path.sep):
    info_len = max(len(_) for _ in cascade)
    for i in range(0, len(cascade)):
        for j in range(0, info_len-len(cascade[i])):
            cascade[i].insert(-1, "")
    import copy
    _cascade = copy.deepcopy(cascade)
    for i, _ in enumerate(cascade):
        file1, is_dir = cascade[i][-1]
        depth = file1.count(sep)
        s_file = "|"
        indent = ""
        for j in range(1, depth):
            if i + 1 < len(cascade):
                s_dir = " "
                start = 0
                for k in range(i-1, -1, -1):
                    # if file1 == "I/test/a/b/c/d/e/f":
                    #     print("\t"*j, j, k, _cascade[k][-1][0])
                    if _cascade[k][-1][0].count(sep) == j:
                        start = k
                        # if file1 == "I/test/a/b/c/d/e/f":
                        #     print(j, k, _cascade[k][-1][0])
                        break
                _root = _cascade[start][-1][0]
                for f in _cascade[start+1:]:
                    if sep in _root:
                        if not f[-1][0].startswith(_root+sep) and f[-1][0].startswith(sep.join(_root.split(sep)[:-1])+sep):
                            s_dir = "|"
                            break
                indent += s_dir + "   "
            else:
                indent += " " * 4
        if is_dir:
            s_file = "'"
            if i + 1 < len(cascade):
                for f in cascade[i + 1:]:
                    if not f[-1][0].startswith(file1+sep) and f[-1][0].startswith(sep.join(file1.split(sep)[:-1])+sep):
                        s_file = "|"
                        break
        else:
            if i == len(cascade) - 1 or i + 1 < len(cascade) and cascade[i + 1][-1][0].count(sep) != file1.count(sep):
                s_file = "'"
        cascade[i][-1] = indent + (s_file + "---- " if depth > 0 else "") + file1.split(sep)[-1]
    formatted = ""
    cols = [len(max(_, key=len)) for _ in list(zip(*cascade))[:-2]]
    template = ""
    for col in cols:
        if template:
            template += " "
        template += "{{:>{}}}".format(col)
    template += " {}\n"
    for file in cascade:
        info = file[:-1]
        if info:
            info.pop(key)
        info.append(file[-1])
        formatted += template.format(*info)
    return formatted


