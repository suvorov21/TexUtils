class BibParser:
    def __init__(self, file_in="", file_out=""):
        self.file_in    = file_in
        self.file_out   = file_out

    # simple bracket parser
    def BracketParser(self, line):
        ls = []
        if '=' in line:
            for ch in line:
                if ch in ["(", "{"]:
                    ls.append(ch)
                    continue
                if ch == "$":
                    if len(ls) > 0:
                        if ls[-1] == "$":
                            ls.pop()
                            continue
                    ls.append(ch)

                if ch in [")", "}"]:
                    if len(ls) > 0:
                        if (ch == ")" and ls[-1] == "(") or \
                        (ch == "}" and ls[-1] == "{"):
                            ls.pop()
                            continue

                        print("error 1 in line ", line)
                        return False
                    else:
                        print("error 2 in line ", line)
                        return False
            if len(ls) > 0:
                print("error 3 in line ", line)
                return False
        return True


    def DoParse(self):
        fo = open(self.file_out, 'w')

        with open(self.file_in) as f:
            # ommit first head lines generated by Mendeley
            # related to Mac OS client only
            # for i in range (0, 5):
            #     f.readline()

            # add few rules
            for line in f:
                # ommit abstract
                if line[:8] =='abstract' or line[:4]== 'file' or line[:8] == 'keywords':
                    continue
                # add month w/o brackets
                if (line[:5] == 'month'):
                    line = line.replace("{", "")
                    line = line.replace("}", "")

                # remove unicode artefacts
                line = line.replace("→", "$\\to$")
                line = line.replace("µ", "$\\mu$")
                line = line.replace("Ɵ", "$\\theta$")
                line = line.replace("×", "$\\times$")
                line = line.replace("×1021", "$\\times10^{21}$")
                line = line.replace("\\nu$¯$\\mu", "\\bar\\nu_\\mu")

                # reverse Mendeley 'TeX adobtation'
                line = line.replace(r"{\$}", "$")
                line = line.replace(r"\backslash", "\\")
                line = line.replace(r"{\{}", "{")
                line = line.replace(r"{\}}", "}")
                line = line.replace(r"{\^{}}", "^")
                line = line.replace(r"{\_}", "_")
                line = line.replace(r"{\#}", "#")
                line = line.replace(r"{\%}", "%")
                line = line.replace(r"{\&}", "&")

                if not self.BracketParser(line):
                    return False

                fo.write(line)

        fo.close()
        return True