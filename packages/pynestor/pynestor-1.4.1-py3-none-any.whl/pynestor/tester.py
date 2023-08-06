from pynestor import *

values = NestorDescSet()
values.add(NestorGitDesc(0, "common/modules", "15.0"))
print(values)
for idx in [""] + list(range(2, 20)):
    opt = "sources.repositories.DEPOT_GIT%s.path" % idx
    if values[opt]:

        print("in", opt, values[opt])