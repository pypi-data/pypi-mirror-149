# relationship.py

def creates_relationships(relations, obj_dir) -> None:
        # fichier des relations
        file = open("{}/RELATIONSHIP.md".format(obj_dir), 'w+', encoding='utf-8')
        with file:
            file.write("## Relations\n")
            sens_relation = "1 -- 1"
            for relation in relations:
                # 1 -- 1
                if relation["isMultiple"] == "false" and relation["isMultiple2"] == "false":
                    sens_relation = "1 -- 1"

                # 1 -- N
                if relation["isMultiple"] == "false" and relation["isMultiple2"] == "true":
                    sens_relation = "1 -- N"

                # N -- 1
                if relation["isMultiple"] == "true" and relation["isMultiple2"] == "false":
                    sens_relation = "N -- 1"

                # N -- N
                if relation["isMultiple"] == "true" and relation["isMultiple2"] == "true":
                    sens_relation = "1 -- 1"

                file.write("- {} : \n\t * [x] {}({}) `{}` {}({})\n".format(
                    relation["relName"],
                    relation["singularName1"],
                    relation["objDef1"],
                    sens_relation,
                    relation["singularName2"],
                    relation["objDef2"]
                ))