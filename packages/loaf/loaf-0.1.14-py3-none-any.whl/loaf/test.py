import __init__ as loaf

"""
loaf.bake(
    host = 'dcrhg4kh56j13bnu.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
    port = 3306,
    user = 'wqt2hfpfgajfr8qs',
    pasw = 'pqyu18vuftxxdgxa',
    db   = 'pf2suqre3ona4htm',
    cursor = "DICTIONARY"
)
q = loaf.query("SELECT * FROM Usuario LIMIT 1")[0]
print(q['id'])
"""

loaf.bake(
    host = 'ec2-18-214-134-226.compute-1.amazonaws.com',
    port = 5432,
    user = 'yqgvibppgwisub',
    pasw = '1e8cee33bf92cf254c2b424841270f8138793d7e309f9c1453ed303a26997ff0',
    db   = 'd82l0e8nslobll',
    mode = "PostgreSQL"
)

loaf.test()
loaf.query("SELECT * FROM public.user")

print("lol "
      "lmao")
